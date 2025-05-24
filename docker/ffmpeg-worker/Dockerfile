# Use a stable, small FFmpeg image as the base
FROM jrottenberg/ffmpeg:4.4-alpine

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Install required Python libraries (add others as needed, e.g., pika for RabbitMQ)
RUN pip3 install boto3

# Create a working directory for your app
WORKDIR /app

# Copy your encoding worker script(s) into the container
COPY ./encode_worker.py /app/encode_worker.py

# If you have a requirements.txt for more dependencies (e.g., pika for RabbitMQ, requests, etc.)
# COPY requirements.txt /app/
# RUN pip3 install -r requirements.txt

# Optional: Add non-root user for security
RUN adduser -D workeruser
USER workeruser

# Set the entrypoint to run your Python worker
ENTRYPOINT ["python3", "/app/encode_worker.py"]