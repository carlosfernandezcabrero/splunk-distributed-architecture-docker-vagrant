# -*- coding: utf-8 -*-


import pika


def write_message(ch, method, properties, body):
    file = open(f"tmp/{method.exchange}.log", "a")
    file.write(body.decode() + "\n")
    file.close()


connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))

channel = connection.channel()
channel.queue_declare("logs")
channel.basic_consume(queue="logs", on_message_callback=write_message, auto_ack=True)
channel.start_consuming()
