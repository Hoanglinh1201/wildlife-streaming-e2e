--- Create Database
CREATE DATABASE IF NOT EXISTS landing;
CREATE DATABASE IF NOT EXISTS staging;
CREATE DATABASE IF NOT EXISTS foundation;
CREATE DATABASE IF NOT EXISTS mart;

-- Create Roles
CREATE USER ingestor IDENTIFIED WITH plaintext_password BY 'ingestor';
GRANT INSERT ON landing.* TO ingestor;

CREATE USER admin IDENTIFIED WITH plaintext_password BY 'admin';
GRANT ALL ON landing.* TO admin;
GRANT ALL ON staging.* TO admin;
GRANT ALL ON foundation.* TO admin;
GRANT ALL ON mart.* TO admin;

CREATE USER transformer IDENTIFIED WITH plaintext_password BY 'transformer';
GRANT ALL on staging.* TO transformer;
GRANT ALL on foundation.* TO transformer;
GRANT ALL on mart.* TO transformer;
GRANT SELECT ON landing.* TO transformer;

CREATE USER consumer IDENTIFIED WITH plaintext_password BY 'consumer';
GRANT SELECT ON mart.* TO consumer;


-- Create Tables
CREATE TABLE landing.cdc_animals
(
    id UUID DEFAULT generateUUIDv4(),
    `kafka_topic` String,
    `kafka_partition` Int32,
    `kafka_offset` Int64,
    `before` Nullable(String),
    `after` Nullable(String),
    `op` String,
    dwh_created_at DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (kafka_topic, kafka_partition, kafka_offset);

CREATE TABLE landing.cdc_trackers
(
     id UUID DEFAULT generateUUIDv4(),
    `kafka_topic` String,
    `kafka_partition` Int32,
    `kafka_offset` Int64,
    `before` Nullable(String),
    `after` Nullable(String),
    `op` String,
    dwh_created_at DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (kafka_topic, kafka_partition, kafka_offset);

CREATE TABLE landing.cdc_events
(
    id UUID DEFAULT generateUUIDv4(),
    `kafka_topic` String,
    `kafka_partition` Int32,
    `kafka_offset` Int64,
    `before` Nullable(String),
    `after` Nullable(String),
    `op` String,
    dwh_created_at DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (kafka_topic, kafka_partition, kafka_offset);
