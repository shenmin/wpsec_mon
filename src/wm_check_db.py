# -*- coding: utf-8 -*-
"""
wm_check_db.py
wpsec_mon

@author: Created by Shen Min (https://nicrosoft.net) on 2023-08-01.
"""

import traceback, time, os, socket
import mysql.connector
import wm_log, wm_config, wm_mail, wm_utils

sendmail_ts_file = '%s/sendmail.ts' % wm_utils.get_run_dir()

def __should_send_mail():
    if not os.path.exists(sendmail_ts_file):
        return True

    with open(sendmail_ts_file, "r") as f:
        timestamp = float(f.read().strip())

    if time.time() - timestamp > 7200:
        return True

    return False

def main():
    mysql_conn = None
    hostname = ""

    if wm_config.config().get_option("mysql_ssh"):
        from sshtunnel import SSHTunnelForwarder
        ssh_tunnel = SSHTunnelForwarder(ssh_address_or_host=wm_config.config().get_option("mysql_ssh_host"), ssh_port=wm_config.config().get_option("mysql_ssh_port"), ssh_username=wm_config.config().get_option("mysql_ssh_user"), ssh_pkey=wm_config.config().get_option("mysql_ssh_pri_key"), remote_bind_address=("127.0.0.1", 3306))

        while True:
            try:
                ssh_tunnel.start()
                mysql_conn = mysql.connector.connect(user=wm_config.config().get_option("mysql_user"), password=wm_config.config().get_option("mysql_password"), host=wm_config.config().get_option("mysql_host"), port=ssh_tunnel.local_bind_port, use_pure=True)
                hostname = wm_config.config().get_option("mysql_ssh_host")
                break
            except Exception as e:
                wm_log.log().log_msg("Failed to connect to MySQL: %s" % e)

                time.sleep(5)
                if not mysql_conn is None:
                    mysql_conn.close()
                ssh_tunnel.stop()
    else:
        try:
            mysql_conn = mysql.connector.connect(user=wm_config.config().get_option("mysql_user"), password=wm_config.config().get_option("mysql_password"), host=wm_config.config().get_option("mysql_host"))
            hostname = socket.gethostname()
        except Exception as e:
            wm_log.log().log_msg("Failed to connect to MySQL: %s" % e)

    if mysql_conn is None:
        return

    dbs = wm_config.config().get_option("dbs")

    if dbs is None or len(dbs) == 0:
        return

    cursor = mysql_conn.cursor()

    result = []

    for db in dbs:
        cursor.execute("USE {}".format(db))
        query = "SELECT COUNT(*) FROM wp_users"
        cursor.execute(query)

        should_user_count = dbs[db].get("user_count", 0)
        user_count = 0
        for count in cursor:
            user_count = count[0]

        if user_count > should_user_count:
            result.append({db:user_count})

    cursor.close()
    mysql_conn.close()

    if len(result) > 0:
        if wm_config.config().get_option("send_email") and __should_send_mail():
            wm_mail.send_alert_for_user_count(hostname, result)

            with open(sendmail_ts_file, "w") as f:
                f.writelines(str(time.time()))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        wm_log.log().log_msg('*** A fatal ERR: %s' % e)
        wm_log.log().log_msg(traceback.format_exc())
    finally:
        wm_log.log().log_msg('WPSEC_MON CheckDB Done!')
