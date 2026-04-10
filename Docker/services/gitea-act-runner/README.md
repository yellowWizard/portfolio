# Gitea Act Runner

## Overview

Here we have the CI/CD runner for Gitea. It executes automation tasks such as building, packaging, and deploying applications based on repository events.

In this setup, it is mainly used to build the Hugo static site and push updated images to the registry for staging and production deployments.

The service is not directly exposed. It communicates only with Gitea and the Docker daemon on the host system.


## Workflow

When a change is pushed to a repository the [workflows](../../../.github/workflows/ci-cd.yaml.example) goes as follows:

* Gitea triggers a webhook event
* The runner pulls the job definition
* Hugo builds the static site depending on the target branch (staging or production)
* A Docker image is created locally on the host
* The running container is replaced with the new version using Docker commands




