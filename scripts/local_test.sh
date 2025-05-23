#!/bin/bash
docker-compose up -d
python scripts/send_job.py --input ./sample.mp4 --profiles ./profiles.json