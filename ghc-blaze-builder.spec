#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	blaze-builder
Summary:	Efficient buffered output
Summary(pl.UTF-8):	Wydajne, buforowane wyjście
Name:		ghc-%{pkgname}
Version:	0.4.1.0
Release:	3
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/blaze-builder
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	c3cc5bdc46bd6e8bf5142cda2b0679b6
URL:		http://hackage.haskell.org/package/blaze-builder
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-bytestring < 1
BuildRequires:	ghc-text >= 0.10
BuildRequires:	ghc-text < 1.3
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-bytestring-prof < 1
BuildRequires:	ghc-text-prof >= 0.10
BuildRequires:	ghc-text-prof < 1.3
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4
Requires:	ghc-base < 5
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-bytestring < 1
Requires:	ghc-text >= 0.10
Requires:	ghc-text < 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library provides an abstraction of buffered output of byte
streams and several convenience functions to exploit it. For example,
it allows to efficiently serialize Haskell values to lazy bytestrings
with a large average chunk size. The large average chunk size allows
to make good use of cache prefetching in later processing steps
(e.g. compression) and reduces the system call overhead when writing
the resulting lazy bytestring to a file or sending it over the
network.

%description -l pl.UTF-8
Ta biblioteka zapewnia warstwę abstrakcji buforowanego wyjścia
strumieni bajtów oraz kilka wygodnych funkcji do jej wykorzystania.
Pozwala na przykład efektywnie serializować wartości haskellowe do
leniwych łańcuchów bajtów o dużym przeciętnym rozmiarze bloku. Duży
przeciętny rozmiar bloku pozwala na dobre wykorzystanie wypełniania
pamięci podręcznej z wyprzedzeniem (prefetch) dla dalszych etapów
przetwarzania (np. kompresji) i zmniejsza narzut wywołań systemowych
przy zapisie wynikowych leniwych łańcuchów bajtów do pliku lub
wysyłaniu ich przez sieć.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-base-prof < 5
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-bytestring-prof < 1
Requires:	ghc-text-prof >= 0.10
Requires:	ghc-text-prof < 1.3

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES README* TODO %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSblaze-builder-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSblaze-builder-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSblaze-builder-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Char
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Char/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Char/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Compat
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Compat/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Compat/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Html
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Html/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Html/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Internal/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSblaze-builder-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Char/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Compat/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Html/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Internal/*.p_hi
%endif
