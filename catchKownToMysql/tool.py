#!usr/bin/python3
#-*- coding:utf-8 -*-
import re

class Tool:
    removeADLink = re.compile('<div class="link_layer.*?"></div>')
    removeImg = re.compile('<img.*?>| {1,7}|&nbsp;')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
