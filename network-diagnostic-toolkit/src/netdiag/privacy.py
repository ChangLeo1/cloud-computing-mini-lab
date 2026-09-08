from __future__ import annotations
import copy, re
from typing import Any

def redact_ipv4(value: str) -> str:
    parts=value.split('.')
    return '.'.join(parts[:3]+['xxx']) if len(parts)==4 and all(p.isdigit() for p in parts) else value

def redact_mac(value: str) -> str:
    if re.fullmatch(r"(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}", value):
        sep=':' if ':' in value else '-'; parts=re.split(r"[:-]",value); return sep.join(['XX','XX','XX','XX',parts[-2],parts[-1]])
    return value

def redact_string(value: str, key: str|None=None) -> str:
    if (key or '').lower() in {'hostname','username','ssid','domain'}: return 'REDACTED'
    if (key or '').lower()=='mac': return redact_mac(value)
    return re.sub(r"\b(?:10\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3})\.\d{1,3}\b", lambda m:redact_ipv4(m.group(0)), value)

def redact(data: Any, key: str|None=None) -> Any:
    if isinstance(data,dict):
        out={}
        for k,v in data.items():
            kl=str(k).lower()
            if kl=='primary_ip_hint' and isinstance(v,str): out[k]=redact_ipv4(v)
            elif kl=='mac' and isinstance(v,list): out[k]=[redact_mac(str(x)) for x in v]
            elif kl in {'hostname','username','ssid','domain'}: out[k]='REDACTED'
            else: out[k]=redact(v,kl)
        return out
    if isinstance(data,list): return [redact(v,key) for v in data]
    if isinstance(data,str): return redact_ipv4(data) if key in {'address','gateway'} else redact_string(data,key)
    return copy.deepcopy(data)
