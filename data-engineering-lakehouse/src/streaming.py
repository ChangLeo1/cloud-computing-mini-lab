from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def streaming_metrics(events: DataFrame) -> DataFrame:
    return (
        events.withWatermark("event_time", "10 minutes")
        .dropDuplicates(["event_id"])
        .groupBy(F.window("event_time", "5 minutes"), "device_type")
        .agg(
            F.avg("power_kw").alias("average_power_kw"),
            F.max("power_kw").alias("maximum_power_kw"),
            F.count("*").alias("event_count"),
        )
    )


def write_delta_stream(df: DataFrame, path: str, checkpoint: str):
    return (
        df.writeStream.format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint)
        .start(path)
    )
