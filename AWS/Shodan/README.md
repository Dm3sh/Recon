# AWS Reconnaissance Script using Shodan API

This script automates reconnaissance on various AWS services using the Shodan API. It discovers publicly exposed AWS resources and performs reverse DNS lookups on discovered IP addresses.

## Features

- **AWS Service Discovery:** Searches for instances of AWS services like EC2, S3, RDS, and more using specific Shodan queries.
- **Filtered Results:** Cleans and filters Shodan search results to include only relevant IP addresses.
- **Reverse DNS Lookup:** Performs reverse DNS lookups on discovered IP addresses and saves the results.
- **Organized Output:** Saves IP addresses and reverse DNS results in service-specific directories with timestamped filenames.
- **User-Friendly Interface:** Prompts the user to select an AWS service to scan and provides clear output.

## Prerequisites

- **Shodan API Key:** You need a valid Shodan API key to use this script. (Free Account's API key will not work)
- **Python 3.x:** Ensure Python 3.x is installed on your machine.
- **Shodan Python Library:** Install the Shodan library using pip.


## Set Up Your Shodan API Key

Replace the placeholder API key in the script with your actual Shodan API key:
```python
api_key = 'Your_Shodan_API_Key_Here'
```

## Output (Directory Structure)
After running the script, it will create a directory structure similar to this:

```
Result/
    ├── EC2_Instances/
    │ ├── EC2_Instances_2024-xx-xx_xx-xx-xx.txt
    │ └── EC2_Instances_reverse_dns_2024-xx-xx_xx-xx-xx.txt
    └── S3_Buckets/
    ├── S3_Buckets_2024-xx-xx_xx-xx-xx.txt
    └── S3_Buckets_reverse_dns_2024-xx-xx_xx-xx-xx.txt
```




