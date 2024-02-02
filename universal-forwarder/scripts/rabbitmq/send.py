# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime

import pika
from dotenv import load_dotenv
from faker import Faker
from faker.providers import internet
from InquirerPy import prompt

load_dotenv(dotenv_path=".env")

RABBITMQ_SERVER = os.getenv("RABBITMQ_SERVER")
DEFAULT_EXCHANGE = "my_exchange"

fake = Faker()
fake.add_provider(internet)

def generate_message():
    return f"[{datetime.now().strftime("%F %T")}] {fake.http_method()} {fake.uri()}"

if __name__ == "__main__":
    interactive = sys.argv[1] if len(sys.argv) > 1 else 0
    
    if (interactive == 0):
        result = prompt([
            {
                "type": "input",
                "message": "Nombre de la exchange:",
                "name": "exchange_name",
                "default": DEFAULT_EXCHANGE,
            },
            {
                "type": "input",
                "message": "Mensaje:",
                "name": "message",
                "default": generate_message(),
            },
        ])


    EXCHANGE_NAME = result["exchange_name"] if interactive == 0 else DEFAULT_EXCHANGE
    QUEUE_NAME = "logs"

    parameters = pika.ConnectionParameters(RABBITMQ_SERVER if RABBITMQ_SERVER else "localhost")
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct")
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=QUEUE_NAME)
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=QUEUE_NAME,
        body=result["message"] if interactive == 0 else generate_message(),
    )

    connection.close()
