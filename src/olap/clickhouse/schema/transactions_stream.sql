-- ClickHouse Table Definition: transactions_stream
CREATE TABLE transactions_stream (
    event_timestamp DateTime,
    user_id UInt64,
    event_type String,
    device_id String,
    platform Enum8('web' = 1, 'ios' = 2, 'android' = 3),
    revenue Decimal(18, 4)
) ENGINE = MergeTree
PARTITION BY toYYYYMM(event_timestamp)
ORDER BY (event_timestamp, user_id, event_type)
TTL event_timestamp + INTERVAL 1 YEAR
SETTINGS index_granularity = 8192;
