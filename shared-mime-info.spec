%global __requires_exclude ^/usr/bin/pkg-config$

Name:		shared-mime-info
Version:	2.1
Release:	1
Summary:	Shared MIME-Info Specification
Group:		Graphical desktop/Other
License:	GPLv2+
URL:		http://freedesktop.org/Software/shared-mime-info
Source0:	https://gitlab.freedesktop.org/xdg/shared-mime-info/-/archive/%{version}/%{name}-%{version}.tar.xz
# Tarball for https://gitlab.freedesktop.org/xdg/xdgmime/-/tree/6663a2288d11b37bc07f5a01b4b85dcd377787e1
Source1:	https://gitlab.freedesktop.org/xdg/xdgmime/-/archive/master/xdgmime-master.tar.gz
Source2:	defaults.list
# KDE Plasma overrides.
Source3:	mimeapps.list
# Not used automatically, but useful to maintainers.
# See comments in the file.
Source100:	sanity-check

BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	libxml2-utils
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	meson
BuildRequires:	itstool
BuildRequires:	xmlto
Requires(post):	/bin/sh

%description
This is the freedesktop.org shared MIME info database.

Many programs and desktops use the MIME system to represent the types of
files. Frequently, it is necessary to work out the correct MIME type for
a file. This is generally done by examining the file's name or contents,
and looking up the correct MIME type in a database.

For interoperability, it is useful for different programs to use the
same database so that different programs agree on the type of a file,
and new rules for determining the type apply to all programs.

This specification attempts to unify the type-guessing systems currently
in use by GNOME, KDE and ROX. Only the name-to-type and contents-to-type
mappings are covered by this spec; other MIME type information, such as
the default handler for a particular type, or the icon to use to display
it in a file manager, are not covered since these are a matter of style.

In addition, freedesktop.org provides a shared database in this format
to avoid inconsistencies between desktops. This database has been
created by converting the existing KDE and GNOME databases to the new
format and merging them together.

%package devel
Summary:	development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 1.3

%description devel
Development files for %{name}.

%prep
%autosetup -p1

tar -xzf %{SOURCE1}
mv xdgmime-*/ xdgmime

%build
%make_build -C xdgmime
# the updated mimedb is later owned as %%ghost to ensure proper file-ownership
# it also asserts it is possible to build it
%meson -Dupdate-mimedb=true -Dxdg-mime-path=./xdgmime/
	
%meson_build

%install
%meson_install

find %{buildroot}%{_datadir}/mime -type d \
| sed -e "s|^%{buildroot}|%%dir |" > %{name}.files
find %{buildroot}%{_datadir}/mime -type f -not -path "*/packages/*" \
| sed -e "s|^%{buildroot}|%%ghost |" >> %{name}.files

mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE2} %{SOURCE3} %{buildroot}%{_datadir}/applications

## remove these bogus files
rm -rf %{buildroot}%{_datadir}/locale/*

%check
%meson_test

%post
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null ||:

%triggerin -- %{_datadir}/mime
%{_bindir}/update-mime-database -n %{_datadir}/mime &>/dev/null ||:

%triggerpostun -- %{_datadir}/mime
[ -x %{_bindir}/update-mime-database ] && %{_bindir}/update-mime-database -n %{_datadir}/mime &>/dev/null ||:

%files -f %{name}.files
%doc NEWS
%{_bindir}/update-mime-database
%dir %{_datadir}/mime
%dir %{_datadir}/mime/packages
%{_datadir}/applications/defaults.list
%{_datadir}/applications/mimeapps.list
%{_datadir}/mime/packages/freedesktop.org.xml
%{_mandir}/man1/update-mime-database.1*

%files devel
%{_datadir}/pkgconfig/shared-mime-info.pc
%{_datadir}/gettext/its/shared-mime-info.its
%{_datadir}/gettext/its/shared-mime-info.loc
