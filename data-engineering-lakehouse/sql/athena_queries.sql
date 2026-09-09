SELECT device_type, date_trunc('hour', event_time) event_hour,
       avg(power_kw) average_power_kw, max(power_kw) peak_power_kw
FROM energy_silver
WHERE event_date = current_date
GROUP BY device_type, date_trunc('hour', event_time);

CREATE TABLE energy_gold
WITH (
  format = 'PARQUET',
  external_location = 's3://replace-me/gold/energy_metrics/',
  partitioned_by = ARRAY['event_date']
) AS
SELECT device_id, device_type, avg(power_kw) average_power_kw,
       avg(CASE WHEN status = 'online' THEN 1.0 ELSE 0.0 END) availability_rate,
       event_date
FROM energy_silver
GROUP BY device_id, device_type, event_date;
