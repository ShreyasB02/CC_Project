'''
RabbitMQ Client to listen for incoming requests on the “health_check” queue and process it.

This consumer must acknowledge that the health-check message has been listened to through the “health_check” queue. (Simple Ack)


'''


import json
import pika
import sys,os
from pymongo import MongoClient

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='insert_record')
    connectionstr="mongodb+srv://shreyas14902:<password>@cc-cluster.kdd2lot.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connectionstr)

    db = client.StudentManagement
    collection = db.students
    
    # Function to insert a record into the database
    def insert_record(data):
        # Set null values for sem and cgpa if they don't exist in the request
        sem = data['sem'] if 'sem' in data else None
        cgpa = data['cgpa'] if 'cgpa' in data else None

        #sql = "INSERT INTO students (SRN, name, sem, section, cgpa) VALUES (%s, %s, %s, %s, %s)"
        val = (data['SRN'], data['name'], sem, data['section'], cgpa)
        
    # Function to handle incoming messages on the insert_record queue
    def callback(ch, method, properties, body):
        data = json.loads(body)
        # Check if SRN, name, and section fields are present in the request
        # if 'SRN' in data['data'] and 'name' in data['data'] and 'section' in data['data']:
        #     insert_record(data['data'])
        #     ch.basic_ack(delivery_tag=method.delivery_tag)
        # else:
        #     print('Error: Missing required fields')
        data = json.loads(body)
        print("[x] Received %r" % data, flush=True)
        collection.insert_one(data)
        # time.sleep(body.count(b'.'))
        # print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

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

