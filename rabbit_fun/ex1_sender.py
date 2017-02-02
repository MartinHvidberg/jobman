
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body='Hello more World!')

print(" [x] Sent 'Hello World!'")

for n in range(6):
    channel.basic_publish(exchange='', routing_key='hello', body="Mymessage number: {}".format(n))

connection.close()
