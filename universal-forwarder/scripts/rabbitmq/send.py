# -*- coding: utf-8 -*-

import os
from datetime import datetime

import pika
from dotenv import load_dotenv
from faker import Faker
from faker.providers import internet
from InquirerPy import prompt

load_dotenv(dotenv_path=".env")
RABBITMQ_SERVER = os.getenv("RABBITMQ_SERVER")

fake = Faker()
fake.add_provider(internet)

result = prompt([
    {
        "type": "input",
        "message": "Nombre de la exchange:",
        "name": "exchange_name",
        "default": "my_exchange",
    },
    {
        "type": "input",
        "message": "Nombre de la cola:",
        "name": "queue_name",
        "default": "logs",
    },
    {
        "type": "input",
        "message": "Mensaje:",
        "name": "message",
        "default": f"[{datetime.now().strftime("%F %T")}] {fake.http_method()} {fake.uri()}",
    },
])


EXCHANGE_NAME = result["exchange_name"]
QUEUE_NAME = result["queue_name"]

parameters = pika.ConnectionParameters(RABBITMQ_SERVER)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct")
channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=QUEUE_NAME)
channel.basic_publish(
    exchange=EXCHANGE_NAME,
    routing_key=QUEUE_NAME,
    body=result["message"],
)

connection.close()
