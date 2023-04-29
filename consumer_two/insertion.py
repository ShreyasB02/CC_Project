'''
RabbitMQ Client to listen for incoming requests on the “health_check” queue and process it.

This consumer must acknowledge that the health-check message has been listened to through the “health_check” queue. (Simple Ack)


'''


import json
import pika
import sys,os,time
from pymongo.mongo_client import MongoClient
import certifi

def main():
    # wait for rmq to boot up
    sleepTime = 20
    time.sleep(sleepTime)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='insert_record',durable=True)
    connectionstr=""
    client = MongoClient(connectionstr)

    db = client['studentdb']
    collection = db['student']

    
    # Function to insert a record into the database
    def insert_record(data):
        # Set null values for sem and cgpa if they don't exist in the request
        sem = data['sem'] if 'sem' in data else None
        cgpa = data['cgpa'] if 'cgpa' in data else None

        #sql = "INSERT INTO students (SRN, name, sem, section, cgpa) VALUES (%s, %s, %s, %s, %s)"
        val = (data['SRN'], data['name'], sem, data['section'], cgpa)
        
    # Function to handle incoming messages on the insert_record queue
    def callback(ch, method, properties, body):
        b = body.decode()
        b1 = b.split(".")
        x = b1[0]
        y = b1[1]
        z = b1[2]
        dict1 = {"SRN": x,"Name":y,"Section":z}
        collection.insert_one(dict1)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Debuuuugggg")
        return "Student saved successfully!"

    # Set up consumer to take only one message at a time
    #channel.basic_qos(prefetch_count=1)

    # Start listening for incoming messages on the insert_record queue
    channel.basic_consume(queue='insert_record', on_message_callback=callback)

    print('Insertion Consumer is waiting for messages...')
    channel.start_consuming()


if __name__== "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)        

