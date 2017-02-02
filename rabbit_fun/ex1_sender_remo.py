#!/usr/bin/env python
import pika


parameters = pika.URLParameters('amqp://guest:guest@192.168.136.13:5672/%2F') # relevant?
# this queue is the destination queue
credentials = pika.PlainCredentials('jobman', 'jobman')
parameters = pika.ConnectionParameters('remote-host', 5672, 'product', credentials)
connection = pika.BlockingConnection(parameters)
print " connection created"

channel = connection.channel()
channel.queue_declare(queue='hello')

channel.basic_publish(exchange='helloEx', routing_key='', body='Hello World!')
print " [x] Sent 'Hello World!'"
connection.close()