import boto3, pika, json, subprocess, os

def fetch_job():
    # Example for RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    method_frame, header_frame, body = channel.basic_get(queue='encode')
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        return json.loads(body)
    return None

def run_ffmpeg(input_path, output_path, profile):
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", f"scale={profile['width']}:{profile['height']}",
        "-b:v", profile['video_bitrate'], "-b:a", profile['audio_bitrate'],
        output_path
    ]
    subprocess.run(cmd, check=True)

def upload_to_s3(local_file, bucket, key):
    s3 = boto3.client('s3')
    s3.upload_file(local_file, bucket, key)

def main():
    while True:
        job = fetch_job()
        if not job:
            continue
        input_file = '/tmp/input.mp4'
        # download from S3
        for profile in job['profiles']:
            output_file = f"/output/{profile['name']}.mp4"
            run_ffmpeg(input_file, output_file, profile)
            upload_to_s3(output_file, 'my-bucket', f"outputs/{job['job_id']}/{profile['name']}.mp4")
        # Enqueue for QC, or trigger QC job directly

if __name__ == "__main__":
    main()