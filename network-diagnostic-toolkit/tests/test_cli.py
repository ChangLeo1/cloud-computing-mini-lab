from netdiag.cli import build_parser, _parse_ports

def test_cli_diagnose_parse():
    a=build_parser().parse_args(['diagnose','--full','--redact','--security']); assert a.command=='diagnose' and a.full and a.redact and a.security

def test_cli_repair_parse():
    a=build_parser().parse_args(['repair','flush-dns','--yes']); assert a.action=='flush-dns' and a.yes

def test_parse_ports(): assert _parse_ports(['example.com:443','10.0.0.1:22'])==[{'host':'example.com','port':443},{'host':'10.0.0.1','port':22}]

def test_cli_custom_targets():
    a=build_parser().parse_args(['diagnose','--target','8.8.8.8','--dns-host','example.com','--port','example.com:443']); assert a.target=='8.8.8.8' and a.dns_host=='example.com' and a.port==['example.com:443']
