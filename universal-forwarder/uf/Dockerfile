FROM python:3.11-slim-bullseye
WORKDIR /usr/local/splunk_forwarder

ARG RELEASE_URL

RUN apt-get update \
    && apt-get install -y procps wget \
    && wget --no-check-certificate --no-cache --no-cookies -O - "https://download.splunk.com/products/universalforwarder/releases/${RELEASE_URL}" | tar -xzf - \
    && apt-get purge -y wget \
    && apt-get autoremove -y --purge \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/splunk_forwarder/splunkforwarder

COPY deploymentclient.conf etc/apps/conf_deployment/default/
COPY splunk-launch.conf etc
COPY server.conf etc/system/local/
COPY outputs.conf etc/system/local/

CMD ./bin/splunk start --answer-yes --accept-license --no-prompt && tail -f /dev/null