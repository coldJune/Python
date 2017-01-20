#coding:utf-8
'''
Created on 2017年1月20日

@author: 笨蛋
'''
import xlwt,os,json
from collections import OrderedDict
txt_path='./../../txt/'
excel_path='./../../excel/'

def txt2excel(txt_path,excel_path):
    #获取路径下所有文件
    txts=os.listdir(txt_path)
    excel_file=xlwt.Workbook()
    for txt in txts:
        txtf=txt_path+txt
        #判断是否为文件
        if os.path.isfile(txtf):
            #打开文件并读取
            with open(txtf) as t:
                data=t.read()
                print(data)
                #转为json,为保持转换前与转换后一致，使用OrderedDict
                dic=json.loads(data,object_pairs_hook=OrderedDict)
                
                #添加sheet
                if str(txt)=='city.txt':
                    table=excel_file.add_sheet(str(txt)[:-4])
                    for row,i in enumerate(list(dic)):
                        table.write(row,0,i)
                        table.write(row,1,dic[i])
                if str(txt)=='numbers.txt':
                    table=excel_file.add_sheet(str(txt)[:-4])
                    for row,i in enumerate(dic):
                        for col,j in enumerate(i):
                            table.write(row,col,j)
                if  str(txt)=='student.txt':
                    table=excel_file.add_sheet(str(txt)[:-4])
                    for row,i in enumerate(list(dic)):
                        print(list(dic[i]))
                        table.write(row,0,i)
                        for col,j in enumerate(list(dic[i])):
                            table.write(row,col+1,j)
                    
    excel_file.save(excel_path+'excel.xls')
                
    return

if __name__=='__main__':
    txt2excel(txt_path, excel_path)
                
                