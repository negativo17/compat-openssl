%ifarch x86_64 
%global openssltarget linux-x86_64
%else
%global openssltarget linux-elf
%endif

Summary:    Utilities from the general purpose cryptography library with TLS implementation
Name:       compat-openssl
Version:    1.0.0t
Release:    1%{?dist}
License:    OpenSSL
URL:        http://www.openssl.org/
Source:     ftp://ftp.openssl.org/source/openssl-%{version}.tar.gz

BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  krb5-devel
BuildRequires:  perl-podlators
BuildRequires:  sed
BuildRequires:  util-linux
BuildRequires:  zlib-devel

%description
The OpenSSL toolkit provides support for secure communications between machines.
OpenSSL includes a certificate management tool and shared libraries which
provide various cryptographic algorithms and protocols.

This package is meant for compatibility purposes with binary programs requiring
version 1.0.0 and only contains the shared libraries.

%prep
%setup -q -n openssl-%{version}

%build 
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"

./Configure \
    --prefix=/usr \
    --openssldir=/etc/ssl \
    --libdir=%{_libdir} \
    shared zlib enable-md2 %{openssltarget}

make depend
make

%install
install -D -m755 libssl.so.1.0.0 %{buildroot}/%{_libdir}/libssl.so.1.0.0
install -D -m755 libcrypto.so.1.0.0 %{buildroot}/%{_libdir}/libcrypto.so.1.0.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/libssl.so.1.0.0
%{_libdir}/libcrypto.so.1.0.0

%changelog
* Wed Oct 12 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0-1
- First build.
