#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket
import threading
import time
import traceback

from kombu import BrokerConnection, Exchange, Queue, Consumer, Producer


def check_heartbeat(source):
    if not source.kwargs.get('heartbeat'):
        print 'Error , heartbeat value error'
        return
    while source.rcv:
        try:
            source.conn.heartbeat_check()
            time.sleep(int(source.kwargs.get('heartbeat', 0)) / 2)
        except:
            print 'check heartbear fail ,try reconnection'
            source.reconnection()
            break


class Connection(object):
    def initconn(self, kwargs):
        HOSTNAME = 'localhost'
        USERID = 'poll_cloud'
        PASSWORK = ''
        VIRTUAL_HOST = 'test'
        PORT = 5672
        CONNECT_TIMEOUT = 5
        HEARTBEAT = 0

        self.conn = BrokerConnection(
            hostname=kwargs.get('hostname') or HOSTNAME,
            userid=kwargs.get('userid') or USERID,
            password=kwargs.get('password') or PASSWORK,
            virtual_host=kwargs.get('virtual_host') or VIRTUAL_HOST,
            port=kwargs.get('port') or PORT,
            connect_timeout=kwargs.get('connect_timeout') or CONNECT_TIMEOUT,
            heartbeat=kwargs.get('heartbeat') or HEARTBEAT,
        )

    def producerFunc(self, exchange='amq.direct', ex_type="direct"):
        self.chan = self.conn.channel()
        self.exchange = Exchange(exchange, type=ex_type)
        self.producer = Producer(self.chan, self.exchange)

    def consumerFunc(self, exchange='amq.direct', ex_type="direct"):
        self.chan = self.conn.channel()
        self.exchange = Exchange(exchange, type=ex_type)


class Publish(Connection):
    def __init__(self, kwargs):
        """
            kwarge :
                 hostname
                 userid
                 password
                 virtual_host
                 port
                 connect_timeout
                 check_heartbeat     1 or 0
                 heartbeat           heartbeat
                 exchange            exchange name
                 ex_type             exchange type
        """
        self.kwargs = kwargs
        self.getconnection()

    def getconnection(self):
        self.initconn(self.kwargs)
        self.producerFunc(self.kwargs.get('exchange'), self.kwargs.get('ex_type'))
        if self.kwargs.get('check_heartbeat'):
            self.start_check_heartbeat()

    def reconnection(self):
        self.chan.close()
        self.conn.close()
        self.getconnection()

    def start_check_heartbeat(self):
        httpd = threading.Thread(target=check_heartbeat, args=[self])
        httpd.start()

    def _to_queue(self, key, data, serializer=None, count=3):
        if count < 0:
            print 'send msg to queue error'
            return False
        try:
            self.producer.publish(data, routing_key=key, serializer=serializer)
            return True
        except:
            time.sleep(self.kwargs.get('heartbeat') or 1)
            self.reconnection()
            self._to_queue(key, data, serializer=serializer, count=count - 1)


class Receive(Connection):
    def __init__(self, kwargs):
        """
            kwarge :
                 hostname
                 userid
                 password
                 virtual_host
                 port
                 connect_timeout
                 check_heartbeat     True or False
                 heartbeat           if check_heartbeat set True this
                 exchange            exchange name
                 ex_type             exchange type
        """
        self.kwargs = kwargs
        self.rcv = True
        self.getconnection()

    def reconnection(self):
        self.chan.close()
        self.conn.close()
        self.getconnection()
        self.setconsumer()
        self.receive_client()

    def start_check_heartbeat(self):
        httpd = threading.Thread(target=check_heartbeat, args=[self])
        httpd.start()

    def getconnection(self):
        self.initconn(self.kwargs)
        self.consumerFunc(self.kwargs.get('exchange'), self.kwargs.get('ex_type'))
        if self.kwargs.get('check_heartbeat'):
            self.start_check_heartbeat()

    def setconsumer(self):
        self.queue = Queue(self.qname, self.exchange, routing_key=self.routekey, auto_delete=self.auto_del)
        consumer = Consumer(self.chan, self.queue, callbacks=[self.handle_message])
        consumer.consume()

    def receive_client(self):
        while self.rcv:
            try:
                self.conn.drain_events(timeout=self.TIME_OUT)
            except socket.timeout:
                print 'receive error'
                break
        self.chan.close()
        self.conn.close()

    def _from_queue(self, qname, routekey=None, auto_del=False, timeout=None):
        if not qname:
            qname = routekey
        self.TIME_OUT = float(timeout) if timeout else timeout
        self.qname = qname
        self.routekey = routekey
        self.auto_del = auto_del
        self.setconsumer()
        self.receive_client()

    def _do(self, body):
        print body
        """ child func """
        pass

    def handle_message(self, body, message):
        try:
            self._do(body)
            message.ack()
        except:
            traceback.print_exc()
            print 'handle msg error'

    def stoprcv(self):
        self.rcv = False


if __name__ == '__main__':
    kwargs = {
        'hostname': 'localhost',
        'userid': 'guest',
        'password': 'guest',
        'virtual_host': 'test',
        'port': 5672,
        'connect_timeout': 10,
        'check_heartbeat': False,
        'heartbeat': True,
        'exchange': 'amq.direct',
        'ex_type': 'direct'
    }

    test = Receive(kwargs=kwargs)

    result = test._from_queue('count', timeout=5)
