#!/usr/bin/env python
# -*- coding:utf-8 -*- 
__author__ = "liukang"

import traceback

from kombu import BrokerConnection, Exchange, Queue, Consumer


class Connection(object):
    def initconn(self, kwargs):
        hostname = 'localhost'
        user_id = 'poll_cloud'
        password = 'poll_cloud'
        virtual_host = 'test',
        port = 5672
        connect_timeout = 10
        heartbeat = 0
        self.conn = BrokerConnection(
            hostname=kwargs.get('hostname') or hostname,
            userid=kwargs.get('userid') or user_id,
            password=kwargs.get('password') or password,
            port=kwargs.get('port') or port,
            virtual_host=kwargs.get('virtual_host') or virtual_host,
            connect_timeout=kwargs.get('connect_timeout') or connect_timeout,
            heartbeat=kwargs.get('heartbeat') or heartbeat
        )

    def consumerFunc(self, exchange='amq.direct', type='direct'):
        self.chan = self.conn.channel()
        self.exchange = Exchange(exchange=exchange, type=type)


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

    def getconnection(self):
        self.initconn(self.kwargs)
        self.consumerFunc(self.kwargs.get('exchange'), self.kwargs.get('ex_type'))

    def setconsumer(self):
        self.queue = Queue(self.qname, self.exchange, routing_key=self.routekey, auto_delete=self.auto_del)
        consumer = Consumer(self.chan, self.queue, callbacks=[self.handle_message])
        consumer.consume()

    def _from_queue(self, qname, routekey=None, auto_del=False, timeout=None):
        if not qname:
            qname = routekey
        self.TIME_OUT = float(timeout) if timeout else timeout
        self.qname = qname
        self.routekey = routekey
        self.auto_del = auto_del
        self.setconsumer()
        self.conn.drain_events(timeout=self.TIME_OUT)

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


if __name__ == '__main__':
    kwargs = {
        'hostname': 'localhost',
        'userid': 'poll_cloud',
        'password': 'poll_cloud',
        'virtual_host': 'test',
        'port': 5672,
        'connect_timeout': 10,
        'heartbeat': 0,
        'exchange': 'amq.direct',
        'ex_type': 'direct'
    }
    test = Receive(kwargs)
    test._from_queue(qname='count', timeout=10)
