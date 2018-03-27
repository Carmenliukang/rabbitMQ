#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "liukang"

from kombu import BrokerConnection, Exchange, Queue, Consumer


def get_rabbitmq_link(rabbitmq_config):
    '''
    返回 rabbitMQ 链接
    :param rabbitmq_config: rabbitMQ配置字典：
                rabbitmq_config = {
                'hostname': '',
                'userid': '',
                'password': '',
                'virtual_host': '',
                'port': 15672,
                'connect_timeout': 5,
                'heartbeat': 10
            }

    :return: conn rabbitmq 指定 virtual_host 链接
    '''
    try:
        HOSTNAME = 'localhost'
        USERID = 'poll_cloud'
        PASSWORD = 'poll_cloud'
        VIRTUAL_HOST = 'test'
        PORT = 5672
        CONNECT_TIMEOUT = 10
        HEARTBEAT = 0

        conn = BrokerConnection(
            hostname=rabbitmq_config.get('hostname', HOSTNAME),
            userid=rabbitmq_config.get('userid', USERID),
            password=rabbitmq_config.get('password', PASSWORD),
            virtual_host=rabbitmq_config.get('virtual_host', VIRTUAL_HOST),
            port=rabbitmq_config.get('port', PORT),
            connect_timeout=rabbitmq_config.get('connect_timeout', CONNECT_TIMEOUT),
            heartbeat=rabbitmq_config.get('heartbeat', HEARTBEAT)
        )

    except Exception as e:
        print e
        conn = None

    return conn


def consumerFunc(conn, exchange='amq.direct', ex_type="direct"):
    '''
    用于创建消费者
    :param exchange: 通道名称
    :param ex_type: 通道类型
    :return: 消费者
    '''
    chan = conn.channel()
    exchange = Exchange(exchange, type=ex_type)

    return exchange, chan


def handle_message(body, message):
    print body
    # time.sleep(5)
    message.ack()


def setconsumer(qname, exchange, routekey, auto_del, chan):
    queue = Queue(qname, exchange, routing_key=routekey, auto_delete=auto_del)
    consumer = Consumer(chan, queue, callbacks=[handle_message])
    consumer.consume()


def get():
    rabbitmq_config = {}
    # rabbitMQ 链接
    conn = get_rabbitmq_link(rabbitmq_config)
    # 消费者
    exchange, chan = consumerFunc(conn=conn)
    # 消费者 消费进程
    setconsumer(qname='count', routekey='count', auto_del=False, chan=chan, exchange=exchange)
    # 关闭通道和关闭队列
    chan.close()
    conn.close()


if __name__ == '__main__':
    get()
