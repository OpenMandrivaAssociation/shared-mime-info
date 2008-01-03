Name:		shared-mime-info
Version:	0.22
Release:	%mkrel 5
Summary:	Shared MIME-Info Specification
Group:		Graphical desktop/Other
License:	GPL
URL:		http://www.freedesktop.org/software/shared-mime-info
Source0:	http://freedesktop.org/~hadess/%{name}-%{version}.tar.bz2
Source1:	defaults.list
# gw fix bug #34988 (html files identified as mozilla bookmarks)
Patch: shared-mime-info-revert-netscape-bookmarks.patch
# gw add *.lzma pattern (fd.o bug #13256)
Patch2:		shared-mime-info-0.21-lzma.patch
# (fc) 0.22-2mdv bugfixes from CVS + testcase
Patch3:		shared-mime-info-0.22-cvsfixes.patch
# (fc) 0.22-2mdv fix VHDL vs CRT magic detection (Mdv bug #31603)
Patch4:		shared-mime-info-0.22-vhdl.patch
Patch5:         shared-mime-info-0.22-office2007.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	libxml2-devel
BuildRequires:  libxml2-utils
BuildRequires:	glib2-devel
BuildRequires:  intltool


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

%prep
%setup -q
%patch -p0
%patch2 -p1 -b .lzma_mime
%patch3 -p1 -b .cvsfixes
%patch4 -p1 -b .vhdl
%patch5 -p1 -b .office2007

#needed by patch3
intltoolize --force
autoreconf

%build
%configure2_5x --disable-update-mimedb
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mime/{application,image,message,multipart,text,audio,inode,model,packages,video}

touch $RPM_BUILD_ROOT%{_datadir}/mime/{XMLnamespaces,aliases,globs,magic,subclasses,mime.cache}

## remove these bogus files
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/locale/*

%clean
rm -rf $RPM_BUILD_ROOT

%check
make check

%post
%update_mime_database

%triggerun -- shared-mime-info < 0.20-3mdv
%update_mime_database

%files
%defattr (-,root,root)
%doc README shared-mime-info-spec.xml NEWS
%_bindir/update-mime-database
%dir %{_datadir}/mime/
%{_datadir}/applications/defaults.list
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
%_datadir/pkgconfig/shared-mime-info.pc


