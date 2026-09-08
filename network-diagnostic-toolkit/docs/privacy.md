# Privacy and Report Handling

## Data minimisation
The toolkit is designed to collect only information useful for network diagnosis: adapter state, local IP/network settings, configured DNS servers, connectivity metrics, route output and local security posture hints.

It must not be extended to collect passwords, browser credentials, authentication tokens, email contents, personal documents, SSH private keys or VPN passwords unless a completely separate, lawful and necessary workflow is designed.

## Public examples
Always use synthetic data or `netdiag diagnose --redact` before publishing reports to GitHub, tickets, portfolios or screenshots.

## Suggested client-report handling
- Store client reports only where access is controlled.
- Do not place real client reports in this public repository.
- Suggested operational retention: up to 30 days unless the client contract or applicable law requires another period.
- Delete or de-identify information when it is no longer needed.

The 30-day value is an internal project policy, not a statutory retention period.
