from netdiag.models import CheckResult
from netdiag.diagnosis import diagnose

def R(name,status='pass',data=None): return CheckResult(name,status,'x',data or {})
def healthy_base(): return [R('adapters'),R('ip_configuration',data={'gateway':'192.168.1.1'}),R('gateway_ping',data={'packet_loss_pct':0}),R('internet_ping',data={'packet_loss_pct':0,'avg_ms':20}),R('internet_tcp'),R('dns_resolution')]
def test_adapter_down(): assert diagnose([R('adapters','fail')]).code=='ADAPTER_DOWN'
def test_ip_dhcp(): assert diagnose([R('adapters'),R('ip_configuration','fail')]).code=='IP_DHCP'
def test_no_gateway(): assert diagnose([R('adapters'),R('ip_configuration','warning',{'gateway':None})]).code=='NO_GATEWAY'
def test_gateway_failure(): assert diagnose([R('adapters'),R('ip_configuration','pass',{'gateway':'192.168.1.1'}),R('gateway_ping','fail')]).code=='LOCAL_GATEWAY'
def test_upstream_failure():
    rs=[R('adapters'),R('ip_configuration',data={'gateway':'192.168.1.1'}),R('gateway_ping'),R('internet_ping','fail'),R('internet_tcp','fail')]
    assert diagnose(rs).code=='UPSTREAM'
def test_dns_failure():
    rs=healthy_base(); rs[-1]=R('dns_resolution','fail'); assert diagnose(rs).code=='DNS'
def test_packet_loss():
    rs=healthy_base(); rs[3]=R('internet_ping','warning',{'packet_loss_pct':12,'avg_ms':20}); assert diagnose(rs).code=='PACKET_LOSS'
def test_latency():
    rs=healthy_base(); rs[3]=R('internet_ping','warning',{'packet_loss_pct':0,'avg_ms':150}); assert diagnose(rs).code=='LATENCY'
def test_service_port():
    rs=healthy_base()+[R('tcp_port','fail')]; assert diagnose(rs).code=='SERVICE_PORT'
def test_healthy(): assert diagnose(healthy_base()).code=='HEALTHY'
def test_icmp_filtered_but_tcp_works():
    rs=healthy_base(); rs[3]=R('internet_ping','fail',{'packet_loss_pct':100}); rs[4]=R('internet_tcp','pass'); assert diagnose(rs).code=='HEALTHY'
