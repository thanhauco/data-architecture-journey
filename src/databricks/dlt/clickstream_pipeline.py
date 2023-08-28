import dlt
from pyspark.sql.functions import *

@dlt.table(
    comment="Raw data from clickstream source",
    table_properties={"quality": "bronze"}
)
def clickstream_bronze():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load(f"/mnt/landing/clickstream")
    )

@dlt.table(
    comment="Cleaned clickstream data",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
def clickstream_silver():
    return (
        dlt.read(f"clickstream_bronze")
        .select("id", "timestamp", "payload.*")
        .withColumn("processed_at", current_timestamp())
    )

@dlt.table(
    comment="Aggregated clickstream metrics",
    table_properties={"quality": "gold"}
)
def clickstream_daily_agg():
    return (
        dlt.read(f"clickstream_silver")
        .groupBy(window("timestamp", "1 day"))
        .count()
    )
