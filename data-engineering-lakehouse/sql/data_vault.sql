CREATE TABLE hub_device (
    device_hk TEXT PRIMARY KEY,
    device_id TEXT UNIQUE NOT NULL,
    load_dts TIMESTAMPTZ NOT NULL,
    record_source TEXT NOT NULL
);

CREATE TABLE hub_location (
    location_hk TEXT PRIMARY KEY,
    location_code TEXT UNIQUE NOT NULL,
    load_dts TIMESTAMPTZ NOT NULL,
    record_source TEXT NOT NULL
);

CREATE TABLE link_device_location (
    device_location_hk TEXT PRIMARY KEY,
    device_hk TEXT NOT NULL REFERENCES hub_device(device_hk),
    location_hk TEXT NOT NULL REFERENCES hub_location(location_hk),
    load_dts TIMESTAMPTZ NOT NULL,
    record_source TEXT NOT NULL
);

CREATE TABLE sat_device_status (
    device_hk TEXT NOT NULL REFERENCES hub_device(device_hk),
    load_dts TIMESTAMPTZ NOT NULL,
    status TEXT NOT NULL,
    power_kw NUMERIC(12,2),
    hashdiff TEXT NOT NULL,
    record_source TEXT NOT NULL,
    PRIMARY KEY (device_hk, load_dts)
);
