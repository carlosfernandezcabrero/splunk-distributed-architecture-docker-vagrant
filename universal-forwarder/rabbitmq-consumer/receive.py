# -*- coding: utf-8 -*-


import os

import pika
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
LOGS_PATH = os.getenv("LOGS_PATH")


def write_message(ch, method, properties, body):
    file = open(
        os.path.join(LOGS_PATH if LOGS_PATH else "/tmp", f"{method.exchange}.log"), "a"
    )
    file.write(body.decode() + "\n")
    file.close()


connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))

channel = connection.channel()
channel.queue_declare("logs")
channel.basic_consume(queue="logs", on_message_callback=write_message, auto_ack=True)
channel.start_consuming()
