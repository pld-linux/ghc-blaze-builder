%define		pkgname	blaze-builder
Summary:	Efficient buffered output
Name:		ghc-%{pkgname}
Version:	0.3.1.1
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	ca14afe9215dd44fe5dc4055a05ec560
URL:		http://hackage.haskell.org/package/PACKAGE_NAME/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-prof
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_releq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddoc files
%define		_noautocompressdoc	*.haddock

%description
This library provides an abstraction of buffered output of byte
streams and several convenience functions to exploit it. For example,
it allows to efficiently serialize Haskell values to lazy bytestrings
with a large average chunk size. The large average chunk size allows
to make good use of cache prefetching in later processing steps
(e.g. compression) and reduces the sytem call overhead when writing
the resulting lazy bytestring to a file or sending it over the
network.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 --enable-library-profiling \
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
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES README* TODO
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Char
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Char/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Html
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Html/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Internal/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Char/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Html/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/Internal/*.p_hi
