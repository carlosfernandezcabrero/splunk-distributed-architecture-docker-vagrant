ARG DOCKER_FROM=python:3.12-slim
FROM $DOCKER_FROM as splunk-enterprise

ARG CONTAINER_RUN=apt-get update && apt-get install -y procps vim && rm -rf /var/lib/apt/lists/*

ENV TZ="Europe/Madrid"

WORKDIR /usr/local
COPY splunk-enterprise.tgz .
RUN tar -xzf splunk-enterprise.tgz

WORKDIR /usr/local/splunk/etc
COPY server.conf system/local
COPY splunk-launch.conf .
COPY user-seed.conf system/local

RUN $CONTAINER_RUN

CMD /usr/local/splunk/bin/splunk start --answer-yes --accept-license --no-prompt \
	&& tail -f /dev/null



FROM splunk-enterprise as hf
WORKDIR /usr/local/splunk
COPY outputs.conf etc/system/local



FROM splunk-enterprise as idx
WORKDIR /usr/local/splunk
COPY inputs.conf etc/system/local



FROM splunk-enterprise as test-sh
WORKDIR /tmp
COPY distsearch.conf /usr/local/splunk/etc/system/local



FROM splunk-enterprise as shcluster-captain
WORKDIR /tmp
COPY shcluster_members.txt .
COPY bootstrap_captain.py .
CMD python bootstrap_captain.py \
	&& tail -f /dev/null