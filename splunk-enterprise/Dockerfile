FROM centos:centos7 as builder

WORKDIR /usr/local

ARG RELEASE_URL

RUN yum install -y wget \
	&& wget --no-check-certificate --no-cache --no-cookies -O - "https://download.splunk.com/products/splunk/releases/${RELEASE_URL}" | tar -xzf - \
	&& yum autoremove -y wget qrencode \
	&& package-cleanup --leaves --all \
	&& yum clean all \
	&& rm -rf /var/cache

WORKDIR /usr/local/splunk/etc

COPY splunk-launch.conf .
COPY user-seed.conf ./system/local



FROM centos:centos7 as splunk-enterprise
COPY --from=builder /usr/local/splunk /usr/local/splunk



FROM splunk-enterprise:latest as splunk-instance
WORKDIR /usr/local/splunk
COPY ./server.conf ./etc/system/local/server.conf
CMD ./bin/splunk start --answer-yes --accept-license --no-prompt \
	&& tail -f /dev/null



FROM splunk-enterprise:latest as hf
WORKDIR /usr/local/splunk
COPY outputs.conf ./etc/system/local/outputs.conf
CMD ./bin/splunk start --answer-yes --accept-license --no-prompt \
	&& tail -f /dev/null



FROM splunk-enterprise:latest as idx
WORKDIR /usr/local/splunk
COPY ./server.conf ./etc/system/local/server.conf
COPY inputs.conf ./etc/system/local/inputs.conf
CMD ./bin/splunk start --answer-yes --accept-license --no-prompt \
	&& tail -f /dev/null

FROM splunk-enterprise:latest as test-sh
WORKDIR /usr/local/splunk
COPY ./server.conf ./etc/system/local/server.conf
CMD ./bin/splunk start --answer-yes --accept-license --no-prompt \
	&& ./bin/splunk add search-server https://192.168.33.5:8089 -auth admin:admin1234 -remoteUsername admin -remotePassword admin1234 \
	&& ./bin/splunk add search-server https://192.168.33.21:8089 -auth admin:admin1234 -remoteUsername admin -remotePassword admin1234 \
	&& ./bin/splunk add search-server https://192.168.33.22:8089 -auth admin:admin1234 -remoteUsername admin -remotePassword admin1234 \
	&& tail -f /dev/null