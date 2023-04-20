'''
It is a RabbitMQ client that can construct queues/exchanges and transfer the necessary data to consumers. The exchange to deliver the messages to one of the 4 different queues(one for each consumer) based on the binding/routing key.

An HTTP Server (Flask for Python/Express for NodeJS) to listen to health_check requests so that it can distribute it to the respective consumer.
'''

import pika
from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# Database Configuration
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'mysql',
    'database': 'cc_student'
}
cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()

@app.route('/health_check', methods=['GET'])
def health_check():
    # send message to consumer_one through RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='health_check')
    channel.basic_publish(exchange='', routing_key='health_check', body='health_check_message')
    connection.close()
    return "OK"

@app.route('/insert_record', methods=['POST'])
def insert_record():
    # send message to consumer_two through RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='insert_record')
    data = request.json
    message = f"{data['Name']}, {data['SRN']}, {data['Section']}"
    channel.basic_publish(exchange='', routing_key='insert_record', body=message)
    connection.close()
    # insert record into mysql
    insert_query = "INSERT INTO student (name, srn, section) VALUES (%s, %s, %s)"
    values = (data['Name'], data['SRN'], data['Section'])
    cursor.execute(insert_query, values)
    cnx.commit()
    return "OK"

@app.route('/read_database', methods=['GET'])
def read_database():
    # send message to consumer_three through RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='read_database')
    channel.basic_publish(exchange='', routing_key='read_database', body='read_database_message')
    connection.close()
    # read database and return the results
    select_query = "SELECT * FROM student"
    cursor.execute(select_query)
    result = cursor.fetchall()
    return str(result)

@app.route('/delete_record', methods=['GET'])
def delete_record():
    # send message to consumer_four through RabbitMQ
    srn = request.args.get('SRN')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='delete_record')
    channel.basic_publish(exchange='', routing_key='delete_record', body=srn)
    connection.close()
    # delete record from mysql
    delete_query = "DELETE FROM student WHERE srn = %s"
    values = (srn,)
    cursor.execute(delete_query, values)
    cnx.commit()
    return "OK"

if __name__ == '__main__':
    app.run(debug=True, port=5001)

