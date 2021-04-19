%global debug_package %{nil}
%global githash ddfbc7733542b8474a0e8f593aba91e06542be4f
Name: macbook12-spi-driver-kmod
Version: 0.493
Release: 2%{?dist}
Summary: Akmod package for macbook12-spi-driver

License: GPL-2.0
URL: https://github.com/roadrunner2/macbook12-spi-driver
Source: https://github.com/roadrunner2/macbook12-spi-driver/archive/%{githash}.tar.gz
# https://patch-diff.githubusercontent.com/raw/roadrunner2/macbook12-spi-driver/pull/55.diff
Patch: 55.patch

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
pushd macbook12-spi-driver-%{githash}
%patch0 -p1
popd
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
* Sun Apr 18 2021 Dick Marinus <dick@mrns.nl> - 0.493-2
- Fix iio_priv_to_dev trouble

* Fri Sep 11 2020 Dick Marinus <dick@mrns.nl> - 0.493-1
- Update to 493

* Sat Aug 31 2019 Dick Marinus <dick@mrns.nl> - 0.294-1
- Update to 294

* Fri Mar 22 2019 Dick Marinus <dick@mrns.nl> - 0.204-0
- initial version
