%define		trac_ver	0.11
%define		plugin		wikirename
Summary:	Add simple support for renaming/moving wiki pages
Name:		trac-plugin-%{plugin}
Version:	2.1.1
Release:	0.1
License:	BSD
Group:		Applications/WWW
# Source0Download:	http://trac-hacks.org/changeset/latest/wikirenameplugin?old_path=/&filename=wikirenameplugin&format=zip
Source0:	%{plugin}plugin.zip
# Source0-md5:	16637f1de20736455568f8fa30c2e935
URL:		http://trac-hacks.org/wiki/WikiRenamePlugin
BuildRequires:	python-devel
BuildRequires:	unzip
Requires:	trac >= %{trac_ver}
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
%setup -q -n %{plugin}plugin

%build
cd %{trac_ver}
%{__python} setup.py build
%{__python} setup.py egg_info

%install
rm -rf $RPM_BUILD_ROOT
cd %{trac_ver}
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	%banner -e %{name} <<-'EOF'
	To enable the %{plugin} plugin, add to conf/trac.ini:

	[components]
	%{plugin}.* = enabled
EOF
fi

%files
%defattr(644,root,root,755)
%doc %{trac_ver}/README
%attr(755,root,root) %{_bindir}/trac-wikirename
%{py_sitescriptdir}/%{plugin}
%{py_sitescriptdir}/TracWikiRename-*.egg-info
