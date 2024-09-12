#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.08.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		libkdcraw
Summary:	Libkdcraw
Name:		ka6-%{kaname}
Version:	24.08.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	7036a09ea5dce79916cc7b31c6e8e1d4
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	libraw-devel >= 0.18
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libkdcraw is a C++ interface around LibRaw library used to decode RAW
picture files. More information about LibRaw can be found at
http://www.libraw.org.

This library is used by kipi-plugins, digiKam and others kipi host
programs.

%description -l pl.UTF-8
Libkdcraw jest interfejsem C++ wokół biblioteki LibRaw używanej do
dekodowania plików RAW. Więcej informacji o LibRaw można znaleźć na
http://www.libraw.org.

Tej biblioteki używają kipi-plugins, digiKam i inne programy kipi.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%ghost %{_libdir}/libKDcrawQt6.so.5
%attr(755,root,root) %{_libdir}/libKDcrawQt6.so.*.*
%{_datadir}/qlogging-categories6/libkdcraw.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KDcrawQt6
%{_libdir}/cmake/KDcrawQt6
%{_libdir}/libKDcrawQt6.so
