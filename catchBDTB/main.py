#!/usr/bin/python3
#--*-- coding:utf-8 --*--
import bdtb
if __name__=="__main__":
    baseUrl="https://tieba.baidu.com/p/3719151137"
    tb=bdtb.BDTB(baseUrl,1,1)
    tb.start()
