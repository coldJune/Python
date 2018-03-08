#!/usr/bin/python3
# -*- coding:UTF-8 -*-

from cgi import FieldStorage
from os import environ
from io import StringIO
from urllib.parse import quote, unquote


class AdvCGI(object):
    # 创建header和url静态类变量，在显示不同页面的方法中会用到这些变量
    header = 'Content-Type:text/html\n\n'
    url = '/cgi-bin/advcgi.py'
    # HTML静态文本表单，其中含有程序语言设置和每种语言的HTML元素
    formhtml = '''
        <HTML>
            <HEAD>
                <TITLE>Advanced CGI Demo</TITLE>
            </HEAD>
            <BODY>
                <H2>Advanced CGI Demo</H2>
                <FORM METHOD=post ACTION='%s' ENCTYPE='multipart/form-data'>
                    <H3>My Cookie Setting</H3>
                    <LI>
                        <CODE><B>CPPuser = %s</B></CODE>
                        <H3>Enter cookie value<BR>
                            <INPUT NAME=cookie value='%s'/>(<I>optional</I>)
                        </H3>
                        <H3>Enter your name<BR>
                            <INPUT NAME=person VALUE='%s'/>(<I>required</I>)
                        </H3>
                        <H3>What languages can you program in ?
                        (<I>at least one required</I>)  
                        </H3>
                        $s
                        <H3>Enter file to upload<SMALL>(max size 4k)</SMALL></H3>
                        <INPUT TYPE=file NAME=upfile VALUE='%s' SIZE=45>
                        <P><INPUT TYPE=submit />
                    </LI>
                </FORM>
            </BODY>
        </HTML>
    '''
    langset = ('Python', 'Java', 'C++', 'C', 'JavaScript')

    langItem = '<INPUT TYPE=checkbox NAME=lang VALUE="%s"%s> %s\n'

    def __init__(self):
        # 初始化实例变量
        self.cookies = {}
        self.who = ''
        self.fn = ''
        self.langs = []
        self.error = ''
        self.fp = None

    def get_cpp_cookies(self):
        """
        当浏览器对应用进行连续调用时，将相同的cookie通过HTTP头发送回服务器
        :return:
        """
        # 通过HTTP_COOKIE访问这些值
        if 'HTTP_COOKIE' in environ:
            cookies = [x.strip() for x in environ['HTTP_COOKIE'].split(';')]
            for eachCookie in cookies:
                # 寻找以CPP开头的字符串
                # 只查找，名为“CPPuser”和“CPPinfo”的cookie值
                if len(eachCookie) > 6 and eachCookie[:3] == 'CPP':
                    # 去除索引8处的值进行计算，计算结果保存到Python对象中
                    tag = eachCookie[3:7]
                    try:
                        # 查看cookie负载，对于非法的Python对象，仅仅保存相应的字符串值。
                        self.cookies[tag] = eval(unquote(eachCookie[8:]))
                    except (NameError, SyntaxError):
                        self.cookies[tag] = unquote(eachCookie[8:])
            # 如果这个cookie丢失，就给他指定一个空字符串
            if 'info' not in self.cookies:
                self.cookies['info'] = ''
            if 'user' not in self.cookies:
                self.cookies['user'] = ''
        else:
            self.cookies['info'] = self.cookies['user'] = ''

        if self.cookies['info'] != '':
            self.who, langstr, self.fn = self.cookies['info'].split(';')
            self.langs = langstr.split(',')
        else:
            self.who = self.fn = ''
            self.langs = ['Python']

    def show_form(self):
        """
        将表单显示给用户
        :return:
        """
        # 从之前的请求中(如果有)获取cookie，并适当地调整表单的格式
        self.get_cpp_cookies()

        langstr = []
        for eachLang in AdvCGI.langset:
            langstr.append(AdvCGI.langItem % (
                eachLang, 'CHECKED' if eachLang in self.langs else '', eachLang))

        if not ('user' in self.cookies and self.cookies['user']):
            cookstatus = '<I>(cookie has not been set yet)</I>'
            usercook = ''
        else:
            usercook = cookstatus = self.cookies['user']

        print('%s%s' % (
            AdvCGI.header, AdvCGI.formhtml % (
                AdvCGI.url, cookstatus, usercook, self.who,
                ''.join(langstr), self.fn)))

    errhtml = '''
            <HTML>
                <HEAD>
                    <TITLE>Advanced CGI Demo</TITLE>
                </HEAD>
                <BODY>
                    <H3>ERROR</H3>
                    <B>%s</B>
                    <P>
                    <FORM>
                        <INPUT TYPE= button VALUE=Back ONCLICK="window.history.back()"></INPUT>
                    </FORM>
                </BODY>
            </HTML>
    '''

    def show_error(self):
        """
        生成错误页面
        :return:
        """
        print('%s%s' % (AdvCGI.header, AdvCGI.errhtml % (self.error)))

    reshtml = '''
    <HTML>
        <HEAD>
            <TITLE>Advanced CGI Demo</TITLE>
        </HEAD>
        <BODY>
            <H2>Your Uploaded Data</H2>
            <H3>Your cookie value is: <B>%s</B></H3>
            <H3>Your name is: <B>%s</B></H3>
            <H3>You can program in the following languages:</H3>
            <UL>%s</UL>
            <H3>Your uploaded file...<BR>
                Name: <I>%s</I><BR>
                Contents:
            </H3>
            <PRE>%s</PRE>
            Click <A HREF="%s"><B>here</B></A> to return to form.
        </BODY>
    </HTML>'''

    def set_cpp_cookies(self):
        """
        应用程序调用这个方法来发送cookie（从Web服务器）到浏览器，并存储在浏览器中
        :return:
        """
        for eachCookie in self.cookies:
            print('Set-Cookie: CPP%s=%s; path=/' % (
                eachCookie, quote(self.cookies[eachCookie])))

    def doResult(self):
        """
        生成结果页面
        :return:
        """
        MAXBYTES = 4096
        langlist = ''.join('<LI>%s<BR>' % eachLang for eachLang in self.langs)
        filedata = self.fp.read(MAXBYTES)
        if len(filedata) == MAXBYTES and f.read():
            filedata = '%s%s' % (filedata, '...<B><I>(file truncated due to size)</I></B>')
        self.fp.close()

        if filedata == '':
            filedata = '<B><I>(file not give or upload error)</I></B>'
        filename = self.fn

        if not ('user' in self.cookies and self.cookies['user']):
            cookstatus = '<I>(cookie has not been set yet)</I>'
            usercook = ''
        else:
            usercook = cookstatus = self.cookies['user']

        self.cookies['info'] = ':'.join((self.who, ','.join(self.langs), filename))
        self.set_cpp_cookies()

        print('%s%s' % (
            AdvCGI.header, AdvCGI.reshtml % (cookstatus, self.who, langlist, filename, filedata, AdvCGI.url)))

    def go(self):
        self.cookies = {}
        self.error = ''
        form = FieldStorage()
        if not list(form.keys()):
            self.show_form()
            return

        if 'person' in form:
            self.who = form['person'].value.strip().title()
            if self.who == '':
                self.error = 'Your name is required.(blank)'
            else:
                self.error = 'Your name is required.(missing)'

        self.cookies['user'] = unquote(form['cookie'].value.strip()) if 'cookie' in form else ''

        if 'lang' in form:
            lang_data = form['lang']
            if isinstance(lang_data, list):
                self.langs = [eachLang.value for eachLang in lang_data]
            else:
                self.langs = [lang_data.value]
        else:
            self.error = 'At least one language required'

        if 'upfile' in form:
            upfile = form['upfile']
            self.fn = upfile.filename or ''
            if upfile.file:
                self.fp = upfile.file
            else:
                self.fp = StringIO('(no data)')
        else:
            self.fp = StringIO('(no file)')
            self.fn = ''

        if not self.error:
            self.doResult()
        else:
            self.show_error()

if __name__ == '__main__':
    page = AdvCGI()
    page.go()
