import netdiag.security as sec
import netdiag.repair as rep

def test_security_non_windows(monkeypatch):
    monkeypatch.setattr(sec,'os_name',lambda:'linux'); assert sec.local_security_posture().status=='warning'
def test_repair_rejects_nonwindows(monkeypatch):
    monkeypatch.setattr(rep,'os_name',lambda:'linux'); ok,msg,snap=rep.perform('flush-dns'); assert not ok and snap is None and 'Windows' in msg
def test_repair_unknown(monkeypatch):
    ok,msg,snap=rep.perform('not-real'); assert not ok and snap is None
