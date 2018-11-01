
from itertools import product
import re

def create_excel_col(seed = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),iter_cnt =1):
    col_lst = ['0']
    for index in range(1, iter_cnt + 1):
        lst = list(product(seed, repeat=index)) #得到排列序元组序列
        lst = map(lambda elem: ''.join(elem), lst)  #将排列元组序列转成字符串序列
        lst = list(set(lst))  #消除重复元素
        lst = sorted(lst)  #按字母ASCII的顺序进行排列
        col_lst += lst

    return col_lst


def extract_question_id(title):
    matches = re.match(r'(?P<prefix>([A-Z0-9]+)(-[0-9]+)*)(-[A-Z]+)?', title)
    return matches.group('prefix')


def test():
    print(extract_question_id('A1-A'))
    print(extract_question_id('A1-AB'))
    print(extract_question_id('A2-1'))
    print(extract_question_id('A2-2-A'))
    print(extract_question_id('A11-22'))
    print(extract_question_id('A11-22-A'))
    print(extract_question_id('I2-1-A'))
    print(extract_question_id('I2-2-1-1'))
    pass


if __name__ == '__main__' :
    test()