
# Self-Hosted Infrastructure Portfolio

## Overview

This project showcases a self-hosted infrastructure deployed on a VPS (Hetzner), designed and managed with a focus on **security, portability, and observability**.

It reflects a hands-on approach to infrastructure design, combining containerization, network security, monitoring, and backup strategies.

---

## Key Highlights

* Fully containerized infrastructure using Docker
* Centralized reverse proxy with WAF (ModSecurity + OWASP CRS)
* Private service access via VPN (WireGuard)
* End-to-end observability (metrics and logs)
* Automated TLS management with wildcard certificates
* Backup strategy with local and offsite redundancy

---

## Architecture

The infrastructure is built around Docker, with each service running in its own container. This ensures isolation, simplifies lifecycle management, and allows the stack to be redeployed on a fresh host with minimal configuration.

A central reverse proxy acts as the single entry point. It handles TLS termination, routes traffic to internal services, and applies security controls through a Web Application Firewall. Services are not directly exposed unless necessary; access to sensitive components is restricted via VPN or authentication layers.


---

## Services

| Service                             | Role                                |
| ----------------------------------- | ----------------------------------- |
| Reverse Proxy (Nginx + ModSecurity) | Secure entry point with WAF         |
| WireGuard                           | Private access to internal services |
| Gitea                               | Self-hosted Git platform            |
| Gitea Act Runner                    | CI/CD runner (work in progress)     |
| Nginx (Public)                      | Static content delivery             |
| Nginx (Staging)                     | Isolated staging environment        |
| Certbot                             | TLS certificate automation          |
| Prometheus                          | Metrics collection                  |
| Grafana                             | Metrics visualization               |
| Loki + Promtail                     | Log aggregation                     |
| Node Exporter                       | Host monitoring                     |
| cAdvisor                            | Container monitoring                |
| Borgmatic                           | Backup automation                   |

The platform integrates several components covering application hosting, networking, observability, and data protection.

A reverse proxy based on Nginx with ModSecurity provides secure external access, while WireGuard enables private connectivity to internal services. Application-level functionality is supported by Gitea, alongside a work-in-progress CI/CD runner.

Static content is served through dedicated Nginx instances for both public and staging environments, with the staging layer protected by VPN access and basic authentication. TLS certificates are automatically managed by Certbot(DNS-01 Challenge).

Monitoring and observability are handled through a combination of Prometheus for metrics collection, Grafana for visualization, and Loki with Promtail for log aggregation. System and container-level visibility is achieved using Node Exporter and cAdvisor.

Finally, Borgmatic and Cron are used to manage automated backups and store them locally and offsite.

---

## Security Approach

At the network level, exposure is limited to essential ports only, with a dual firewall strategy combining Hetzner’s cloud firewall and a host-level UFW configuration. Access to the system is restricted through hardened SSH settings, including a non-standard port, disabled root login, and key-based authentication. Sensitive services are not publicly reachable and require VPN access.

At the application level, the reverse proxy is reinforced with ModSecurity and the OWASP Core Rule Set. Additional protection is provided by Fail2Ban, which monitors authentication attempts and web server behavior, applying progressive bans while allowing trusted sources and VPN ranges.

TLS and DNS are configured with privacy and automation in mind. DNS is managed via Njalla, and wildcard certificates are issued using the DNS-01 challenge, with automatic renewal handled by Certbot.

---

## Coming Soon

* CI/CD pipeline completion (Gitea Act Runner)
* Mail server integration
* Advanced alerting system
* Improved rate limiting and bot detection

