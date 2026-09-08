from __future__ import annotations
import platform, subprocess
from dataclasses import dataclass

@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str

def os_name() -> str:
    return platform.system().lower()

def run_command(args: list[str], timeout: float = 15.0) -> CommandResult:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout, shell=False, errors="replace")
        return CommandResult(proc.returncode, proc.stdout.strip(), proc.stderr.strip())
    except FileNotFoundError as exc:
        return CommandResult(127, "", str(exc))
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
        return CommandResult(124, stdout.strip(), (stderr or "command timed out").strip())
