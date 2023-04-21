'''
It is a RabbitMQ client that can construct queues/exchanges and transfer the necessary data to consumers. The exchange to deliver the messages to one of the 4 different queues(one for each consumer) based on the binding/routing key.

An HTTP Server (Flask for Python/Express for NodeJS) to listen to health_check requests so that it can distribute it to the respective consumer.
'''

from flask import Flask, request
import pika
import json

app = Flask(__name__)

# Establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Declare the queues
channel.queue_declare(queue='health_check')
channel.queue_declare(queue='insert_record')
channel.queue_declare(queue='delete_record')
channel.queue_declare(queue='read_database')

@app.route('/health_check', methods=['GET'])
def health_check():
    # Send a message to the health_check queue
    message = {'message': 'Health Check'}
    channel.basic_publish(exchange='',
                          routing_key='health_check',
                          body=json.dumps(message))
    return 'Health check request has been sent'

@app.route('/insert_record', methods=['POST'])
def insert_record():
    # Get the data from the request
    data = request.get_json()
    
    # Send a message to the insert_record queue
    message = {'message': 'Insert Record', 'data': data}
    channel.basic_publish(exchange='',
                          routing_key='insert_record',
                          body=json.dumps(message))
    return 'Record has been inserted'

@app.route('/delete_record/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    # Send a message to the delete_record queue
    message = {'message': 'Delete Record', 'record_id': record_id}
    channel.basic_publish(exchange='',
                          routing_key='delete_record',
                          body=json.dumps(message))
    return f'Record with id {record_id} has been deleted'

@app.route('/read_database', methods=['GET'])
def read_database():
    # Send a message to the read_database queue
    message = {'message': 'Read Database'}
    channel.basic_publish(exchange='',
                          routing_key='read_database',
                          body=json.dumps(message))
    return 'Request to read database has been sent'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
