from __future__ import annotations
import ipaddress, re
from .models import CheckResult
from .system import os_name, run_command

def _gateway_windows() -> str | None:
    script = "(Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Where-Object {$_.NextHop -ne '0.0.0.0'} | Sort-Object RouteMetric | Select-Object -First 1 -ExpandProperty NextHop)"
    out = run_command(["powershell", "-NoProfile", "-Command", script])
    return out.stdout.strip() if out.returncode == 0 and out.stdout.strip() else None

def _gateway_linux() -> str | None:
    out = run_command(["ip", "route", "show", "default"])
    if out.returncode != 0: return None
    m = re.search(r"default\s+via\s+(\S+)", out.stdout); return m.group(1) if m else None

def _gateway_macos() -> str | None:
    out = run_command(["route", "-n", "get", "default"])
    if out.returncode != 0: return None
    m = re.search(r"gateway:\s+(\S+)", out.stdout); return m.group(1) if m else None

def default_gateway() -> str | None:
    name = os_name()
    return _gateway_windows() if name == "windows" else _gateway_linux() if name == "linux" else _gateway_macos() if name == "darwin" else None

def assess_ip_configuration(adapter_result: CheckResult) -> CheckResult:
    adapters = adapter_result.data.get("adapters", []) if adapter_result.data else []
    active = [a for a in adapters if a.get("is_up") and a.get("ipv4")]
    primary = next((a for a in active if a.get("primary")), active[0] if active else None)
    if not primary:
        return CheckResult("ip_configuration", "fail", "No active IPv4 configuration", {"gateway": default_gateway()})
    addresses, valid_non_apipa = [], False
    for entry in primary.get("ipv4", []):
        addr = entry.get("address")
        try:
            ip = ipaddress.ip_address(addr); valid = not ip.is_loopback and not ip.is_unspecified
            apipa = ip.version == 4 and ip in ipaddress.ip_network("169.254.0.0/16")
            valid_non_apipa = valid_non_apipa or (valid and not apipa)
        except ValueError:
            valid, apipa = False, False
        addresses.append({**entry, "valid": valid, "apipa": apipa})
    gw = default_gateway()
    status = "pass" if valid_non_apipa and gw else "warning" if valid_non_apipa else "fail"
    summary = "IPv4 configuration and default gateway detected" if status == "pass" else "IPv4 address detected but no default gateway found" if valid_non_apipa else "IPv4 address is missing or APIPA/invalid"
    return CheckResult("ip_configuration", status, summary, {"adapter": primary.get("name"), "addresses": addresses, "gateway": gw})
