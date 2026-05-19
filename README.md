# Multi-Domain Systems and Network Engineering Portfolio

This repository serves as a centralized technical portfolio demonstrating practical engineering experience across infrastructure deployment, automation, systems administration, and advanced network design. 

---

## Repository Architecture


* **[Self-Hosted Infrastructure:](./self-hosted-vps)** contains the configuration files for containerized applications running on a public cloud VPS, managed via local docker-compose files and monitored via an observability stack.
* **[Network Lab Environments:](./cisco-network-lab)** hosts Cisco Packet Tracer simulations and network topologies, starting with a multi-site infrastructure built around a 3-tier hierarchy featuring routing, gateway redundancy, and centralized wireless connectivity.


---
## Project Summary

### Systems & DevOps
* **Containerization** implements Docker and Docker Compose to manage and deploy internal services.
* **Reverse Proxy** handles external traffic via Nginx integrated with ModSecurity.
* **Automation** utilizes Gitea with a self-hosted runner to execute a Hugo-based static website deployment pipeline.
* **Observability** collects system telemetry and logs using Prometheus, Grafana, and Loki.

### Network Architecture
* **Topology Design** organizes the local network layout into Core, Distribution, and Access layers.
* **Routing Setup** manages inter-site connectivity over IPv4 and IPv6 subnets using the OSPF protocol.
* **Redundancy Configuration** provides backup gateways for the local subnets via HSRPv2.
* **Wireless Deployment** integrates Lightweight Access Points controlled centrally by a WLC through Layer 3 CAPWAP tunnels and DHCP Option 43.

---
