import shodan
import time
import datetime
import os
import threading

# Initialize the Shodan API client
api_key = ''  #### Replace with your Shodan API key ####
api = shodan.Shodan(api_key)

# Define Shodan dorks for various AWS services with more detailed queries
aws_dorks = {
    'EC2 Instances': [
        'port:80 org:"Amazon.com Inc." hostname:"*.compute.amazonaws.com"',
        'port:443 org:"Amazon.com Inc." hostname:"*.compute.amazonaws.com"'
    ],
    'S3 Buckets': [
        's3.amazonaws.com',
        'bucket.s3.amazonaws.com'
    ],
    'RDS Instances': [
        'rds.amazonaws.com',
        'port:3306 rds.amazonaws.com',
        'port:5432 rds.amazonaws.com'
    ],
    'Elastic Beanstalk': [
        'elasticbeanstalk.com',
        'elasticbeanstalk.com port:80',
        'elasticbeanstalk.com port:443'
    ],
    'CloudFront': [
        'cloudfront.net',
        'cloudfront.net port:80',
        'cloudfront.net port:443'
    ],
    'Elastic Load Balancer': [
        'elb.amazonaws.com',
        'elb.amazonaws.com port:80',
        'elb.amazonaws.com port:443'
    ],
    'API Gateway': [
        'execute-api.amazonaws.com',
        'execute-api.amazonaws.com port:443'
    ],
    'Lambda': [
        'lambda.amazonaws.com',
        'lambda.amazonaws.com port:443'
    ]
}

# Function to search Shodan for given dorks and return cleaned results
def search_shodan(dorks):
    results_by_dork = {}
    for dork in dorks:
        try:
            # Search Shodan with the specified dork
            results = api.search(dork)
            
            # Print the number of results found
            print(f'Results found for "{dork}": {results["total"]}')
            
            # Iterate through the results and clean the output
            cleaned_results = []
            for result in results['matches']:
                if 'http' in result and result['http']['status'] == 200 and '.' in result['ip_str']:  # Filter by HTTP status 200 and IPv4
                    if result['http']['status'] not in [400, 403]:  # Exclude HTTP status codes 400 and 403
                        cleaned_results.append(result['ip_str'])
            
            results_by_dork[dork] = cleaned_results
        except shodan.APIError as e:
            print(f'Error: {e}')
            results_by_dork[dork] = []
        # Pause between queries to avoid rate limits
        time.sleep(1)
    
    return results_by_dork

# Function to perform reverse DNS lookup and save results to a file
def perform_reverse_dns(ip_addresses, service):
    reverse_dns_results = {}
    for ip in ip_addresses:
        try:
            host = api.host(ip)
            if 'hostnames' in host:
                hostnames = host['hostnames']
            else:
                hostnames = ['No reverse DNS records found']

            reverse_dns_results[ip] = hostnames
        except shodan.APIError as e:
            print(f'Error: {e}')
            reverse_dns_results[ip] = ['Error occurred during reverse DNS lookup']

        # Pause between queries to avoid rate limits
        time.sleep(1)

    # Save reverse DNS results to a file
    return save_reverse_dns_results(reverse_dns_results, service)

def save_reverse_dns_results(reverse_dns_results, service):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'{service}_reverse_dns_{timestamp}.txt'
    service_folder = service.replace(' ', '_')  # Replace spaces with underscores for folder name
    output_dir = os.path.join('Result', service_folder)
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        for ip, hostnames in reverse_dns_results.items():
            f.write(f'IP: {ip}\n')
            f.write('Hostnames:\n')
            for hostname in hostnames:
                f.write(f'- {hostname}\n')
            f.write('\n')
    
    return filepath

# Function to save IP addresses to a file with a timestamped filename in the service folder
def save_ip_addresses(ip_addresses, service):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'{service}_{timestamp}.txt'
    service_folder = service.replace(' ', '_')  # Replace spaces with underscores for folder name
    output_dir = os.path.join('Result', service_folder)
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        for ip in ip_addresses:
            f.write(f'{ip}\n')
    
    return filepath

# Function to print the banner
def print_banner():
    banner = """
    ╔════════════════════════════════════════════════╗
    ║                                                ║
    ║           *** AWS Reconnaissance ***           ║
    ║                                                ║
    ╚════════════════════════════════════════════════╝
    """
    print(banner)

# Function to get user input for the service to scan
def get_user_choice():
    print("Select the AWS service you want to scan for:")
    for i, (service, _) in enumerate(aws_dorks.items(), 1):
        print(f"{i}. {service}")
    
    choice = input("Enter the number of your choice: ")
    if choice.isdigit() and 1 <= int(choice) <= len(aws_dorks):
        service = list(aws_dorks.keys())[int(choice) - 1]
        return service
    else:
        print("Invalid choice. Please enter a valid number.")
        return get_user_choice()

# Function to display a loading indicator while performing reverse DNS lookup
def loading_indicator():
    while True:
        for symbol in "|/-\\":
            print(f"\rPerforming reverse DNS lookup... {symbol}", end="", flush=True)
            time.sleep(0.1)

# Main script logic
def main_script():
    print_banner()
    # Get the user's choice of AWS service to scan
    service = get_user_choice()
    dorks = aws_dorks[service]

    # Search Shodan and display the results
    results_by_dork = search_shodan(dorks)
    all_results = []
    for dork, results in results_by_dork.items():
        print(f'--- Results for "{dork}" ---')
        for result in results:
            print(result)
        all_results.extend(results)
        print()

    # Save the IP addresses to a file in the service folder
    ip_file = save_ip_addresses(all_results, service)
    print(f'IP addresses saved to {ip_file}')

    # Start the loading indicator in a separate thread
    loading_thread = threading.Thread(target=loading_indicator)
    loading_thread.daemon = True
    loading_thread.start()

    # Perform reverse DNS lookup and save results to a file in the service folder
    reverse_dns_file = perform_reverse_dns(all_results, service)
    print(f'\nReverse DNS results saved to {reverse_dns_file}')

if __name__ == "__main__":
    main_script()
