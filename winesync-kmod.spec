%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

%global winesync_commit 9ac10c6e711ec096274ecc676ae83a7cf2a1213f

Name:     winesync-kmod
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  Wine synchronization primitive driver
License:  GPLv2
URL:      https://repo.or.cz/linux/zf.git/shortlog/refs/heads/winesync4
VCS:      {{{ git_dir_vcs }}}
Source:   {{{ git_dir_pack }}}

Patch0:   winesync.patch

BuildRequires: kmodtool

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Wine synchronization primitive driver

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

{{{ git_dir_setup_macro }}}
%patch 0

for kernel_version  in %{?kernel_versions} ; do
  mkdir -p _kmod_build_${kernel_version%%___*}
  cp -a winesync.c winesync.h Makefile _kmod_build_${kernel_version%%___*}/
done

%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/winesync.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/winesync.ko
done
%{?akmod_install}

%changelog
{{{ git_dir_changelog }}}
