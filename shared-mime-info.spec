Name:		shared-mime-info
Version:	0.90
Release:	%mkrel 10
Summary:	Shared MIME-Info Specification
Group:		Graphical desktop/Other
#gw main is GPL, test program is LGPL
License:	GPL+ and LGPLv2+
URL:		http://www.freedesktop.org/wiki/Software/shared-mime-info
Source0:	http://freedesktop.org/~hadess/%{name}-%{version}.tar.bz2
Source1:	defaults.list
# KDE 4 overrides.
Source2:	mimeapps.list
Patch0: shared-mime-info-xz.patch
# (fc) 0.22-2mdv fix VHDL vs CRT magic detection (Mdv bug #31603)
Patch4:		shared-mime-info-0.80-vhdl.patch
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
%patch0 -p1 -b .xz
%patch4 -p1 -b .vhdl

%build
%configure2_5x --disable-update-mimedb
#gw parallel make fails in 0.90
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
install -m 644 %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mime/{application,image,message,multipart,text,audio,inode,model,packages,video}

touch $RPM_BUILD_ROOT%{_datadir}/mime/{XMLnamespaces,aliases,globs,magic,subclasses,mime.cache}

## remove these bogus files
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/locale/*

%clean
rm -rf $RPM_BUILD_ROOT

%check
make check

%post
%{_bindir}/update-mime-database %{_datadir}/mime > /dev/null

%triggerun -- shared-mime-info < 0.20-3mdv
%{_bindir}/update-mime-database %{_datadir}/mime > /dev/null

%triggerin -- %{_datadir}/mime/packages/*.xml
%{_bindir}/update-mime-database %{_datadir}/mime > /dev/null

%triggerpostun -- %{_datadir}/mime/packages/*.xml
%{_bindir}/update-mime-database %{_datadir}/mime > /dev/null

%files
%defattr (-,root,root)
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
%_datadir/pkgconfig/shared-mime-info.pc


%changelog
* Tue Aug 09 2011 Denis Koryavov <dkoryavov@mandriva.org> 0.90-8mdv2011.0
+ Revision: 693727
- Added priorities for the inode/directory.

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.90-7
+ Revision: 669978
- mass rebuild

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 0.90-6
+ Revision: 640253
- rebuild to obsolete old packages

* Fri Feb 11 2011 Funda Wang <fwang@mandriva.org> 0.90-5
+ Revision: 637208
- wrong name of trigger, there is no triggerpostin, but triggerin

* Tue Feb 08 2011 Funda Wang <fwang@mandriva.org> 0.90-4
+ Revision: 636825
- update_mime_database macro is empty now, so we need to push real command

* Tue Feb 08 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.90-3
+ Revision: 636780
- fix trigger to fire after package has been installed and after uninstall

* Tue Feb 08 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.90-2
+ Revision: 636776
- replace mandriva filetrigger with rpm5 file trigger (~#62395)

* Fri Dec 03 2010 Götz Waschk <waschk@mandriva.org> 0.90-1mdv2011.0
+ Revision: 606053
- new version
- rediff patch 0
- disable parallel make

* Sat Oct 02 2010 Götz Waschk <waschk@mandriva.org> 0.80-1mdv2011.0
+ Revision: 582514
- new version
- rediff patches

* Wed Feb 03 2010 Götz Waschk <waschk@mandriva.org> 0.71-1mdv2010.1
+ Revision: 499880
- new version
- rediff the patches
- update license

* Sun Oct 25 2009 Götz Waschk <waschk@mandriva.org> 0.70-5mdv2010.0
+ Revision: 459265
- replace writer64 by writer in KDE mimeapps as well
- remove openoffice.org64 from defaults list (bug #54878)

* Mon Oct 12 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.70-4mdv2010.0
+ Revision: 456873
- Remove conflicts
- Remove the versionnate buildrequire and add a conflicts

* Thu Oct 08 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.70-2mdv2010.0
+ Revision: 455993
- Versionnate buildrequire

* Wed Oct 07 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.70-1mdv2010.0
+ Revision: 455557
- Update to version 0.70 ( Recommended by KDE )
  Rediff patches

* Fri Apr 24 2009 Götz Waschk <waschk@mandriva.org> 0.60-3mdv2010.0
+ Revision: 368966
- replace kpdf by ocular (bug #47658)

* Fri Apr 17 2009 Helio Chissini de Castro <helio@mandriva.com> 0.60-2mdv2009.1
+ Revision: 367913
- Add xz on the list of mimetypes

* Thu Feb 26 2009 Götz Waschk <waschk@mandriva.org> 0.60-1mdv2009.1
+ Revision: 345050
- new version
- drop patch 5

  + Frederik Himpe <fhimpe@mandriva.org>
    - Use Evince instead of tetex-xdvi for application/x-dvi

* Mon Oct 20 2008 Götz Waschk <waschk@mandriva.org> 0.51-4mdv2009.1
+ Revision: 295632
- update patch 5 with generic icon support

* Fri Sep 05 2008 Helio Chissini de Castro <helio@mandriva.com> 0.51-3mdv2009.0
+ Revision: 281444
- Added firefox as addition in the mimeapps.list, so kde can use firefox as default browser for applicatin/xml+html and text/html
  Thi solution not breaks konqueror navigation as well, so the konqueror usage remains the same
- Updated same mimes for defaults.list

* Fri Aug 08 2008 Götz Waschk <waschk@mandriva.org> 0.51-2mdv2009.0
+ Revision: 268246
- remove totem from the cd player list

* Thu Jul 31 2008 Frederic Crozat <fcrozat@mandriva.com> 0.51-1mdv2009.0
+ Revision: 257716
- Release 0.51
- Rengerate patch5

* Thu Jun 12 2008 Frederic Crozat <fcrozat@mandriva.com> 0.40-1mdv2009.0
+ Revision: 218370
- Release 0.40

* Wed Jun 11 2008 Pixel <pixel@mandriva.com> 0.30-2mdv2009.0
+ Revision: 217913
- add rpm filetrigger running update-mime-database when rpm install/remove a mime file

* Mon May 19 2008 Götz Waschk <waschk@mandriva.org> 0.30-1mdv2009.0
+ Revision: 208896
- new version
- update URL
- drop patch 2
- update patch 4

* Fri Mar 21 2008 Frederic Crozat <fcrozat@mandriva.com> 0.23-2mdv2008.1
+ Revision: 189424
- Update default applications list and add autorun applications for hotplugged medias / devices

* Thu Jan 17 2008 Götz Waschk <waschk@mandriva.org> 0.23-1mdv2008.1
+ Revision: 153974
- new version
- drop patches 0,3

* Tue Jan 08 2008 Götz Waschk <waschk@mandriva.org> 0.22-6mdv2008.1
+ Revision: 146378
- add kpdf for pdf files

* Thu Jan 03 2008 Götz Waschk <waschk@mandriva.org> 0.22-5mdv2008.1
+ Revision: 141776
- add some MIME types from Office 2007

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Oct 23 2007 Götz Waschk <waschk@mandriva.org> 0.22-4mdv2008.1
+ Revision: 101428
- fix bug #34988 (html files identified as mozilla bookmarks)

* Thu Sep 20 2007 Götz Waschk <waschk@mandriva.org> 0.22-3mdv2008.0
+ Revision: 91373
- fix entries for OO.o in defaults.list

* Thu Sep 13 2007 Frederic Crozat <fcrozat@mandriva.com> 0.22-2mdv2008.0
+ Revision: 85071
- Patch3 (CVS): various bug fixes
- Patch4: fix VHDL vs CRT magic detection (Mdv bug #31603)

* Mon Jul 30 2007 Götz Waschk <waschk@mandriva.org> 0.22-1mdv2008.0
+ Revision: 56517
- new version
- drop patches 3,4

  + Frederic Crozat <fcrozat@mandriva.com>
    - Update patch 4 with additional aliases

* Fri Jul 27 2007 Frederic Crozat <fcrozat@mandriva.com> 0.21-4mdv2008.0
+ Revision: 56360
- Patch3 (CVS): add video/avi as alias to video/x-msvideo
- Patch4 : add additional Ogg mimetypes / extensions
- Add totem as default player for ogg files

* Sun Jul 15 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.21-3mdv2008.0
+ Revision: 52240
- add lzma to defaults.list
- update lzma patch (P2) with pattern for tar archives as well

* Wed May 16 2007 Frederic Crozat <fcrozat@mandriva.com> 0.21-2mdv2008.0
+ Revision: 27313
- Set nautilus-cd-burner before file-roller as default application for ISO file (Mdv bug #30833)

* Tue Apr 24 2007 Götz Waschk <waschk@mandriva.org> 0.21-1mdv2008.0
+ Revision: 17740
- new version
- drop merged patches 0,1


* Fri Mar 30 2007 Frederic Crozat <fcrozat@mandriva.com> 0.20-6mdv2007.1
+ Revision: 149882
- Update defaults.list : add more mimetype, use totem instead of rhythmbox by
  default for audio files (Mdv bug #24022), it works best for not imported files

* Sun Mar 11 2007 Götz Waschk <waschk@mandriva.org> 0.20-5mdv2007.1
+ Revision: 141290
- add lzma

* Sun Mar 04 2007 Götz Waschk <waschk@mandriva.org> 0.20-4mdv2007.1
+ Revision: 132700
- fix upgrade

* Fri Mar 02 2007 Frederic Crozat <fcrozat@mandriva.com> 0.20-3mdv2007.1
+ Revision: 131454
- Patch1: resync with ufraw for raw digicam format

  + Thierry Vignaud <tvignaud@mandriva.com>
    - no need to package big ChangeLog when NEWS is already there

* Wed Feb 28 2007 Frederic Crozat <fcrozat@mandriva.com> 0.20-2mdv2007.1
+ Revision: 127085
-Remove patch16, it is networkmanager specific
-generate real patch to output correct type for RealVideo (fdo bug #10122) and no longer subclass them as text/plain
-Fix defaults.list for Real types

* Thu Feb 08 2007 Götz Waschk <waschk@mandriva.org> 0.20-1mdv2007.1
+ Revision: 117749
- new version
- drop merged patches 0 and 2
- update file list

* Mon Jan 22 2007 Götz Waschk <waschk@mandriva.org> 0.19-3mdv2007.1
+ Revision: 111706
- Import shared-mime-info

* Mon Jan 22 2007 G�tz Waschk <waschk@mandriva.org> 0.19-3mdv2007.1
- add alias image/pdf for pdf documents
- unpack patches

* Fri Sep 15 2006 Frederic Crozat <fcrozat@mandriva.com> 0.19-2mdv2007.0
- Patch7: fix detection of Real files

* Sat Sep 09 2006 Frederic Crozat <fcrozat@mandriva.com> 0.19-1mdv2007.0
- New version 0.19 (goetz)
- fix URL
- drop patches 3,4,5,7
- clean defaults.list

* Tue Jul 04 2006 Frederic Crozat <fcrozat@mandriva.com> 0.18-1mdv2007.0
- Release 0.18
- Remove patches 0, 1, 8 (merged upstream)
- Regenerate patch2

* Fri Apr 14 2006 G�tz Waschk <waschk@mandriva.org> 0.17-3mdk
- include Fedora patches

* Wed Mar 22 2006 G�tz Waschk <waschk@mandriva.org> 0.17-2mdk
- improve patch 1
- patch 5: remove directory alias that was breaking nautilus

* Mon Mar 20 2006 G�tz Waschk <waschk@mandriva.org> 0.17-1mdk
- add mime.cache
- rediff patch 1
- New release 0.17
- use mkrel

* Thu Sep 01 2005 Frederic Crozat <fcrozat@mandriva.com> 0.16-3mdk 
- Patch4: add powerpoint alias (Mdk bug #17645)

* Sat Jul 09 2005 G�tz Waschk <waschk@mandriva.org> 0.16-2mdk
- update patch 1 to add WMA audio

* Tue Apr 19 2005 G�tz Waschk <waschk@linux-mandrake.com> 0.16-1mdk
- drop patch 4
- New release 0.16

* Fri Mar 04 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 0.15-3mdk 
- Source1: defaults applications to use for GNOME (based on Fedora)
- Patch4 (CVS): various fixes

* Fri Oct 01 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.15-2mdk
- lib64 fixes to pkgconfig files

* Thu Sep 02 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.15-1mdk
- Release 0.15
- Remove postun script, let rpm do its job

* Wed Aug 18 2004 G�tz Waschk <waschk@linux-mandrake.com> 0.14-5mdk
- update patch1 to make wmv an alias of asf

* Tue Aug 03 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.14-4mdk
- Patch2 : add glob for palm databases

* Sun May 16 2004 G�tz Waschk <waschk@linux-mandrake.com> 0.14-3mdk
- fix asf, wmv and asx

* Sat Apr 17 2004 G�tz Waschk <waschk@linux-mandrake.com> 0.14-2mdk
- fix dia magic detection (Hamish Mackenzie)

* Sat Apr 03 2004 G�tz Waschk <waschk@linux-mandrake.com> 0.14-1mdk
- add pkgconfig file
- drop patch (fixed upstream)
- fix url
- new version

