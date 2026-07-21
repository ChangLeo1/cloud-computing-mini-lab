import json

import pandas as pd

from src.batch_pipeline import bronze_to_silver
from src.generator import generate_event


def test_bronze_to_silver(tmp_path):
    input_path = tmp_path / "events.jsonl"
    event = generate_event("SOLAR_001")
    input_path.write_text(json.dumps(event) + "\n" + json.dumps(event), encoding="utf-8")
    silver = tmp_path / "silver.parquet"
    quarantine = tmp_path / "bad.jsonl"
    valid, invalid = bronze_to_silver(str(input_path), str(silver), str(quarantine))
    assert valid == 2
    assert invalid == 0
    assert len(pd.read_parquet(silver)) == 1
