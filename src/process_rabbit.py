#!/usr/bin/env python
import pika
import sys
import os
import time  # Optional: for adding delays or other time-related logic
import json
from try_tika import extract_text_and_dates

# --- Connection Parameters ---
# Adjust these if your RabbitMQ setup is different (e.g., different host, port, or credentials)
# These defaults match the podman-compose example IF you kept user/pass as guest/guest
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.environ.get("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "guest")  # Use the user you configured
RABBITMQ_PASS = os.environ.get(
    "RABBITMQ_PASS", "guest"
)  # Use the password you configured
QUEUE_NAME = "celery"  # The specific queue we want to read from


# --- Callback function to process messages ---
def message_callback(channel, method_frame, header_frame, body):
    """
    This function is called whenever a message is received from the queue.
    """
    print(f" [x] Received message from queue '{QUEUE_NAME}'")
    print(f"     Delivery Tag: {method_frame.delivery_tag}")
    print(f"     Message Headers: {header_frame}")

    # Try decoding the message body (often JSON or simple text)
    try:
        # Celery often uses JSON, but adjust encoding/decoding as needed
        decoded_body = body.decode("utf-8")
        print(f"     Message Body (decoded): {decoded_body}")
        file_path = json.loads(decoded_body)[0][0]
        print(file_path)
        (text, md) = extract_text_and_dates(file_path)
        print(text)
        print(md["dates_extracted"])
        # --- ADD YOUR MESSAGE PROCESSING LOGIC HERE ---
        # For example, parse JSON, update database, call another function, etc.
        # time.sleep(1) # Simulate work
        print(" [x] Finished processing message.")

    except Exception as e:
        print(f" [!] Error processing message body: {e}")
        # Consider how to handle errors - maybe reject and requeue?
        # channel.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=False) # Example: Reject without requeueing
        # For now, we will still acknowledge it to remove it from the queue

    # Acknowledge the message: Tells RabbitMQ the message was successfully processed
    # If the script crashes before this, RabbitMQ will requeue the message (if persistent)
    print(f" [>] Acknowledging message (tag: {method_frame.delivery_tag})...")
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    print(" [<] Message acknowledged.")


# --- Main connection and consumption logic ---
def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials,
        # Optional: Increase heartbeat interval if experiencing timeouts on slow networks/debugging
        # heartbeat=600,
        # blocked_connection_timeout=300
    )
    connection = None  # Initialize for finally block

    try:
        print(
            f" [*] Attempting to connect to RabbitMQ ({RABBITMQ_HOST}:{RABBITMQ_PORT})..."
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        print(" [*] Connection successful.")

        # Declare the queue (optional but good practice)
        # This ensures the queue exists. If it already exists with the same properties,
        # this command does nothing. If it exists with different properties, it might error.
        # 'durable=True' means the queue definition will survive a broker restart.
        # Your producer should also declare it as durable.
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        print(f" [*] Ensured queue '{QUEUE_NAME}' exists.")

        # Optional: Set Quality of Service (prefetch count)
        # This tells RabbitMQ not to give more than `prefetch_count` messages to this worker
        # at a time. Once the worker acknowledges a message, RabbitMQ sends another.
        # This can prevent a worker from being overwhelmed.
        channel.basic_qos(prefetch_count=1)

        # Start consuming messages from the queue
        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=message_callback,
            auto_ack=False,  # We will manually acknowledge messages in the callback
        )

        print(
            f" [*] Waiting for messages on queue '{QUEUE_NAME}'. To exit press CTRL+C"
        )
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as e:
        print(
            f" [!] Connection Error: Could not connect to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}."
        )
        print(f"     Error details: {e}")
        print(
            f"     Ensure RabbitMQ is running and credentials (user: {RABBITMQ_USER}) are correct."
        )
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n [!] Keyboard interrupt received. Stopping consumer...")
        # Gracefully stop consuming and close connection
        if connection and connection.is_open:
            if (
                "channel" in locals() and channel.is_open
            ):  # Check if channel was successfully created
                print(" [*] Stopping consuming...")
                channel.stop_consuming()  # Stop consuming new messages
                print(" [*] Consumer stopped.")
            connection.close()
            print(" [*] RabbitMQ connection closed.")
        print(" [*] Exiting script.")
        sys.exit(0)

    except Exception as e:
        print(f" [!] An unexpected error occurred: {e}")
        # Ensure connection is closed even on unexpected errors
        if connection and connection.is_open:
            connection.close()
            print(" [*] RabbitMQ connection closed due to error.")
        sys.exit(1)


if __name__ == "__main__":
    main()
