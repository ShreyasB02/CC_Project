'''
RabbitMQ Client to listen for incoming requests on the “read_database” queue and process it.
This consumer must retrieve all the records present in the database.
'''

import http
import pika, sys , os
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
    client = MongoClient("mongodb://mongodb:27017")

    db = client.StudentManagement
    collection = db.students
    def callback(ch,method,properties,body):
        # cursor.execute("SELECT * FROM student") #create student column in db
        # records = cursor.fetchall()
        # response= json.dumps(records)
        #if retrieved data to be published
        # ch.basic_publish(
        #     exchange='',
        #     routing_key=properties.reply_to,
        #     properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        #     body=response)
        print("Found Details: ", list(collection.find({})), flush=True)



    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='read_database')
        #handle 1 message at a time:
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='read_database', on_message_callback=callback, auto_ack=True)  #ACk
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


 
