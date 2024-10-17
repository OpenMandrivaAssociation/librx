Summary:	POSIX regexp functions
Name:		librx
Version:	1.5
Release:	%mkrel 4
License:	GPLv2+
URL:		https://www.gnu.org/software/rx/rx.html
Group:		Text tools
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:	ftp://ftp.gnu.org/gnu/rx/rx-%{version}.tar.bz2
Patch0:		rx-1.5-shared.patch
Patch1:		rx-1.5-texinfo.patch
Patch2:		librx-1.5-libdir64.patch
BuildRequires:	texinfo libtool

%description
Rx is, among other things, an implementation of the interface
specified by POSIX for programming with regular expressions.  Some
other implementations are GNU regex.c and Henry Spencer's regex
library.

%package devel
Summary:	POSIX regexp functions, developers library
Group:		Development/C
Requires:	%{name} = %{version}-%{release}

%description devel
Rx is, among other things, an implementation of the interface
specified by POSIX for programming with regular expressions.  Some
other implementations are GNU regex.c and Henry Spencer's regex
library.

This package contains files needed for development with librx.

%prep
%setup -q -n rx-%{version}
%patch0 -p1
%patch1 -p1 -b .texipatch
%ifarch x86_64 ppc64 sparc64
%patch2 -p1 -b .64bit
%endif

%build
%configure
make %{?_smp_mflags}
make doc/rx.info

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_infodir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
make install DESTDIR=${RPM_BUILD_ROOT}
install -m 644 doc/rx.info ${RPM_BUILD_ROOT}%{_infodir}
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/librx.la
chmod -x ${RPM_BUILD_ROOT}%{_includedir}/rxposix.h

%clean
rm -rf ${RPM_BUILD_ROOT}

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%post devel
/sbin/install-info %{_infodir}/rx.info \ 
    %{_infodir}/dir 2>/dev/null || :

%postun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/rx.info \
    %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc ANNOUNCE BUILDING COOKOFF rx/ChangeLog
%{_includedir}/*
%{_infodir}/*
%{_libdir}/*.so
%{_libdir}/*.a
