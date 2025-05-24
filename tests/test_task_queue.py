# tests/test_task_queue.py
import pytest
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.send_job import send_to_queue, receive_from_queue

def test_queue_roundtrip():
    job = {"job_id": "test123", "input_url": "s3://bucket/test.mp4", "profiles": [{"name": "720p"}]}
    send_to_queue(job)
    received = receive_from_queue()
    assert received["job_id"] == "test123"
    assert "profiles" in received