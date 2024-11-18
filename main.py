import requests
from bs4 import BeautifulSoup
import dns.resolver
from concurrent.futures import ThreadPoolExecutor
import random
import time
import socket
from builtwith import builtwith
from ipwhois import IPWhois
import pyfiglet
from colorama import Fore, Style

# Daftar User-Agent untuk rotasi
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/116.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
]

# Fungsi untuk mencari subdomain dengan berbagai mesin pencari
def search_engine_crawl(domain, engine):
    print(Fore.YELLOW + f"\n[INFO] Crawling potential subdomains using {engine}..." + Style.RESET_ALL)
    subdomains = set()
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    search_urls = {
        "google": lambda page: f"https://www.google.com/search?q=site:{domain}&start={10 * (page - 1)}",
        "yandex": lambda page: f"https://yandex.ru/search/?text=site:{domain}&p={page - 1}",
        "bing": lambda page: f"https://www.bing.com/search?q=site:{domain}&first={10 * (page - 1)}",
        "duckduckgo": lambda page: f"https://html.duckduckgo.com/html/?q=site:{domain}&s={10 * (page - 1)}",
    }

    if engine not in search_urls:
        print(Fore.RED + f"[ERROR] Unsupported search engine: {engine}" + Style.RESET_ALL)
        return []

    for page in range(1, 4):  # Crawl multiple pages
        try:
            url = search_urls[engine](page)
            response = requests.get(url, headers=headers, timeout=5)
            time.sleep(random.uniform(2, 5))  # Rate limiting

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href and domain in href:
                        potential_subdomain = href.split("//")[-1].split("/")[0]
                        if domain in potential_subdomain:
                            subdomains.add(potential_subdomain)
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[ERROR] Unable to crawl {engine}: {e}" + Style.RESET_ALL)

    return list(subdomains)

# Fungsi untuk memeriksa apakah subdomain valid menggunakan DNS query
def resolve_subdomain(subdomain):
    try:
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(subdomain, 'A')
        ip_address = answers[0].to_text()
        print(Fore.GREEN + f"[VALID] {subdomain} -> {ip_address}" + Style.RESET_ALL)
        return subdomain, ip_address
    except dns.resolver.NXDOMAIN:
        return None, None
    except Exception as e:
        print(Fore.RED + f"[ERROR] {subdomain}: {e}" + Style.RESET_ALL)
        return None, None

# Fungsi untuk mendapatkan detail CMS menggunakan builtwith
def get_cms_info(url):
    try:
        info = builtwith(url)
        cms = info.get("cms", ["Unknown"])
        return cms
    except Exception as e:
        return [f"Error: {e}"]

# Fungsi untuk mendapatkan detail IP Address menggunakan ipwhois
def get_ip_info(ip_address):
    try:
        obj = IPWhois(ip_address)
        info = obj.lookup_rdap()
        return {
            "asn": info.get("asn", "Unknown"),
            "asn_description": info.get("asn_description", "Unknown"),
            "network": info.get("network", {}).get("name", "Unknown"),
            "country": info.get("network", {}).get("country", "Unknown"),
        }
    except Exception as e:
        return {"error": str(e)}

# Fungsi utama
def main():
    # Banner ASCII
    banner = pyfiglet.figlet_format("Tuwili Sub Domain")
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.LIGHTMAGENTA_EX + "Subdomain Finder and Crawler with Detailed Info" + Style.RESET_ALL)
    print("=" * 50)

    domain = input(Fore.BLUE + "Enter the domain (e.g., example.com): " + Style.RESET_ALL)

    # Crawling subdomain melalui berbagai mesin pencari
    crawled_subdomains = set()
    for engine in ["google", "yandex", "bing", "duckduckgo"]:
        crawled_subdomains.update(search_engine_crawl(domain, engine))

    # Resolusi DNS subdomain yang ditemukan
    print(Fore.YELLOW + "\n[INFO] Resolving DNS records for crawled subdomains..." + Style.RESET_ALL)
    valid_subdomains = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(resolve_subdomain, subdomain) for subdomain in crawled_subdomains]
        for future in futures:
            subdomain, ip = future.result()
            if subdomain:
                valid_subdomains.append((subdomain, ip))

    # Menampilkan hasil
    print(Fore.LIGHTCYAN_EX + "\n=== Results ===" + Style.RESET_ALL)
    if valid_subdomains:
        for subdomain, ip_address in valid_subdomains:
            url = f"http://{subdomain}"
            print(Fore.LIGHTGREEN_EX + f"\nSubdomain: {subdomain}" + Style.RESET_ALL)

            # Deteksi CMS
            cms_info = get_cms_info(url)
            print(Fore.LIGHTYELLOW_EX + f"  CMS: {', '.join(cms_info)}" + Style.RESET_ALL)

            # Resolusi IP dan informasi tambahan
            ip_info = get_ip_info(ip_address)
            print(Fore.LIGHTBLUE_EX + f"  IP Address: {ip_address}" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + f"  ASN: {ip_info.get('asn')}" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + f"  ASN Description: {ip_info.get('asn_description')}" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + f"  Network: {ip_info.get('network')}" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + f"  Country: {ip_info.get('country')}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "No valid subdomains found." + Style.RESET_ALL)

    print(Fore.LIGHTMAGENTA_EX + "\n[INFO] Task completed!" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
