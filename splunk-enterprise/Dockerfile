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

EXPOSE 8000


FROM centos:centos7 as splunk-enterprise
COPY --from=builder /usr/local/splunk /usr/local/splunk


FROM splunk-enterprise:latest as manager
WORKDIR /usr/local/splunk
COPY ./server.conf ./etc/system/local/server.conf
EXPOSE 8089
RUN ./bin/splunk start --answer-yes --accept-license --no-prompt
CMD ./bin/splunk start && tail -f /dev/null


FROM splunk-enterprise:latest as sh
ARG ADMIN_PASSWD
ARG HOST_IP
ARG REPLICATION_PORT
ARG MANAGER_IP
ARG SHCLUSTER_LABEL
ARG SECRET
WORKDIR /usr/local/splunk
COPY ./server.conf ./etc/system/local/server.conf
EXPOSE 8089 ${REPLICATION_PORT}
RUN ./bin/splunk start --answer-yes --accept-license --no-prompt \
	&& ./bin/splunk init shcluster-config -auth admin:${ADMIN_PASSWD} -mgmt_uri https://${HOST_IP}:8089 -replication_port ${REPLICATION_PORT} -replication_factor 1 -conf_deploy_fetch_url https://${MANAGER_IP}:8089 -secret ${SECRET} -shcluster_label ${SHCLUSTER_LABEL}
CMD ./bin/splunk start && tail -f /dev/null


FROM splunk-enterprise:latest as idx
WORKDIR /usr/local/splunk
COPY ./server.conf ./etc/system/local/server.conf
EXPOSE 8080 8089
RUN ./bin/splunk start --answer-yes --accept-license --no-prompt
CMD ./bin/splunk start && tail -f /dev/null