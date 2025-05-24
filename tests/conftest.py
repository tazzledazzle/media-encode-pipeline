# tests/conftest.py
import pytest
import boto3
import os
from moto import mock_aws

@pytest.fixture
def mock_s3_bucket():
    with mock_aws():
        s3 = boto3.client('s3')
        bucket_name = 'test-bucket'
        s3.create_bucket(Bucket=bucket_name)
        
        test_videos = {
            'test_video_good.mp4': 'tests/fixtures/test_video_good.mp4',
            'test_video_black.mp4': 'tests/fixtures/test_video_black.mp4'
        }
        
        for key, path in test_videos.items():
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    s3.put_object(Bucket=bucket_name, Key=key, Body=f)
        
        yield bucket_name

@pytest.fixture
def video_good():
    return "tests/fixtures/test_video_good.mp4"

@pytest.fixture
def video_black():
    return "tests/fixtures/test_video_black.mp4"

@pytest.fixture
def mock_s3_bucket():
    with mock_s3():
        # Create a mock S3 bucket
        s3 = boto3.client('s3')
        bucket_name = 'test-bucket'
        s3.create_bucket(Bucket=bucket_name)
        
        # Upload test videos to mock S3
        test_videos = {
            'test_video_good.mp4': 'tests/fixtures/test_video_good.mp4',
            'test_video_black.mp4': 'tests/fixtures/test_video_black.mp4'
        }
        
        for key, path in test_videos.items():
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    s3.put_object(Bucket=bucket_name, Key=key, Body=f)
        
        yield bucket_name