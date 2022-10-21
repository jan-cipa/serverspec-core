%global install_dir /opt/gdc/serverspec-core
%if 0%{?el7}
# SCL related definitions (CentOS 7 only)
%global scl rh-ruby26
%global _scl_prefix /opt/rh/%{scl}
%endif

Name:             serverspec-core
Summary:          GoodData ServerSpec integration
Version:          2.0.1
Release:          2%{?dist}.gdc1

Group:            GoodData/Tools

License:          ISC
URL:              https://github.com/gooddata/serverspec-core
Source0:          %{name}.tar.gz

%if 0%{?el7}
BuildRequires:    %{scl}-ruby
BuildRequires:    %{scl}-ruby-devel
BuildRequires:    %{scl}-rubygem-rake
BuildRequires:    %{scl}-rubygem-bundler
Requires:         %{scl}-rubygem-bundler
%else
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: rubygem-rake
BuildRequires: rubygem-bundler
Requires:      rubygem-bundler
%endif
BuildRequires: git gcc-c++ make

%prep
%setup -q -c

%build
%if 0%{?el7}
source %{_scl_prefix}/enable
%endif
bundle install --standalone --binstubs --without=development

%install
mkdir -p $RPM_BUILD_ROOT%{install_dir}
cp -a * .bundle $RPM_BUILD_ROOT%{install_dir}
%if 0%{?el7}
cp -a /opt/rh/%{scl}/root/usr/share/gems/* $RPM_BUILD_ROOT%{install_dir}/bundle/ruby/
%else
cp -a /usr/share/gems/* $RPM_BUILD_ROOT%{install_dir}/bundle/ruby/
%endif
install -d $RPM_BUILD_ROOT/usr/bin
mv ./bin/serverspec $RPM_BUILD_ROOT/usr/bin/serverspec
%if 0%{?el7}
sed -i 's,@@SCL_PREFIX@@,%{_scl_prefix},g' $RPM_BUILD_ROOT/usr/bin/serverspec
%else
sed -i '/@@SCL_PREFIX@@/d' $RPM_BUILD_ROOT/usr/bin/serverspec
%endif
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/
mv $RPM_BUILD_ROOT%{install_dir}/serverspec.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/serverspec

%description
GoodData ServerSpec integration - core package.

%files
%attr(0755, root, root) %dir %{install_dir}
%attr(0755, root, root) %{install_dir}/.bundle
%attr(0755, root, root) %{install_dir}/bundle
%attr(0755, root, root) %{install_dir}/bin
%attr(0755, root, root) %dir %{install_dir}/cfg
%attr(0755, root, root) %dir %{install_dir}/spec
%attr(0755, root, root) %dir %{install_dir}/reports
%attr(0755, root, root) %{install_dir}/spec/types
%attr(0755, root, root) %{install_dir}/spec/helper
%attr(0755, root, root) %{install_dir}/cfg/cfg_helper.rb
%attr(0755, root, root) %{install_dir}/cfg/serverspec.yml
%attr(0755, root, root) %{install_dir}/cfg/local.yml
%attr(0755, root, root) %{install_dir}/check_last_run.sh
%attr(0755, root, root) %{install_dir}/cron_run.sh
%attr(0755, root, root) %{install_dir}/Gemfile*
%attr(0755, root, root) %{install_dir}/Rakefile
%attr(0755, root, root) %{install_dir}/spec/spec_helper.rb
%attr(0755, root, root) %{install_dir}/spec/common/test/hosts_spec.rb
%attr(0755, root, root) %doc %{install_dir}/*.md
%attr(0755, root, root) %doc %{install_dir}/LICENSE.txt
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/serverspec
%attr(0755, root, root) /usr/bin/serverspec
%exclude %{install_dir}/makemeusable
%exclude %{install_dir}/specs/serverspec-core.spec
%exclude %{install_dir}/reports/.gitignore
%exclude %{install_dir}/spec/types/.gitignore

%changelog
* Fri Apr 10 2020 Hung Cao <hung.cao@gooddata.com> - 2.0.0-3%{?dist}.gdc1
- CONFIG: SETI-4110 Bump ruby version to 2.6

* Thu Jan 02 2020 King Nguyen <king.nguyen@gooddata.com> - 1.9.13-9%{?dist}.gdc1
- CONFIG: SETI-3728 Bump version of package to 1.9.13-9

* Wed Apr 10 2019 Robert Moucha <robert.moucha@gooddata.com> - 1.9.13-9%{?dist}.gdc1
- TRIVIAL: Do not throw out the rspec exit code

* Tue Aug 07 2018 Adam Tkac <adam.tkac@gooddata.com> - 1.9.13-8%{?dist}.gdc1
- add rubygem-bundler Require

* Fri Jul 27 2018 Michal Vanco <michal.vanco@gooddata.com> - 1.9.13-7%{?dist}.gdc1
- SETI-1475: update rubocop version due to https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-8418

* Thu Jun 15 2017 Andrey Arapov <andrey.arapov@gooddata.com> - 1.9.13-6%{?dist}.gdc1
- SETI-537: use patches from rspec_junit_formatter 0.3.0.pre5

* Thu Jun 15 2017 Andrey Arapov <andrey.arapov@gooddata.com> - 1.9.13-5%{?dist}.gdc1
- SETI-537: revert two previous changes as they required ruby >2 which we do
  not have in EL6.

* Wed Jun 14 2017 Roman Neuhauser <roman.neuhauser@gooddata.com> - 1.9.13-4%{?dist}.gdc1
- getting the previous revision to actually work

* Wed Jun 14 2017 Roman Neuhauser <roman.neuhauser@gooddata.com> - 1.9.13-3%{?dist}.gdc1
- update rspec_junit_formatter to 0.3.0.pre5

* Tue May 23 2017 Martin Surovcak <martin.surovcak@gooddata.com> - 1.9.13-2%{?dist}.gdc1
- update specinfra as previous build was buggy

* Tue May 23 2017 Martin Ducar <martin.ducar@gooddata.com> - 1.9.13-1%{?dist}.gdc1
- upgrade serverspec gem to support content_as_yaml

* Wed May 17 2017 Martin Ducar <martin.ducar@gooddata.com> - 1.9.12-1%{?dist}.gdc1
- docker backend add with el6 compatibility

* Fri Jan 06 2017 Yury Tsarev <yury.tsarev@gooddata.com> 1.9.11-1%{?dist}.gdc
- set serverspec backend early

* Fri Dec 02 2016 Dinar Valeev <dinar.valeev@gooddata.com> 1.9.10-2%{?dist}.gdc
- don't require lsb-redhat-core

* Mon Nov 14 2016 Martin Ducar <martin.ducar@gooddata.com> 1.9.10-1%{?dist}.gdc
- cron_run possible verb/verbs fix

* Mon Nov 14 2016 Hung Cao <hung.cao@gooddata.com> 1.9.9-1%{?dist}.gdc
- cron_run improvements for better nrpe integration

* Tue Oct 04 2016 Martin Surovcak <martin.surovcak@gooddata.com> 1.9.8-1%{?dist}.gdc
- cron_run fixes
- it is mandatory to pass a fqdn or test run subject

* Mon Oct 03 2016 Martin Surovcak <martin.surovcak@gooddata.com> 1.9.7-1%{?dist}.gdc
- cron_run allows passing fqdn as an argument

* Tue Aug 30 2016 Martin Surovcak <martin.surovcak@gooddata.com> 1.9.6-2%{?dist}.gdc
- fix typo in changelog
- fix missing redirect of date to logfile

* Wed Aug 17 2016 Martin Surovcak <martin.surovcak@gooddata.com> 1.9.6-1%{?dist}.gdc
- cron_run.sh logs date

* Thu Mar 31 2016 Yury Tsarev <yury.tsarev@gooddata.com> 1.9.5-1%{?dist}.gdc
- Provide parallel console output for junit enabled rubocop run

* Wed Mar 16 2016 Yury Tsarev <yury.tsarev@gooddata.com> 1.9.4-1%{?dist}.gdc
- Enhance rubocop junit formatter output

* Wed Mar 16 2016 Radek Smidl <radek.smidl@gooddata.com> 1.9.3-1%{?dist}.gdc
- cron_run.sh can take command line parameters

* Tue Mar 15 2016 Yury Tsarev <yury.tsarev@gooddata.com> 1.9.2-1%{?dist}.gdc
- Update embedded rubocop version to 0.37

* Tue Mar 1 2016 Yury Tsarev <yury.tsarev@gooddata.com> 1.9.1-1%{?dist}.gdc
- Add customized rspec formatter
- Include LICENSE.txt

* Wed Dec 16 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.9-1%{?dist}.gdc
- Add junit formatter to rubocop

* Fri Dec 11 2015 Martin Ducár <martin.ducar@gooddata.com> 1.8-1%{?dist}.gdc
- Added netcat dependency for host port reachable test

* Fri Nov 20 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.8-0%{?dist}.gdc
- New rake task selfcheck to test serverspec-core features
- New be_in matcher using include?

* Mon Nov 2 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.7-7%{?dist}.gdc
- Fix rubygem193-bundler dependency for el6 with proper dist evaluation

* Mon Nov 2 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.7-6%{?dist}.gdc
- Enable el6/el7 cross packaging
- Fix exit status default value

* Thu Oct 22 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.7-1.gdc
- Remove tag notion confusion by renaming serverspec tag to label

* Fri Aug 28 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.6-1.gdc
- Embed rubocop rake tasks into serverspec

* Mon Aug 10 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.5-1.gdc
- Add cista related gems

* Mon Aug 10 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.4-1.gdc
- Add junit formatter

* Mon Aug 10 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.3-5.gdc
- Fix the case of undefined roles for host

* Wed Aug 05 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.3-4.gdc
- Compile overall json report also with default rake task

* Wed Aug 05 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.3-3.gdc
- Add runtime dependency on bundler

* Tue Aug 04 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.3-2.gdc
- Update cron_run.sh to use bundled serverspec

* Tue Aug 04 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.3-1.gdc
- Update dependencies in bundle to include recent specinfra enhancements
- Provide default rake task so the user can just run `serverspec` for testing

* Tue Aug 04 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.2-2.gdc
- Package serverspec together with isolated rubygem bundle
- Introduce systemwide wrapper of /usr/bin/serverspec

* Mon Jul 20 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.1-2.gdc
- fix _spec.rb inclusion in SPEC_DIR

* Thu Jul 16 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.1-1.gdc
- Sample minimal local configuration provided
- Output formatting option in CLI
- Tag filtering ability in CLI

* Tue Jul 14 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-11.gdc
- fixed bug when including custom types

* Mon Jul 13 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-10.gdc
- types are included from both SPEC_DIR and pgk_root paths
- fix YAML include
- get_all_hosts respects CFG_DIR option

* Thu Jul 02 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-9.gdc
- default spec_helper provides SPEC_DIR to all included specs and helpers
- spec/types is back

* Thu Jul 02 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-8.gdc
- exclude reports/.gitignore

* Thu Jul 02 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-7.gdc
- create default reports directory while installing package
- do not include types in package - they should be delivered with specs

* Wed Jul 01 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-6.gdc
- cron should not exec bundle anymore

* Mon Jun 29 2015 Radek Smidl <radek.smidl@gooddata.com> 1.0-5.gdc
- REPORTS_PATH renamed to REPORTS_DIR

* Mon Jun 29 2015 Radek Smidl <radek.smidl@gooddata.com> 1.0-4.gdc
- CONF_DIR and SPEC_DIR options added

* Mon Jun 29 2015 Radek Smidl <radek.smidl@gooddata.com> 1.0-3.gdc
- sysconfig support added

* Wed Jun 10 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.0-2.gdc
- Fix versioning and file inclusion

* Tue Jun 09 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-1.gdc
- Initial rpmbuild
