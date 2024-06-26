#!/usr/bin/python3

import sys
from configparser import ConfigParser

config = ConfigParser()
config.optionxform = str

config.read("/tmp/server.conf")


config["clustering"] = {
    "master_uri": "https://192.168.56.2:8089",
    "pass4SymmKey": "yoursecretkey",
    "mode": "searchhead",
}

replication_port_section = "replication_port://9888"
if not config.has_section(replication_port_section):
    config.add_section(replication_port_section)

config["shclustering"] = {
    "conf_deploy_fetch_url": "https://192.168.56.2:8089",
    "disabled": "0",
    "pass4SymmKey": "yoursecretkey",
    "shcluster_label": "cluster_1",
    "replication_factor": "2",
    "mgmt_uri": sys.argv[1],
}

with open("/tmp/server.conf", "w") as config_file:
    config.write(config_file)
