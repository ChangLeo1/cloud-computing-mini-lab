CREATE TABLE dim_device (
    device_key BIGSERIAL PRIMARY KEY,
    device_id TEXT UNIQUE NOT NULL,
    device_type TEXT NOT NULL,
    region TEXT NOT NULL,
    commissioned_at TIMESTAMPTZ,
    valid_from TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_to TIMESTAMPTZ,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE fact_device_reading (
    event_id UUID PRIMARY KEY,
    device_key BIGINT NOT NULL REFERENCES dim_device(device_key),
    event_time TIMESTAMPTZ NOT NULL,
    power_kw NUMERIC(12,2) NOT NULL,
    voltage NUMERIC(8,2),
    status TEXT NOT NULL,
    ingestion_time TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_fact_device_time ON fact_device_reading(device_key, event_time DESC);
CREATE INDEX idx_fact_status_time ON fact_device_reading(status, event_time DESC);
