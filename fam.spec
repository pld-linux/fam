Summary:	Fam, the File Alteration Monitor
Summary(pl):	Monitor zmian w plikach
Name:		fam
Version:	2.6.7
Release:	1
License:	GPL/LGPL
Group:		Networking/Daemons
Source0:	ftp://oss.sgi.com/projects/fam/download/%{name}-%{version}.tar.gz
Patch0:		%{name}-dnotify.patch
Patch1:		%{name}-build.patch
Patch2:		%{name}-clean_files.patch
Patch3:		%{name}-libstdc++.patch
URL:		http://oss.sgi.com/projects/fam/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
Prereq:		rc-inetd
Requires:	inetdaemon
Requires:	portmap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
fam, the File Alteration Monitor, provides a daemon and an API which
applications can use to be notified when specific files or directories
are changed.

%description -l pl
fam dostarcza serwer i API pozwalaj±ce aplikacjom na uzyskiwanie
informacji o zmianach w okre¶lonych plikach lub katalogach.

%package libs
Summary:	Libraries for FAM
Summary(pl):	Biblioteki FAMa
Group:		Libraries
Obsoletes:	libfam0

%description libs
Libraries for FAM.

%description libs -l pl
Biblioteki FAMa.

%package devel
Summary:	Includes to develop using FAM
Summary(pl):	Pliki nag³ówkowe FAM
Group:		Development/Libraries
Requires:	%{name}-libs
Obsoletes:	libfam0-devel

%description devel
Includes to develop using FAM.

%description devel -l pl
Pliki nag³ówkowe FAM.

%package static
Summary:	FAM static libraries
Summary(pl):	Biblioteki statyczne FAM
Group:		Development/Libraries
Requires:	%{name}

%description static
FAM static libraries.

%description static -l pl
Biblioteki statyczne FAM.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
rm -f missing
libtoolize --copy --force
aclocal
autoconf
automake -a -c -f
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gzip -9nf AUTHORS ChangeLog NEWS README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%config %{_sysconfdir}/%{name}.conf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/*.h
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
