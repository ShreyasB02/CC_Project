'''
RabbitMQ Client to listen for incoming requests on the “health_check” queue and process it.

This consumer must acknowledge that the health-check message has been listened to through the “health_check” queue. (Simple Ack)
'''

import http
import pika, sys , os
import mysql.connector
import json

def main():

    def callback(ch,method,properties,body):
        print(f"Received health-check message: {body}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))  # add the appropriate host later ( rmq running in its own container. which is in its own network)
    channel = connection.channel()
    channel.queue_declare(queue='health_check')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='health_check', on_message_callback=callback,auto_ack=True) # change the auto_ack ie remove it if it interferes with previous ack
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__=="__main__":
    main()    