## Automated Subdomain Reconnaissance Framework

Bash script to automate subdomain reconnaissance for bug bounty and pentesting.  
It combines multiple tools for enumeration, resolution, and live host discovery, and can send results directly to Telegram Bot.
-----------------------------------------------------------------------

## Features
- Subdomain enumeration with:
    - [Subfinder]
    - [Assetfinder]
    - [Amass]
-  Merge and deduplicate results into a single list
-  DNS resolution with [dnsx]
-  Live host detection with [httpx]
-  Notifications to Telegram bot using [notify]
