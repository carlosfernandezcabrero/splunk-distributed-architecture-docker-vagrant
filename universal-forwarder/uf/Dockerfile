ARG DOCKER_FROM=python:3.12-slim
FROM $DOCKER_FROM

ARG CONTAINER_RUN=apt-get update && apt-get install -y procps vim && rm -rf /var/lib/apt/lists/*

ENV TZ="Europe/Madrid"

WORKDIR /usr/local/splunk_forwarder
COPY universalforwarder.tgz .
RUN tar -xzf universalforwarder.tgz && rm universalforwarder.tgz \ 
    && $CONTAINER_RUN

WORKDIR /usr/local/splunk_forwarder/splunkforwarder
COPY deploymentclient.conf etc/apps/conf_deployment/default/
COPY splunk-launch.conf etc
COPY server.conf etc/system/local/
COPY outputs.conf etc/system/local/

CMD ./bin/splunk start --answer-yes --accept-license --no-prompt && tail -f /dev/null