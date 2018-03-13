#!/usr/bin/python3
# -*- coding:UTF-8 -*-

# 返回一个表示Python对象的字符串
# 用来美观地输出Python对象
from json import dumps
from pprint import pprint


# Python字典，使用字典是因为其可以构建具有结构化层次的属性。
# 在等价的JSON表示方法中，会移除所有额外的逗号
Books = {
    '0000001': {
        'title': 'Core',
        'edition': 2,
        'year': 2007,
    },
    '0000002': {
        'title': 'Python Programming',
        'edition': 3,
        'authors': ['Jack', 'Bob', 'Jerry'],
        'year': 2009,
    },
    '0000003': {
        'title': 'Programming',
        'year': 2009,
    }
}

# 显示转储的Python字典
print('***RAW DICT***')
print(Books)

# 使用更美观的方法输出
print('***PRETTY_PRINTED DICT***')
pprint(Books)

# 使用json.dumps()内置的美观的输出方式，传递缩进级别
print('***PRETTY_PRINTED JSON***')
print(dumps(Books, indent=4))
