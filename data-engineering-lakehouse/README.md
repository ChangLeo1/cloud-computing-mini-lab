# Real Time Energy Data Lakehouse

Portfolio project demonstrating an end to end data platform for distributed energy telemetry.

## Coverage

AWS S3, Glue, Athena, Lambda, CloudWatch, EMR, Fargate and MSK patterns

Advanced SQL across PostgreSQL and DynamoDB design examples

Python, PySpark and Spark Structured Streaming

Databricks medallion architecture and Delta Lake

GitHub Actions CI, testing, deployment practices and infrastructure as code

Data Vault, star schema, serverless processing, monitoring and incident response

## Architecture

Python generator to Kafka or MSK to Spark Structured Streaming to S3 Bronze to Glue or Databricks Silver to Delta Gold to Athena and dashboards.

## Quick start

```bash
cd data-engineering-lakehouse
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.generator --records 100 --output data/sample/events.jsonl
pytest
```

Run local streaming services with:

```bash
docker compose up --build
```

## Repository map

`src` contains generation, validation, batch and streaming logic.

`sql` contains relational modelling, advanced analytics, Data Vault and Athena queries.

`infrastructure` contains Terraform examples for S3, Glue, Lambda, CloudWatch and serverless deployment.

`docs` contains architecture, data dictionary, operations, cost and incident documentation.

## Lakehouse layers

Bronze stores immutable raw events with ingestion metadata.

Silver standardises types, removes duplicates, validates quality and enriches device metadata.

Gold provides energy balance, device reliability, fault and communication availability metrics.

## Production engineering practices

The project includes structured logging, quarantine handling, tests, CI, data quality checks, partitioning, monitoring metrics, alarms, failure scenarios and recovery documentation.

## Important note

AWS and Databricks resources are templates. Review variable values and estimated cost before deployment.