from __future__ import annotations
import socket
from typing import Any
import psutil
from .models import CheckResult

def _primary_ip_hint() -> str | None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("1.1.1.1", 80))
        return sock.getsockname()[0]
    except OSError:
        return None
    finally:
        sock.close()

def collect_adapters() -> CheckResult:
    try:
        addrs = psutil.net_if_addrs(); stats = psutil.net_if_stats(); primary_hint = _primary_ip_hint()
        items: list[dict[str, Any]] = []
        for name, entries in addrs.items():
            ipv4, mac = [], []
            for entry in entries:
                if entry.family == socket.AF_INET:
                    ipv4.append({"address": entry.address, "netmask": entry.netmask})
                elif getattr(psutil, "AF_LINK", None) == entry.family:
                    mac.append(entry.address)
            if not ipv4 and not mac: continue
            stat = stats.get(name)
            items.append({"name": name, "is_up": bool(stat.isup) if stat else None, "speed_mbps": stat.speed if stat else None,
                          "ipv4": ipv4, "mac": mac, "primary": any(x.get("address") == primary_hint for x in ipv4)})
        up = [x for x in items if x.get("is_up") and x.get("ipv4")]
        return CheckResult("adapters", "pass" if up else "fail",
                           f"{len(up)} active IPv4 adapter(s) detected" if up else "No active IPv4 adapter detected",
                           {"adapters": items, "primary_ip_hint": primary_hint})
    except Exception as exc:
        return CheckResult("adapters", "error", "Adapter inspection failed", error=str(exc))
