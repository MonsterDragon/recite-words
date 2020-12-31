#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
1、数据库函数
2、main:创建数据库、表
"""

import pymysql, json, traceback
from my_log.log_func import log_error

CREATE_WORD = """
CREATE DATABASE WORD
"""

CREATE_WORD_TABLE = """
CREATE TABLE VOCALBULARY
(
id int primary key auto_increment,
word varchar(20) not null,
sentence text,
meaning text,
attrs varchar(20)
)charset utf8
"""

# 默认连接 word 库
def connect_db(host="localhost", user="root", password="shuzhan123", db="word", port=3306, charset="utf8"):
    connection = pymysql.connect(host=host, user=user, password=password, db=db, port=port, charset=charset) 
    return connection

# 执行相关的sql语句
def exe_sql(connection, sql):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
    except Exception:
        log_error("execute sql failed: {}".format(traceback.format_exc()))

if __name__ == "__main__":
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_WORD_TABLE)
    except Exception:
        log_error("execute sql failed: {}".format(traceback.format_exc()))
    # pass
