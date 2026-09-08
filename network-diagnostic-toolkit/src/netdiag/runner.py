from __future__ import annotations
from .adapters import collect_adapters
from .config import load_config
from .diagnosis import diagnose
from .dns import resolve_hostname
from .ip_config import assess_ip_configuration
from .models import CheckResult
from .ping import ping_host
from .ports import test_tcp_port
from .security import local_security_posture
from .traceroute import trace_route

def run_diagnostics(config_path=None, full=False, security=False, internet_ip=None, dns_hostname=None, tcp_targets=None):
    cfg=load_config(config_path); t=cfg['thresholds']; e=cfg['execution']; targets=dict(cfg['targets'])
    if internet_ip: targets['internet_ip']=internet_ip
    if dns_hostname: targets['dns_hostname']=dns_hostname
    if tcp_targets is not None: targets['tcp_targets']=tcp_targets
    results=[]
    adapters=collect_adapters(); results.append(adapters); ipcfg=assess_ip_configuration(adapters); results.append(ipcfg); gateway=ipcfg.data.get('gateway') if ipcfg.data else None
    results.append(ping_host(gateway,count=e['ping_count'],timeout_ms=e['ping_timeout_ms'],latency_good_ms=t['gateway_latency_ms']['good'],latency_warning_ms=t['gateway_latency_ms']['warning'],loss_good_pct=t['packet_loss_pct']['good'],loss_warning_pct=t['packet_loss_pct']['warning'],name='gateway_ping') if gateway else CheckResult('gateway_ping','fail','Gateway ping skipped because no gateway was detected',{}))
    public_ip=targets['internet_ip']; results.append(ping_host(public_ip,count=e['ping_count'],timeout_ms=e['ping_timeout_ms'],latency_good_ms=t['internet_latency_ms']['good'],latency_warning_ms=t['internet_latency_ms']['warning'],loss_good_pct=t['packet_loss_pct']['good'],loss_warning_pct=t['packet_loss_pct']['warning'],name='internet_ping'))
    fallback=test_tcp_port(public_ip,443,e['tcp_timeout_seconds']); fallback.name='internet_tcp'; results.append(fallback)
    results.append(resolve_hostname(targets['dns_hostname'],t['dns_response_ms']['good'],t['dns_response_ms']['warning']))
    for target in targets.get('tcp_targets',[]): results.append(test_tcp_port(target['host'],int(target['port']),e['tcp_timeout_seconds']))
    if full: results.append(trace_route(public_ip,e['traceroute_max_hops'],e['traceroute_timeout_ms']))
    if security: results.append(local_security_posture())
    cfg=dict(cfg); cfg['targets']=targets
    return results,diagnose(results,packet_loss_warning_pct=t['packet_loss_pct']['warning'],latency_warning_ms=t['internet_latency_ms']['warning']),cfg
