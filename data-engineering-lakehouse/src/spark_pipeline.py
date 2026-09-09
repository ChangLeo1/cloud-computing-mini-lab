from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, StringType, StructField, StructType, TimestampType

SCHEMA = StructType([
    StructField("event_id", StringType(), False),
    StructField("device_id", StringType(), False),
    StructField("device_type", StringType(), False),
    StructField("event_time", TimestampType(), False),
    StructField("power_kw", DoubleType(), False),
    StructField("voltage", DoubleType(), True),
    StructField("status", StringType(), False),
    StructField("region", StringType(), False),
])


def transform_silver(df: DataFrame) -> DataFrame:
    window_spec = Window.partitionBy("device_id").orderBy("event_time").rowsBetween(-2, 0)
    return (
        df.dropDuplicates(["event_id"])
        .filter(F.col("power_kw") >= 0)
        .withColumn("event_date", F.to_date("event_time"))
        .withColumn("rolling_power_kw", F.avg("power_kw").over(window_spec))
        .withColumn("is_available", F.when(F.col("status") == "online", 1).otherwise(0))
    )


def build_gold(df: DataFrame) -> DataFrame:
    return df.groupBy("device_id", "device_type", "event_date").agg(
        F.avg("power_kw").alias("average_power_kw"),
        F.max("power_kw").alias("peak_power_kw"),
        F.avg("is_available").alias("availability_rate"),
        F.sum(F.when(F.col("status") == "fault", 1).otherwise(0)).alias("fault_count"),
    )


def spark() -> SparkSession:
    return SparkSession.builder.appName("energy-lakehouse").getOrCreate()
