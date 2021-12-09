#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
from twisted.internet import protocol
from twisted.internet import reactor
import ulog
 
SERVER_PORT = 9998
process_cb = None

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)
 
class Process(protocol.Protocol):
    def connectionMade(self):
        ulog.debug(f'IP: {self.transport.getPeer().host}, port: {self.transport.getPeer().port}, connect')
 
    def connectionLost(self, reason):
        ulog.debug('Lost client connection. Reason: %s' % reason)
        ulog.debug(f'IP: {self.transport.getPeer().host}, port: {self.transport.getPeer().port}, disconnect')


    def dataReceived(self, data:bytes):
        global process_cb
        if data:
            data_str = data.decode()
            ulog.debug(data_str)
            if data_str == 'exit':
                reactor.stop()
            if process_cb:
                process_cb(data_str)
        self.transport.write(data)
        
def main(cb = None):
    try:
        global process_cb
        process_cb = cb
        ulog.init("server", "DEBUG")
        factory = protocol.ServerFactory()
        factory.protocol = Process
        reactor.listenTCP(SERVER_PORT, factory)
        reactor.run()
        
    except Exception as e:
        print(e)
    
    finally:
        ulog.exit()
 
def print_cb(s:str):
    print(f'print_cb: f{s}')

if __name__ == '__main__':
    main(print_cb) 