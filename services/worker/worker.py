import json
import os
import random
import time
from datetime import datetime

import redis

LEVELS = ["debug", "info", "warn", "error"]


def normalize_level(value: str) -> str:
    lower = (value or "info").lower()
    return lower if lower in LEVELS else "info"


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
JOB_QUEUE_KEY = os.getenv("JOB_QUEUE_KEY", "cloud:jobs")
JOB_HASH_PREFIX = os.getenv("JOB_HASH_PREFIX", "cloud:job:")
LOG_LEVEL = normalize_level(os.getenv("LOG_LEVEL", "info"))


def log(level: str, message: str, **extras):
    normalized = normalize_level(level)
    if LEVELS.index(normalized) < LEVELS.index(LOG_LEVEL):
        return
    payload = {"level": normalized, "message": message, **extras, "timestamp": datetime.utcnow().isoformat()}
    print(json.dumps(payload))


def summarize_text(text: str) -> dict:
    # Simulate CPU-bound work with a deterministic transformation
    time.sleep(random.uniform(0.5, 1.5))
    words = text.split()
    summary = " ".join(words[:20]) + ("..." if len(words) > 20 else "")
    return {
        "word_count": len(words),
        "character_count": len(text),
        "uppercase_letters": sum(1 for char in text if char.isupper()),
        "summary": summary,
    }


def process_job(job_payload: dict) -> dict:
    text = job_payload.get("text", "")
    if not text:
        raise ValueError("Payload missing 'text'")
    return summarize_text(text)


def run_worker():
    client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    log("info", "Worker connected to Redis", redis_url=REDIS_URL)
    while True:
        try:
            queue, raw_job = client.blpop(JOB_QUEUE_KEY)
            job_data = json.loads(raw_job)
            job_id = job_data.get("jobId")
            payload = job_data.get("payload", {})
            job_key = f"{JOB_HASH_PREFIX}{job_id}"

            log("info", "Job picked up", job_id=job_id, queue=queue)
            now = datetime.utcnow().isoformat()
            client.hset(job_key, mapping={"status": "running", "startedAt": now})

            try:
                result = process_job(payload)
                finished = datetime.utcnow().isoformat()
                client.hset(
                    job_key,
                    mapping={
                        "status": "completed",
                        "completedAt": finished,
                        "result": json.dumps(result),
                    },
                )
                log("info", "Job completed", job_id=job_id)
            except Exception as job_error:
                client.hset(
                    job_key,
                    mapping={
                        "status": "failed",
                        "completedAt": datetime.utcnow().isoformat(),
                        "error": str(job_error),
                    },
                )
                log("error", "Job failed", job_id=job_id, error=str(job_error))
        except redis.exceptions.ConnectionError as conn_error:
            log("error", "Redis connection lost, retrying", error=str(conn_error))
            time.sleep(3)
            client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        except KeyboardInterrupt:
            log("warn", "Worker interrupted, shutting down gracefully")
            break


if __name__ == "__main__":
    run_worker()

