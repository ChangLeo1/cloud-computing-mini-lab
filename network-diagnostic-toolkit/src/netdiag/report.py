from __future__ import annotations
import html, json, os, platform, socket
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .privacy import redact

def build_report(results,diagnosis,config,redact_output=False)->dict[str,Any]:
    report={"tool":"network-diagnostic-toolkit","version":"1.0.0","generated_at":datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds'),"device":{"hostname":socket.gethostname(),"username":os.environ.get('USERNAME') or os.environ.get('USER') or 'unknown',"os":platform.platform()},"results":[r.to_dict() for r in results],"diagnosis":diagnosis.to_dict(),"disclaimer":"Diagnostic thresholds are indicative and are not ISP SLAs. Use only on systems and networks you own or are authorised to support.","retention_guidance_days":config.get('privacy',{}).get('retention_days',30)}
    return redact(report) if redact_output else report

def write_json(report,path:Path):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8'); return path

def write_text(report,path:Path):
    path.parent.mkdir(parents=True,exist_ok=True); d=report.get('diagnosis',{}); lines=['NETWORK DIAGNOSTIC REPORT',f"Generated: {report['generated_at']}",f"Device: {report['device'].get('hostname')}",f"OS: {report['device'].get('os')}",'','TEST RESULTS']
    lines += [f"[{x['status'].upper():7}] {x['name']}: {x['summary']}" for x in report.get('results',[])]
    lines += ['', 'DIAGNOSIS', f"{d.get('title')} ({d.get('code')})", d.get('explanation',''), '', 'RECOMMENDATIONS'] + [f"{i}. {x}" for i,x in enumerate(d.get('recommendations',[]),1)] + ['',report.get('disclaimer','')]
    path.write_text('\n'.join(lines),encoding='utf-8'); return path

def write_html(report,path:Path):
    path.parent.mkdir(parents=True,exist_ok=True); rows=''.join(f"<tr><td>{html.escape(x['name'])}</td><td>{html.escape(x['status'])}</td><td>{html.escape(x['summary'])}</td></tr>" for x in report.get('results',[])); d=report.get('diagnosis',{}); recs=''.join(f"<li>{html.escape(x)}</li>" for x in d.get('recommendations',[]))
    body = """<!doctype html><html><head><meta charset='utf-8'><title>Network Diagnostic Report</title><style>body{font-family:Arial,sans-serif;max-width:980px;margin:32px auto;padding:0 20px;line-height:1.45}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccc;padding:8px;text-align:left}th{background:#f4f4f4}code{background:#f6f6f6;padding:2px 4px}</style></head><body>"""
    body += f"<h1>Network Diagnostic Report</h1><p><b>Generated:</b> {html.escape(report['generated_at'])}<br><b>Device:</b> {html.escape(str(report['device'].get('hostname')))}<br><b>OS:</b> {html.escape(str(report['device'].get('os')))}</p>"
    body += f"<h2>Test Results</h2><table><thead><tr><th>Check</th><th>Status</th><th>Summary</th></tr></thead><tbody>{rows}</tbody></table><h2>Diagnosis</h2><p><b>{html.escape(str(d.get('title')))}</b> <code>{html.escape(str(d.get('code')))}</code></p><p>{html.escape(str(d.get('explanation','')))}</p><h3>Recommendations</h3><ol>{recs}</ol><p><small>{html.escape(report.get('disclaimer',''))}</small></p></body></html>"
    path.write_text(body,encoding='utf-8'); return path

def write_audit_log(report,path:Path):
    path.parent.mkdir(parents=True,exist_ok=True)
    summary={
        'generated_at':report.get('generated_at'),
        'diagnosis_code':report.get('diagnosis',{}).get('code'),
        'severity':report.get('diagnosis',{}).get('severity'),
        'check_counts':{s:sum(1 for x in report.get('results',[]) if x.get('status')==s) for s in ['pass','warning','fail','error']}
    }
    with path.open('a',encoding='utf-8') as fh: fh.write(json.dumps(summary,ensure_ascii=False)+'\n')
    return path

def write_all(report,output_dir):
    directory=Path(output_dir); stamp=datetime.now().strftime('%Y%m%d-%H%M%S')
    return {'json':str(write_json(report,directory/f'netdiag-{stamp}.json')),'text':str(write_text(report,directory/f'netdiag-{stamp}.txt')),'html':str(write_html(report,directory/f'netdiag-{stamp}.html')),'audit_log':str(write_audit_log(report,directory/'netdiag-audit.log'))}
