from __future__ import annotations
from .models import CheckResult
from .system import os_name, run_command

def trace_route(host: str, max_hops: int = 20, timeout_ms: int = 1000) -> CheckResult:
    args = ["tracert", "-d", "-h", str(max_hops), "-w", str(timeout_ms), host] if os_name() == "windows" else ["traceroute", "-n", "-m", str(max_hops), "-w", str(max(1, timeout_ms/1000)), host]
    out = run_command(args, timeout=max_hops*max(1, timeout_ms/1000)+10); text=(out.stdout or out.stderr).strip()
    if out.returncode == 127: return CheckResult("traceroute", "warning", "Traceroute utility is not installed", {"host":host}, out.stderr)
    return CheckResult("traceroute", "pass" if out.returncode==0 and text else "warning", f"Traceroute completed for {host}" if text else f"Traceroute produced no output for {host}", {"host":host,"output":"\n".join(text.splitlines()[:60])}, out.stderr or None)
