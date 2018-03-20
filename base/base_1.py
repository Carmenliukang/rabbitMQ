#!/usr/bin/env python
# -*- coding:utf-8 -*- 
__author__ = "liukang"

import datetime

from kombu import Connection

rabbitmq_config = {}
HOSTNAME = 'localhost'
USERID = 'poll_cloud'
PASSWORD = 'poll_cloud'
VIRTUAL_HOST = 'test'
PORT = 5672
CONNECT_TIMEOUT = 3
HEARTBEAT = 0
# "amqp://guest:guest@localhost:5672//"中的amqp就是上文所提到的transport，
# 后面的部分是连接具体transport所需的参数，具体含义下篇博客中会讲到
with Connection(hostname=rabbitmq_config.get('hostname', HOSTNAME),
                userid=rabbitmq_config.get('userid', USERID),
                password=rabbitmq_config.get('password', PASSWORD),
                virtual_host=rabbitmq_config.get('virtual_host', VIRTUAL_HOST),
                port=rabbitmq_config.get('port', PORT),
                connect_timeout=rabbitmq_config.get('connect_timeout', CONNECT_TIMEOUT),
                heartbeat=rabbitmq_config.get('heartbeat', HEARTBEAT)) as conn:
    simple_queue = conn.SimpleQueue('test')
    message = 'helloword, sent at %s' % datetime.datetime.today()
    simple_queue.put(message, routing_key='count', serializer=None)
    print('Sent: %s' % message)
    simple_queue.close()
