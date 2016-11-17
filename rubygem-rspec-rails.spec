%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from rspec-rails-2.6.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rspec-rails

# Circular dependency with rubygem-ammeter.
%{?_with_bootstrap: %global bootstrap 1}

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 3.4.0
Release: 5%{?dist}
Summary: RSpec for Rails
Group: Development/Languages
License: MIT
URL: http://github.com/rspec/rspec-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rspec/rspec-rails.git && cd rspec-rails && git checkout v3.4.0
# tar czvf rspec-rails-3.4.0-tests.tgz features/ spec/
Source1: %{gem_name}-%{version}-tests.tgz

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems)
Requires:      %{?scl_prefix}rubygem(activesupport) >= 3.0
Requires:      %{?scl_prefix}rubygem(activesupport) < 4.3
Requires:      %{?scl_prefix}rubygem(actionpack) >= 3.0
Requires:      %{?scl_prefix}rubygem(actionpack) < 4.3
Requires:      %{?scl_prefix}rubygem(railties) >= 3.0
Requires:      %{?scl_prefix}rubygem(railties) < 4.3
Requires:      %{?scl_prefix}rubygem(rspec-core) => 3.4.0
Requires:      %{?scl_prefix}rubygem(rspec-core) < 3.5
Requires:      %{?scl_prefix}rubygem(rspec-expectations) => 3.4.0
Requires:      %{?scl_prefix}rubygem(rspec-expectations) < 3.5
Requires:      %{?scl_prefix}rubygem(rspec-mocks) => 3.4.0
Requires:      %{?scl_prefix}rubygem(rspec-mocks) < 3.5
Requires:      %{?scl_prefix}rubygem(rspec-support) => 3.4.0
Requires:      %{?scl_prefix}rubygem(rspec-support) < 3.5
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
%if ! 0%{?bootstrap}
BuildRequires: %{?scl_prefix}rubygem(cucumber)
BuildRequires: %{?scl_prefix}rubygem(actionmailer)
BuildRequires: %{?scl_prefix}rubygem(activerecord)
BuildRequires: %{?scl_prefix}rubygem(ammeter)
BuildRequires: %{?scl_prefix_ruby}rubygem(bundler)
BuildRequires: %{?scl_prefix}rubygem(railties)
BuildRequires: %{?scl_prefix}rubygem(rspec)
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
%endif
BuildArch:     noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
RSpec for Rails-3+.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%if ! 0%{?bootstrap}

%check
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}

# Bundler is used to execute two tests, so give him Gemfile.
echo "gem 'rspec', :require => false" > Gemfile

# I have no idea why this is passing upstream, since when RSpec are not supposed
# to be loaded, then RSpec::Support can't exist.
sed -i '/uninitialized constant RSpec::Support/ s/::Support//' spec/sanity_check_spec.rb

# Avoid git dependency. This is not funcitonal test anyway, just style check.
sed -i 's/`git ls-files -z`/""/' spec/rspec/rails_spec.rb

%{?scl:scl enable %{scl} - << \EOF}
rspec -rspec_helper -rbundler spec
%{?scl:EOF}

# Needs to generate a rails test application or ship pregenerated one (see
# generate:app rake task). This would be quite fragile.
# cucumber
popd
%endif

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_instdir}/License.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Capybara.md
%doc %{gem_instdir}/Changelog.md
%doc %{gem_instdir}/README.md

%changelog
* Wed Apr 06 2016 Pavel Valena <pvalena@redhat.com> - 3.4.0-5
- Enable tests

* Wed Apr 06 2016 Pavel Valena <pvalena@redhat.com> - 3.4.0-4
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 08 2015 Vít Ondruch <vondruch@redhat.com> - 3.4.0-2
- Re-enable tests.

* Tue Dec 08 2015 Mamoru TASAKA <mtasaka@fedoraproject.og> - 3.4.0-1
- Update to rspec-rails 3.4.0.
- Once disable tests

* Tue Aug 04 2015 Vít Ondruch <vondruch@redhat.com> - 3.3.3-1
- Update to rspec-rails 3.3.3.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 25 2015 Vít Ondruch <vondruch@redhat.com> - 3.2.1-1
- Update to rspec-rails 3.2.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 12 2014 Vít Ondruch <vondruch@redhat.com> - 2.14.1-1
- Update to rspec-rails 2.14.1.

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.og> - 2.14.0-2
- Enable test suite again

* Fri Aug 16 2013 Mamoru TASAKA <mtasaka@fedoraproject.og> - 2.14.0-1
- Update to rspec-rails 2.14.0
- Still tests is disabled for now

* Mon Aug 12 2013 Josef Stribny <jstribny@redhat.com> - 2.13.0-4
- Relax Rails deps and disable tests for now

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.0-2
- Enable test suite again

* Thu Mar 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.13.0-1
- Update to rspec-rails 2.13.0

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 2.12.0-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.0-2
- Enable test suite again

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.12.0-1
- Update to rspec-rails 2.12.0

* Tue Oct 16 2012 Vít Ondruch <vondruch@redhat.com> - 2.11.4-1
- Update to rspec-rails 2.11.4.

* Sat Oct 13 2012 Vít Ondruch <vondruch@redhat.com> - 2.11.0-1
- Update to rspec-rails 2.11.0.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Vít Ondruch <vondruch@redhat.com> - 2.8.1-2
- Tests enabled.

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 2.8.1-1
- Rebuilt for Ruby 1.9.3.
- Update to rspec-rails 2.8.1.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Vít Ondruch <vondruch@redhat.com> - 2.6.1-3
- Fixed .gemspec to contain correct dependencies (rhbz#747405).

* Tue Aug 23 2011 Vít Ondruch <vondruch@redhat.com> - 2.6.1-2
- Rebuilt due to the trailing slash bug of rpm-4.9.1

* Tue Jun 07 2011 Vít Ondruch <vondruch@redhat.com> - 2.6.1-1
- Updated to the rspec-rails 2.6.1

* Mon May 23 2011 Vít Ondruch <vondruch@redhat.com> - 2.6.0-1
- Initial package
