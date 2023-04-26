'''
RabbitMQ Client to listen for incoming requests on the “health_check” queue and process it.

This consumer must acknowledge that the health-check message has been listened to through the “health_check” queue. (Simple Ack)
'''

import http
import pika, sys , os,time
#import mysql.connector
import json
import pymongo
def main():
    sleepTime = 20
    time.sleep(sleepTime)

    print('Connecting to server ...')
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))

    channel = connection.channel()


    channel.queue_declare(queue='health_check', durable=True)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        print("Health Check ACK ")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return "Health check ACKed"


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='health_check', on_message_callback=callback)
    channel.start_consuming()

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)