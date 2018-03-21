#!/usr/bin/env python
# -*- coding:utf-8 -*- 
__author__ = "liukang"

from kombu import BrokerConnection, Exchange, Producer


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


def producerFunc(conn, exchange='amq.direct', ex_type="direct"):
    '''
    用于创建生产者队列
    :param exchange: exchange交换机通道名称
    :param ex_type: exchange交换机通道类型
    :return: 生产者
    '''
    try:
        chan = conn.channel()
        exchange = Exchange(exchange, type=ex_type)
        producer = Producer(chan, exchange)

        return chan, producer

    except Exception as e:
        print e
        return None


def post(data):
    rabbitmq_config = {}
    # rabbitMQ 链接
    conn = get_rabbitmq_link(rabbitmq_config)
    # 生产者
    chan, producer = producerFunc(conn=conn)
    # 插入数据
    if producer:
        producer.publish(body=data, routing_key='count')
        chan.close()
        conn.close()
    else:
        print 'error'


if __name__ == '__main__':
    data = {'name': 'liukang'}
    post(data)
