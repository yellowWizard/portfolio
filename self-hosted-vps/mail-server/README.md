# 🐮 Standalone Mail Infrastructure (Mailcow)

This module implements a fully isolated email infrastructure using **Mailcow (Dockerized)**. To protect the sender reputation of the main platform and guarantee high deliverability, this mail server is deployed on an entirely dedicated host with a separate `.me` domain.

## Why Mailcow?

Mailcow was chosen because it provides a production-ready mail stack out of the box, integrating Postfix, Dovecot, Rspamd, Fail2ban, and an automated ACME client into a single ecosystem, alongside other core security and management services. It handles everything from mail routing and spam filtering to brute-force protection and SSL/TLS certificates without requiring complex, manual integration of individual tools.

## Host Sizing & Resources

The infrastructure is deployed on a dedicated **Hetzner CX33 (4 vCPUs, 8 GB RAM, 80 GB NVMe)**. This specific machine was chosen to meet Mailcow's hardware requirements and to ensure the entire email stack runs smoothly under any condition.

## DNS Configuration

To ensure high email deliverability and strictly verify sender authenticity, I configured a comprehensive set of DNS records. This setup handles secure routing, auto-configuration for mail clients, and cryptographic anti-spoofing policies.


| Record Type | Host / Name | Value / Target | Purpose |
| :--- | :--- | :--- | :--- |
| **A** | `mail` | `178.104.157.12` | Maps the hostname to the dedicated IPv4 address. |
| **AAAA** | `mail` | `21:48:119:ffa3::1` | Maps the hostname to the dedicated IPv6 address. |
| **MX** | `@` | `mail.domain.me` (Priority 10) | Directs incoming emails to the Mailcow infrastructure. |
| **SPF (TXT)** | `@` | `v=spf1 mx a ip4:178.104.157.12 -all` | Restricts outbound mail to the server's IPs with a strict hard-fail policy. |
| **DKIM (TXT)** | `dkim._domainkey` | `v=DKIM1; k=rsa; t=s; s=email; p=...` | Holds the public cryptographic key used to verify digital signatures. |
| **DMARC (TXT)** | `_dmarc` | `v=DMARC1; p=quarantine;` | Instructs receiving servers to quarantine messages failing SPF/DKIM checks. |
| **CNAME** | `autoconfig` / `autodiscover` | `mail.domain.me` | Enables seamless automatic email client setup (Outlook, Thunderbird). |

## Security & Monitoring

The mail server uses Mailcow's built-in tools to keep the infrastructure secure and track activity:
* **Netfilter Container**: Acts as an automated brute-force protection system, parsing authentication logs to dynamically ban malicious IPs at the firewall level.
* **RRD Graphs**: Provides clean visual statistics directly in the dashboard to monitor sent, received, and rejected messages at a glance.
* **Queue Watchdog**: Configured with API alerts to send immediate notifications if the outbound mail queue gets blocked or if the server IP hits a public blacklist.

## Testing & Warm-up Workflow

To ensure high email deliverability from a fresh Hetzner IP, the setup uses the following validation workflow::
* **Rspamd Testing**: Used to pre-evaluate message headers and cryptographic alignments, securing a clean **10/10 score on Mail-Tester**.
* **Forced TLS**: Configured the server to always require TLS encryption for outbound transport to meet modern security benchmarks.
* **Mailflow**: Integrated the inbox with Mailflow to automate daily interactions, safely scaling email volume to build a positive sender reputation.
