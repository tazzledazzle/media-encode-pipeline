# tests/test_storage.py
import pytest
import boto3
from moto import mock_aws
import sys
import os

# Add the docker directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'docker'))

from ffmpeg_worker.encode_worker import upload_to_s3

@mock_aws
def test_s3_upload():
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="test-bucket")
    local_file = "tests/fixtures/test_video_good.mp4"
    upload_to_s3(local_file, "test-bucket", "uploads/test_video.mp4")
    response = s3.list_objects(Bucket="test-bucket")
    assert "Contents" in response