#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import json
import copy
import random
import time
import datetime

DEPO_DIR = "depocity"
WRONG_DIR = "wrong_book"
DEPO = "depocity_{}.json"
WRONG = "wrong_book_{}.json"
WORD_STR = "word: \n"
SENTENCE_STR = "sentence: \n"
TRANSLATION_STR = "translation: \n"
wrong_dict = dict()

# 获取前一天的错题文件及仓库json文件的列表
def get_file():
    file_list = list()
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    file_list.append(os.path.abspath(os.path.join(os.getcwd(), DEPO_DIR + "/" + DEPO.format(yesterday))))
    file_list.append(os.path.abspath(os.path.join(os.getcwd(), WRONG_DIR + "/" + WRONG.format(yesterday))))
    return file_list

def read_depocity(file_name):
    with open(file_name, 'r') as f:
        dig = json.load(f, encoding="utf-8") # loads是字符串 load是文件
	return dig

def wrong_book(con, tkey):
    global wrong_dict
    wrong_dict[tkey] = con[tkey]

def output_book():
    now = time.strftime('%Y-%m-%d',time.localtime(int(time.time())))
    with open(os.path.abspath(os.path.join(os.getcwd(), WRONG_DIR + "/" + WRONG.format(now))), 'a') as w:
	json_str = json.dumps(wrong_dict, ensure_ascii=False, sort_keys=True, encoding="utf-8", indent=4)
        w.write(json_str.encode("utf-8"))

def testing(con):
    length = len(con.keys())
    text = copy.deepcopy(con.keys())
    num = 1
    while (length > 0):
        print("******* Index: %d ******\n" % num)
        i = random.randint(0, length-1)
        print(SENTENCE_STR + "\n\t" + con[text[i]]["sentence"] + "\n")
        word = str(raw_input("\nPlease enter word: "))
	if (word != text[i]):
            print("\n" + TRANSLATION_STR + "\n\t" + con[text[i]]["translation"] + "\n")
            word = str(raw_input("\nPlease enter word: "))
	    if (word != text[i]):
                print("\n" + WORD_STR + "\n\t" + text[i] + " " + con[text[i]]["attr"] + "\n")
                print("\n=== Index: %d \033[1;31;40merror!\033[0m! ===\n" % num)
                # 写入错题本
                wrong_book(con, text[i])
            else:
                print("\n=== Index: %d \033[1;32;40mcorrect!\033[0m! ===\n" % num)
        else:
            print("\n=== Index: %d \033[1;32;40mcorrect!\033[0m! ===\n" % num)
        num += 1
        length -= 1
        text.remove(text[i])

def main():
    filenames = get_file()
    for i in filenames:
        content = read_depocity(i)
        testing(content)
    output_book()

if __name__ == "__main__":
    main()
