Summary:    Utilities for managing the XFS filesystem
Name:       xfsprogs
Version:    4.9.0
Release:    1%{?dist}
License:    GPL+ and LGPLv2+
URL:        http://oss.sgi.com/projects/xfs/
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    http://kernel.org/pub/linux/utils/fs/xfs/xfsprogs/%{name}-%{version}.tar.gz
%define sha1 xfsprogs=6d6dcf7f0bbf0e0104fb47af0cba1647817cf6e8
BuildRequires:  gettext
BuildRequires:  readline-devel

%description
The xfsprogs package contains administration and debugging tools for the
XFS file system.

%package devel
Summary: XFS filesystem-specific static libraries and headers
Group: Development/Libraries
Requires: xfsprogs = %{version}-%{release}

%description devel
Libraries and header files needed to develop XFS filesystem-specific programs.

%package lang
Summary: Additional language files for xfsprogs
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of xfsprogs.

%prep
%setup -q

%build
make DEBUG=-DNDEBUG     \
     INSTALL_USER=root  \
     INSTALL_GROUP=root \
     LOCAL_CONFIGURE_OPTIONS="--enable-readline"

%install
make DESTDIR=%{buildroot} PKG_DOC_DIR=%{_usr}/share/doc/%{name}-%{version} install
make DESTDIR=%{buildroot} PKG_DOC_DIR=%{_usr}/share/doc/%{name}-%{version} install-dev

#find %{buildroot}/lib64/ -name '*.so' -delete
find %{buildroot}/%{_lib64dir} -name '*.la' -delete
find %{buildroot}/%{_lib64dir} -name '*.a' -delete

%find_lang %{name}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc doc/CHANGES doc/COPYING doc/CREDITS README
/sbin/*
/lib64/*.so.*.*
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/xfs
%{_includedir}/xfs/*
/lib64/*.so
/lib64/*.so.1
%{_mandir}/man3/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Fri Jan 6 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.9.0-1
-   Initial build.  First version
