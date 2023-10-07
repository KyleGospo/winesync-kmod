%if 0%{?fedora}
%global debug_package %{nil}
%endif

Name:     winesync
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  Wine synchronization primitive driver
License:  GPLv2
URL:      https://repo.or.cz/linux/zf.git/shortlog/refs/heads/winesync4

Source0:  https://raw.githubusercontent.com/KyleGospo/winesync-kmod/main/99-winesync.rules
Source1:  https://raw.githubusercontent.com/KyleGospo/winesync-kmod/main/LICENSE

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
Wine synchronization primitive driver

%build
install -D -m 0644 %{SOURCE0} %{buildroot}%{_udevrulesdir}/99-winesync.rules
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datarootdir}/licenses/winesync/LICENSE

%files
%license LICENSE
%{_udevrulesdir}/99-winesync.rules

%changelog
{{{ git_dir_changelog }}}
