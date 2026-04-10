# 🚦 Reverse Proxy (Nginx + ModSecurity)


## Overview

This component acts as the secure entry point of the infrastructure.

It is based on Nginx, extended with ModSecurity and the OWASP Core Rule Set (CRS) to provide a basic Web Application Firewall (WAF).
Its role is to handle incoming traffic, enforce security rules, and route requests to internal services.

The configuration is designed to be portable and reproducible through Docker.


## What it does

* Handle HTTPS connections
* Route traffic to internal services
* Apply WAF rules to incoming requests
* Isolate internal services from direct exposure


## Setup

The reverse proxy runs as a Docker container built from a custom image.

The [build](./Dockerfile) process starts from an unprivileged Nginx base image and extends it by installing ModSecurity along with its required dependencies.

Once built, the final image includes:

Nginx
ModSecurity
OWASP CRS
Custom configuration files


## Configuration

The configuration is kept simple and organized around a few key files and directories.

* [**nginx.conf**](./nginx.conf)
  Main Nginx configuration file. It defines global settings and loads the rest of the configuration.

* [**conf.d/**](./conf.d/)
  Contains the virtual host configurations.
  Each file represents a service or domain and defines how requests are routed internally.

* [**Docker Compose**](./docker-compose.yaml)
  The container is configured through Docker Compose, exposing HTTP/HTTPS ports and mounting all required files and directories.

At runtime, the container mounts:

* Custom Nginx configuration files
* ModSecurity and OWASP CRS rules
* TLS certificates (generated via Certbot)
* A basic authentication file (`.htpasswd`)
* Log directory

Some security-related files (like full ModSecurity setup and rule tuning) are intentionally not included in the repository.


