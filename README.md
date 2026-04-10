# 🐳 Self-Hosted Infrastructure Portfolio


## Overview

This project showcases a self-hosted infrastructure deployed on a VPS (Hetzner). It reflects a hands-on approach to infrastructure design, combining containerization, network security, monitoring, and backup strategies.

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

The platform integrates components across application hosting, networking, observability, CI/CD, and data protection.

External access is handled through a reverse proxy based on Nginx with ModSecurity, acting as an entry point with WAF enforcement. Internal services are not directly exposed and are reachable only through controlled access mechanisms such as WireGuard VPN or authentication layers.

Application and code management are provided by Gitea, complemented by a basic CI/CD pipeline using GitHub Actions. The pipeline builds the Hugo-based static site, packages it into a Docker image, and deploys it to either staging or production environments, enabling a simple automated release flow.

Static content is served via dedicated Nginx instances for public and staging environments. The staging environment is isolated and protected through VPN access and additional authentication controls. TLS certificates are automatically issued and renewed via Certbot using the DNS-01 challenge.

Observability is implemented through Prometheus for metrics collection, Grafana for visualization, and Loki with Promtail for centralized logging. Host and container-level monitoring is provided by Node Exporter and cAdvisor.

Backups are managed through Borgmatic and scheduled via Cron, with data stored both locally and offsite to ensure redundancy.


---


## Coming Soon

* Mail server integration
* Advanced alerting system
* Improved rate limiting and bot detection

