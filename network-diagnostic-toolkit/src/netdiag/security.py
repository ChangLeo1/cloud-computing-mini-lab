from __future__ import annotations
import json
from .models import CheckResult
from .system import os_name, run_command

def _windows_firewall() -> dict:
    out = run_command(["powershell","-NoProfile","-Command","Get-NetFirewallProfile | Select-Object Name,Enabled | ConvertTo-Json -Compress"])
    if out.returncode != 0 or not out.stdout: return {"status":"unknown","details":out.stderr or "Unable to query firewall"}
    try:
        profiles=json.loads(out.stdout); profiles=[profiles] if isinstance(profiles,dict) else profiles
        return {"status":"enabled" if all(bool(p.get('Enabled')) for p in profiles) else "attention","profiles":profiles}
    except Exception as exc: return {"status":"unknown","details":str(exc)}

def _windows_update_service() -> dict:
    out=run_command(["powershell","-NoProfile","-Command","Get-Service -Name wuauserv | Select-Object Status,StartType | ConvertTo-Json -Compress"])
    if out.returncode != 0 or not out.stdout: return {"status":"unknown","details":out.stderr or "Unable to query Windows Update service"}
    try: return {"status":"configured","details":json.loads(out.stdout)}
    except Exception as exc: return {"status":"unknown","details":str(exc)}

def local_security_posture() -> CheckResult:
    if os_name() != "windows": return CheckResult("security_posture","warning","Security posture checks are Windows-focused",{"platform_supported":False,"mfa":"manual verification required","backup":"manual verification required"})
    fw=_windows_firewall(); wu=_windows_update_service(); status="pass" if fw.get("status")=="enabled" else "warning"
    return CheckResult("security_posture",status,"Local security posture collected (not an Essential Eight certification)",{"platform_supported":True,"windows_firewall":fw,"windows_update_service":wu,"backup":"manual verification required","mfa":"manual verification required","note":"Essential Eight-aligned recommendations only; this is not a compliance certification."})
