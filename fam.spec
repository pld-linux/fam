Summary:	FAM, the File Alteration Monitor
Summary(pl.UTF-8):   Monitor zmian w plikach
Summary(pt_BR.UTF-8):   FAM, um monitor de alterações em arquivos
Name:		fam
Version:	2.7.0
Release:	6
License:	GPL
Group:		Daemons
Source0:	ftp://oss.sgi.com/projects/fam/download/stable/%{name}-%{version}.tar.gz
# Source0-md5:	1bf3ae6c0c58d3201afc97c6a4834e39
Source1:	%{name}.inetd
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-dnotify.patch
Patch1:		%{name}-cleanup.patch
Patch2:		%{name}-gcc34.patch
Patch3:		%{name}-paths.patch
Patch4:		%{name}-gcc4.patch
URL:		http://oss.sgi.com/projects/fam/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FAM, the File Alteration Monitor, provides a daemon and an API which
applications can use to be notified when specific files or directories
are changed.

%description -l pl.UTF-8
FAM dostarcza serwer i API pozwalające aplikacjom na uzyskiwanie
informacji o zmianach w określonych plikach lub katalogach.

%description -l pt_BR.UTF-8
O FAM fornece um servidor e uma API que aplicações podem usar para
receber notificações sobre mudanças em arquivos ou diretórios
específicos.

%package common
Summary:	FAM, the File Alteration Monitor - common files
Summary(pl.UTF-8):   Monitor zmian w plikach - wspólne pliki
Group:		Daemons
Requires:	%{name}-libs = %{version}-%{release}
Requires:	portmap
Conflicts:	fam < 2.7.0

%description common
FAM, the File Alteration Monitor, provides a daemon and an API which
applications can use to be notified when specific files or directories
are changed.

%description common -l pl.UTF-8
FAM dostarcza serwer i API pozwalające aplikacjom na uzyskiwanie
informacji o zmianach w określonych plikach lub katalogach.

%description common -l pt_BR.UTF-8
O FAM fornece um servidor e uma API que aplicações podem usar para
receber notificações sobre mudanças em arquivos ou diretórios
específicos.

%package inetd
Summary:	inetd configs for FAM
Summary(pl.UTF-8):   Pliki konfiguracyjne do użycia FAM poprzez inetd
Group:		Daemons
Requires:	%{name}-common = %{version}-%{release}
Requires:	inetdaemon
Requires:	portmap
Requires:	rc-inetd
Provides:	fam = %{version}-%{release}
Obsoletes:	fam < 2.7.0
Obsoletes:	fam-standalone
Conflicts:	gamin
# no RPC support in rc-inet script before
Conflicts:	inetd < 0.17-12
# no working RPC and tcp/wait support before
Conflicts:	rlinetd < 0.6-1
# PORT option was required before
Conflicts:	xinetd < 2.3.14-2

%description inetd
FAM configs for running from inetd.

%description inetd -l pl.UTF-8
Pliki konfiguracyjna FAM do startowania demona poprzez inetd.

%package standalone
Summary:	Standalone daemon configs for FAM
Summary(pl.UTF-8):   Pliki konfiguracyjne do startowania FAM w trybie standalone
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	/sbin/chkconfig
Requires:	rc-scripts
Provides:	fam = %{version}-%{release}
Obsoletes:	fam < 2.7.0
Obsoletes:	fam-inetd
Conflicts:	gamin

%description standalone
FAM configs for running as a standalone daemon.

%description standalone -l pl.UTF-8
Pliki konfiguracyjne FAM do startowania demona w trybie standalone.

%package libs
Summary:	Libraries for FAM
Summary(pl.UTF-8):   Biblioteki FAMa
Summary(pt_BR.UTF-8):   FAM, um monitor de alteraçoes em arquivos
License:	LGPL
Group:		Libraries
Obsoletes:	libfam0
Conflicts:	gamin-libs

%description libs
Libraries for FAM.

%description libs -l pl.UTF-8
Biblioteki FAMa.

%description libs -l pt_BR.UTF-8
FAM, um monitor de alteraçoes em arquivos.

%package devel
Summary:	Includes to develop using FAM
Summary(pl.UTF-8):   Pliki nagłówkowe FAM
Summary(pt_BR.UTF-8):   Arquivos para desenvolvimento com a libfam
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel
Obsoletes:	libfam0-devel
Conflicts:	gamin-devel

%description devel
Includes to develop using FAM.

%description devel -l pl.UTF-8
Pliki nagłówkowe FAM.

%description devel -l pt_BR.UTF-8
Bibliotecas e arquivos de inclusão para desenvolvimento com a libfam.

%package static
Summary:	FAM static libraries
Summary(pl.UTF-8):   Biblioteki statyczne FAM
Summary(pt_BR.UTF-8):   Bibliotecas estáticas para desenvolvimento com a libfam
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Conflicts:	gamin-static

%description static
FAM static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne FAM.

%description static -l pt_BR.UTF-8
Bibliotecas estáticas para desenvolvimento com a libfam.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig/rc-inetd,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/sgi_fam
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/famd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/famd

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install test/test.c++ $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post inetd
%service -q rc-inetd reload

%postun inetd
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%post standalone
/sbin/chkconfig --add famd
%service famd restart "FAM daemon"

%preun standalone
if [ "$1" = "0" ]; then
	%service famd stop
	/sbin/chkconfig --del famd
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files common
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_sbindir}/*
%config %{_sysconfdir}/%{name}.conf
%{_mandir}/man5/*
%{_mandir}/man8/*

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/sgi_fam

%files standalone
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/famd
%attr(754,root,root) /etc/rc.d/init.d/famd

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
