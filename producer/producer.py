'''
It is a RabbitMQ client that can construct queues/exchanges and transfer the necessary data to consumers. The exchange to deliver the messages to one of the 4 different queues(one for each consumer) based on the binding/routing key.

An HTTP Server (Flask for Python/Express for NodeJS) to listen to health_check requests so that it can distribute it to the respective consumer.
'''

from flask import Flask, request
import pika
import json

app = Flask(__name__)

# Establish a connection with RabbitMQ server
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
# channel = connection.channel()

# channel_health_check = connection.channel()
# channel_insertion = connection.channel()
# channel_deletion = connection.channel()
# channel_read = connection.channel()

# # Declare the queues
# channel.queue_declare(queue='health_check')
# channel.queue_declare(queue='insert_record')
# channel.queue_declare(queue='delete_record')
# channel.queue_declare(queue='read_database')

# above code creating issues

@app.route("/", methods = ["GET"])
def routes():
    message = {
        "to health check": "http://127.0.0.1:5050/health_check",
        "to read data": "http://127.0.0.1:5050/read_database",
        "to insert data": "http://127.0.0.1:5050/insert_record/<record>",
        "to delete data": "http://127.0.0.1:5050/delete_record/<record>"
    }
    
    return json.dumps(message, indent = 4)


@app.route('/health_check', methods=['GET'])
def health_check():
    # Send a message to the health_check queue
    message = {'message': 'Health Check'}
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='health_check', durable=True)
    channel.basic_publish(exchange='',
                          routing_key='health_check',
                          body=json.dumps(message))
    connection.close() # for testing
    return 'Health check request has been sent'

@app.route('/insert_record/<SRN>/<Name>/<Section>', methods=['POST'])
def insert_record(SRN,Name,Section):
    # Get the data from the request
    # data = request.get_json()
    # srn = data.get('SRN')
    # name = data.get('name')
    # section = data.get('section')

    # if not all([srn, name, section]):
    #     return 'Missing fields: SRN, name, section', 400

    # # Send a message to the insert_record queue
    # message = {'message': 'Insert Record', 'data': data}
    # channel.basic_publish(exchange='',
    #                       routing_key='insert_record',
    #                       body=json.dumps(message))
    # return 'Record has been inserted'
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    b= SRN+"."+Name+"."+Section
    channel = connection.channel()
    channel.queue_declare(queue='insert_record', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='insert_record',
        body= b,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    print(" Message to insert record sent")
    return " Message to insert record sent "     
    
# @app.route('/delete_record/<record_id>', methods=['DELETE'])
# def delete_record(record_id):
#     # Send a message to the delete_record queue
#     message = {'message': 'Delete Record', 'record_id': record_id}
#     channel.basic_publish(exchange='',
#                           routing_key='delete_record',
#                           body=json.dumps(message))
#     return f'Record with id {record_id} has been deleted'


@app.route('/delete_record/<SRN>', methods=['GET'])
def delete_record(SRN):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    b= SRN
    channel = connection.channel()
    channel.queue_declare(queue='delete_record', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='delete_record',
        body= b,
        properties=pika.BasicProperties(
            delivery_mode=2, 
        ))
    connection.close()
    print(f"Deleting record for {SRN}")
    return f"Delete done for {SRN}"

@app.route('/read_database', methods=['GET'])
def read_database():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='read_database', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='read_database',
        body="Read Database message sent",
        properties=pika.BasicProperties(
            delivery_mode=2,  
        ))
    connection.close()
    return f'Retrieving all records...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
