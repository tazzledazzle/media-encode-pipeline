# tests/test_qc_worker.py
import pytest
import os
import sys
import pathlib

# Add the project root to Python path
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.absolute()
sys.path.append(str(PROJECT_ROOT))

from tests.conftest import mock_s3_bucket
from tests.fixtures import video_good, video_black

from docker.qc_worker.qc_worker import qc_black_frames, qc_loudness, qc_freeze

class TestQCWorker:
    def setup_class(self):
        self.test_dir = "tests/fixtures"
        self.good_video = os.path.join(self.test_dir, "test_video_good.mp4")
        self.black_video = os.path.join(self.test_dir, "test_video_black.mp4")
        self.silent_video = os.path.join(self.test_dir, "test_video_silent.mp4")
        self.freeze_video = os.path.join(self.test_dir, "test_video_freeze.mp4")

    def test_black_frames_detected(self):
        """Test detection of black frames"""
        assert not qc_black_frames(self.black_video)
        assert qc_black_frames(self.good_video)

    def test_black_frames_threshold(self):
        """Test black frame detection with threshold"""
        # This test assumes the black video has more than 50% black frames
        assert not qc_black_frames(self.black_video, threshold=0.5)
        # This test assumes the good video has less than 5% black frames
        assert qc_black_frames(self.good_video, threshold=0.05)

    def test_loudness_check(self):
        """Test loudness detection"""
        assert qc_loudness(self.good_video)
        assert not qc_loudness(self.silent_video)

    def test_loudness_threshold(self):
        """Test loudness detection with custom thresholds"""
        # Test with stricter threshold
        assert qc_loudness(self.good_video, threshold=-23)
        # Test with more lenient threshold
        assert qc_loudness(self.good_video, threshold=-16)

    def test_freeze_detection(self):
        """Test freeze frame detection"""
        assert qc_freeze(self.good_video)
        assert not qc_freeze(self.freeze_video)

    def test_freeze_duration(self):
        """Test freeze detection with duration threshold"""
        # Test with shorter duration threshold
        assert qc_freeze(self.good_video, min_duration=0.1)
        # Test with longer duration threshold
        assert not qc_freeze(self.freeze_video, min_duration=5.0)

    def test_invalid_input(self):
        """Test QC with invalid input file"""
        with pytest.raises(Exception):
            qc_black_frames("not_a_video.mp4")
        with pytest.raises(Exception):
            qc_loudness("not_a_video.mp4")
        with pytest.raises(Exception):
            qc_freeze("not_a_video.mp4")

    def test_qc_all_checks(self):
        """Test all QC checks together"""
        # Good video should pass all checks
        assert qc_black_frames(self.good_video)
        assert qc_loudness(self.good_video)
        assert qc_freeze(self.good_video)

        # Bad video should fail at least one check
        assert not qc_black_frames(self.black_video)
        assert not qc_loudness(self.silent_video)
        assert not qc_freeze(self.freeze_video)


