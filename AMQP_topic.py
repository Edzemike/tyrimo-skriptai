#!/usr/bin/env python
import pika
# import logging
import time
import ntplib
import datetime

from dateutil import parser

# logging.basicConfig(level=logging.DEBUG)
credentials = pika.PlainCredentials('edita2', 'test')
parameters = pika.ConnectionParameters('185.80.128.169',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()


channel.queue_declare(queue='testtopc')


client_ntp = ntplib.NTPClient()
time_to_stop = time.time() + 60 * 60

channel.basic_publish(exchange='', routing_key='testtopic', body="begin")

while time.time() < time_to_stop:
    try:
        client_ntp = ntplib.NTPClient()
        response = client_ntp.request('0.pool.ntp.org', version=3)
        print "got response"
        if response:
            print "inside"
            channel.basic_publish(exchange='', routing_key='testtopic',
                                  body=str(
                                      datetime.datetime.now()+
                                      datetime.timedelta(0,response.offset)))
            print "published"
        print "after sending", str(datetime.datetime.now()+
                                   datetime.timedelta(0,response.offset))
    except:
        print "ntp connection failed"
        continue
    time.sleep(5)
    
channel.basic_publish(exchange='', routing_key='testtopic', body="end")

connection.close()
