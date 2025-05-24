# tests/test_task_queue.py
import pytest
import sys
import os

# Add the scripts directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from send_job import send_to_queue, receive_from_queue

def test_queue_roundtrip():
    job = {"job_id": "test123", "input_url": "s3://bucket/test.mp4", "profiles": [{"name": "720p"}]}
    send_to_queue(job)
    received = receive_from_queue()
    assert received["job_id"] == "test123"
    assert "profiles" in received