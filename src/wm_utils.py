# -*- coding: utf-8 -*-
"""
wm_utils.py
wpsec_mon

@author: Created by Shen Min (https://nicrosoft.net) on 2023-08-01.
"""

import codecs, os, time

def get_run_dir():
    path = os.getcwd()

    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def write_to_file(content, filename):
    f = codecs.open(filename, 'w+', 'utf-8')
    f.writelines(content)
    f.close()

def read_from_file(filename):
    if os.path.isfile(filename):
        f = codecs.open(filename, 'r', 'utf-8')
        r = f.read()
    else:
        r = None
    return r

def ensure_remove(file, loop=True):
    while loop:
        try:
            os.remove(file)
            break
        except:
            time.sleep(0.1)