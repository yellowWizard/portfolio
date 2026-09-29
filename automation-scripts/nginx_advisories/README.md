# Nginx Security Monitor

This script scrapes the official Nginx security advisories page to check if a specific version in use is vulnerable. 

If it detects new vulnerabilities not yet recorded in the local JSON file, it updates the archive and sends an immediate notification via a Telegram bot.

