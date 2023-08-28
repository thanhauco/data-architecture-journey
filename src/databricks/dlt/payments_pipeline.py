import dlt
from pyspark.sql.functions import *

@dlt.table(
    comment="Raw data from payments source",
    table_properties={"quality": "bronze"}
)
def payments_bronze():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load(f"/mnt/landing/payments")
    )

@dlt.table(
    comment="Cleaned payments data",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
def payments_silver():
    return (
        dlt.read(f"payments_bronze")
        .select("id", "timestamp", "payload.*")
        .withColumn("processed_at", current_timestamp())
    )

@dlt.table(
    comment="Aggregated payments metrics",
    table_properties={"quality": "gold"}
)
def payments_daily_agg():
    return (
        dlt.read(f"payments_silver")
        .groupBy(window("timestamp", "1 day"))
        .count()
    )
