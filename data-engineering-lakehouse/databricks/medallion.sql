CREATE TABLE IF NOT EXISTS bronze.device_events
USING DELTA
LOCATION '${bronze_path}';

CREATE OR REPLACE TABLE silver.device_readings AS
SELECT DISTINCT event_id, device_id, device_type,
       CAST(event_time AS TIMESTAMP) event_time,
       CAST(power_kw AS DOUBLE) power_kw,
       CAST(voltage AS DOUBLE) voltage,
       status, region, current_timestamp() processing_time
FROM bronze.device_events
WHERE power_kw >= 0 AND status IN ('online', 'offline', 'fault');

MERGE INTO silver.device_readings target
USING updates source
ON target.event_id = source.event_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

CREATE OR REPLACE TABLE gold.device_reliability AS
SELECT device_id, device_type, date(event_time) event_date,
       avg(power_kw) average_power_kw,
       avg(CASE WHEN status = 'online' THEN 1.0 ELSE 0.0 END) availability_rate,
       sum(CASE WHEN status = 'fault' THEN 1 ELSE 0 END) fault_count
FROM silver.device_readings
GROUP BY device_id, device_type, date(event_time);

DESCRIBE HISTORY silver.device_readings;
