from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.validation import validate_event


def bronze_to_silver(input_path: str, silver_path: str, quarantine_path: str) -> tuple[int, int]:
    valid: list[dict] = []
    invalid: list[dict] = []
    for line in Path(input_path).read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        ok, errors = validate_event(event)
        if ok:
            valid.append(event)
        else:
            invalid.append({"event": event, "errors": errors})
    silver = pd.DataFrame(valid)
    if not silver.empty:
        silver = silver.drop_duplicates(subset=["event_id"])
        silver["event_time"] = pd.to_datetime(silver["event_time"], utc=True)
        silver["event_date"] = silver["event_time"].dt.date.astype(str)
        Path(silver_path).parent.mkdir(parents=True, exist_ok=True)
        silver.to_parquet(silver_path, index=False)
    Path(quarantine_path).parent.mkdir(parents=True, exist_ok=True)
    Path(quarantine_path).write_text("\n".join(json.dumps(x) for x in invalid), encoding="utf-8")
    return len(valid), len(invalid)
