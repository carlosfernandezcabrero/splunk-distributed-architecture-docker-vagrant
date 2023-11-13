FROM nginx:mainline-alpine3.18-slim

WORKDIR /etc/nginx

RUN rm -rf /usr/share/nginx/html/* && rm -rf conf.d/*

COPY nginx.conf nginx.conf
