%define		trac_ver	0.11
%define		plugin		wikirename
Summary:	Add simple support for renaming/moving wiki pages
Name:		trac-plugin-%{plugin}
Version:	2.1.1
Release:	1
License:	BSD
Group:		Applications/WWW
Source0:	http://trac-hacks.org/changeset/latest/wikirenameplugin?old_path=/&format=zip#/%{plugin}-%{version}.zip
# Source0-md5:	c2c5d628406ca268d59bf231386e062a
URL:		http://trac-hacks.org/wiki/WikiRenamePlugin
BuildRequires:	python-devel
BuildRequires:	unzip
Requires:	trac >= %{trac_ver}.7-3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This plugin allows you to rename wiki pages. It is an evolution of the
WikiRenameScript, and currently has the same limitations.

It will move a page and its history, and will rewrite explicit links
[wiki:PageName Label] leading to it from other wiki pages. It will
also move any attachments on the page.

caution: Currently this plugin doesn't interact well with the
TagsPlugin. You should be careful to remove any tags on a page before
renaming it, and then re-adding them to the new page.

You can access the page rename form through the Admin system. For
convenience, a link is also added to the context navigation bar in the
wiki.

%prep
%setup -qc
mv %{plugin}plugin/%{trac_ver}/* .

%build
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
trac-enableplugin "%{plugin}.*"

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/trac-wikirename
%{py_sitescriptdir}/%{plugin}
%{py_sitescriptdir}/TracWikiRename-*.egg-info
