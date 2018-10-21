
from itertools import product


def create_excel_col(seed = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),iter_cnt =1):
    col_lst = ['0']
    for index in range(1, iter_cnt + 1):
        lst = list(product(seed, repeat=index)) #得到排列序元组序列
        lst = map(lambda elem: ''.join(elem), lst)  #将排列元组序列转成字符串序列
        lst = list(set(lst))  #消除重复元素
        lst = sorted(lst)  #按字母ASCII的顺序进行排列
        col_lst += lst

    return col_lst


def test():
    cols = create_excel_col(iter_cnt=2)
    print(cols)
    print(cols[27])

    pass

if __name__ == '__main__' :
    test()