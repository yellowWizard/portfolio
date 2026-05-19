# 🐳 Self-Hosted Infrastructure Portfolio

# Self-Hosted Infrastructure Portfolio (Cloud Environment)

This project showcases a personal self-hosted infrastructure deployed on a Hetzner VPS to simulate a production-like environment. The primary objective is to demonstrate practical experience in system design, infrastructure automation, containerization, security, monitoring, and CI/CD workflows.

The architecture emphasizes reproducibility, security, and observability, serving real production services while acting as a continuous integration sandbox for architectural evaluation.

---

## Architectural Overview

The platform provides a highly distributed ecosystem for application hosting, networking, observability, CI/CD, and secure communication.

External traffic is handled exclusively through an **Nginx reverse proxy** with **ModSecurity** acting as a **Web Application Firewall**. Internal services are decoupled and isolated from direct public exposure, remaining accessible only via controlled access mechanisms such as a secure WireGuard **VPN tunnel** or explicit authentication layers.

Application management and code workflows are driven by Gitea, working alongside a CI/CD pipeline running on a self-hosted Act Runner. The pipeline builds and deploys a Hugo-based static site to staging or production entirely within the local container infrastructure. Static content is served via dedicated Nginx instances for production and staging environments, with staging restricted behind the VPN layer. TLS certificates are automated using Certbot with DNS-01 validation.

### Core Ecosystem Components

* **Mail Infrastructure** relies on a self-hosted, Dockerized Mailcow suite. The deployment involves rigid DNS configurations including SPF, DKIM, and DMARC policies to maintain optimal deliverability.
* **Observability Suite** integrates Prometheus, Grafana, and Loki. Host and container metrics are collected dynamically via Node Exporter and cAdvisor, while logs are aggregated via Promtail to achieve full environment transparency.
* **Data Resilience** leverages Borgmatic to execute encrypted scheduled backups via cron, ensuring both local redundancy and offsite data preservation.

---

## 🛠️ Service Deployment Matrix

The table below lists the operational roles and deployment models chosen for each component of the cloud environment.

<div align="center">

| Service                             | Role                                |
| ----------------------------------- | ----------------------------------- |
| [Reverse Proxy (Nginx + ModSecurity)](./main-server/core/nginx-reverse-proxy/) | Secure entry point with WAF         |
| [WireGuard](./main-server/core/wireguard/)                           | Private access to internal services |
| [MailCow](./mail-server/)                               | Self-hosted Dockerized Mail Suite |
| [Gitea](./main-server/services/gitea/)                               | Self-hosted Git platform            |
| [Gitea Act Runner](./main-server/services/gitea-act-runner/)                    | CI/CD runner     |
| [Nginx (Public)](./main-server/services/nginx-prod/)                      | Static content delivery             |
| [Nginx (Staging)](./main-server/services/nginx-staging/)                     | Isolated staging environment        |
| [Certbot](./main-server/core/certbot/)                             | TLS certificate automation          |
| [Prometheus](./main-server/monitoring/)                          | Metrics collection                  |
| [Grafana](./main-server/monitoring/)                             | Metrics visualization               |
| [Loki + Promtail](./main-server/monitoring/)                     | Log aggregation                     |
| [Node Exporter](./main-server/monitoring/)                       | Host monitoring                     |
| [cAdvisor](./main-server/monitoring/)                            | Container monitoring                |
| [Borgmatic](./main-server/backup/borgmatic/)                           | Backup automation                   |

</div>
