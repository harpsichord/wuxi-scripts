ame:           sat_utils
Version:        1.0
Release:        1%{?dist}
Summary:        various utilities written by team SAT@kwai

Group:          sfop
BuildArch:      x86_64
License:        GPL
URL:            https://github.com/harpsichord
Source0:        %{name}-%{version}.tar.gz

%define _unpackaged_files_terminate_build 0

%description
analyzer - utitlies doing data/info analysis
    |-satBlockInfo.py - get storage info when there is RAID controller installed
    |-xsos - Ryan Sawhill Aroha's sosreport examiner
    |-satVersions.sh - extract drv/firmware version from sosreport logs
collector - utitlies which collect key information from various sources
    |-satBiosSettings.py - get BIOS settings independent of OEM specific tools
    |-satRms.py - pull various fields from RMS database
poc - proof of concept of they way data/info might be collected/analyzed
    |-wxParser.py - parse BIOS settings from k=v format to JSON
    |-getBios.sh - primeval way of getting bios settings

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/%{_bindir}/%{name}-%{version}
mkdir -p %{buildroot}/%{_bindir}/%{name}-%{version}/analyzer
mkdir -p %{buildroot}/%{_bindir}/%{name}-%{version}/collector
mkdir -p %{buildroot}/%{_bindir}/%{name}-%{version}/poc
install -m 0755 analyzer/satBlockInfo.py %{buildroot}/%{_bindir}/%{name}-%{version}/analyzer/satBlockInfo.py
install -m 0755 analyzer/satVersions.sh %{buildroot}/%{_bindir}/%{name}-%{version}/analyzer/satVersions.sh
install -m 0755 analyzer/xsos %{buildroot}/%{_bindir}/%{name}-%{version}/analyzer/xsos
install -m 0755 collector/satBiosSettings.py %{buildroot}/%{_bindir}/%{name}-%{version}/collector/satBiosSettings.py
install -m 0755 collector/satRms.py %{buildroot}/%{_bindir}/%{name}-%{version}/collector/satRms.py
install -m 0755 poc/wxParser.py %{buildroot}/%{_bindir}/%{name}-%{version}/poc/wxParser.py
install -m 0755 poc/getBios.sh %{buildroot}/%{_bindir}/%{name}-%{version}/poc/getBios.sh
install -m 0755 README %{buildroot}/%{_bindir}/%{name}-%{version}/README

%files
/%{_bindir}/%{name}-%{version}/analyzer/satBlockInfo.py
/%{_bindir}/%{name}-%{version}/analyzer/satVersions.sh
/%{_bindir}/%{name}-%{version}/analyzer/xsos
/%{_bindir}/%{name}-%{version}/collector/satBiosSettings.py
/%{_bindir}/%{name}-%{version}/collector/satRms.py
/%{_bindir}/%{name}-%{version}/poc/wxParser.py
/%{_bindir}/%{name}-%{version}/poc/getBios.sh

%changelog
* Thu Sep 19 2019 Wu Xi  1.0.0
  - Initial rpm release
