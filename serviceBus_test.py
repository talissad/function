import os
import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from local_settings import CONNECTION_STR, QUEUE_NAME


#envia uma unica mensagem
def send_single_message(sender):
    message = ServiceBusMessage("Single Message")
    sender.send_messages(message)
    print("Sent a single message")

#envia uma lista
def send_a_list_of_messages(sender):
    messages = [ServiceBusMessage("Message in list") for _ in range(5)]
    sender.send_messages(messages)
    print("Sent a list of 5 messages")

#envia um lote
def send_batch_message(sender):
    batch_message = sender.create_message_batch()
    for _ in range(10):
        try:
            batch_message.add_message(ServiceBusMessage("Message inside a ServiceBusMessageBatch"))
        except ValueError:
            # ServiceBusMessageBatch object reaches max_size.
            # New ServiceBusMessageBatch object can be created here to send more data.
            break
    sender.send_messages(batch_message)
    print("Sent a batch of 10 messages")

def send_users(users):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=False)
    with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        with sender:
            # Envia todos em uma mensagem só
            # sender.send_messages(ServiceBusMessage(json.dumps(users)))


            # Envia um por um
            batch_message = sender.create_message_batch()
            for user in users:
                try:
                    batch_message.add_message(ServiceBusMessage(json.dumps(user)))
                except ValueError:
                    # ServiceBusMessageBatch object reaches max_size.
                    # New ServiceBusMessageBatch object can be created here to send more data.
                    break
            sender.send_messages(batch_message)
            
    print("Done sending messages")
    print("-----------------------")

    with servicebus_client:
        # get the Queue Receiver object for the queue
        receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME, max_wait_time=5)
        with receiver:
            for msg in receiver:
                print("Received: " + str(msg))
                receiver.complete_message(msg)

    print("Acabou de receber")