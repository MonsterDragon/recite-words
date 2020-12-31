#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys, traceback, time, json
import recity
from word_base.basefunc import connect_db
from my_log.log_func import log_error

SELECT_SQL = """
select * from VOCALBULARY where word='{}'
"""
INSERT_SQL = """
insert into VOCALBULARY values(null,"{}","{}","{}","{}")
"""

all_dict = dict()

# 查询表中是否已有单词
def query(connection, word):
    global all_dict
    try:
        with connection.cursor() as cursor:
            query_str = cursor.execute(SELECT_SQL.format(word))
            query_tuple = cursor.fetchone()
    except Exception:
        log_error("query err: {}".format(traceback.format_exc()))
    if query_tuple:
        ele_dict = dict()
        ele_dict[query_tuple[1]] = dict()
        ele_dict[query_tuple[1]]["sentence"] = query_tuple[2]
        ele_dict[query_tuple[1]]["translation"] = query_tuple[3]
        ele_dict[query_tuple[1]]["attr"] = query_tuple[4]
        all_dict.update(ele_dict)
    return query_tuple

def circle(param):
    while True:
        result = raw_input("{}: ".format(param))
        status = raw_input("again: \'a\', continue: \'c\': ")
        if status == 'a':
            continue
        if status == 'c':
            return result

# 向表中增加数据，向dict中添加单词元素
def insert(connection):
    global all_dict
    argus_list = ["word", "sentence", "meaning", "attrs"]
    json_list = ["word", "sentence", "translation", "attr"]
    ele_dict = {}
    try:
        with connection.cursor() as cursor:
            for seq, i in enumerate(argus_list):
                result = circle(i)
                if seq == 0:
                    ele_dict[result] = {}
                else:
                    ele_dict[ele_dict.keys()[0]][json_list[seq]] = result
            cursor.execute(INSERT_SQL.format(ele_dict.keys()[0], ele_dict[ele_dict.keys()[0]]["sentence"], ele_dict[ele_dict.keys()[0]]["translation"], ele_dict[ele_dict.keys()[0]]["attr"]))
            print(INSERT_SQL.format(ele_dict.keys()[0], ele_dict[ele_dict.keys()[0]]["sentence"], ele_dict[ele_dict.keys()[0]]["translation"], ele_dict[ele_dict.keys()[0]]["attr"]))
            time.sleep(3)
            print("\t\033[1;31;40mcommit data\033[0m!\n")
            connection.commit()
            print("\t\033[1;32;40mcommit successfully!\033[0m\n")
            
    except Exception:
        log_error("query err: {}".format(traceback.format_exc()))
        connection.rollback()
    # all_dict.update(ele_dict)
    query(connection, ele_dict.keys()[0])

def output_book():
    now = time.strftime('%Y-%m-%d',time.localtime(int(time.time())))
    with open(os.path.abspath(os.path.join(os.getcwd(), "depocity/" + "depocity_" + "{}.json".format(now))), 'a') as w:
        json_str = json.dumps(all_dict, ensure_ascii=False, sort_keys=True, encoding="utf-8", indent=4)
        w.write(json_str.encode("utf-8"))

def exe():
    while True:
        word = raw_input("\"end\" will kill this process now input word: ")
        if word == "end":
            break
        connection = connect_db()
        result = query(connection, word)
        print all_dict
        if not result:
            print("\nquery nothing match, please continue\n")
            print("\"insert\" will insert data to db \"pass\" will renew the proceture\n")
            chosen = raw_input("\n\'i\' insert \'p\' pass input word: ")
            if chosen == "i":
                insert(connection)
            elif chosen == "p":
                continue
    output_book()

if __name__ == "__main__":
    exe()
