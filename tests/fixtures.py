import os

def get_fixture_path(filename):
    return os.path.join(os.path.dirname(__file__), 'fixtures', filename)

def video_good():
    return get_fixture_path('test_video_good.mp4')

def video_black():
    return get_fixture_path('test_video_black.mp4')
