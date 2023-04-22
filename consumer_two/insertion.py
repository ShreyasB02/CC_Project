'''
RabbitMQ Client to listen for incoming requests on the “health_check” queue and process it.

This consumer must acknowledge that the health-check message has been listened to through the “health_check” queue. (Simple Ack)


'''


import json
import pika
import mysql.connector


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='insert_record')

    # Set up MySQL connection
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="cc_student"
    )
    mysql_cursor = db.cursor()

    # Function to insert a record into the database
    def insert_record(data):
        # Set null values for sem and cgpa if they don't exist in the request
        sem = data['sem'] if 'sem' in data else None
        cgpa = data['cgpa'] if 'cgpa' in data else None

        sql = "INSERT INTO students (SRN, name, sem, section, cgpa) VALUES (%s, %s, %s, %s, %s)"
        val = (data['SRN'], data['name'], sem, data['section'], cgpa)
        mysql_cursor.execute(sql, val)
        db.commit()

    # Function to handle incoming messages on the insert_record queue
    def callback(ch, method, properties, body):
        data = json.loads(body)
        # Check if SRN, name, and section fields are present in the request
        if 'SRN' in data['data'] and 'name' in data['data'] and 'section' in data['data']:
            insert_record(data['data'])
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            print('Error: Missing required fields')

    # Set up consumer to take only one message at a time
    channel.basic_qos(prefetch_count=1)

    # Start listening for incoming messages on the insert_record queue
    channel.basic_consume(queue='insert_record', on_message_callback=callback)

    print('Insertion Consumer is waiting for messages...')
    channel.start_consuming()


if __name__== "__main__":
    main()        
        

