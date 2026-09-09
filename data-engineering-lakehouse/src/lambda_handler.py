from __future__ import annotations

import json
import os

import boto3

from src.validation import validate_event

s3 = boto3.client("s3")


def handler(event, context):
    destination = os.environ.get("QUARANTINE_PREFIX", "quarantine/")
    results = []
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        body = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8")
        bad = []
        for line in body.splitlines():
            item = json.loads(line)
            ok, errors = validate_event(item)
            if not ok:
                bad.append({"event": item, "errors": errors})
        if bad:
            qkey = f"{destination}{key.replace('/', '_')}"
            s3.put_object(Bucket=bucket, Key=qkey, Body="\n".join(json.dumps(x) for x in bad))
        results.append({"key": key, "invalid_records": len(bad)})
    return {"statusCode": 200, "body": json.dumps(results)}
