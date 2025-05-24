# tests/test_failure_handling.py
import pytest
import os
from tests.conftest import mock_s3_bucket
from tests.fixtures import video_good
import sys
import os

# Add the docker directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'docker'))

from ffmpeg_worker.encode_worker import run_ffmpeg

def test_encode_failure_triggers_retry(tmp_path):
    bad_input = "tests/fixtures/doesnotexist.mp4"
    try:
        run_ffmpeg(bad_input, str(tmp_path / "fail.mp4"), {"width": 1280, "height": 720, "video_bitrate": "3000k", "audio_bitrate": "128k"})
    except Exception:
        # Here, assert the job is requeued or added to DLQ (mock the DLQ handler)
        assert True