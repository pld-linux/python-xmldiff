#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Create diffs of XML files
Summary(pl.UTF-8):	Tworzenie diffów plików XML
Name:		python-xmldiff
# keep 2.4 here for python 2.x support
Version:	2.4
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/xmldiff/
Source0:	https://files.pythonhosted.org/packages/source/x/xmldiff/xmldiff-%{version}.tar.gz
# Source0-md5:	1728f65d01c5cb1f3c3838d489a1569d
URL:		https://pypi.org/project/xmldiff/
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-lxml >= 3.1.0
BuildRequires:	python-pytest
BuildRequires:	python-six
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-sphinx_argparse >= 0.2.2
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xmldiff is a library and a command-line utility for making diffs out
of XML. This may seem like something that doesn't need a dedicated
utility, but change detection in hierarchical data is very different
from change detection in flat data. XML type formats are also not only
used for computer readable data, it is also often used as a format for
hierarchical data that can be rendered into human readable formats. A
traditional diff on such a format would tell you line by line the
differences, but this would not be be readable by a human. xmldiff
provides tools to make human readable diffs in those situations.

%description -l pl.UTF-8
xmldiff to biblioteka i narzędzie linii poleceń do tworzenia
zestawienia różnic (diffów) danych XML. Może to nie wydawać się
zadaniem wymagającym dedykowanego narzędzia, ale wykrywanie zmian w
danych hierarchicznych różni się od wykrywania zmian w płaskich
danych. Formaty typu XML nie służą tylko do danych czytelnych dla
komputera, ale często są używane także jako format danych
hierarchicznych odwzorowywanych w formatach czytelnych dla ludzi.
Tradycyjny diff takiego formatu pokaże różnice linia po linii, ale nie
będzie to czytelne dla człowieka. xmldiff udostępnia narzędzia do
tworzenia diffów czytelnych dla człowieka w takich sytuacjach.

%package apidocs
Summary:	API documentation for Python xmldiff module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona xmldiff
Group:		Documentation

%description apidocs
API documentation for Python xmldiff module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona xmldiff.

%prep
%setup -q -n xmldiff-%{version}

%build
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/xmldiff{,-2}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/xmlpatch{,-2}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/xmldiff-2
%attr(755,root,root) %{_bindir}/xmlpatch-2
%{py_sitescriptdir}/xmldiff
%{py_sitescriptdir}/xmldiff-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
