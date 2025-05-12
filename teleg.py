import requests
import re

# Конфигурация API
API_KEYS = {
    'abuseipdb': 'ваш_ключ',
    'virustotal': 'ваш_ключ'
}

def validate_ip(ip):
    ipv4_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    return re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip)

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ipwhois.app/json/{ip}")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def get_threat_info(ip):
    try:
        headers = {'Key': API_KEYS['abuseipdb']}
        response = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
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

def print_full_report(ip):
    print("\n\033[1;36m" + "="*50)
    print(f"ПОЛНЫЙ ОТЧЁТ ПО IP: {ip}")
    print("="*50 + "\033[0m")

    if info := get_ip_info(ip):
        print("\n\033[1;34m[Основная информация]\033[0m")
        print(f"IP: {info.get('ip', 'N/A')}")
        print(f"Тип IP: {'Публичный' if info.get('type') == 'ipv4' else info.get('type', 'N/A')}")
        print(f"Страна: {info.get('country', 'N/A')} ({info.get('country_code', '')})")
        print(f"Регион: {info.get('region', 'N/A')}")
        print(f"Город: {info.get('city', 'N/A')}")
        print(f"Континент: {info.get('continent', 'N/A')}")
        print(f"Координаты: {info.get('latitude', 'N/A')}, {info.get('longitude', 'N/A')}")
        print(f"Часовой пояс: {info.get('timezone', 'N/A')}")

        print("\n\033[1;34m[Сеть и организация]\033[0m")
        print(f"ASN: {info.get('asn', 'N/A')}")
        print(f"Организация: {info.get('org', 'N/A')}")
        print(f"Провайдер: {info.get('isp', 'N/A')}")
        print(f"Диапазон: {info.get('range', 'N/A')}")
        print(f"Домашняя страница: {info.get('asn_org', 'N/A')}")

        print("\n\033[1;34m[Анализ приватности]\033[0m")
        print(f"VPN: {'Да' if info.get('vpn') else 'Нет'}")
        print(f"Прокси: {'Да' if info.get('proxy') else 'Нет'}")
        print(f"TOR: {'Да' if info.get('tor') else 'Нет'}")
        print(f"Мобильный: {'Да' if info.get('mobile') else 'Нет'}")

    if threat := get_threat_info(ip):
        print("\n\033[1;34m[AbuseIPDB Отчёт]\033[0m")
        print(f"Уровень угрозы: {threat.get('abuseConfidenceScore', 0)}%")
        print(f"Последний отчёт: {threat.get('lastReportedAt', 'N/A')}")
        print(f"Всего отчётов: {threat.get('totalReports', 0)}")
        print(f"Категории угроз: {', '.join(str(cat) for cat in threat.get('reportCategories', []))}")

    if vt := get_virustotal_info(ip):
        print("\n\033[1;34m[VirusTotal Статистика]\033[0m")
        stats = vt.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
        print(f"Malicious: {stats.get('malicious', 0)}")
        print(f"Suspicious: {stats.get('suspicious', 0)}")
        print(f"Harmless: {stats.get('harmless', 0)}")
        print(f"Undetected: {stats.get('undetected', 0)}")
        print(f"Дата анализа: {vt.get('data', {}).get('attributes', {}).get('last_analysis_date', 'N/A')}")

def main():
    print("\n\033[1;36m== IP Анализатор ==\033[0m")
    ip = input("Введите IP-адрес: ").strip()
    if validate_ip(ip):
        print_full_report(ip)
    else:
        print("\033[1;31mНеверный формат IP!\033[0m")

if __name__ == "__main__":
    main()
