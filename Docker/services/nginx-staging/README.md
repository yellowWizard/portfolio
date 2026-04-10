# Staging Nginx (Hugo Site)

## Overview

This service hosts a staging version of a static Hugo site used to test CI/CD deployments before releasing changes to production.

It can only be accessed through the WireGuard VPN, and even then it is protected by reverse proxy basic authentication to ensure it remains strictly a testing environment.

