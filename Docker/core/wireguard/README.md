# WireGuard VPN

## Overview

This service provides private access to the internal infrastructure using WireGuard VPN.

It allows secure connectivity to services that are not exposed publicly, such as internal dashboards and staging environments.

The setup is based on a prebuilt and stable Docker image, with minimal custom configuration.


## Configuration

The main adjustment required on the host system was enabling packet forwarding through UFW:

* `DEFAULT_FORWARD_POLICY=ACCEPT`

This allows VPN traffic to be routed correctly between clients and internal networks.

Aside from this, no additional networking changes were needed.


