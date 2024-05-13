import json
import os
import sys
import time

import pika

from models import Contact

exchange_name = "web21_hw8"
queue_name = "web21_hw8_send_message"


def send_message(contact):
    print(f"Sending message to {contact.fullname} on {contact.email}")
    time.sleep(1)
    print(f"Sending complete message to {contact.fullname} on {contact.email}")
    return True


def main():
    credentials = pika.PlainCredentials("guest", "guest")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        pk = json.loads(body.decode()).get("id")
        contact = Contact.objects(id=pk, is_send=False).first()
        if contact:
            print(f" [x] Received {pk}")
            # print(f" [x] Received {method.delivery_tag} task")
            res = send_message(contact)
            if res:
                contact.update(set__is_send=True)
                ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
