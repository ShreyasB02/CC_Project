'''
It is a RabbitMQ client that can construct queues/exchanges and transfer the necessary data to consumers. The exchange to deliver the messages to one of the 4 different queues(one for each consumer) based on the binding/routing key.

An HTTP Server (Flask for Python/Express for NodeJS) to listen to health_check requests so that it can distribute it to the respective consumer.
'''

import pika
import json
import os, sys
from flask import Flask , request # for the http REST requests

import pika
import json
from flask import Flask, request

app = Flask(__name__)
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
exchange_name = 'exchange_name'
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

@app.route('/health_check', methods=['GET'])
def health_check():
    message = {'type': 'health_check', 'data': 'RabbitMQ connection is established'}
    channel.basic_publish(exchange=exchange_name, routing_key='health_check', body=json.dumps(message))
    return 'OK'

@app.route('/insert_record', methods=['POST'])
def insert_record():
    data = request.json
    message = {'type': 'insert_record', 'data': data}
    channel.basic_publish(exchange=exchange_name, routing_key='insert_record', body=json.dumps(message))
    return 'OK'

@app.route('/read_database', methods=['GET'])
def read_database():
    message = {'type': 'read_database', 'data': ''}
    channel.basic_publish(exchange=exchange_name, routing_key='read_database', body=json.dumps(message))
    return 'OK'

@app.route('/delete_record/<srn>', methods=['GET'])
def delete_record(srn):
    message = {'type': 'delete_record', 'data': {'srn': srn}}
    channel.basic_publish(exchange=exchange_name, routing_key='delete_record', body=json.dumps(message))
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, port=5001)

