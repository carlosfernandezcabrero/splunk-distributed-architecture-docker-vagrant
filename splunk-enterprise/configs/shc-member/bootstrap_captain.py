import os
from configparser import ConfigParser

config = ConfigParser()
config.read("/usr/local/splunk/etc/system/local/user-seed.conf")

username = config["user_info"]["USERNAME"]
pwd = config["user_info"]["PASSWORD"]

file = open("shcluster_members.txt", "r")
contents = file.read().replace(":", "").splitlines()
file.close()

server_list = ":8089,https://".join(contents)

cmd_start_splunk = (
    "/usr/local/splunk/bin/splunk start --answer-yes --accept-license --no-prompt"
)
cmd_bootstrap_captain = '/usr/local/splunk/bin/splunk bootstrap shcluster-captain -servers_list "https://{}:8089" -auth {}:{}'.format(
    server_list, username, pwd
)

os.system(" && ".join([cmd_start_splunk, cmd_bootstrap_captain]))
