#!/usr/bin/env python
import pika
# import logging
import time
import ntplib
import datetime

offset = None
while offset==None:
    try:
        client_ntp = ntplib.NTPClient()
        response = client_ntp.request('0.pool.ntp.org', version=3)
        offset = datetime.timedelta(0,response.offset)
        print "laiko sikrtumas: ", offset
    except:
        print "ntp connection failed"

credentials = pika.PlainCredentials('edita2', 'test')
parameters = pika.ConnectionParameters('185.80.128.169',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()


channel.queue_declare(queue='testtopc')


time_to_stop = time.time() + 30 * 60
time_to_sync = time.time() + 1 * 60

print "begin at: ", datetime.datetime.now() + offset
channel.basic_publish(exchange='', routing_key='testtopic', body="begin")

while time.time() < time_to_stop:
    if time.time() > time_to_sync:
        time_to_sync = time.time() + 1 * 60
        try:
            client_ntp = ntplib.NTPClient()
            response = client_ntp.request('0.pool.ntp.org', version=3)
            offset = datetime.timedelta(0,response.offset)
            print offset
        except:
            print "ntp connection failed"
    try:
        channel.basic_publish(exchange='', routing_key='testtopic',
                              body=str(datetime.datetime.now() + offset))
        print "sent"
    except:
        print "failed to publish"
    time.sleep(0.5)
    
channel.basic_publish(exchange='', routing_key='testtopic', body="end")

connection.close()

print "ended at: ", datetime.datetime.now() + offset
