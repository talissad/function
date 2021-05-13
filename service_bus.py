import os
import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from local_settings import CONNECTION_STR, QUEUE_NAME


def send_users(users):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=False)
    with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        with sender:
            batch_message = sender.create_message_batch()
            for user in users:
                try:
                    mapped_user = {"id": user["id"], "name": user["displayName"], "email": user["mail"], "jobTitle": user["jobTitle"]}
                    batch_message.add_message(ServiceBusMessage(json.dumps(mapped_user)))
                    print(mapped_user)
                except ValueError:
                    # ServiceBusMessageBatch object reaches max_size.
                    # New ServiceBusMessageBatch object can be created here to send more data.
                    break
            sender.send_messages(batch_message)