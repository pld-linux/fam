# TODO:
# - add rc-inetd support for fam service.
#
Summary:	Fam, the File Alteration Monitor
Summary(pl):	Monitor zmian w plikach
Summary(pt_BR):	FAM, um monitor de altera��es em arquivos
Name:		fam
Version:	2.6.9
Release:	3
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://oss.sgi.com/projects/fam/download/%{name}-%{version}.tar.gz
Patch0:		%{name}-dnotify.patch
Patch1:		%{name}-build.patch
Patch2:		%{name}-rpcsvc.patch
Patch3:		%{name}-gcc3.patch
URL:		http://oss.sgi.com/projects/fam/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
Prereq:		rc-inetd
Requires:	%{name}-libs = %{version}
Requires:	inetdaemon
Requires:	portmap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gcc_ver	%(%{__cc} -dumpversion | cut -b 1)
%if %{_gcc_ver} == 2
%define		__cxx		"%{__cc}"
%endif

%description
fam, the File Alteration Monitor, provides a daemon and an API which
applications can use to be notified when specific files or directories
are changed.

%description -l pl
fam dostarcza serwer i API pozwalaj�ce aplikacjom na uzyskiwanie
informacji o zmianach w okre�lonych plikach lub katalogach.

%description -l pt_BR
O fam fornece um servidor e uma API que aplica��es podem usar para
receber notifica��es sobre mudan�as em arquivos ou diret�rios
espec�ficos.

%package libs
Summary:	Libraries for FAM
Summary(pl):	Biblioteki FAMa
Summary(pt_BR):	FAM, um monitor de altera�oes em arquivos
License:	LGPL
Group:		Libraries
Obsoletes:	libfam0

%description libs
Libraries for FAM.

%description libs -l pl
Biblioteki FAMa.

%description libs -l pt_BR
FAM, um monitor de altera�oes em arquivos.

%package devel
Summary:	Includes to develop using FAM
Summary(pl):	Pliki nag��wkowe FAM
Summary(pt_BR):	Arquivos para desenvolvimento com a libfam
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}
Obsoletes:	libfam0-devel

%description devel
Includes to develop using FAM.

%description devel -l pl
Pliki nag��wkowe FAM.

%description devel -l pt_BR
Bibliotecas e arquivos de inclus�o para desenvolvimento com a libfam.

%package static
Summary:	FAM static libraries
Summary(pl):	Biblioteki statyczne FAM
Summary(pt_BR):	Bibliotecas est�ticas para desenvolvimento com a libfam
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
FAM static libraries.

%description static -l pl
Biblioteki statyczne FAM.

%description static -l pt_BR
Bibliotecas est�ticas para desenvolvimento com a libfam.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%config %{_sysconfdir}/%{name}.conf
%{_mandir}/man1/fam.1m*

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
