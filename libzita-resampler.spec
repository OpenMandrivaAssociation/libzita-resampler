%define name_base       zita-resampler
%define lib_major       1
%define lib_name        %mklibname %name_base %{lib_major}
%define lib_name_devel  %mklibname %name_base -d



Summary:       Fast, high-quality sample rate conversion library
Name:          libzita-resampler
Version:       1.1.0
Release:       2
License:       GPLv2+
Group:         Sound
URL:           http://www.kokkinizita.net/linuxaudio/zita-resampler/resampler.html
Source0:       http://www.kokkinizita.net/linuxaudio/downloads/zita-resampler-%{version}.tar.bz2
BuildRequires: sndfile-devel

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
Requires:      %{lib_name} = %{version}-%{release}
Provides:      %{name}-devel = %{version}-%{release}

%description -n %{lib_name_devel}
This package contains the headers and development libraries
for %{name}.



%package -n %{name_base}
Group:         Sound
Requires:      %{lib_name} = %{version}-%{release}
Summary:       The zresample executable comming with %{name}


%description -n %{name_base}
zita-resampler is a C++ library for resampling audio signals. It is
designed to be used within a real-time processing context, to be fast,
and to provide high-quality sample rate conversion.

This package provides the zresample executable.


%prep
%setup -q -n %name_base-%{version}

# To make sure to have the correct Fedora specific flags:
sed -i 's|-O2|%{optflags} -I../libs|' libs/Makefile
sed -i 's|-O3|%{optflags} -I../libs|' apps/Makefile
sed -i 's|ldconfig||' libs/Makefile
sed -i 's|-march=native||' libs/Makefile
sed -i 's|-march=native||' apps/Makefile

%build
export LDFLAGS="-L../libs"
#make % {?_smp_mflags} -C libs
%make -C libs
# In order to build apps, we need to create the symlink
# Note that this is originally done at "make install" stage
strip libs/libzita-resampler.so.%{version}
ln -sf libzita-resampler.so.%{version} libs/libzita-resampler.so
make %{?_smp_mflags} -C apps

%install
make PREFIX=%{buildroot}%{_prefix} LIBDIR=%{_lib} -C libs install
make PREFIX=%{buildroot}%{_prefix} BINDIR=%{_bin} \
     MANDIR=%{buildroot}%{_mandir}/man1 -C apps install

%clean

%files -n %{name_base}
%{_bindir}/zresample
%{_mandir}/man1/zresample.*

%files -n %{lib_name}
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/%{name}.so.*

%files -n %{lib_name_devel}
%defattr(-,root,root,-)
%doc docs/*
%{_libdir}/%{name}.so
%{_includedir}/%{name_base}/*.h


%changelog
* Sun Apr 15 2012 Frank Kober <emuse@mandriva.org> 1.1.0-1
+ Revision: 791106
- removed march CXX flag from Makefile
- update to new version 1.1.0
  o libmajor is 1
  o separate package for zresample binary
  o drop patch0, got fixed upstream

* Wed Nov 02 2011 Alexander Khrukin <akhrukin@mandriva.org> 0.1.1-2
+ Revision: 712209
- rpmlint fixes and dependency fixed into mklibname

* Wed Nov 02 2011 Alexander Khrukin <akhrukin@mandriva.org> 0.1.1-1
+ Revision: 712202
- imported package libzita-resampler

