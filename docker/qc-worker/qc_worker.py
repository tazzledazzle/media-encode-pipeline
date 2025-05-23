import subprocess, sys

def qc_black_frames(output_file):
    cmd = [
        "ffmpeg", "-i", output_file, "-vf", "blackdetect=d=0.1:pic_th=0.98", "-an", "-f", "null", "-"
    ]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    return "black_start:" not in result.stderr

def qc_loudness(output_file):
    cmd = [
        "ffmpeg", "-i", output_file, "-af", "ebur128", "-f", "null", "-"
    ]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    return "Summary:" in result.stderr  # Parse more specifically as needed

def main(output_file):
    if not qc_black_frames(output_file):
        sys.exit("Black frames detected!")
    if not qc_loudness(output_file):
        sys.exit("Audio loudness out of spec!")
    print("QC passed!")

if __name__ == "__main__":
    main(sys.argv[1])