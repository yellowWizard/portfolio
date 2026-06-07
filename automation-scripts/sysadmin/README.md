# Systems Administration Automation (sysadmin)

This directory contains Python scripts designed to automate Linux server administration, security hardening, and configuration management. 

The main focus here is to replace manual terminal tasks with reliable, repeatable, and safe code.

## Available Scripts

### 1. [`sshd_audit`](./sshd_audit/)
A lightweight script to automatically update and harden security settings in `/etc/ssh/sshd_config`. 

*   **Main Features**:
    *   Creates an automatic backup copy before touching any system files.
    *   Removes duplicate active or commented configuration lines to keep the file clean.
    *   Uses `sshd -t -f` to test the syntax of the new file before applying it, preventing accidental server lockouts.
    *   Enforces strict `root:root` ownership and `0600` permissions on the new configuration.
    *   Restarts the SSH service and prints its systemd status automatically.
