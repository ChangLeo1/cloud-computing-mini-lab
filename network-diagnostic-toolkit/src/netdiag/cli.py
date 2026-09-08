from __future__ import annotations
import argparse, sys
from . import __version__
from .repair import ACTIONS, perform
from .report import build_report, write_all
from .runner import run_diagnostics

def _parse_ports(values):
    if not values: return None
    out=[]
    for value in values:
        if ':' not in value: raise argparse.ArgumentTypeError(f"Invalid --port value '{value}'. Use HOST:PORT")
        host,port=value.rsplit(':',1)
        try: port_i=int(port)
        except ValueError: raise argparse.ArgumentTypeError(f"Invalid port in '{value}'")
        if not host or not (1 <= port_i <= 65535): raise argparse.ArgumentTypeError(f"Invalid --port value '{value}'")
        out.append({'host':host,'port':port_i})
    return out

def _print_results(results,diagnosis):
    for r in results: print(f"[{r.status.upper():7}] {r.name:<20} {r.summary}")
    print('\nDIAGNOSIS'); print(f"{diagnosis.title} [{diagnosis.code}]"); print(diagnosis.explanation)
    for i,rec in enumerate(diagnosis.recommendations,1): print(f"  {i}. {rec}")
def cmd_diagnose(args):
    results,diagnosis,cfg=run_diagnostics(args.config,args.full,args.security,args.target,args.dns_host,_parse_ports(args.port)); _print_results(results,diagnosis); paths=write_all(build_report(results,diagnosis,cfg,args.redact),args.output_dir); print('\nReports:'); [print(f"  {k}: {v}") for k,v in paths.items()]; return 0 if diagnosis.severity in {'info','low'} else 2
def cmd_repair(args):
    spec=ACTIONS[args.action]; print(f"Action: {args.action}\n{spec['description']}"); print('A pre-repair snapshot will be saved. Use only on a system you own or are authorised to support.')
    if not args.yes and input('Type YES to continue: ').strip()!='YES': print('Cancelled. No repair action executed.'); return 1
    ok,msg,snap=perform(args.action,args.output_dir); print(f'Snapshot: {snap}' if snap else 'No snapshot created.'); print(msg); return 0 if ok else 3
def build_parser():
    p=argparse.ArgumentParser(prog='netdiag',description='Privacy-aware network diagnostic toolkit'); p.add_argument('--version',action='version',version=f'netdiag {__version__}'); sub=p.add_subparsers(dest='command',required=True)
    d=sub.add_parser('diagnose',help='Run network diagnostics'); d.add_argument('--full',action='store_true',help='Include traceroute'); d.add_argument('--security',action='store_true',help='Include local Windows security posture hints'); d.add_argument('--redact',action='store_true',help='Redact host/user/local-address details in reports'); d.add_argument('--config',help='YAML config override'); d.add_argument('--target',help='Override public connectivity IP target'); d.add_argument('--dns-host',help='Override DNS hostname target'); d.add_argument('--port',action='append',help='TCP target as HOST:PORT; repeat for multiple targets'); d.add_argument('--output-dir',default='reports'); d.set_defaults(func=cmd_diagnose)
    r=sub.add_parser('repair',help='Run a guided Windows network repair action'); r.add_argument('action',choices=sorted(ACTIONS)); r.add_argument('--yes',action='store_true'); r.add_argument('--output-dir',default='reports'); r.set_defaults(func=cmd_repair); return p
def main(argv=None):
    args=build_parser().parse_args(argv); return args.func(args)
if __name__=='__main__': sys.exit(main())
