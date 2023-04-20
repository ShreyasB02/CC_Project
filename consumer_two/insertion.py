'''
RabbitMQ Client to listen for incoming requests on the “health_check” queue and process it.

This consumer must acknowledge that the health-check message has been listened to through the “health_check” queue. (Simple Ack)


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

    cursor = db.cursor()

    def insertRecord(data): # data taken from json(?)
        

    def callback(ch,method,properties,body):

