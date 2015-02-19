%define _disable_ld_no_undefined 1

Name:		shared-mime-info
Version:	1.4
Release:	1
Summary:	Shared MIME-Info Specification
Group:		Graphical desktop/Other
#gw main is GPL, test program is LGPL
License:	GPL+ and LGPLv2+
URL:		http://www.freedesktop.org/wiki/Software/shared-mime-info
Source0:	http://freedesktop.org/~hadess/%{name}-%{version}.tar.xz
Source1:	defaults.list
# KDE 4 overrides.
Source2:	mimeapps.list
Patch0:		shared-mime-info-1.3-x-iso9660-image.patch
# (fc) 0.22-2mdv fix VHDL vs CRT magic detection (Mdv bug #31603)
Patch5:		shared-mime-info-0.80-vhdl.patch
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	libxml2-utils
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	intltool

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
%setup -q
%apply_patches

%build
%configure \
	--disable-update-mimedb

%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/mime/{application,image,message,multipart,text,audio,inode,model,packages,video}

touch %{buildroot}%{_datadir}/mime/{XMLnamespaces,aliases,globs,magic,subclasses,mime.cache}

## remove these bogus files
rm -rf %{buildroot}%{_datadir}/locale/*

%check
make check

%post
%{_bindir}/update-mime-database %{_datadir}/mime > /dev/null

%triggerun -- shared-mime-info < 0.20-3mdv
%{_bindir}/update-mime-database %{_datadir}/mime > /dev/null

%triggerin -- %{_datadir}/mime/packages/*.xml
%{_bindir}/update-mime-database -n %{_datadir}/mime > /dev/null

%triggerpostun -- %{_datadir}/mime/packages/*.xml
%{_bindir}/update-mime-database -n %{_datadir}/mime > /dev/null

%files
%doc README shared-mime-info-spec.xml NEWS
%_bindir/update-mime-database
%dir %{_datadir}/mime/
%{_datadir}/applications/defaults.list
%{_datadir}/applications/mimeapps.list
%dir %{_datadir}/mime/application
%dir %{_datadir}/mime/image
%dir %{_datadir}/mime/message
%dir %{_datadir}/mime/multipart
%dir %{_datadir}/mime/text
%dir %{_datadir}/mime/audio
%dir %{_datadir}/mime/inode
%dir %{_datadir}/mime/model
%dir %{_datadir}/mime/packages
%dir %{_datadir}/mime/video
%ghost %{_datadir}/mime/XMLnamespaces
%ghost %{_datadir}/mime/aliases
%ghost %{_datadir}/mime/globs
%ghost %{_datadir}/mime/magic
%ghost %{_datadir}/mime/subclasses
%ghost %{_datadir}/mime/mime.cache
%{_datadir}/mime/packages/freedesktop.org.xml
%_mandir/man1/update-mime-database.1*

%files devel
%_datadir/pkgconfig/shared-mime-info.pc
