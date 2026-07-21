from __future__ import annotations

from datetime import datetime

REQUIRED_FIELDS = {
    "event_id",
    "device_id",
    "device_type",
    "event_time",
    "power_kw",
    "voltage",
    "status",
    "region",
}
VALID_STATUS = {"online", "offline", "fault"}


def validate_event(event: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = REQUIRED_FIELDS.difference(event)
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    try:
        datetime.fromisoformat(str(event.get("event_time", "")).replace("Z", "+00:00"))
    except ValueError:
        errors.append("invalid event_time")
    if not isinstance(event.get("power_kw"), (int, float)) or event.get("power_kw", -1) < 0:
        errors.append("power_kw must be non negative")
    if event.get("status") not in VALID_STATUS:
        errors.append("invalid status")
    return not errors, errors
