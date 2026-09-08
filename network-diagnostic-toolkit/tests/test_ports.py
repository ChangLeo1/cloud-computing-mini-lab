import netdiag.ports as mod
class DummySocket:
    def __enter__(self): return self
    def __exit__(self,*a): pass

def test_tcp_pass(monkeypatch):
    monkeypatch.setattr(mod.socket,'create_connection',lambda *a,**k:DummySocket())
    assert mod.test_tcp_port('example.com',443).status=='pass'
def test_tcp_fail(monkeypatch):
    def boom(*a,**k): raise OSError('refused')
    monkeypatch.setattr(mod.socket,'create_connection',boom)
    r=mod.test_tcp_port('example.com',81); assert r.status=='fail' and 'refused' in r.error
