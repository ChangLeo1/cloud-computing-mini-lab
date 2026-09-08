from netdiag.models import CheckResult
import netdiag.ip_config as mod

def test_valid_ip_with_gateway(monkeypatch):
    monkeypatch.setattr(mod,'default_gateway',lambda:'192.168.1.1')
    a=CheckResult('adapters','pass','x',{'adapters':[{'name':'Wi-Fi','is_up':True,'primary':True,'ipv4':[{'address':'192.168.1.50','netmask':'255.255.255.0'}]}]})
    r=mod.assess_ip_configuration(a); assert r.status=='pass' and r.data['gateway']=='192.168.1.1'
def test_apipa_fails(monkeypatch):
    monkeypatch.setattr(mod,'default_gateway',lambda:None)
    a=CheckResult('adapters','pass','x',{'adapters':[{'name':'Wi-Fi','is_up':True,'primary':True,'ipv4':[{'address':'169.254.1.50','netmask':'255.255.0.0'}]}]})
    assert mod.assess_ip_configuration(a).status=='fail'
def test_valid_ip_no_gateway_warns(monkeypatch):
    monkeypatch.setattr(mod,'default_gateway',lambda:None)
    a=CheckResult('adapters','pass','x',{'adapters':[{'name':'Ethernet','is_up':True,'primary':True,'ipv4':[{'address':'10.0.0.20','netmask':'255.255.255.0'}]}]})
    assert mod.assess_ip_configuration(a).status=='warning'
