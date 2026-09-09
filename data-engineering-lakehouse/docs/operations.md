# Operations runbook

## Monitored signals

Pipeline completion, input volume, invalid record count, processing latency, Lambda errors, Glue failures, Kafka consumer lag, checkpoint age and estimated daily scan cost.

## Failure exercises

Remove required fields, send negative power, duplicate event identifiers, delay events by fifteen minutes, pause the producer, change schema, corrupt JSON and delete a streaming checkpoint in a non production environment.

## Response sequence

Confirm impact, stop harmful writes, inspect CloudWatch logs, isolate invalid data, restore from Bronze, replay idempotently, verify row counts and publish an incident summary.

## Reliability controls

Immutable Bronze storage, deterministic event identifiers, quarantine prefixes, checkpoints, retries with backoff, dead letter handling, schema contracts, automated tests and least privilege IAM.
