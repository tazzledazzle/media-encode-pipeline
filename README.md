# Media Encoding Pipeline

A scalable media encoding pipeline built with Docker containers and FastAPI.

## Prerequisites

- Docker Desktop (with Docker Buildx enabled)
- Python 3.8+
- Git
- AWS CLI (for S3 operations)

## Architecture Overview

The pipeline consists of three main components:

1. **API Service** (`pipeline-api`)
   - FastAPI-based REST API
   - Handles job submission and status tracking
   - Manages task queue

2. **FFmpeg Worker** (`ffmpeg-worker`)
   - Handles video encoding tasks
   - Supports multiple profiles (e.g., 720p, 1080p)
   - Uses FFmpeg for transcoding

3. **QC Worker** (`qc-worker`)
   - Performs quality control checks
   - Validates encoded files
   - Ensures compliance with specifications

## Building Containers

### For Apple Silicon (ARM64)

```bash
# Build FFmpeg Worker
cd docker/ffmpeg-worker
docker buildx build --platform linux/arm64 -t media-encode-pipeline/ffmpeg-worker:arm64 .

# Build QC Worker
cd ../qc-worker
docker buildx build --platform linux/arm64 -t media-encode-pipeline/qc-worker:arm64 .
```

### For AMD64

```bash
# Build FFmpeg Worker
cd docker/ffmpeg-worker
docker buildx build --platform linux/amd64 -t media-encode-pipeline/ffmpeg-worker:amd64 .

# Build QC Worker
cd ../qc-worker
docker buildx build --platform linux/amd64 -t media-encode-pipeline/qc-worker:amd64 .
```

## Running the Pipeline

1. Start the API service:

```bash
cd pipeline-api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Start the workers:

```bash
# FFmpeg Worker
docker run -d media-encode-pipeline/ffmpeg-worker:arm64

# QC Worker
docker run -d media-encode-pipeline/qc-worker:arm64
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

### For AMD64

```bash
# Build FFmpeg Worker
cd docker/ffmpeg-worker
docker buildx build --platform linux/amd64 -t media-encode-pipeline/ffmpeg-worker:amd64 .

# Build QC Worker
cd ../qc-worker
docker buildx build --platform linux/amd64 -t media-encode-pipeline/qc-worker:amd64 .
```

## Running the Pipeline

1. Start the API service:
```bash
cd pipeline-api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Start the workers:
```bash
# FFmpeg Worker
docker run -d media-encode-pipeline/ffmpeg-worker:arm64

# QC Worker
docker run -d media-encode-pipeline/qc-worker:arm64
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Configuration

The pipeline requires the following environment variables:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `S3_BUCKET_NAME`
- `RABBITMQ_HOST`
- `RABBITMQ_PORT`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
