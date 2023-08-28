import dlt
from pyspark.sql.functions import *

@dlt.table(
    comment="Raw data from orders source",
    table_properties={"quality": "bronze"}
)
def orders_bronze():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load(f"/mnt/landing/orders")
    )

@dlt.table(
    comment="Cleaned orders data",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
def orders_silver():
    return (
        dlt.read(f"orders_bronze")
        .select("id", "timestamp", "payload.*")
        .withColumn("processed_at", current_timestamp())
    )

@dlt.table(
    comment="Aggregated orders metrics",
    table_properties={"quality": "gold"}
)
def orders_daily_agg():
    return (
        dlt.read(f"orders_silver")
        .groupBy(window("timestamp", "1 day"))
        .count()
    )
