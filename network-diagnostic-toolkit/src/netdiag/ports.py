from __future__ import annotations
import socket, time
from .models import CheckResult

def test_tcp_port(host: str, port: int, timeout_seconds: float = 3.0) -> CheckResult:
    start = time.perf_counter()
    try:
        with socket.create_connection((host, int(port)), timeout=timeout_seconds):
            elapsed = (time.perf_counter()-start)*1000
            return CheckResult("tcp_port", "pass", f"TCP {host}:{port} reachable", {"host": host, "port": int(port), "connect_ms": round(elapsed,2)})
    except OSError as exc:
        elapsed = (time.perf_counter()-start)*1000
        return CheckResult("tcp_port", "fail", f"TCP {host}:{port} unreachable", {"host": host, "port": int(port), "connect_ms": round(elapsed,2)}, str(exc))
