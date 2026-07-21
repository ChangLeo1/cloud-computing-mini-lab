WITH ordered AS (
    SELECT d.device_id, f.event_time, f.power_kw,
           LAG(f.power_kw) OVER (PARTITION BY d.device_id ORDER BY f.event_time) AS previous_power
    FROM fact_device_reading f JOIN dim_device d USING (device_key)
)
SELECT *, power_kw - previous_power AS power_change
FROM ordered
WHERE previous_power IS NOT NULL AND power_kw < previous_power * 0.5;

SELECT d.device_type, DATE_TRUNC('hour', f.event_time) AS event_hour,
       AVG(f.power_kw) AS average_power,
       AVG(CASE WHEN f.status = 'online' THEN 1.0 ELSE 0.0 END) AS availability_rate
FROM fact_device_reading f JOIN dim_device d USING (device_key)
GROUP BY d.device_type, DATE_TRUNC('hour', f.event_time);

WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY device_key, event_time ORDER BY ingestion_time DESC) AS rn
    FROM fact_device_reading
)
SELECT * FROM ranked WHERE rn = 1;
