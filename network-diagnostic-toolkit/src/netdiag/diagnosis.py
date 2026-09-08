from __future__ import annotations
from .models import CheckResult, Diagnosis

def _find(results,name): return next((r for r in results if r.name==name),None)
def diagnose(results:list[CheckResult],packet_loss_warning_pct:float=5,latency_warning_ms:float=100)->Diagnosis:
    adapters=_find(results,'adapters'); ipcfg=_find(results,'ip_configuration'); gw=_find(results,'gateway_ping'); internet=_find(results,'internet_ping'); tcp=_find(results,'internet_tcp'); dns=_find(results,'dns_resolution')
    if adapters and adapters.status in {'fail','error'}: return Diagnosis('ADAPTER_DOWN','high','No active network adapter','No active IPv4-capable adapter was detected.',['Check Wi-Fi/Ethernet is enabled and physically connected.','Verify the adapter is enabled in Windows Settings or Device Manager.'])
    if ipcfg and ipcfg.status=='fail': return Diagnosis('IP_DHCP','high','IP configuration problem','The host does not have a valid non-APIPA IPv4 configuration.',['Check DHCP availability or the configured static IP.','Confirm subnet mask and address are appropriate for the local network.'])
    if ipcfg and not ipcfg.data.get('gateway'): return Diagnosis('NO_GATEWAY','high','Default gateway missing','A usable IPv4 address was found, but no default gateway was detected.',['Check DHCP/default gateway settings.','If using a static IP, verify the gateway address.'])
    if gw and gw.status=='fail': return Diagnosis('LOCAL_GATEWAY','high','Local LAN or gateway issue','The host cannot reliably reach its default gateway.',['Check Ethernet/Wi-Fi link quality.','Verify VLAN, switch port, wireless association and gateway availability.','Do not reset shared network equipment without authorisation.'])
    internet_works=bool((internet and internet.status in {'pass','warning'}) or (tcp and tcp.status=='pass'))
    if not internet_works: return Diagnosis('UPSTREAM','high','Internet or upstream connectivity issue','The local gateway appears available but public connectivity was not confirmed.',['Check router/ONT/modem WAN status.','Check ISP outage or upstream routing.','ICMP may be filtered; validate with TCP/HTTPS where possible.'])
    if dns and dns.status=='fail': return Diagnosis('DNS','medium','DNS resolution failure','Public connectivity is available, but hostname resolution failed.',['Verify the configured DNS server.','Flush the local DNS cache if authorised.','Test an approved alternate DNS resolver or contact the network administrator.'])
    # Treat a completely failed public ICMP test as inconclusive when the TCP fallback succeeds.
    # Many networks filter ICMP even though Internet service is otherwise healthy. Gateway loss
    # remains meaningful because it measures the local LAN path.
    losses=[]
    if gw and isinstance(gw.data.get('packet_loss_pct'),(int,float)):
        losses.append(gw.data.get('packet_loss_pct'))
    if internet and isinstance(internet.data.get('packet_loss_pct'),(int,float)) and not (internet.status=='fail' and tcp and tcp.status=='pass'):
        losses.append(internet.data.get('packet_loss_pct'))
    if losses and max(losses)>packet_loss_warning_pct: return Diagnosis('PACKET_LOSS','medium','Unstable connection',f'Packet loss exceeded {packet_loss_warning_pct}% during testing.',['Compare wired and wireless performance.','Check signal quality, cabling and interface errors.','Repeat tests at different times to identify intermittency.'])
    lat=[]
    if internet and isinstance(internet.data.get('avg_ms'),(int,float)) and not (internet.status=='fail' and tcp and tcp.status=='pass'):
        lat.append(internet.data.get('avg_ms'))
    if lat and max(lat)>latency_warning_ms: return Diagnosis('LATENCY','medium','High latency',f'Average internet latency exceeded {latency_warning_ms} ms.',['Check for congestion or heavy local traffic.','Compare multiple targets before concluding the ISP path is at fault.'])
    if any(r.name=='tcp_port' and r.status=='fail' for r in results): return Diagnosis('SERVICE_PORT','low','Service-specific connectivity issue','Basic connectivity works, but one or more requested TCP services were unreachable.',['Verify the remote service is listening.','Check firewall, ACL, proxy or application policy for the specific port.'])
    return Diagnosis('HEALTHY','info','Basic connectivity appears healthy','The core adapter, IP, gateway, public connectivity and DNS checks did not identify a major fault.',['If the user still reports problems, test the affected application, destination and time window.','Run --full for traceroute and additional context.'])
