#!usr/bin/python3
#-*- coding:utf-8 -*-

import craw
if __name__=='__main__':
    for i in range(1,251):
        url='https://list.jd.com/list.html?cat=1713,3258&page='+str(i)+'&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main'
        craw.craw(url,i)
    print('爬取圖片結束，成功保存%d圖片'%craw.sum)
