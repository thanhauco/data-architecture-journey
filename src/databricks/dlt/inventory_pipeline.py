import dlt
from pyspark.sql.functions import *

@dlt.table(
    comment="Raw data from inventory source",
    table_properties={"quality": "bronze"}
)
def inventory_bronze():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load(f"/mnt/landing/inventory")
    )

@dlt.table(
    comment="Cleaned inventory data",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
def inventory_silver():
    return (
        dlt.read(f"inventory_bronze")
        .select("id", "timestamp", "payload.*")
        .withColumn("processed_at", current_timestamp())
    )

@dlt.table(
    comment="Aggregated inventory metrics",
    table_properties={"quality": "gold"}
)
def inventory_daily_agg():
    return (
        dlt.read(f"inventory_silver")
        .groupBy(window("timestamp", "1 day"))
        .count()
    )
