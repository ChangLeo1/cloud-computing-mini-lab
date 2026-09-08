from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from .dns import dns_servers
from .ip_config import default_gateway
from .system import os_name, run_command
ACTIONS={'flush-dns':{'command':['ipconfig','/flushdns'],'admin':False,'description':'Flush the local Windows DNS resolver cache.'},'renew-dhcp':{'command':None,'admin':False,'description':'Release and renew the Windows DHCP lease. Connectivity will be interrupted briefly.'},'reset-winsock':{'command':['netsh','winsock','reset'],'admin':True,'description':'Reset the Winsock catalog. A reboot may be required.'},'reset-ip-stack':{'command':['netsh','int','ip','reset'],'admin':True,'description':'Reset the TCP/IP stack. A reboot is normally required.'}}
def snapshot(output_dir):
    directory=Path(output_dir); directory.mkdir(parents=True,exist_ok=True); data={'created_at':datetime.now().isoformat(timespec='seconds'),'gateway':default_gateway(),'dns_servers':dns_servers(),'note':'Pre-repair snapshot for audit/reference. This toolkit does not automatically roll back OS networking changes.'}; path=directory/f"pre-repair-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"; path.write_text(json.dumps(data,indent=2),encoding='utf-8'); return path
def perform(action,output_dir='reports'):
    if action not in ACTIONS: return False,f'Unknown repair action: {action}',None
    if os_name()!='windows': return False,'Repair actions are currently supported only on Windows.',None
    snap=snapshot(output_dir)
    if action=='renew-dhcp':
        release=run_command(['ipconfig','/release'],timeout=30); renew=run_command(['ipconfig','/renew'],timeout=60); ok=release.returncode==0 and renew.returncode==0; return ok,(release.stdout+'\n'+renew.stdout+'\n'+release.stderr+'\n'+renew.stderr).strip(),snap
    out=run_command(ACTIONS[action]['command'],timeout=60); return out.returncode==0,(out.stdout or out.stderr),snap
