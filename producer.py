import json
from datetime import datetime

import pika
from faker import Faker

from models import Contact

fake = Faker("uk-UA")
exchange_name = "web21_hw8"
queue_name = "web21_hw8_send_message"

credentials = pika.PlainCredentials("guest", "guest")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange=exchange_name, exchange_type="direct")
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name)


def create_tasks(nums: int):
    for i in range(nums):
        new_contact = Contact(
            fullname=fake.full_name(),
            email=fake.email(),
            subject=fake.sentence(nb_words=5),
            text=fake.sentence(nb_words=40),
        )
        cont_res = new_contact.save()
        # print(cont_res)
        message = {"id": str(cont_res.id)}
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=queue_name,
            body=json.dumps(message).encode(),
        )

        # message = {"id": i, "payload": f"Date: {datetime.now().isoformat()}"}
        # channel.basic_publish(
        #     exchange="web21 exchange",
        #     routing_key="web21_queue",
        #     body=json.dumps(message).encode(),
        # )

    message = b"Hello World!!!"


if __name__ == "__main__":
    create_tasks(10)


# print(f" [x] Sent {message}")
# connection.close()
