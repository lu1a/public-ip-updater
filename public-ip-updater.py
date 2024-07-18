import requests
import os
import sys


def get_public_ip():
    """Get the current public IP address of the machine using multiple services."""
    urls = [
        'https://api.ipify.org?format=json',
        'https://ipinfo.io/json',
        'https://ifconfig.me/all.json'
    ]

    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            if 'ip' in response.json():
                return response.json()['ip']
            elif 'ip' in response.json().get('ip', ''):
                return response.json()['ip']
        except requests.RequestException:
            continue

    raise Exception("Failed to retrieve public IP address from all services.")


def read_ip_from_file(file_path):
    """Read the IP address from the specified file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            ip = file.read().strip()
            return ip
    return None


def write_ip_to_file(file_path, ip):
    """Write the IP address to the specified file."""
    with open(file_path, 'w') as file:
        file.write(ip)


def call_dummy_api(new_ip, api_key, domain_name):
    """Call a dummy API endpoint with the new IP address and API key."""
    url = 'https://jsonplaceholder.typicode.com/posts'
    payload = {'ip': new_ip, 'CNAME': domain_name}
    headers = {'Authorization': f'Bearer {api_key}'}
#    response = requests.post(url, json=payload, headers=headers)
    print("Would have called: ", url, headers, payload)
    return 201
#    return response.status_code


def main(api_key, domain_name):
    file_path = 'ip_address.txt'
    current_ip = get_public_ip()
    saved_ip = read_ip_from_file(file_path)

    if current_ip != saved_ip:
        print(f"IP has changed from {saved_ip} to {current_ip}")
        write_ip_to_file(file_path, current_ip)
        status_code = call_dummy_api(current_ip, api_key, domain_name)
        print(f"Dummy API called, status code: {status_code}")
    else:
        print("IP address has not changed.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python check_ip.py <namecheap_api_key> <domain_name_to_update>")
        sys.exit(1)
    api_key = sys.argv[1]
    domain_name = sys.argv[2]
    main(api_key, domain_name)

