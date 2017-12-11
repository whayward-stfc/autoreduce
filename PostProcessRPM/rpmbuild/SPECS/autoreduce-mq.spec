Summary: autoreduce-mq
Name: autoreduce-mq
Version: 1.3
Release: 16
Group: Applications/Engineering
prefix: /usr
BuildRoot: %{_tmppath}/%{name}
License: Unknown
Source: autoreduce-mq.tgz
Requires: libNeXus.so.0()(64bit) libc.so.6()(64bit) libc.so.6(GLIBC_2.2.5)(64bit)
Requires: mantid 
Requires: python-stompest 
Requires: python-stompest.async
Requires: python-requests
%define debug_package %{nil}


%description
Autoreduce program to automatically catalog and reduce neutron data

%prep
%setup -q -n %{name}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/autoreduce
mkdir -p %{buildroot}/opt/activemq/conf
install -m 664 ../autoreduce-mq/etc/autoreduce/post_process_consumer.conf  %{buildroot}%{_sysconfdir}/autoreduce/post_process_consumer.conf
install -m 664 ../autoreduce-mq/opt/activemq/conf/activemq.xml  %{buildroot}/opt/activemq/conf/activemq.xml
install -m 755 -d 	 ../autoreduce-mq/usr	 %{buildroot}/usr
mkdir -p %{buildroot}%{_bindir}
install -m 755	 ../autoreduce-mq/usr/bin/autoreduction_logging_setup.py	 %{buildroot}%{_bindir}/autoreduction_logging_setup.py
install -m 755	 ../autoreduce-mq/usr/bin/daemon.py	 %{buildroot}%{_bindir}/daemon.py
install -m 755	 ../autoreduce-mq/usr/bin/queueProcessor.py	 %{buildroot}%{_bindir}/queueProcessor.py
install -m 755	 ../autoreduce-mq/usr/bin/queueProcessor_daemon.py	 %{buildroot}%{_bindir}/queueProcessor_daemon.py
install -m 755	 ../autoreduce-mq/usr/bin/Configuration.py	 %{buildroot}%{_bindir}/Configuration.py
install -m 755	 ../autoreduce-mq/usr/bin/PostProcessAdmin.py	 %{buildroot}%{_bindir}/PostProcessAdmin.py
install -m 755	 ../autoreduce-mq/usr/bin/statusMonitor.py	 %{buildroot}%{_bindir}/statusMonitor.py
install -m 755	 ../autoreduce-mq/usr/bin/statusMonitor_daemon.py	 %{buildroot}%{_bindir}/statusMonitor_daemon.py


%post

%files
%config %{_sysconfdir}/autoreduce/post_process_consumer.conf
%config /opt/activemq/conf/activemq.xml
%attr(755, -, -) %{_bindir}/autoreduction_logging_setup.py
%attr(755, -, -) %{_bindir}/queueProcessor.py
%attr(755, -, -) %{_bindir}/queueProcessor_daemon.py
%attr(755, -, -) %{_bindir}/statusMonitor.py
%attr(755, -, -) %{_bindir}/statusMonitor_daemon.py

%attr(755, -, -) %{_bindir}/daemon.py
%attr(755, -, -) %{_bindir}/Configuration.py
%attr(755, -, -) %{_bindir}/PostProcessAdmin.py