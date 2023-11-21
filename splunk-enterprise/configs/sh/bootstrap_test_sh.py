import os
from configparser import ConfigParser

config = ConfigParser()
config.read("/usr/local/splunk/etc/system/local/user-seed.conf")

username = config["user_info"]["USERNAME"]
pwd = config["user_info"]["PASSWORD"]

os.system(
    "/usr/local/splunk/bin/splunk start --answer-yes --accept-license --no-prompt && /usr/local/splunk/bin/splunk add search-server https://192.168.33.5:8089 -auth {}:{} -remoteUsername {} -remotePassword {}".format(
        username, pwd, username, pwd
    )
)
