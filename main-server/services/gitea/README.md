# 🗂️ Gitea


## Overview

A self-hosted Git platform used to manage source code and repositories for the infrastructure and CI/CD workflows. 

The service is only accessible through the WireGuard VPN and the reverse proxy.

Authentication is required to access repositories and administrative features.


## Setup

Gitea runs as a Docker container using the official image, with persistent storage for repositories, configuration, and metadata.

It is integrated with the rest of the stack and works closely with the CI/CD runner to automate builds and deployments.

