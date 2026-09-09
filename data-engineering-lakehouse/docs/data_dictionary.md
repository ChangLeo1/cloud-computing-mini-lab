# Data dictionary

| Field | Type | Description |
| --- | --- | --- |
| event_id | string UUID | Idempotency and deduplication key |
| device_id | string | Stable business identifier |
| device_type | string | solar, wind, battery, diesel or fuel cell |
| event_time | timestamp UTC | Time generated at source |
| power_kw | double | Active power |
| voltage | double | Device voltage |
| status | string | online, offline or fault |
| region | string | Operational area |
| ingestion_time | timestamp UTC | Platform arrival time |
| processing_time | timestamp UTC | Silver transformation time |
