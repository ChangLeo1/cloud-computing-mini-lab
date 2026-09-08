from __future__ import annotations
import re
from .models import CheckResult
from .system import os_name, run_command

def parse_ping_output(text: str):
    loss = avg = minimum = maximum = None
    m = re.search(r"\((\d+(?:\.\d+)?)%\s*loss\)", text, re.I) or re.search(r"(\d+(?:\.\d+)?)%\s*packet loss", text, re.I)
    if m: loss = float(m.group(1))
    m = re.search(r"Minimum\s*=\s*(\d+)ms,\s*Maximum\s*=\s*(\d+)ms,\s*Average\s*=\s*(\d+)ms", text, re.I)
    if m: minimum, maximum, avg = map(float, m.groups())
    else:
        m = re.search(r"(?:rtt|round-trip).*?=\s*([\d.]+)/([\d.]+)/([\d.]+)/", text, re.I)
        if m: minimum, avg, maximum = map(float, m.groups())
    return loss, minimum, avg, maximum

def ping_host(host: str, count: int = 10, timeout_ms: int = 1000, latency_good_ms: float = 50, latency_warning_ms: float = 100,
              loss_good_pct: float = 1, loss_warning_pct: float = 5, name: str = "ping") -> CheckResult:
    if os_name() == "windows":
        args = ["ping", "-n", str(count), "-w", str(timeout_ms), host]; timeout = max(5, count * timeout_ms / 1000 + 5)
    else:
        args = ["ping", "-c", str(count), "-W", str(max(1, int(timeout_ms / 1000))), host]; timeout = max(5, count * max(1, timeout_ms / 1000) + 5)
    out = run_command(args, timeout=timeout); combined = f"{out.stdout}\n{out.stderr}".strip()
    loss, minimum, avg, maximum = parse_ping_output(combined)
    if loss is None:
        return CheckResult(name, "error" if out.returncode not in (0,1) else "fail", f"Unable to parse ping result for {host}", {"host": host, "raw_excerpt": combined[-1200:]}, out.stderr or None)
    status = "fail" if loss > loss_warning_pct or (avg is not None and avg > latency_warning_ms) or loss >= 100 else "warning" if loss >= loss_good_pct or (avg is not None and avg >= latency_good_ms) else "pass"
    summary = f"{host}: {loss:.1f}% loss" + (f", {avg:.1f} ms avg" if avg is not None else "")
    return CheckResult(name, status, summary, {"host": host, "packet_loss_pct": loss, "min_ms": minimum, "avg_ms": avg, "max_ms": maximum, "returncode": out.returncode})
