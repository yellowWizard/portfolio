# SSHD Configuration Audit Script

A simple Python script to automatically update security settings in `/etc/ssh/sshd_config`. 

## How It Works

I designed this script to safely automate configuration changes. It follows a step-by-step process to avoid breaking the SSH service:

1. **Root Check**: The script immediately checks if it is running as `root`. If not, it stops to prevent permission errors.
2. **Backup**: It creates a copy of the original configuration file before making any changes.
3. **Duplicate Clean-up**: It reads the file line by line. If a setting is defined multiple times (active or commented out), it updates the first one and deletes the duplicates to keep the file clean.
4. **Temporary Working File**: The script writes everything to a `.tmp` file first, rather than modifying the active configuration directly.
5. **Syntax Check**: Before applying the new file, it tests the syntax using `sshd -t -f`. If there is an error, the script stops and leaves the original file untouched, preventing server lockouts.
6. **Atomic Replace**: If the syntax is correct, it uses `os.replace` to securely swap the temporary file into production in a single step.
7. **Permissions Enforced**: It sets proper ownership (`root:root`) and strict permissions (`0600`) on both the backup and the new configuration file.
8. **Service Restart**: Finally, it restarts the SSH daemon and prints `systemctl status sshd` to verify that everything is running correctly.

## How Text Processing is Handled

The script filters and edits the text of the configuration file using Python string operations:

* It reads each line, strips empty spaces, and if a line starts with `#`, it temporarily removes the symbol to check if a valid SSH option is hidden inside it.
* Splits lines into lists of words and only inspects lines that contain exactly two words (the option name and its value), which is the standard format for simple SSH directives(complex directives containing multiple values are ignored).
* Then it compares the option name with the target keys. If they match, it checks if the value is already correct; if not it replaces the old value with the new one, joins the words back together with a space, and appends a newline character (`\n`) before writing it to the file.
* Finally it checks if there are any mandatory options that were completely missing from the original configuration and adds them if necessary, separating them with clear comment banners.

## Enforced Settings

The script sets the following baseline:
* Custom SSH Port (`Port 2222`)
* No direct root login (`PermitRootLogin no`)
* No password authentication (`PasswordAuthentication no`)
* Public key authentication enabled (`PubkeyAuthentication yes`)

## Requirements
* Python 3.x
* Root privileges

## How to Run It

Since the script modifies system files (`/etc/ssh/sshd_config`), it must be executed with root privileges.

```bash
sudo python3 sshd_audit.py
```



*Note: Make sure to open the new custom port (e.g., 2222) in your firewall before running the script, or you might get locked out of your server.*

