Summary:	Fam, the File Alteration Monitor
Summary(pl):	Monitor zmian w plikach
Summary(pt_BR):	FAM, um monitor de alterações em arquivos
Name:		fam
Version:	2.7.0
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://oss.sgi.com/projects/fam/download/stable/%{name}-%{version}.tar.gz
# Source0-md5:	1bf3ae6c0c58d3201afc97c6a4834e39
Source1:	%{name}.inetd
Patch0:		%{name}-dnotify.patch
URL:		http://oss.sgi.com/projects/fam/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
PreReq:		rc-inetd
Requires:	%{name}-libs = %{version}-%{release}
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

%description -l pt_BR
O fam fornece um servidor e uma API que aplicações podem usar para
receber notificações sobre mudanças em arquivos ou diretórios
específicos.

%package libs
Summary:	Libraries for FAM
Summary(pl):	Biblioteki FAMa
Summary(pt_BR):	FAM, um monitor de alteraçoes em arquivos
License:	LGPL
Group:		Libraries
Obsoletes:	libfam0

%description libs
Libraries for FAM.

%description libs -l pl
Biblioteki FAMa.

%description libs -l pt_BR
FAM, um monitor de alteraçoes em arquivos.

%package devel
Summary:	Includes to develop using FAM
Summary(pl):	Pliki nag³ówkowe FAM
Summary(pt_BR):	Arquivos para desenvolvimento com a libfam
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel
Obsoletes:	libfam0-devel

%description devel
Includes to develop using FAM.

%description devel -l pl
Pliki nag³ówkowe FAM.

%description devel -l pt_BR
Bibliotecas e arquivos de inclusão para desenvolvimento com a libfam.

%package static
Summary:	FAM static libraries
Summary(pl):	Biblioteki statyczne FAM
Summary(pt_BR):	Bibliotecas estáticas para desenvolvimento com a libfam
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
FAM static libraries.

%description static -l pl
Biblioteki statyczne FAM.

%description static -l pt_BR
Bibliotecas estáticas para desenvolvimento com a libfam.

%prep
%setup -q
#%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
##%{__autoconf}
##%{__autoheader}
%{__automake}
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/sgi_fam

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%config %{_sysconfdir}/%{name}.conf
%attr(640,root,root) /etc/sysconfig/rc-inetd/sgi_fam
%{_mandir}/man1/fam.1m*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
