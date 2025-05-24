# tests/conftest.py
import os
import sys
import pytest
import boto3
from moto import mock_aws

# Add the project root to Python path so we can import from any directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def mock_s3_bucket(aws_credentials):
    with mock_aws():
        s3 = boto3.client('s3', region_name="us-east-1")
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