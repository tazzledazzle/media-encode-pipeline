import os
import json
import uuid
import boto3
import pika
import logging
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
QUEUE_TYPE = os.getenv("QUEUE_TYPE", "sqs").lower()  # 'sqs' or 'rabbitmq'

# AWS SQS Configuration
SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "media-encode-jobs")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# RabbitMQ Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "media-encode-jobs")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
def receive_from_sqs():
    try:
        sqs = boto3.client("sqs", region_name=AWS_REGION)
        # Get the queue URL
        response = sqs.get_queue_url(QueueName=SQS_QUEUE_NAME)
        queue_url = response['QueueUrl']
        # Receive the message
        messages = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        if 'Messages' in messages:
            message = messages['Messages'][0]
            receipt_handle = message['ReceiptHandle']
            body = json.loads(message['Body'])
            # Delete the message from the queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            logger.info(f"Job received from SQS queue '{SQS_QUEUE_NAME}': {body['job_id']}")
            return body
        else:
            logger.warning("No messages received from SQS.")
            return None
    except ClientError as e:
        logger.error(f"Failed to receive job from SQS: {e}")
        raise

def receive_from_rabbitmq():
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        method_frame, header_frame, body = channel.basic_get(queue=RABBITMQ_QUEUE, auto_ack=True)
        if method_frame:
            job = json.loads(body)
            logger.info(f"Job received from RabbitMQ queue '{RABBITMQ_QUEUE}': {job['job_id']}")
            connection.close()
            return job
        else:
            logger.warning("No messages received from RabbitMQ.")
            connection.close()
            return None
    except Exception as e:
        logger.error(f"Failed to receive job from RabbitMQ: {e}")
        raise

def receive_from_queue():
    if QUEUE_TYPE == "sqs":
        return receive_from_sqs()
    elif QUEUE_TYPE == "rabbitmq":
        return receive_from_rabbitmq()
    else:
        raise ValueError(f"Unsupported QUEUE_TYPE: {QUEUE_TYPE}")

def send_to_sqs(job: dict):
    try:
        sqs = boto3.client("sqs", region_name=AWS_REGION)
        # Get the queue URL
        response = sqs.get_queue_url(QueueName=SQS_QUEUE_NAME)
        queue_url = response['QueueUrl']
        # Send the message
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(job)
        )
        logger.info(f"Job sent to SQS queue '{SQS_QUEUE_NAME}': {job['job_id']}")
    except ClientError as e:
        logger.error(f"Failed to send job to SQS: {e}")
        raise

def send_to_rabbitmq(job: dict):
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(job),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        logger.info(f"Job sent to RabbitMQ queue '{RABBITMQ_QUEUE}': {job['job_id']}")
        connection.close()
    except Exception as e:
        logger.error(f"Failed to send job to RabbitMQ: {e}")
        raise

def send_to_queue(job: dict):
    if QUEUE_TYPE == "sqs":
        send_to_sqs(job)
    elif QUEUE_TYPE == "rabbitmq":
        send_to_rabbitmq(job)
    else:
        raise ValueError(f"Unsupported QUEUE_TYPE: {QUEUE_TYPE}")

if __name__ == "__main__":
    # Example job
    job = {
        "job_id": str(uuid.uuid4()),
        "input_url": "s3://your-bucket/input_video.mp4",
        "profiles": [
            {
                "name": "720p",
                "width": 1280,
                "height": 720,
                "video_bitrate": "3000k",
                "audio_bitrate": "128k"
            },
            {
                "name": "480p",
                "width": 854,
                "height": 480,
                "video_bitrate": "1500k",
                "audio_bitrate": "128k"
            }
        ]
    }
    send_to_queue(job)