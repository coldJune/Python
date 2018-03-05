#!/usr/bin/python3
# -*- coding:UTF-8 -*-

from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import os


class SwitchUI(object):
    # 窗口的基类，定义页面的布局绑定的方法
    def __init__(self):
        # 定义顶层窗口
        self.top = Tk(className='office转换工具')
        self.choose_frame = Frame(self.top, width=300)
        # 定义提示label
        self.choose_label = Label(self.choose_frame, text='选择文件(夹)', width=15)
        self.choose_label.pack(side=LEFT, fill=BOTH)
        # 定义输入框
        self.choose_entry = Entry(self.choose_frame, width=30)
        self.choose_entry.pack(side=LEFT, fill=BOTH)
        # 定义按钮
        self.choose_button_dir = Button(self.choose_frame, width=10, text='选择目录', command=self.choose_dir)
        self.choose_button_dir.pack(side=RIGHT)
        self.choose_button_file = Button(self.choose_frame, width=10, text='选择文件', command=self.choose_file)
        self.choose_button_file.pack(side=RIGHT)
        self.choose_frame.pack()
        # 定义目标目录
        self.to_frame = Frame(self.top, width=300)
        # 定义提示label
        self.to_label = Label(self.to_frame, text='目标目录', width=15)
        self.to_label.pack(side=LEFT)
        # 定义输入框
        self.to_entry = Entry(self.to_frame, width=30)
        self.to_entry.pack(side=LEFT)
        # 定义按钮
        self.to_button = Button(self.to_frame, width=5, text='选择', command=self.to)
        self.to_button.pack(side=RIGHT)
        self.to_frame.pack()
        # 定义选项的子容器
        self.radio_frame = Frame(self.top)
        # 使用radio创建单选项
        self.switch_type = StringVar()
        self.radio_pdf2word = Radiobutton(self.radio_frame, variable=self.switch_type, text='PDF转WORD', value='pdf2word')
        self.radio_word2pdf = Radiobutton(self.radio_frame, variable=self.switch_type, text='WORD转PDF', value='word2pdf')
        self.radio_pdf2word.pack(side=LEFT, fill=BOTH)
        self.radio_word2pdf.pack(side=RIGHT, fill=BOTH)
        self.radio_frame.pack()
        # 定义文件列表显示子容器
        self.list_frame = Frame(self.top, width=300)
        # 定义滚动条
        self.list_scroll = Scrollbar(self.list_frame)
        # 定义列表并绑定滚动条
        self.list_box = Listbox(self.list_frame, height=15, width=50, yscrollcommand=self.list_scroll.set)
        self.list_scroll.config(command=self.list_box.yview)
        # 显示 列表和列表容器
        self.list_box.pack()
        self.list_frame.pack()
        # 操作按钮
        self.switch_button = Button(text='确定转换', command=self.switch)
        self.switch_button.pack(side=BOTTOM, fill=BOTH)
        # 定义数据源
        self.switch_dir = ''
        self.switch_files = []

    def choose_dir(self, ev=None):
        # 选择目录
        input_value = self.choose_entry.get()
        list_value = self.list_box.get(0)
        choose_dir = fd.askdirectory()
        if input_value:
            # 如果输入值不为空则清空输入
            self.choose_entry.delete(0, len(input_value)+1)

        if list_value:
            self.list_box.delete(0, END)
        # 获取目录值并显示在输入框和列表
        if not choose_dir != '':
            self.choose_entry.insert(END, choose_dir)
            self.list_box.insert(END, choose_dir)
            self.list_box.insert(END, '******************操作文件列表***********************')
            self.list_box.update()
            self.choose_entry.update()

    def choose_file(self, ev=None):
        # 选择文件或文件列表
        input_value = self.choose_entry.get()
        list_value = self.list_box.get(0)
        # 获取转换类型
        switch_type = self.switch_type.get()
        if switch_type:
            if switch_type == 'pdf2word':
                filetypes = [('PDF文档', '*.pdf')]
            elif switch_type == 'word2pdf':
                filetypes = [('WORD文档', '*.doc'), ('WORD文档', '*.docx')]
        else:
            mb.showwarning('提示', '请选择装换类型')
            return
        choose_files = fd.askopenfilenames(filetypes=filetypes)
        print(choose_files)
        if input_value:
            # 如果输入值不为空则清空输入
            self.choose_entry.delete(0, len(input_value) + 1)

        if list_value:
            self.list_box.delete(0, END)
        # 获取目录值并显示在输入框和列表
        if choose_files != '':
            self.choose_entry.insert(END, ';'.join(choose_files))
            # 选择多个文件，分行显示
            for choose_file in choose_files:
                self.list_box.insert(END, choose_file)
            self.list_box.insert(END, '******************操作文件列表***********************')
            self.list_box.update()
            self.choose_entry.update()

    def to(self, ev=None):
        pass

    def switch(self, ev=None):
        pass

if __name__ == '__main__':
    SwitchUI()
    mainloop()
