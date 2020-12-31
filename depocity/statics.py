#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, json, re, traceback
from my_log.log_func import log_error
from word_base.basefunc import connect_db

reload(sys)
sys.setdefaultencoding('utf8')

INSERT_DATA = """
INSERT INTO VOCALBULARY VALUES
(
null,
"{}",
"{}",
"{}",
"{}"
)
"""

all_dict = dict()

def get_file(dirname):
    try:
        file_list = os.listdir(dirname)
        return file_list
    except Exception:
        log_error("get current filenames failed: {}".format(traceback.format_exc()))

def read_file(filename):
    global all_dict
    with open (filename, 'r') as f:
        ele = json.load(f, encoding="utf-8")
        all_dict.update(ele)

def write_sql(data):
    try:
        connection = connect_db()
    except Exception:
        log_error("connect to db error: {}".format(traceback.format_exc()))
    try:
        with connection.cursor() as cursor:
            for i in data.keys():
                print("=============%s===========" % i)
                cursor.execute("set names 'utf8'")
                print("=============%s===========" % INSERT_DATA.format(i, data[i]["sentence"], data[i]["translation"], data[i]["attr"]))
                cursor.execute(INSERT_DATA.format(i, data[i]["sentence"], data[i]["translation"], data[i]["attr"]))
                connection.commit()
    except Exception:
        connection.rollback()
        log_error("exe sql failed: {}".format(traceback.format_exc()))

if __name__ == "__main__":
    filenames = get_file(os.getcwd())
    pattern = re.compile(r'depocity_\d{4}-\d{2}-\d{2}.json')
    for i in filenames:
        if not re.match(pattern, i):
            filenames.remove(i)
            break
        read_file(i)
    write_sql(all_dict)
