# Network Diagnostic Toolkit

A privacy-aware command-line toolkit for Windows-focused IT/network support. It collects local network configuration, tests gateway/public connectivity, DNS, latency, packet loss and TCP ports, applies a rule-based diagnosis engine, and generates JSON/TXT/HTML reports.

> **Authorisation first:** use this toolkit only on devices and networks you own or are explicitly authorised to support. It does not perform subnet-wide discovery, credential testing, brute force, packet interception or vulnerability exploitation.

## What it checks

- Network adapters and active IPv4 configuration
- Default gateway detection and gateway reachability
- Public IP connectivity with ICMP plus a TCP/443 fallback
- DNS server configuration and hostname resolution time
- Packet loss and latency thresholds
- Requested TCP service reachability
- Optional traceroute (`--full`)
- Optional local Windows security posture hints (`--security`)
- Privacy-redacted reports (`--redact`)
- Guided Windows repairs with explicit confirmation and a pre-change snapshot

## Diagnosis codes

`ADAPTER_DOWN`, `IP_DHCP`, `NO_GATEWAY`, `LOCAL_GATEWAY`, `UPSTREAM`, `DNS`, `PACKET_LOSS`, `LATENCY`, `SERVICE_PORT`, `HEALTHY`.

## Installation (Windows PowerShell)

```powershell
git clone https://github.com/ChangLeo1/cloud-computing-mini-lab.git
cd cloud-computing-mini-lab\network-diagnostic-toolkit
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

## Quick start

```powershell
netdiag --version
netdiag diagnose
netdiag diagnose --full --security
netdiag diagnose --full --security --redact
netdiag diagnose --target 8.8.8.8 --dns-host example.com --port example.com:443
```

Reports are written to `reports/` as JSON, text and HTML. A privacy-minimised `netdiag-audit.log` records timestamp, diagnosis/severity and status counts without host/user/IP details.

## Custom thresholds / targets

Copy `config/default.yaml`, change only what you need, then run:

```powershell
netdiag diagnose --config .\config\default.yaml
```

The default thresholds are **diagnostic classifications only**, not ISP service-level guarantees.

## Guided repairs

The toolkit never silently changes network settings. Repair commands show what they will do, save a pre-repair snapshot, and require typing `YES` unless `--yes` is intentionally supplied.

```powershell
netdiag repair flush-dns
netdiag repair renew-dhcp
netdiag repair reset-winsock
netdiag repair reset-ip-stack
```

Some actions require an elevated PowerShell and/or a reboot. A snapshot is for audit/reference; automatic rollback of Windows networking changes is **not** claimed.

## Privacy mode

```powershell
netdiag diagnose --redact
```

Redaction removes/reduces host name, user name, local IPv4 and MAC details in generated reports. Public demo reports must use `--redact` or synthetic data.

The tool does **not** intentionally collect passwords, browser credentials, cookies, tokens, SSH private keys, VPN passwords, email contents or personal documents.

## Safe operational scope

Allowed examples when authorised:

- Inspect the local host's own network configuration
- Ping its configured default gateway
- Test DNS resolution
- Test an explicitly specified service/port
- Run traceroute to a configured public target

Out of scope by design:

- Subnet-wide scanning by default
- Password guessing / brute force
- Credential dumping
- Exploitation
- Firewall bypass
- Intercepting other users' traffic

See `docs/authorisation-and-scope.md` and `docs/compliance-and-legal.md` before using the toolkit for paid client work.

## Testing

```powershell
pip install -e .[dev]
pytest -q
pytest --cov=netdiag --cov-report=term-missing
```

The repository includes 30+ automated tests plus a manual Windows test plan covering healthy, DNS failure, adapter-down, APIPA/DHCP, gateway, upstream, port, packet-loss/latency, reporting, privacy and repair behaviour.

## Project structure

```text
network-diagnostic-toolkit/
├── src/netdiag/          # diagnostic modules and CLI
├── tests/                # automated tests
├── config/default.yaml   # targets and thresholds
├── examples/             # synthetic/redacted reports
├── docs/                 # authorisation, privacy, compliance, service templates
└── .github/workflows/    # Windows + Ubuntu CI
```

## Commercial use notes

If you use this as part of an IT support service, define the scope in writing, obtain authorisation before testing, minimise collected data, protect reports, and avoid promises that every issue will be fixed. Australian consumer guarantees can apply to services and cannot simply be excluded by a generic disclaimer.

## Licence

MIT. This repository is a diagnostic/support tool, not legal advice, a penetration-testing tool, an ISP SLA measurement product, or an Essential Eight compliance certification.
