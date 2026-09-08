from __future__ import annotations
import json, re, socket, time
from .models import CheckResult
from .system import os_name, run_command

def dns_servers() -> list[str]:
    servers: list[str] = []
    if os_name() == "windows":
        script = "Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object {$_.ServerAddresses.Count -gt 0} | Select-Object -ExpandProperty ServerAddresses | ConvertTo-Json -Compress"
        out = run_command(["powershell", "-NoProfile", "-Command", script])
        if out.returncode == 0 and out.stdout:
            try:
                parsed = json.loads(out.stdout); servers = [parsed] if isinstance(parsed, str) else [str(x) for x in parsed] if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                servers = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", out.stdout)
    else:
        try:
            text = open("/etc/resolv.conf", encoding="utf-8", errors="ignore").read(); servers = re.findall(r"^nameserver\s+(\S+)", text, flags=re.MULTILINE)
        except OSError: pass
    return list(dict.fromkeys(servers))

def resolve_hostname(hostname: str, good_ms: float = 100, warning_ms: float = 300) -> CheckResult:
    start = time.perf_counter()
    try:
        infos = socket.getaddrinfo(hostname, None); elapsed = (time.perf_counter() - start) * 1000
        ips = sorted({item[4][0] for item in infos})
        status = "pass" if elapsed < good_ms else "warning" if elapsed <= warning_ms else "fail"
        return CheckResult("dns_resolution", status, f"Resolved {hostname} in {elapsed:.1f} ms", {"hostname": hostname, "resolved_addresses": ips, "response_ms": round(elapsed, 2), "dns_servers": dns_servers()})
    except socket.gaierror as exc:
        elapsed = (time.perf_counter() - start) * 1000
        return CheckResult("dns_resolution", "fail", f"DNS resolution failed for {hostname}", {"hostname": hostname, "response_ms": round(elapsed, 2), "dns_servers": dns_servers()}, str(exc))
