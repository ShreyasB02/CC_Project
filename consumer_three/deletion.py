'''
RabbitMQ Client to listen for incoming requests on the “delete_record” queue and process it.

This consumer must delete a record from the database based on the SRN which has been listened to through the “delete_record” queue.
'''

import http
import pika, sys , os,time
# import mysql.connector
import json
from pymongo import MongoClient


def main():
    # db = mysql.connector.connect(
    #     host = "localhost",
    #     user = "root",
    #     password ="password",
    #     database= "cc_student"
    #     )
    # cursor =db.cursor()

    # mongo:
    connectionstr="mongodb+srv://ccrmq:ccrmq@cluster0.s2ksf4g.mongodb.net/test"
    client = MongoClient(connectionstr)

    db = client['studentdb']
    collection = db['student']

    def deleteRecs(srn):
        try:
            delete_query = f"DELETE FROM student WHERE SRN='{srn}'"
            #cursor.execute(delete_query)
            #db.commit()
            #cursor.close()
            #db.close()
            return True
        except:
            return False    
    sleepTime = 20
    time.sleep(sleepTime)
    print('Consumer_three connecting to server ...')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='delete_record', durable=True)

    def callback(ch, method, properties, body):
        b = body.decode()
        collection.delete_one({"SRN":b})
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return "Student deleted successfully!"
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='delete_record', on_message_callback=callback)
    channel.start_consuming()

if __name__ == "__main__":
    if __name__ == '__main__':
        try:
            main()
        except KeyboardInterrupt:
            print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)