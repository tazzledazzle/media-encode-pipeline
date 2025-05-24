# tests/test_encode_worker.py
import pytest
import os
import sys
import pathlib
import subprocess

# Add the project root to Python path
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.absolute()
sys.path.append(str(PROJECT_ROOT))

from tests.conftest import mock_s3_bucket
from tests.fixtures import video_good

from docker.ffmpeg_worker.encode_worker import run_ffmpeg

class TestEncodeWorker:
    def setup_class(self):
        self.test_dir = "tests/fixtures"
        self.good_video = os.path.join(self.test_dir, "test_video_good.mp4")
        self.black_video = os.path.join(self.test_dir, "test_video_black.mp4")

    def test_encode_success_720p(self, tmp_path):
        """Test successful 720p encoding"""
        output_file = tmp_path / "output_720p.mp4"
        profile = {
            "width": 1280,
            "height": 720,
            "video_bitrate": "3000k",
            "audio_bitrate": "128k"
        }
        
        run_ffmpeg(self.good_video, str(output_file), profile)
        assert output_file.exists()
        assert output_file.stat().st_size > 10000
        
        # Verify output dimensions using ffprobe
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", 
             "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", str(output_file)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "1280x720"

    def test_encode_success_480p(self, tmp_path):
        """Test successful 480p encoding"""
        output_file = tmp_path / "output_480p.mp4"
        profile = {
            "width": 854,
            "height": 480,
            "video_bitrate": "1500k",
            "audio_bitrate": "128k"
        }
        
        run_ffmpeg(self.good_video, str(output_file), profile)
        assert output_file.exists()
        assert output_file.stat().st_size > 10000

    def test_encode_invalid_input(self, tmp_path):
        """Test encoding with non-existent input file"""
        with pytest.raises(Exception):
            run_ffmpeg("not_a_video.mp4", str(tmp_path / "fail.mp4"), {
                "width": 1280,
                "height": 720,
                "video_bitrate": "3000k",
                "audio_bitrate": "128k"
            })

    def test_encode_invalid_profile(self, tmp_path):
        """Test encoding with invalid profile parameters"""
        with pytest.raises(Exception):
            run_ffmpeg(self.good_video, str(tmp_path / "fail.mp4"), {
                "width": -1,  # Invalid width
                "height": 720,
                "video_bitrate": "3000k",
                "audio_bitrate": "128k"
            })

    def test_encode_black_video(self, tmp_path):
        """Test encoding of black frame video"""
        output_file = tmp_path / "output_black.mp4"
        profile = {
            "width": 1280,
            "height": 720,
            "video_bitrate": "3000k",
            "audio_bitrate": "128k"
        }
        
        run_ffmpeg(self.black_video, str(output_file), profile)
        assert output_file.exists()
        assert output_file.stat().st_size > 10000

    def test_encode_with_metadata(self, tmp_path):
        """Test encoding with metadata preservation"""
        output_file = tmp_path / "output_metadata.mp4"
        profile = {
            "width": 1280,
            "height": 720,
            "video_bitrate": "3000k",
            "audio_bitrate": "128k",
            "preserve_metadata": True
        }
        
        run_ffmpeg(self.good_video, str(output_file), profile)
        assert output_file.exists()
        assert output_file.stat().st_size > 10000
