# -*- coding: utf-8 -*-
import xlrd
import sys
from imp import reload
reload(sys)
#test.txt = K:\红河州\8.泸西县\泸西县-林业局\泸西县林业统建计.xls
#os.remove(r"test.txt")
def read_excel(sheet_index):
    # 打开文件
    workbook = xlrd.open_workbook('test.xls')
    # 根据sheet索引或者名称获取sheet内容
    sheet2 = workbook.sheet_by_index(sheet_index) # sheet索引从0开始
    a = []
    for rowNum in range(0,sheet2.nrows ):
        tmp=""
        for colNum in range(0,sheet2.ncols):
            if sheet2.cell(rowNum ,colNum ).value != None:
                tmp += str(sheet2.cell(rowNum, colNum).value)
        a.append(tmp)
    return a

newlist = read_excel(15)
print(newlist)
