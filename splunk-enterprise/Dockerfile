FROM centos:centos7 as splunk-enterprise

ENV TZ="Europe/Madrid"

WORKDIR /usr/local
COPY splunk-enterprise.tgz .
RUN tar -xzf splunk-enterprise.tgz

WORKDIR /usr/local/splunk/etc
COPY server.conf system/local/server.conf
COPY splunk-launch.conf .
COPY user-seed.conf system/local

CMD /usr/local/splunk/bin/splunk start --answer-yes --accept-license --no-prompt \
	&& tail -f /dev/null



FROM splunk-enterprise as hf
WORKDIR /usr/local/splunk
COPY outputs.conf etc/system/local/outputs.conf



FROM splunk-enterprise as idx
WORKDIR /usr/local/splunk
COPY inputs.conf etc/system/local/inputs.conf



FROM splunk-enterprise as test-sh
WORKDIR /tmp
COPY bootstrap_test_sh.py .
CMD python bootstrap_test_sh.py \
	&& tail -f /dev/null



FROM splunk-enterprise as shcluster-captain
WORKDIR /tmp
COPY shcluster_members.txt .
COPY bootstrap_captain.py .
CMD python bootstrap_captain.py \
	&& tail -f /dev/null