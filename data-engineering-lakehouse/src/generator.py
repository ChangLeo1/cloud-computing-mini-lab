from __future__ import annotations

import argparse
import json
import random
import uuid
from datetime import datetime, timezone
from pathlib import Path

DEVICE_TYPES = ["solar", "wind", "battery", "diesel", "fuel_cell"]


def generate_event(device_id: str | None = None) -> dict:
    device_type = random.choice(DEVICE_TYPES)
    return {
        "event_id": str(uuid.uuid4()),
        "device_id": device_id or f"{device_type.upper()}_{random.randint(1, 20):03d}",
        "device_type": device_type,
        "event_time": datetime.now(timezone.utc).isoformat(),
        "power_kw": round(random.uniform(0, 500), 2),
        "voltage": round(random.uniform(380, 420), 2),
        "status": random.choices(["online", "offline", "fault"], [0.94, 0.04, 0.02])[0],
        "region": random.choice(["melbourne_east", "melbourne_west", "regional_vic"]),
    }


def write_events(records: int, output: str) -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for _ in range(records):
            handle.write(json.dumps(generate_event()) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=int, default=100)
    parser.add_argument("--output", default="data/sample/events.jsonl")
    args = parser.parse_args()
    write_events(args.records, args.output)


if __name__ == "__main__":
    main()
