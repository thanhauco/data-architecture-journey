import dlt
from pyspark.sql.functions import *

@dlt.table(
    comment="Raw data from users source",
    table_properties={"quality": "bronze"}
)
def users_bronze():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load(f"/mnt/landing/users")
    )

@dlt.table(
    comment="Cleaned users data",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
def users_silver():
    return (
        dlt.read(f"users_bronze")
        .select("id", "timestamp", "payload.*")
        .withColumn("processed_at", current_timestamp())
    )

@dlt.table(
    comment="Aggregated users metrics",
    table_properties={"quality": "gold"}
)
def users_daily_agg():
    return (
        dlt.read(f"users_silver")
        .groupBy(window("timestamp", "1 day"))
        .count()
    )
