#!/usr/bin/python3

import sys
from configparser import ConfigParser

server_path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/server.conf"

config = ConfigParser()
config.optionxform = str

config.read(server_path)

if not config.has_section("general"):
    config.add_section("general")

config["general"]["serverName"] = sys.argv[1]

with open(server_path, "w") as config_file:
    config.write(config_file)
