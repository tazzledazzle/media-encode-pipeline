# tests/test_e2e_pipeline.py
import pytest
import time
import boto3
from moto import mock_aws
from scripts.send_job import send_to_queue
from docker.ffmpeg_worker.encode_worker import receive_from_queue, run_ffmpeg, upload_to_s3
from docker.qc_worker.qc_worker import run_all_qc

@pytest.fixture
def mock_s3_bucket():
    with mock_aws():
        s3 = boto3.client('s3')
        bucket_name = 'test-bucket'
        s3.create_bucket(Bucket=bucket_name)
        
        test_videos = {
            'test_video_good.mp4': 'tests/fixtures/test_video_good.mp4'
        }
        
        for key, path in test_videos.items():
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    s3.put_object(Bucket=bucket_name, Key=key, Body=f)
        
        yield bucket_name

def test_full_pipeline(monkeypatch, tmp_path, mock_s3_bucket):
    # Simulate sending and receiving a job
    job = {
        "job_id": "e2e123",
        "input_url": f"s3://{mock_s3_bucket}/test_video_good.mp4",
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
    # 5. Upload to S3 (moto mock as above)
    # 6. Validate upload