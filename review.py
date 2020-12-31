#!/usr/bin/env python
# -*- coding:utf-8 -*-

from recity import *

def get_file():
    file_list = list()
    today = datetime.date.today()
    file_list.append(os.path.abspath(os.path.join(os.getcwd(), WRONG_DIR + "/" + WRONG.format(today))))
    return file_list

def read_depocity(file_name):
    with open(file_name, 'r') as f:
        dig = json.load(f, encoding="utf-8") # loads是字符串 load是文件
	return dig

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

if __name__ == "__main__":
    main()
