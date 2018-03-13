#!/usr/bin/python3
# -*- coding:UTF-8 -*-

#
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString


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
        'authors': 'Jack:Bob:Jerry',
        'year': 2009,
    },
    '0000003': {
        'title': 'Programming',
        'year': 2009,
    }
}

# 创建顶层对象
# 将所有其他内容添加到该节点下
books = Element('books')
for isbn, info in Books.items():
    # 对于每一本书添加一个book子节点
    # 如果原字典没有提供作者和版本，则使用提供的默认值。
    book = SubElement(books, 'book')
    info.setdefault('authors', 'Bob')
    info.setdefault('edition', 1)
    for key, val in info.items():
        # 遍历所有键值对，将这些内容作为其他子节点添加到每个book中
        SubElement(book, key).text = ', '.join(str(val).split(':'))

xml = tostring(books)
print('*** RAW XML***')
print(xml)

print('***PRETTY-PRINTED XML***')
dom = parseString(xml)
print(dom.toprettyxml('     '))

print('***FLAT STRUCTURE***')
for elmt in books.iter():
    print(elmt.tag, '-', elmt.text)

print('\n***TITLE ONLY***')
for book in books.findall('.//title'):
    print(book.text)
