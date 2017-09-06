# coding:utf-8
import os

BASE_DIR = os.path.dirname(__file__)

def convert2PY(string):
    """该函数通过输入汉字返回其拼音，如果输入多个汉字，则返回第一个汉字拼音.
       如果输入数字字符串，或者输入英文字母，则返回其本身(英文字母如果为大写，转化为小写)
    """
    path = os.path.join(BASE_DIR, 'pinyin.txt')
    f = open(path)
    lines = f.readlines()


    def convert(ch):
        intord = ord(ch[0:1])
        if (intord >= 48 and intord <= 57):
            return ch[0:1]
        if (intord >= 65 and intord <=90 ) or (intord >= 97 and intord <=122):
            return ch[0:1].lower()
        for line in lines:
            if ch in line:
                line = line.split(',')[0].replace('\n','')
                return line[1:len(line)-1]

        return ''

    if (len(string)==0):
        return ''
    if not (isinstance(string,str)):
        string = string.decode('utf-8')

    py = ''
    for i in range(0,len(string)):
        ch = string[i]
        py += convert(ch)

    return py

print((convert2PY('乐123aafdff')))