# -*- coding: utf-8 -*-
"""
wm_config.py
wpsec_mon

@author: Created by Shen Min (https://nicrosoft.net) on 2023-08-01.
"""

import json
import wm_utils

_def_options = {
    "time_diff": 0,
    "debug": False,
    "mysql_ssh": False,
    "mysql_ssh_host": "",
    "mysql_ssh_port": 22,
    "mysql_ssh_user": "root",
    "mysql_ssh_pri_key": "/home/user/.ssh/id_rsa",
    "mysql_host": "127.0.0.1",
    "mysql_user": "root",
    "mysql_password": "",
    "dbs":{"wordpress1":{"user_count":1, "root_path":"/home/web/wordpress1/public_html/"}, "wordpress2": {"user_count":2, "root_path":"/home/web/wordpress2/public_html/"}},
    "send_email": True,
    "smtp_host": "smtp.googlemail.com",
    "smtp_port": 587,
    "smtp_user": "",
    "smtp_password": "",
    "send_email_to": "me@gmail.com",
    "send_email_subject_prefix": "WordPress Alert from wpsec_mon: ",
    "send_email_subject_suffix_uc": "Suspicious Users Added", # Alert for users added
    "send_email_subject_suffix_fc": "Suspicious Files Added" # Alert for files added
}

_options_obj = None

class wm_config:
    options = _def_options

    def __init__(self):
        options_str = wm_utils.read_from_file(wm_utils.get_run_dir() + "/settings.conf")
        if options_str is None:
            self.options = _def_options
        else:
            try:
                self.options = json.loads(options_str)
            except Exception:
                self.options = _def_options

    def write_config(self):
        options_str = json.dumps(self.options, indent=4, sort_keys=True)
        if not options_str is None:
            wm_utils.write_to_file(options_str, wm_utils.get_run_dir() + "/settings.conf")

    def get_option(self, option_key):
        global _def_options
        r = self.options.get(option_key, None)
        if r is None:
            r = _def_options.get(option_key, None)
        return r

def config():
    global _options_obj
    if _options_obj is None:
        _options_obj = wm_config()

    return _options_obj

def main():
    config().write_config()

if __name__ == "__main__":
    main()
