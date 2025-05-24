import pytest
import sys
import os
import json
import boto3
from moto import mock_aws
import pathlib

# Add the project root to Python path
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.absolute()
sys.path.append(str(PROJECT_ROOT))

from scripts.send_job import send_to_queue, receive_from_queue

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@mock_aws
def test_queue_roundtrip(aws_credentials):
    # Set up mocked SQS
    sqs = boto3.client('sqs', region_name="us-east-1")
    queue_name = 'media-encode-jobs'
    sqs.create_queue(QueueName=queue_name)

    job = {
        "job_id": "test123",
        "input_url": "s3://bucket/test.mp4",
        "profiles": [{"name": "720p"}]
    }

    send_to_queue(job)
    received = receive_from_queue()
    assert received["job_id"] == "test123"
    assert "profiles" in received