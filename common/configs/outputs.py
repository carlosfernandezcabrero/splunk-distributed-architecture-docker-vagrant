#!/usr/bin/python3

import sys
from configparser import ConfigParser

outputs_path = sys.argv[1]

config = ConfigParser()
config.optionxform = str

config.read(outputs_path)

config["tcpout"] = {"defaultGroup": "de_group"}

config["tcpout:de_group"] = {"server": "192.168.33.5:9997"}

with open("/tmp/indexers.txt", "r") as indexers_file:
    indexers = indexers_file.read().replace(":", "").splitlines()
    pr_group_servers = ":9997,".join(indexers)
    config["tcpout:pr_group"] = {"server": f"{pr_group_servers}:9997"}

with open(outputs_path, "w") as config_file:
    config.write(config_file)
