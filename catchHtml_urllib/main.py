#!/usr/bin/python3
import catchHtml

if __name__=='__main__':
    catchHtml.readHtml()#read Html
    catchHtml.simulate_search()#simulate search
    #use proxy
    proxy_addr='117.23.56.4:808'
    data=catchHtml.use_proxy(proxy_addr,'https://www.baidu.com')
    print(data)
    catchHtml.use_cookie()#use cookie
