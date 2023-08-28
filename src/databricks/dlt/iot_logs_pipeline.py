import dlt
from pyspark.sql.functions import *

@dlt.table(
    comment="Raw data from iot_logs source",
    table_properties={"quality": "bronze"}
)
def iot_logs_bronze():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load(f"/mnt/landing/iot_logs")
    )

@dlt.table(
    comment="Cleaned iot_logs data",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
def iot_logs_silver():
    return (
        dlt.read(f"iot_logs_bronze")
        .select("id", "timestamp", "payload.*")
        .withColumn("processed_at", current_timestamp())
    )

@dlt.table(
    comment="Aggregated iot_logs metrics",
    table_properties={"quality": "gold"}
)
def iot_logs_daily_agg():
    return (
        dlt.read(f"iot_logs_silver")
        .groupBy(window("timestamp", "1 day"))
        .count()
    )
