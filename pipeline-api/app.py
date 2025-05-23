from fastapi import FastAPI, Request
import boto3, uuid, json

app = FastAPI()

@app.post("/encode-job")
async def submit_job(req: Request):
    job = await req.json()
    job['job_id'] = str(uuid.uuid4())
    # Push to SQS
    sqs = boto3.client('sqs')
    sqs.send_message(QueueUrl="QUEUE_URL", MessageBody=json.dumps(job))
    return {"status": "queued", "job_id": job['job_id']}