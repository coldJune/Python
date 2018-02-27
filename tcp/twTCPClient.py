#!usr/bin/python
# -*- coding:UTF-8 -*-

from twisted.internet import  protocol, reactor

HOST = '127.0.0.1'
PORT = 12345


class TWClientProtocol(protocol.Protocol):
    def sendData(self):
        # 需要发送数据时调用
        # 会在一个循环中继续，直到不输入任何内容来关闭连接
        data = input('> ')
        if data:
            print('...send %s...' % data)
            self.transport.write(bytes(data, 'utf-8'))
        else:
            self.transport.loseConnection()

    def connectionMade(self):
        #
        self.sendData()

    def dataReceived(self, data):
        print(data.decode('utf-8'))
        self.sendData()


class TWClientFactory(protocol.ClientFactory):
    # 创建了一个客户端工厂
    protocol = TWClientProtocol
    clientConnectionLost = clientConnectionFailed = \
        lambda self, connector, reason: reactor.stop()

# 创建了一个到服务器的连接并运行reactor，实例化了客户端工厂
# 因为这里不是服务器，需要等待客户端与我们通信，并且这个工厂为每一次连接都创建一个新的协议对象。
# 客户端创建单个连接到服务器的协议对象，而服务器的工厂则创建一个来与客户端通信
reactor.connectTCP(HOST, PORT, TWClientFactory())
reactor.run()