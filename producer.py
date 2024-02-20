import pika
import string
import random
import time
from threading import Thread

def send_messages(queue_name, message_length):
    # RabbitMQ connection parameters
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=queue_name,durable=True)

    # Generate random message
    def generate_random_message():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=message_length))

    # Continuously send messages
    while True:
        message = generate_random_message()
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        print(f"Sent message: {message}")

if __name__ == "__main__":
    # Configuration
    queue_name = "bugs.queue"  # Queue name
    message_length = 50  # Length of random strings

    # Start sending messages
    send_thread = Thread(target=send_messages, args=(queue_name, message_length))
    send_thread.daemon = True
    send_thread.start()

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
