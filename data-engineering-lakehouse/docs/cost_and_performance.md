# Cost and performance

Store raw JSON only in Bronze and convert Silver and Gold to Parquet or Delta.

Partition by event date and use device type only when cardinality and query patterns justify it.

Use predicate pushdown, partition pruning and column selection in Athena.

Compact small files and avoid excessive Spark repartitioning.

Use Lambda for short event driven tasks, Fargate for container workloads, Glue for managed Spark and EMR when cluster control is required.

Configure AWS Budgets before deployment and destroy experimental resources after validation.
