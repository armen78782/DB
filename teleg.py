import requests
import re
import dns.resolver
import argparse
from datetime import datetime

# Конфигурация API (замените ключи при необходимости)
API_KEYS = {
    'abuseipdb': 'ваш_ключ',
    'virustotal': 'ваш_ключ'
}

def validate_ip(ip):
    ipv4_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    return re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip)

def get_geo_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719")
        return response.json() if response.json()['status'] == 'success' else None
    except:
        return None

def get_whois_info(ip):
    try:
        response = requests.get(f"http://ipwhois.app/json/{ip}")
        return response.json()
    except:
        return None

def get_threat_info(ip):
    try:
        headers = {'Key': API_KEYS['abuseipdb']}
        response = requests.get(
            f"https://api.abuseipdb.com/api/v2/check",
            headers=headers,
            params={'ipAddress': ip, 'maxAgeInDays': 90}
        )
        return response.json()['data'] if response.status_code == 200 else None
    except:
        return None

def get_virustotal_info(ip):
    try:
        headers = {'x-apikey': API_KEYS['virustotal']}
        response = requests.get(
            f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
            headers=headers
        )
        return response.json() if response.status_code == 200 else None
    except:
        return None

def get_dns_records(domain):
    try:
        result = {}
        for qtype in ['A', 'AAAA', 'MX', 'TXT', 'NS']:
            answers = dns.resolver.resolve(domain, qtype, raise_on_no_answer=False)
            result[qtype] = [str(r) for r in answers]
        return result
    except:
        return None

def print_full_report(ip):
    print("\n\033[1;36m" + "="*40)
    print(f"Полный отчет для {ip}")
    print("="*40 + "\033[0m")

    # Гео-информация
    if geo := get_geo_info(ip):
        print("\n\033[1;34m[Геолокация]\033[0m")
        print(f"Страна: {geo.get('country', 'N/A')}")
        print(f"Город: {geo.get('city', 'N/A')}")
        print(f"Координаты: {geo.get('lat', 'N/A')}, {geo.get('lon', 'N/A')}")
        print(f"Провайдер: {geo.get('isp', 'N/A')}")

    # Whois информация
    if whois := get_whois_info(ip):
        print("\n\033[1;34m[WHOIS]\033[0m")
        print(f"Регистратор: {whois.get('isp', 'N/A')}")
        print(f"ASN: {whois.get('asn', 'N/A')}")
        print(f"Диапазон: {whois.get('range', 'N/A')}")

    # Информация об угрозах
    if threat := get_threat_info(ip):
        print("\n\033[1;34m[Угрозы]\033[0m")
        print(f"Уровень угрозы: {threat.get('abuseConfidenceScore', 0)}%")
        print(f"Последний отчет: {threat.get('lastReportedAt', 'N/A')}")
        print(f"Всего отчетов: {threat.get('totalReports', 0)}")

    # VirusTotal информация
    if vt := get_virustotal_info(ip):
        print("\n\033[1;34m[VirusTotal]\033[0m")
        stats = vt.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
        print(f"Вредоносные: {stats.get('malicious', 0)}")
        print(f"Подозрительные: {stats.get('suspicious', 0)}")

def main_menu():
    while True:
        print("\n\033[1;36m=== Главное меню ===")
        print("1. Проверить IP-адрес")
        print("2. Проверить домен")
        print("3. Выход\033[0m")

        choice = input("\nВыберите действие: ").strip()

        if choice == '1':
            ip = input("Введите IP-адрес: ").strip()
            if validate_ip(ip):
                print_full_report(ip)
            else:
                print("\033[1;31mНеверный формат IP!\033[0m")

        elif choice == '2':
            domain = input("Введите домен: ").strip()
            if records := get_dns_records(domain):
                print("\n\033[1;34m[DNS Записи]\033[0m")
                for qtype, values in records.items():
                    print(f"{qtype}: {', '.join(values) if values else 'N/A'}")
            else:
                print("\033[1;31mОшибка получения DNS записей!\033[0m")

        elif choice == '3':
            print("\nВыход...")
            break

        else:
            print("\033[1;31mНеверный выбор!\033[0m")

if __name__ == "__main__":
    main_menu()
