# Example incident report

## Incident

Silver processing failed after a source changed `power_kw` from number to string.

## Detection

CloudWatch alarm triggered after the Glue job failed and Gold freshness exceeded the service objective.

## Root cause

The producer deployed an unannounced schema change without contract validation.

## Resolution

The team routed incompatible records to quarantine, updated the parser, replayed affected Bronze partitions and verified Gold aggregates.

## Prevention

Add schema contract tests, producer compatibility checks, deployment gates and an alert on type drift before Silver writes.
