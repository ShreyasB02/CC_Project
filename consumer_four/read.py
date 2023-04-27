'''
RabbitMQ Client to listen for incoming requests on the “read_database” queue and process it.
This consumer must retrieve all the records present in the database.
'''

import http
import pika, sys , os,time
# import mysql.connector
from pymongo import MongoClient
import json #incase we need to send the data

# Rabbitmq is hosted on its own container running on its own network

def main():
    # db = mysql.connector.connect(
    #     host = "localhost",
    #     user = "root",
    #     password ="password",
    #     database= "cc_student"
    #     )
    # cursor =db.cursor()
    connectionstr="mongodb+srv://ccrmq:ccrmq@cluster0.s2ksf4g.mongodb.net/test"
    client = MongoClient(connectionstr)

    db = client['studentdb']
    collection = db['student']
    def callback(ch, method, properties, body):
        ans = collection.find({})
        for document in ans:
            print(document)
    # ch.basic_publish(
    #     exchange='',
    #     routing_key=properties.reply_to,
    #     properties=pika.BasicProperties(correlation_id=properties.correlation_id),
    #     body=json.dumps(result)
    # )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return "Database read"


    sleepTime = 20
    time.sleep(sleepTime)
    print('Consumer_four connecting to server ...')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='read_database', durable=True)
        #handle 1 message at a time:
    #channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='read_database', on_message_callback=callback)  #ACk
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


 
