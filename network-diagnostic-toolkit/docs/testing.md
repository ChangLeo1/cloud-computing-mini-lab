# Testing and Acceptance Guide

This is the repository-side test checklist. The user-facing Word manual contains the same test programme in greater detail.

## Safety first

- Use only systems and networks you own or are explicitly authorised to support.
- Run disruption tests (adapter disable, static/APIPA IP, gateway changes, DHCP renew, Winsock/IP reset) only on a lab VM or a non-critical local machine.
- Do not run disruptive tests through an RDP/remote session that depends on the same network path.
- Repairs never run silently; inspect the action and snapshot first.

## Automated baseline

```powershell
pip install -e .[dev]
pytest -q
pytest --cov=netdiag --cov-report=term-missing
```

Current development baseline: 36 automated tests pass; measured local statement coverage is 66%. These numbers validate implemented rule paths and helpers, not real-world diagnosis accuracy.

## Functional checks

| ID | Function | Command / method | Expected result |
|---|---|---|---|
| T01 | CLI/version | `netdiag --version` | `netdiag 1.0.0` |
| T02 | Healthy baseline | `netdiag diagnose` | Core checks execute and reports are created |
| T03 | Full route | `netdiag diagnose --full` | `traceroute` check appears |
| T04 | Security hints | `netdiag diagnose --security` | Firewall/update status plus manual backup/MFA hints |
| T05 | Privacy | `netdiag diagnose --redact` | Host/user and private local address details are redacted in reports |
| T06 | Custom target | `netdiag diagnose --target 8.8.8.8` | Internet check uses 8.8.8.8 |
| T07 | Custom DNS | `netdiag diagnose --dns-host example.com` | DNS check resolves example.com |
| T08 | TCP port | `netdiag diagnose --port example.com:443` | TCP port check appears |
| T09 | Custom config | `netdiag diagnose --config .\config\default.yaml` | YAML options are loaded |
| T10 | Reports | inspect `reports/` | JSON, TXT, HTML and audit log exist |

## Deterministic diagnosis-engine tests

```powershell
pytest tests/test_diagnosis.py -q
```

This verifies: adapter down, invalid/APIPA IP, missing gateway, gateway failure, upstream failure, DNS failure, packet loss, high latency, service-port failure, healthy state, and the ICMP-filtered/TCP-fallback case.

## Safe fault injection examples

- DNS: `netdiag diagnose --dns-host does-not-exist.invalid` -> expected `DNS` when normal Internet connectivity works.
- Upstream target: `netdiag diagnose --target 203.0.113.1 --port 203.0.113.1:443` -> expected `UPSTREAM` on ordinary Internet access because TEST-NET-3 is not intended for public service.
- Service port: `netdiag diagnose --port 127.0.0.1:9` -> expected `SERVICE_PORT` if nothing is listening locally on TCP/9.
- Adapter/IP/gateway scenarios: use an isolated Windows VM and change only that VM's adapter/static IPv4 configuration.

Packet-loss and latency classification are deterministic in unit tests. Do not deliberately degrade a production/client network simply to create these failures; use a lab traffic emulator if live integration testing is required.

## Repair testing

First test cancellation:

```powershell
netdiag repair flush-dns
# type anything other than YES
```

Expected: cancelled; no repair action executes.

Approved lab tests:

```powershell
netdiag repair flush-dns
netdiag repair renew-dhcp
netdiag repair reset-winsock
netdiag repair reset-ip-stack
```

Each executed repair saves a pre-repair JSON snapshot. DHCP renew can interrupt connectivity. Winsock/IP-stack reset may require elevated PowerShell and a reboot.

## Acceptance criteria

- 36/36 current automated tests pass.
- Diagnosis-engine rule tests pass for all defined synthetic scenarios.
- Core diagnostics run without administrator rights on Windows 10/11.
- JSON/TXT/HTML reports and privacy-minimised audit log are generated.
- Redacted public/demo reports contain no real hostname, username, full private IPv4 address, or full MAC address.
- No credential collection is implemented.
- Suggested normal diagnostic runtime target: under 30 seconds on a responsive network; full traceroute target: under 90 seconds. These are project targets, not guarantees or SLAs.
