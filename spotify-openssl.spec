%ifarch x86_64 
%global openssltarget linux-x86_64
%else
%global openssltarget linux-elf
%endif

Summary:    Utilities from the general purpose cryptography library with TLS implementation
Name:       spotify-openssl
Version:    1.0.0t
Release:    2%{?dist}
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

Requires:       spotify-client%{?_isa}
# Obsoletes old compat-openssl package, breaks some Steam games
Provides:       compat-openssl = 1.0.0t
Obsoletes:      compat-openssl <= 1.0.0t

%description
The OpenSSL toolkit provides support for secure communications between machines.
OpenSSL includes a certificate management tool and shared libraries which
provide various cryptographic algorithms and protocols.

This package is meant for compatibility purposes with Spotify which requires an
old version 1.0.0 in a non-standard path.

%prep
%setup -q -n openssl-%{version}

%build 
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"

./Configure \
    --prefix=%{_prefix} \
    --openssldir=%{_sysconfdir}/ssl \
    --libdir=%{_libdir} \
    shared zlib enable-md2 %{openssltarget}

make depend
make

%install
install -D -m755 libssl.so.1.0.0 %{buildroot}/%{_libdir}/spotify-client/libssl.so.1.0.0
install -D -m755 libcrypto.so.1.0.0 %{buildroot}/%{_libdir}/spotify-client/libcrypto.so.1.0.0

%files
%license LICENSE
%{_libdir}/spotify-client/libssl.so.1.0.0
%{_libdir}/spotify-client/libcrypto.so.1.0.0

%changelog
* Sun Feb 12 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0t-2
- Rename to spotify-openssl and do not install along with system libraries.

* Wed Oct 12 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0-1
- First build.
