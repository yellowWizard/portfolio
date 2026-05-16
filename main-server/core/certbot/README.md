# 🔐 Certbot (DNS-01 + Njalla)


## Overview

Here I'm using Certbot with the DNS-01 challenge through Njalla, allowing wildcard certificates to be generated and used across the infrastructure.

Certificates are shared with other services (like the reverse proxy) through a Docker volume.


## What is does

* Issue TLS certificates
* Automatically renew certificates
* Provide wildcard certificate support
* Share certificates with other containers


## Setup

The service runs from a custom Docker image based on Certbot.

The image extends the official base by adding support for the Njalla DNS plugin, which is required for DNS-based validation.


## How it works

It runs only when needed, triggered by a scheduled [cron job](./crontab).

When executed, the process works as follows:

* Certbot runs the `renew` command using the Njalla DNS plugin
* DNS-01 validation is performed to prove domain ownership
* Certificates are issued or renewed and stored in a shared Docker volume (`certbot_certs`)
* A deploy hook adjusts file permissions to ensure compatibility with services running as non-root users
* The reverse proxy is reloaded to apply the updated certificates


## Todo

* Improve secret management (e.g. Docker secrets)
* Reduce reliance on Docker socket
* Clean up permission handling

