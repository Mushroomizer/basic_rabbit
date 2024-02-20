import pika

def consume_messages(queue_name, batch_size):
    # RabbitMQ connection parameters
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=queue_name,durable=True)

    # Consume messages from the queue
    def callback(ch, method, properties, body):
        print(f"Received message: {body.decode()}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Start consuming messages
    try:
        print(f"Consuming messages from queue '{queue_name}' in batches of size {batch_size}...")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Exiting...")
        connection.close()

if __name__ == "__main__":
    # Configuration
    queue_name = "bugs.queue"  # Queue name
    batch_size = 10  # Batch size

    # Start consuming messages
    consume_messages(queue_name, batch_size)
