FROM jrottenberg/ffmpeg:4.4-alpine

RUN apk add --no-cache python3 py3-pip

RUN pip3 install boto3

WORKDIR /app

COPY qc_worker.py /app/qc_worker.py

RUN adduser -D workeruser

USER workeruser

ENTRYPOINT ["python3", "/app/qc_worker.py"]