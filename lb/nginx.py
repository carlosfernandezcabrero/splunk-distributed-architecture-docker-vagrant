#!/usr/bin/python3

from nginx import Conf, Events, Http, Key, Location, Server, Upstream, dumpf

conf = Conf()
http = Http()

u = Upstream("splunk", Key("ip_hash", ""))
with open("/tmp/shcluster_members.txt") as f:
    for line in f:
        line = line.strip().replace(":", "")
        u.add(Key("server", f"{line}:8000"))
http.add(u)

s = Server()
s.add(Location("~ /", Key("proxy_pass", "http://splunk")))
http.add(s)

conf.add(Events(), http)

dumpf(conf, "/tmp/nginx.conf")
