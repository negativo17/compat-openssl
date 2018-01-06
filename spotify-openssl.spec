# Remove bundled libraries from requirements/provides
%global         __requires_exclude ^(libcrypto\\.so\\..*|libssl\\.so\\..*)$
%global         __provides_exclude ^(lib.*\\.so.*)$

%ifarch x86_64 
%global openssltarget linux-x86_64
%else
%global openssltarget linux-elf
%endif

Name:           spotify-openssl
Version:        1.1.0g
Release:        1%{?dist}
Summary:        Spotify compatibility package - OpenSSL
License:        OpenSSL
URL:            http://www.openssl.org/

ExclusiveArch:  x86_64 %{ix86}

Source:         ftp://ftp.openssl.org/source/openssl-%{version}.tar.gz

BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  krb5-devel
BuildRequires:  perl-podlators
BuildRequires:  sed
BuildRequires:  util-linux
BuildRequires:  zlib-devel

Requires:       spotify-client%{?_isa}

%description
This package is meant for compatibility purposes with Spotify which requires old
versions of specific libraries in a non-standard path.

%prep
%setup -q -n openssl-%{version}

%build 
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"

./Configure \
    --prefix=%{_prefix} \
    --openssldir=%{_sysconfdir}/ssl \
    --libdir=%{_libdir} \
    shared zlib enable-md2 %{openssltarget} "%{optflags}"

make depend
make

%install
install -D -m755 libssl.so.1.1 %{buildroot}/%{_libdir}/spotify-client/libssl.so.1.1
install -D -m755 libcrypto.so.1.1 %{buildroot}/%{_libdir}/spotify-client/libcrypto.so.1.1

%files
%license LICENSE
%{_libdir}/spotify-client/libssl.so.1.1
%{_libdir}/spotify-client/libcrypto.so.1.1

%changelog
* Sat Jan 06 2018 Simone Caronni <negativo17@gmail.com> - 1.1.0g-1
- Update to 1.1 for RHEL/CentOS.

* Wed Oct 04 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0t-4
- Add proper compiler flags.

* Wed Mar 01 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0t-3
- Remove compat-openssl Provides/Requires.
- Filter out libraries in Provides/Requires.
- Update description, summary.
- Make it ExclusiveArch as the client itself.

* Sun Feb 12 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0t-2
- Rename to spotify-openssl and do not install along with system libraries.

* Wed Oct 12 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0-1
- First build.
