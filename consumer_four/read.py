'''
RabbitMQ Client to listen for incoming requests on the “read_database” queue and process it.
This consumer must retrieve all the records present in the database.
'''

import http
import pika, sys , os
import mysql.connector
import json #incase we need to send the data

# Rabbitmq is hosted on its own container running on its own network

def main():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password ="password",
        database= "cc_student"
        )
    cursor =db.cursor()

    def callback(ch,method,properties,body):
        cursor.execute("SELECT * FROM student") #create student column in db
        records = cursor.fetchall()
        response= json.dumps(records)
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=response)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='read_database')
        #handle 1 message at a time:
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='read_database', on_message_callback=callback, auto_ack=True)  #ACk
        channel.start_consuming()


if __name__ == "__main__":
    main()


 
