# Architecture

## Batch path

External files and APIs land in S3 Bronze. Lambda validates file shape and writes invalid records to quarantine. Glue Crawlers register metadata. Glue or Spark transforms raw data into Parquet Silver tables. Athena and Databricks query Gold products.

## Streaming path

Python producers publish telemetry to Kafka locally or MSK in AWS. Spark Structured Streaming applies event time watermarks, deduplication and five minute windows. Delta Lake checkpoints provide restartability.

## AWS service roles

S3 provides durable object storage and lifecycle management.

Glue provides metadata, crawling and managed Spark ETL.

Athena provides serverless SQL over S3.

Lambda provides event driven validation and orchestration.

CloudWatch provides logs, metrics and alarms.

EMR is the option for greater control over large Spark clusters.

Fargate runs containerised ingestion jobs that exceed Lambda limits.

MSK provides managed Kafka for streaming workloads.

## NoSQL pattern

DynamoDB table design uses `device_id` as the partition key and `event_time` as the sort key. A global secondary index on `status` supports operational lookup, while time range queries remain device scoped to avoid scans.
