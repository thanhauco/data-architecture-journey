import dlt
from pyspark.sql.functions import *

@dlt.table(
    comment="Raw data from events source",
    table_properties={"quality": "bronze"}
)
def events_bronze():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load(f"/mnt/landing/events")
    )

@dlt.table(
    comment="Cleaned events data",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
def events_silver():
    return (
        dlt.read(f"events_bronze")
        .select("id", "timestamp", "payload.*")
        .withColumn("processed_at", current_timestamp())
    )

@dlt.table(
    comment="Aggregated events metrics",
    table_properties={"quality": "gold"}
)
def events_daily_agg():
    return (
        dlt.read(f"events_silver")
        .groupBy(window("timestamp", "1 day"))
        .count()
    )
