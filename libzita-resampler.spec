%define name_base       zita-resampler
%define name            libzita-resampler
%define version         0.1.1
%define release         %mkrel 1
%define lib_major       2
%define lib_name        %mklibname %name_base %{lib_major}
%define lib_name_devel  %mklibname %name_base -d



Summary:       Fast, high-quality sample rate conversion library
Name:          %{name}
Version:       %{version}
Release:       %{release}
License:       GPLv2+
Group:         Sound
URL:           http://www.kokkinizita.net/linuxaudio/zita-resampler/resampler.html
Source0:       http://www.kokkinizita.net/linuxaudio/downloads/zita-resampler-%{version}.tar.bz2
# abort() in undefined in the header file unless we #include <stdlib.h>
# Patch sent upstream via email as there is no bug tracker
Patch0:        zita-resampler-fix-include.patch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libsndfile-devel

%description 
zita-resampler is a C++ library for resampling audio signals. It is
designed to be used within a real-time processing context, to be fast,
and to provide high-quality sample rate conversion.

The library operates on signals represented in single-precision
floating point format. For multichannel operation both the input and
output signals are assumed to be stored as interleaved samples.

The API allows a trade-off between quality and CPU load. For the
latter a range of approximately 1:6 is available. Even at the highest
quality setting zita-resampler will be faster than most similar
libraries, e.g. libsamplerate.

%package -n %{lib_name}
Group:         Sound
Summary:       Fast, high-quality sample rate conversion library


%description -n %{lib_name}
zita-resampler is a C++ library for resampling audio signals. It is
designed to be used within a real-time processing context, to be fast,
and to provide high-quality sample rate conversion.

The library operates on signals represented in single-precision
floating point format. For multichannel operation both the input and
output signals are assumed to be stored as interleaved samples



%package  -n %{lib_name_devel}
Summary:       Development libraries and headers for %{name}
Group:         Sound
Requires:      %{name} = %{version}-%{release}

%description -n %{lib_name_devel}
This package contains the headers and development libraries for %{name}.

%prep
%setup -q -n %name_base-%{version}
%patch0 -p1 -b .fix.include

# To make sure to have the correct Fedora specific flags:
sed -i 's|-O2|%{optflags} -I../libs|' libs/Makefile
sed -i 's|-O3|%{optflags} -I../libs|' apps/Makefile

%build
export LDFLAGS="-L../libs"
#make % {?_smp_mflags} -C libs
%make -C libs
# In order to build apps, we need to create the symlink
# Note that this is originally done at "make install" stage
ln -sf libzita-resampler.so.%{version} libs/libzita-resampler.so
make %{?_smp_mflags} -C apps

%install
rm -rf %{buildroot}
make PREFIX=%{buildroot}%{_prefix} LIBDIR=%{_lib} -C libs install

# The application name is too generic. Just rename:
mkdir -p %{buildroot}%{_bindir}
install -pm 755 apps/resample %{buildroot}%{_bindir}/zita-resample


%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/%{name}.so.*
%{_bindir}/zita-resample

%files -n %{lib_name_devel}
%defattr(-,root,root,-)
%doc docs/*
%{_libdir}/%{name}.so
%{_includedir}/*.h
