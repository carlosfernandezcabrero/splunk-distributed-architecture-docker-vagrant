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

EXPOSE 8000


FROM centos:centos7 as splunk-enterprise
COPY --from=builder /usr/local/splunk /usr/local/splunk


FROM splunk-enterprise:latest as manager
WORKDIR /usr/local/splunk
COPY ./server.conf ./etc/system/local/server.conf
EXPOSE 8089
RUN ./bin/splunk start --answer-yes --accept-license --no-prompt --seed-passwd admin1234
CMD ./bin/splunk start && tail -f /dev/null


FROM splunk-enterprise:latest as sh
WORKDIR /usr/local/splunk
COPY ./server.conf ./etc/system/local/server.conf
EXPOSE 8089
RUN ./bin/splunk start --answer-yes --accept-license --no-prompt --seed-passwd admin1234
CMD ./bin/splunk start && tail -f /dev/null


FROM splunk-enterprise:latest as idx
WORKDIR /usr/local/splunk
COPY ./server.conf ./etc/system/local/server.conf
EXPOSE 8080 8089
RUN ./bin/splunk start --answer-yes --accept-license --no-prompt --seed-passwd admin1234
CMD ./bin/splunk start && tail -f /dev/null