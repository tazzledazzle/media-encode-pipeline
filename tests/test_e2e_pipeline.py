# tests/test_e2e_pipeline.py
import pytest
import boto3
import os
import sys
from moto import mock_aws

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.send_job import send_to_queue
from docker.ffmpeg_worker.encode_worker import receive_from_queue, run_ffmpeg, upload_to_s3
from docker.qc_worker.qc_worker import run_all_qc

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@mock_aws
def test_full_pipeline(monkeypatch, tmp_path, aws_credentials):
    # Set up mocked S3
    s3 = boto3.client('s3', region_name="us-east-1")
    bucket_name = 'test-bucket'
    s3.create_bucket(Bucket=bucket_name)
    
    # Upload test video to mocked S3
    test_video_path = 'tests/fixtures/test_video_good.mp4'
    if os.path.exists(test_video_path):
        with open(test_video_path, 'rb') as f:
            s3.put_object(Bucket=bucket_name, Key='test_video_good.mp4', Body=f)
    
    # Define job
    job = {
        "job_id": "e2e123",
        "input_url": f"s3://{bucket_name}/test_video_good.mp4",
        "profiles": [{"name": "720p", "width": 1280, "height": 720, "video_bitrate": "3000k", "audio_bitrate": "128k"}]
    }
    
    # 1. Send to queue
    send_to_queue(job)
    
    # 2. Worker receives
    recv_job = receive_from_queue()
    
    # 3. Encode
    output_file = tmp_path / "e2e_output_720p.mp4"
    run_ffmpeg(recv_job["input_url"], str(output_file), recv_job["profiles"][0])
    
    # 4. QC
    qc_results = run_all_qc(str(output_file))
    assert all(qc_results.values())
    
    # 5. Upload to S3
    upload_to_s3(str(output_file), bucket_name, "e2e_output_720p.mp4")
    
    # 6. Validate upload
    response = s3.get_object(Bucket=bucket_name, Key="e2e_output_720p.mp4")
    content = response["Body"].read()
    assert content  # Ensure the uploaded file is not empty