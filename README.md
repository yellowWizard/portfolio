# 🐳 Self-Hosted Infrastructure Portfolio


## Overview

This project is a personal self-hosted infrastructure built as a technical portfolio. It is designed to demonstrate practical experience in system design, infrastructure automation, containerization, security, monitoring, and CI/CD workflows.

The environment is deployed on a VPS (Hetzner) and simulates a production-like setup, with a strong focus on reproducibility, security, and observability.

Beyond serving real services, the main purpose of this project is to experiment with infrastructure technologies and test architectural decisions in a real environment while documenting the results.

---


## Key Highlights

* Fully containerized infrastructure using Docker
* Self Hosted Mail Server (MailCow)
* Private service access via VPN (WireGuard)
* Centralized reverse proxy with WAF (ModSecurity + OWASP CRS)
* End-to-end observability (metrics and logs)
* Backup strategy with local and offsite redundancy
* Basic CI/CD pipeline with automated build and container deployment

---


## Services

The platform provides a distributed ecosystem for application hosting, networking, observability, CI/CD, and secure communication.

A complete mail infrastructure is provided by a self-hosted Mailcow (Dockerized) instance. The setup involves DNS configuration, including SPF, DKIM, and DMARC policies, to ensure high deliverability and security. To establish a solid sender reputation, a warm-up strategy is currently active, gradually building trust for both the domain and the dedicated IP with major email providers

External access is handled through an Nginx reverse proxy with ModSecurity acting as a WAF. Internal services are not directly exposed and are accessible only via controlled access mechanisms such as WireGuard or authentication layers.

Application and code management are provided by Gitea, along with a CI/CD pipeline running on a self-hosted Act Runner. The pipeline builds and deploys a Hugo-based static site to staging or production entirely within the infrastructure.

Static content is served via dedicated Nginx instances for production and staging environments, with staging isolated and VPN-restricted. TLS certificates are managed automatically using Certbot with DNS-01 validation.

Observability is provided by Prometheus, Grafana, and Loki, with host and container metrics collected via Node Exporter and cAdvisor.

Backups are handled by Borgmatic and executed on a schedule via cron.


<div align="center">

| Service                             | Role                                |
| ----------------------------------- | ----------------------------------- |
| [Reverse Proxy (Nginx + ModSecurity)](./Docker/core/nginx-reverse-proxy/) | Secure entry point with WAF         |
| [WireGuard](./Docker/core/wireguard/)                           | Private access to internal services |
| [MailCow](#)                               | Self-hosted Dockerized Mail Suite |
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



