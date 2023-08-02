# WordPress Security Monitor (wpsec_mon)

## Requirements
Developed under Python 3.10 environment, not tested in other versions. However, it should also be compatible with other versions of Python.

    pip install mysql-connector-python sshtunnel

## Usage
Generate default configuration file:

    python wm_config.py

A sample configuration file for running with MySQL locally:

    {
        "dbs": {
            "wp1": {
                "root_path": "/home/web/wordpress1/public_html/",
                "user_count": 1
            },
            "wp2": {
                "root_path": "/home/web/wordpress2/public_html/",
                "user_count": 1
            }
        },
        "debug": false,
        "mysql_host": "127.0.0.1",
        "mysql_password": "password",
        "mysql_ssh": false,
        "mysql_user": "root",
        "send_email": true,
        "send_email_to": "**notification**@gmail.com",
        "smtp_host": "smtp.googlemail.com",
        "smtp_password": "password",
        "smtp_port": 465,
        "send_email_subject_prefix":"WordPress Alert from wpsec_mon: ",
        "send_email_subject_suffix_uc": "Suspicious Users Added",
        "send_email_subject_suffix_fc": "Suspicious Files Added",
        "smtp_user": "**sender**@gmail.com",
        "time_diff": 0
    }

or for connecting to MySQL with SSH:

    {
        "dbs": {
            "wp1": {
                "root_path": "/home/web/wordpress1/public_html/",
                "user_count": 1
            },
            "wp2": {
                "root_path": "/home/web/wordpress2/public_html/",
                "user_count": 1
            }
        },
        "debug": false,
        "mysql_host": "127.0.0.1",
        "mysql_password": "password",
        "mysql_ssh": true,
        "mysql_ssh_host": "mysql.example-host.com",
        "mysql_ssh_port": 22,
        "mysql_ssh_pri_key": "/home/user/.ssh/id_rsa",
        "mysql_ssh_user": "root",
        "mysql_user": "root",
        "send_email": true,
        "send_email_to": "**notification**@gmail.com",
        "smtp_host": "smtp.googlemail.com",
        "smtp_password": "password",
        "smtp_port": 465,
        "send_email_subject_prefix":"WordPress Alert from wpsec_mon: ",
        "send_email_subject_suffix_uc": "Suspicious Users Added",
        "send_email_subject_suffix_fc": "Suspicious Files Added",
        "smtp_user": "**sender**@gmail.com",
        "time_diff": 0
    }

Check user count in WordPress DB: 

    python wm_check_db.py

