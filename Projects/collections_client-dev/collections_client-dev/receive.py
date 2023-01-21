#!/usr/bin/env python
import os
import pika
import sys

from config import settings


def main():
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        settings.RABBITMQ_HOST,
        settings.RABBITMQ_PORT,
        "/",
        credentials
    ))
    channel = connection.channel()

    channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        # import_data()

    channel.basic_consume(queue=settings.RABBITMQ_QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        while True:
            ...
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
