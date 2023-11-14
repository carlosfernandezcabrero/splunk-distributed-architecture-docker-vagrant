FROM centos:centos7 as builder

WORKDIR /usr/local

ARG RELEASE_URL=7.3.6/linux/splunk-7.3.6-47d8552a4d84-Linux-x86_64.tgz

RUN yum install -y wget \
	&& wget --no-check-certificate --no-cache --no-cookies -O - "https://download.splunk.com/products/splunk/releases/${RELEASE_URL}" | tar -xzf - \
	&& yum autoremove -y wget qrencode \
	&& package-cleanup --leaves --all \
	&& yum clean all \
	&& rm -rf /var/cache



FROM centos:centos7 as splunk-enterprise
COPY --from=builder /usr/local/splunk /usr/local/splunk

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
WORKDIR /usr/local/splunk
CMD ./bin/splunk start --answer-yes --accept-license --no-prompt \
	&& ./bin/splunk add search-server https://192.168.33.5:8089 -auth admin:admin1234 -remoteUsername admin -remotePassword admin1234 \
	&& ./bin/splunk add search-server https://192.168.33.21:8089 -auth admin:admin1234 -remoteUsername admin -remotePassword admin1234 \
	&& ./bin/splunk add search-server https://192.168.33.22:8089 -auth admin:admin1234 -remoteUsername admin -remotePassword admin1234 \
	&& tail -f /dev/null