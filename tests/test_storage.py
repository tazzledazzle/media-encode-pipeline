# tests/test_storage.py
import pytest
import boto3
from moto import mock_aws
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docker.ffmpeg_worker.encode_worker import upload_to_s3

@mock_aws
def test_s3_upload():
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="test-bucket")
    local_file = "tests/fixtures/test_video_good.mp4"
    upload_to_s3(local_file, "test-bucket", "uploads/test_video.mp4")
    response = s3.list_objects(Bucket="test-bucket")
    assert "Contents" in response