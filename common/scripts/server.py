#!/usr/bin/python3

import sys
from configparser import ConfigParser

config = ConfigParser()
config.optionxform = str

config.read("/tmp/server.conf")

if not config.has_section("general"):
    config.add_section("general")

config["general"]["serverName"] = sys.argv[1]

with open("/tmp/server.conf", "w") as config_file:
    config.write(config_file)
