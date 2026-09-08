# Troubleshooting Decision Flow

1. **Adapter active?** If no -> `ADAPTER_DOWN`.
2. **Valid non-APIPA IPv4?** If no -> `IP_DHCP`.
3. **Default gateway exists?** If no -> `NO_GATEWAY`.
4. **Gateway reachable?** If no -> `LOCAL_GATEWAY`.
5. **Public IP/TCP connectivity?** If no -> `UPSTREAM`.
6. **DNS works?** If no -> `DNS`.
7. **Packet loss > configured warning threshold?** -> `PACKET_LOSS`.
8. **Latency > configured warning threshold?** -> `LATENCY`.
9. **Requested TCP service unreachable?** -> `SERVICE_PORT`.
10. Otherwise -> `HEALTHY`.

TCP/443 to the configured public IP is used as a fallback because ICMP can be blocked without total Internet loss.
