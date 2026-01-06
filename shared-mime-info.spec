%global __requires_exclude ^/usr/bin/pkg-config$

%ifnarch %{riscv}
# (tpg) optimize it a bit
%global optflags %{optflags} -Oz --rtlib=compiler-rt
%endif

Name:		shared-mime-info
Version:	2.4
Release:	2
Summary:	Shared MIME-Info Specification
Group:		Graphical desktop/Other
License:	GPLv2+
URL:		https://freedesktop.org/Software/shared-mime-info
Source0:	https://gitlab.freedesktop.org/xdg/shared-mime-info/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Tarball for https://gitlab.freedesktop.org/xdg/xdgmime
Source1:	https://gitlab.freedesktop.org/xdg/xdgmime/-/archive/74a00cf508a24ba3b3bedeb4d4c05fd6d1211ead/xdgmime-74a00cf508a24ba3b3bedeb4d4c05fd6d1211ead.tar.bz2
#Source1:	https://gitlab.freedesktop.org/xdg/xdgmime/-/archive/master/xdgmime-master.tar.gz
# Not used automatically, but useful to maintainers.
# See comments in the file.
Source100:	sanity-check
BuildRequires:	gettext
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	libxml2-utils
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	meson
BuildRequires:	itstool
BuildRequires:	xmlto
Requires(post):	/bin/sh

%patchlist
shared-mime-info-openat-missing-argument.patch

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
%setup
tar -xzf %{SOURCE1}
mv xdgmime-*/* xdgmime/
%autopatch -p1

cd xdgmime
%meson

%build
%set_build_flags
cd xdgmime
%meson_build
cd ..

# the updated mimedb is later owned as %%ghost to ensure proper file-ownership
# it also asserts it is possible to build it
%meson \
    -Dupdate-mimedb=true \
    -Dxdgmime-path=./xdgmime

%meson_build

%install
%meson_install

WD="$(pwd)"
find %{buildroot}%{_datadir}/mime -type d \
| sed -e "s|^%{buildroot}|%%dir |" > %{name}.files
# We used to do
# find %{buildroot}%{_datadir}/mime -type f -not -path "*/packages/*" \
# | sed -e "s|^%{buildroot}|%%ghost |" >> %{name}.files
# here -- but this causes a funny hard to see breakage when building
# inside a directory called "packages" (crossbuild...)
cd %{buildroot}%{_datadir}/mime
find . -type f |grep -v "/packages/" \
| sed -e "s|^\.|%%ghost %{_datadir}/mime|" >> ${WD}/%{name}.files
cd ${WD}

## remove these bogus files
rm -rf %{buildroot}%{_datadir}/locale/*

%check
%meson_test

%post
touch --no-create %{_datadir}/mime/packages &>/dev/null ||:

%transfiletriggerin -- %{_datadir}/mime
update-mime-database -n %{_datadir}/mime &> /dev/null ||:

%transfiletriggerpostun -- %{_datadir}/mime
update-mime-database -n %{_datadir}/mime &> /dev/null ||:

%files -f %{name}.files
%doc NEWS
%{_bindir}/update-mime-database
%{_datadir}/mime/packages/freedesktop.org.xml
%doc %{_mandir}/man1/update-mime-database.1*

%files devel
%{_datadir}/pkgconfig/shared-mime-info.pc
%{_datadir}/gettext/its/shared-mime-info.its
%{_datadir}/gettext/its/shared-mime-info.loc
