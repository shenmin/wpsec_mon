# -*- coding: utf-8 -*-
"""
wm_log.py
wpsec_mon

@author: Created by Shen Min (https://nicrosoft.net) on 2023-08-01.
"""

import codecs, os, time
import wm_utils, wm_config

_log_obj = None

class wm_log:
    def __init__(self, filename):
        self.__fileA = '%s/%s.log' % (wm_utils.get_run_dir(), filename)
        self.__fileB = '%s/%s.0.log' % (wm_utils.get_run_dir(), filename)
        self.__c = 0
        time_diff = wm_config.config().get_option('time_diff')
        self.__time_diff = time_diff * 3600

    def __check_file_size(self):
        if os.path.isfile(self.__fileA):
            try:
                fs = os.path.getsize(self.__fileA)
            except:
                fs = 0

            while fs >= 100000000:
                try:
                    if os.path.isfile(self.__fileB):
                        os.remove(self.__fileB)
                except:
                    pass

                try:
                    os.rename(self.__fileA, self.__fileB)
                except:
                    pass

                if not os.path.isfile(self.__fileA):
                    fs = 0
                else:
                    try:
                        fs = os.path.getsize(self.__fileA)
                    except:
                        fs = 0

    def log_msg(self, msg):
        f = codecs.open(self.__fileA, 'a', 'utf-8')

        succ = True
        try:
            f.writelines('[%s] - %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + self.__time_diff)), msg))
        except:
            succ = False

        if not succ:
            try:
                msg = msg.decode('gbk', 'ignore')
                f.writelines('[%s] - %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + self.__time_diff)), msg))
            except:
                f.writelines('[%s] - %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + self.__time_diff)), 'can not write log'))

        f.close()
        self.__c += 1

        if self.__c >= 20:
            self.__check_file_size()
            self.__c = 0

def log():
    global _log_obj
    if _log_obj is None:
        _log_obj = wm_log('wpsec_mon')
    return _log_obj
