# 🐳 Self-Hosted Infrastructure Portfolio


## Overview

This project is a personal self-hosted infrastructure built as a technical portfolio. It is designed to demonstrate practical experience in system design, infrastructure automation, containerization, security, monitoring, and CI/CD workflows.

The environment is deployed on a VPS (Hetzner) and simulates a production-like setup, with a strong focus on reproducibility, security, and observability.

Beyond serving real services, the main purpose of this project is to experiment with infrastructure technologies and test architectural decisions in a real environment while documenting the results. It also acts as a public showcase of my work and ongoing learning in the DevOps and infrastructure space.

---


## Key Highlights

* Fully containerized infrastructure using Docker
* Centralized reverse proxy with WAF (ModSecurity + OWASP CRS)
* Private service access via VPN (WireGuard)
* End-to-end observability (metrics and logs)
* Automated TLS management with wildcard certificates
* Backup strategy with local and offsite redundancy
* Basic CI/CD pipeline with automated build and container deployment

---


## Architecture

The infrastructure is container-based, with services orchestrated through Docker to ensure isolation and reproducibility. Each component is deployed independently, allowing the entire stack to be rebuilt quickly on a new host.

---


## Services

<div align="center">

| Service                             | Role                                |
| ----------------------------------- | ----------------------------------- |
| [Reverse Proxy (Nginx + ModSecurity)](./Docker/core/nginx-reverse-proxy/) | Secure entry point with WAF         |
| [WireGuard](./Docker/core/wireguard/)                           | Private access to internal services |
| [Gitea](./Docker/services/gitea/)                               | Self-hosted Git platform            |
| [Gitea Act Runner](./Docker/services/gitea-act-runner/)                    | CI/CD runner     |
| [Nginx (Public)](./Docker/services/nginx-prod/)                      | Static content delivery             |
| [Nginx (Staging)](./Docker/services/nginx-staging/)                     | Isolated staging environment        |
| [Certbot](./Docker/core/certbot/)                             | TLS certificate automation          |
| [Prometheus](./Docker/monitoring/)                          | Metrics collection                  |
| [Grafana](./Docker/monitoring/)                             | Metrics visualization               |
| [Loki + Promtail](./Docker/monitoring/)                     | Log aggregation                     |
| [Node Exporter](./Docker/monitoring/)                       | Host monitoring                     |
| [cAdvisor](./Docker/monitoring/)                            | Container monitoring                |
| [Borgmatic](./Docker/backup/borgmatic/)                           | Backup automation                   |

</div>

The platform integrates application hosting, networking, observability, CI/CD, and data protection into a single self-hosted system.

External access is handled through an Nginx reverse proxy with ModSecurity acting as a WAF. Internal services are not directly exposed and are accessible only via controlled access mechanisms such as WireGuard or authentication layers.

Application and code management are provided by Gitea, along with a CI/CD pipeline running on a self-hosted Act Runner. The pipeline builds and deploys a Hugo-based static site to staging or production entirely within the infrastructure.

Static content is served via dedicated Nginx instances for production and staging environments, with staging isolated and VPN-restricted. TLS certificates are managed automatically using Certbot with DNS-01 validation.

Observability is provided by Prometheus, Grafana, and Loki, with host and container metrics collected via Node Exporter and cAdvisor.

Backups are handled by Borgmatic and executed on a schedule via cron, with data stored both locally and offsite for redundancy.

---


## Coming Soon

* Mail server integration
* Advanced alerting system
* Improved rate limiting and bot detection

