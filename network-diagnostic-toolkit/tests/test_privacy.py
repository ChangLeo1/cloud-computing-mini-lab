from netdiag.privacy import redact, redact_ipv4, redact_mac

def test_redact_ipv4(): assert redact_ipv4('192.168.1.23')=='192.168.1.xxx'
def test_redact_mac(): assert redact_mac('AA:BB:CC:DD:EE:FF')=='XX:XX:XX:XX:EE:FF'
def test_redact_nested():
    data={'device':{'hostname':'LEO-PC','username':'leo'},'ip':{'address':'10.0.0.5','gateway':'10.0.0.1'},'mac':['AA:BB:CC:DD:EE:FF']}
    out=redact(data)
    assert out['device']['hostname']=='REDACTED'; assert out['device']['username']=='REDACTED'
    assert out['ip']['address']=='10.0.0.xxx'; assert out['ip']['gateway']=='10.0.0.xxx'; assert out['mac'][0].endswith('EE:FF')

def test_public_ip_not_redacted_in_free_text(): assert redact({'host':'1.1.1.1'})['host']=='1.1.1.1'
def test_private_ip_redacted_in_text(): assert 'xxx' in redact({'summary':'gateway 192.168.50.1 failed'})['summary']
