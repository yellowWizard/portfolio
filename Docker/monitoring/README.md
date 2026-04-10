# 📊 Monitoring


## Overview

This folder contains the monitoring stack used across the infrastructure.

The setup is built around Grafana, Prometheus and Loki to provide a simple but effective observability layer covering metrics, logs and visualization.

All services are exposed through a reverse proxy but are **only accessible via VPN**, so nothing is publicly reachable.


## What it does

This stack gives a full overview of what’s happening inside the infrastructure:

* Collects metrics from the host and containers
* Aggregates logs from Docker workloads
* Provides dashboards and a central UI
* Helps with debugging and basic troubleshooting

It’s not meant to be a full enterprise-grade observability platform, but it covers the essential needs well.


## How it works

At a high level, everything revolves around two data flows: metrics and logs.

Prometheus periodically scrapes metrics from multiple targets, including the host (via node exporter), containers (via cadvisor) and internal services. These metrics are stored as time-series data and later queried by Grafana.

For logs, Promtail discovers running Docker containers and reads their logs directly from the host. It then pushes them to Loki, which stores and indexes them. Grafana connects to Loki to make logs searchable and explorable.

Grafana sits on top of both systems and acts as the single interface to query and visualize everything.


## Todo

* Add alerting (Alertmanager)
* Improve access control in Grafana
* Refine log retention and storage strategy
* Reduce reliance on Docker socket where possible
