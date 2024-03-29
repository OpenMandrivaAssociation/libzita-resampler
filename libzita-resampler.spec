%define major 1
%define libname %mklibname zita-resampler %{major}
%define devname %mklibname zita-resampler -d

Summary:	Fast, high-quality sample rate conversion library
Name:		libzita-resampler
Version:	1.11.2
Release:	1
License:	GPLv3
Group:		Sound
Url:		https://kokkinizita.linuxaudio.org/linuxaudio/zita-resampler/resampler.html
Source0:	https://kokkinizita.linuxaudio.org/linuxaudio/downloads/zita-resampler-%{version}.tar.xz
BuildRequires:	pkgconfig(sndfile)

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

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Fast, high-quality sample rate conversion library
Group:		System/Libraries

%description -n %{libname}
zita-resampler is a C++ library for resampling audio signals. It is
designed to be used within a real-time processing context, to be fast,
and to provide high-quality sample rate conversion.

The library operates on signals represented in single-precision
floating point format. For multichannel operation both the input and
output signals are assumed to be stored as interleaved samples

%files -n %{libname}
%doc AUTHORS COPYING
%{_libdir}/%{name}.so.%{version}
%{_libdir}/%{name}.so.%{major}

#----------------------------------------------------------------------------

%package  -n %{devname}
Summary:	Development libraries and headers for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains the headers and development libraries
for %{name}.

%files -n %{devname}
%doc docs/*
%{_libdir}/%{name}.so
%{_includedir}/zita-resampler/*.h

#----------------------------------------------------------------------------

%package -n zita-resampler
Summary:	The zresample executable comming with %{name}
Group:		Sound

%description -n zita-resampler
zita-resampler is a C++ library for resampling audio signals. It is
designed to be used within a real-time processing context, to be fast,
and to provide high-quality sample rate conversion.

This package provides the zresample executable.

%files -n zita-resampler
%{_bindir}/zresample
%{_bindir}/zretune
%{_mandir}/man1/zresample.*
%{_mandir}/man1/zretune.*

#----------------------------------------------------------------------------

%prep
%setup -q -n zita-resampler-%{version}

# To make sure to have the correct Fedora specific flags:
sed -i 's|-O2|%{optflags}|' source/Makefile
sed -i 's|-O2|%{optflags} -I../source|' apps/Makefile
sed -i 's|ldconfig||' source/Makefile
sed -i 's|-march=native||' source/Makefile
sed -i 's|-march=native||' apps/Makefile
sed -i -e '/install -d/d' apps/Makefile

%build
export LDFLAGS="-L../source"
%make_build PREFIX=%{_prefix} -C source
# In order to build apps, we need to create the symlink
# Note that this is originally done at "make install" stage
ln -sf libzita-resampler.so.%{version} source/libzita-resampler.so

%make_build PREFIX=%{_prefix} -C apps

%install
ln -sf libzita-resampler.so.%{version} source/libzita-resampler.so.%{major}
mkdir -p %{buildroot}%{_mandir}/man1 %{buildroot}%{_bindir}
%make_install PREFIX=%{_prefix} -C source
%make_install PREFIX=%{_prefix} -C apps

