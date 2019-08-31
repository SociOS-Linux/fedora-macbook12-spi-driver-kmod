%global debug_package %{nil}
%global githash be3639a6e9a0a385e3ed41d17e9c874af815cb0f
Name: macbook12-spi-driver-kmod
Version: 0.294
Release: 1%{?dist}
Summary: Akmod package for macbook12-spi-driver

License: GPL-2.0
URL: https://github.com/roadrunner2/macbook12-spi-driver
Source: https://github.com/roadrunner2/macbook12-spi-driver/archive/%{githash}.tar.gz

BuildRequires:  %{_bindir}/kmodtool gcc
Provides: macbook12-spi-driver-kmod-common

ExclusiveArch:  i686 x86_64
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Akmod package for macbook12-spi-driver

%prep
%{?kmodtool_check}

kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T
mkdir %{name}-%{version}-src
pushd %{name}-%{version}-src
tar xf %{SOURCE0}
popd

for kernel_version in %{?kernel_versions} ; do
 cp -a %{name}-%{version}-src _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}/macbook12-spi-driver-%{githash}
 make -C ${kernel_version##*___} M=`pwd` modules
 popd
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}/macbook12-spi-driver-%{githash}
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 install -m 0755 *.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 popd
done

chmod 0755 $RPM_BUILD_ROOT%{kmodinstdir_prefix}*%{kmodinstdir_postfix}/* || :
%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT

%package -n macbook12-spi-driver-kmod-common
Summary: Dummy package

%description  -n macbook12-spi-driver-kmod-common
Dummy package

%files -n macbook12-spi-driver-kmod-common

%changelog
* Sat Aug 31 2019 Dick Marinus <dick@mrns.nl> - 0.294-1
- Update to 294

* Fri Mar 22 2019 Dick Marinus <dick@mrns.nl> - 0.204-0
- initial version
