# tests/test_k8s_e2e.py (Pseudo, requires K8s access and S3 creds)
import requests, time

def test_submit_and_check_pipeline():
    job_payload = {...}
    # Submit via API endpoint
    r = requests.post("https://your-api/encode-job", json=job_payload)
    job_id = r.json()["job_id"]
    # Poll output location / status API
    for _ in range(20):
        status = requests.get(f"https://your-api/job-status/{job_id}").json()
        if status["state"] == "complete":
            assert status["qc_passed"] is True
            return
        time.sleep(15)
    assert False, "Pipeline did not complete in time"