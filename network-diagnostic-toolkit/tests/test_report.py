import json
from pathlib import Path
from netdiag.models import CheckResult, Diagnosis
from netdiag.report import build_report, write_all

def test_report_redaction(tmp_path:Path,monkeypatch):
    monkeypatch.setattr('netdiag.report.socket.gethostname',lambda:'LEO-PC')
    report=build_report([CheckResult('x','pass','gateway 192.168.1.1',{'address':'192.168.1.5'})],Diagnosis('HEALTHY','info','OK','Fine',[]),{'privacy':{'retention_days':30}},True)
    assert report['device']['hostname']=='REDACTED' and report['results'][0]['data']['address'].endswith('xxx')
def test_write_all(tmp_path:Path):
    report={'generated_at':'2026-09-08T12:00:00+10:00','device':{'hostname':'PC','os':'Windows'},'results':[{'name':'dns','status':'pass','summary':'ok'}],'diagnosis':{'title':'Healthy','code':'HEALTHY','explanation':'ok','recommendations':['none']},'disclaimer':'test'}
    paths=write_all(report,tmp_path); assert set(paths)=={'json','text','html','audit_log'}
    assert all(Path(p).exists() for p in paths.values())
    assert json.loads(Path(paths['json']).read_text())['diagnosis']['code']=='HEALTHY'
