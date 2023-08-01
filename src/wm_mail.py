# -*- coding: utf-8 -*-
"""
wm_mail.py
wpsec_mon

@author: Created by Shen Min (https://nicrosoft.net) on 2023-08-01.
"""

import smtplib
from email.mime.text import MIMEText
import wm_config

def send_alert_for_user_count(data):
    subject = wm_config.config().get_option("send_email_subject_prefix") + wm_config.config().get_option("send_email_subject_suffix_uc")

    body = ""
    for item in data:
        for key, value in item.items():
            if len(body) > 0:
                body += "\n"
            body += "Database: %s, Current User Count: %d" % (key, value)

    send_mail(subject, body)

def send_mail(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = wm_config.config().get_option("smtp_user")
    msg['To'] = wm_config.config().get_option("send_email_to")

    server = smtplib.SMTP_SSL(wm_config.config().get_option("smtp_host"), wm_config.config().get_option("smtp_port"))
    server.login(wm_config.config().get_option("smtp_user"), wm_config.config().get_option("smtp_password"))
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':
    send_mail()
