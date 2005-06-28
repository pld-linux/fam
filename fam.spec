Summary:	Fam, the File Alteration Monitor
Summary(pl):	Monitor zmian w plikach
Summary(pt_BR):	FAM, um monitor de altera��es em arquivos
Name:		fam
Version:	2.6.10
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://oss.sgi.com/projects/fam/download/stable/%{name}-%{version}.tar.gz
# Source0-md5:	1c5a2ea659680bdd1e238d7828a857a7
Source1:	%{name}.inetd
Patch0:		%{name}-dnotify.patch
Patch1:		%{name}-build.patch
Patch2:		%{name}-rpcsvc.patch
Patch3:		%{name}-cleanup.patch
Patch4:		%{name}-gcc34.patch
URL:		http://oss.sgi.com/projects/fam/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package inetd
Summary:	inetd configs for fam
Summary(pl):	Pliki konfiguracyjne do u�ycia fam poprzez inetd
Group:		Daemons
PreReq:		%{name}-common = %{epoch}:%{version}-%{release}
PreReq:		rc-inetd
Requires:	inetdaemon
Requires:	portmap
Conflicts:	rlinetd
Conflicts:	inetd
#Requires:	xinetd

%description inetd
Fam configs for running from inetd.

%description inetd -l pl
Pliki konfiguracyjna fam do startowania demona poprzez inetd.

%package standalone
Summary:	Standalone daemon configs for fam
Summary(pl):	Pliki konfiguracyjne do startowania fam w trybie standalone
Group:		Daemons
PreReq:		%{name}-common = %{epoch}:%{version}-%{release}
PreReq:		rc-scripts

%description standalone
Fam configs for running as a standalone daemon.

%description standalone -l pl
Pliki konfiguracyjne fam do startowania demona w trybie
standalone.

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
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel
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
Requires:	%{name}-devel = %{version}-%{release}

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
