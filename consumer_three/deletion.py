'''
RabbitMQ Client to listen for incoming requests on the “delete_record” queue and process it.

This consumer must delete a record from the database based on the SRN which has been listened to through the “delete_record” queue.
'''

import http
import pika, sys , os
import mysql.connector
import json


def main():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password ="password",
        database= "cc_student"
        )
    cursor =db.cursor()

    def deleteRecs(srn):
        try:
            delete_query = f"DELETE FROM student WHERE SRN='{srn}'"
            cursor.execute(delete_query)
            db.commit()
            cursor.close()
            db.close()
            return True
        except:
            return False    
    def callback(ch,method,properties,body):
        # srn : recieved via queue
        srn = body.decode()
        if deleteRecs(srn):
            print(f"Record with SRN {srn} deleted successfully.")
        else:
            print(f"Error deleting record with SRN {srn}.")
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq')) # give the network ip for the rabbitmq image
    channel = connection.channel()
    channel.queue_declare(queue='delete_record')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='delete_record', on_message_callback=callback)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()     

if __name__ == "__main__":
    main()       