#!usr/bin/python3
# -*- coding:UTF-8 -*-

# 常用模块导入，特别是twisted.internet的protocol和reactor
from twisted.internet import protocol, reactor
from time import ctime

# 设置端口号
PORT = 12345


class TWServProtocol(protocol.Protocol):
    # 继承Protocol类
    def connectionMade(self):
        # 重写connectionMade()方法
        # 当一个客户端连接到服务器是会执行这个方法
        client = self.client = self.transport.getPeer().host
        print('...connected from:', client)

    def dataReceived(self, data):
        # 重写dataReceived()方法
        # 当服务器接收到客户端通过网络发送的一些数据的时候会调用此方法
        self.transport.write(bytes('[%s] %s' % (
            ctime(), data.decode('utf-8')), 'utf-8'))

# 创建一个协议工厂，每次得到一个接入连接是，制造协议的一个实例
# 在reactor中安装一个TCP监听器，以此检查服务请求
# 当接收到一个请求时，就是创建一个就是创建一个TWServProtocol实例来处理客户端事务
factory = protocol.Factory()
factory.protocol = TWServProtocol
print('waiting for connection...')
reactor.listenTCP(PORT, factory)
reactor.run()
