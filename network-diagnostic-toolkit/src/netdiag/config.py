from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
DEFAULTS={"targets":{"internet_ip":"1.1.1.1","dns_hostname":"cloudflare.com","tcp_targets":[{"host":"cloudflare.com","port":443}]},"thresholds":{"gateway_latency_ms":{"good":5,"warning":20},"internet_latency_ms":{"good":50,"warning":100},"packet_loss_pct":{"good":1,"warning":5},"dns_response_ms":{"good":100,"warning":300}},"execution":{"ping_count":10,"ping_timeout_ms":1000,"tcp_timeout_seconds":3,"traceroute_max_hops":20,"traceroute_timeout_ms":1000},"privacy":{"retention_days":30}}
def deep_merge(base:dict,override:dict)->dict:
    out=dict(base)
    for k,v in override.items(): out[k]=deep_merge(out[k],v) if isinstance(v,dict) and isinstance(out.get(k),dict) else v
    return out
def load_config(path:str|Path|None=None)->dict[str,Any]:
    if path is None: return DEFAULTS
    with open(path,encoding='utf-8') as fh: override=yaml.safe_load(fh) or {}
    return deep_merge(DEFAULTS,override)
