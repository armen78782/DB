import requests

LEAKCHECK_API = "cd7838a05a1cf8a1354b20e31098bfa08ae1bfa7"
DEHASHED_USER = "email@domain.com"
DEHASHED_PASS = "your_password"

def check_leakcheck(query):
    try:
        r = requests.get(f"https://leakcheck.io/api/search?key={LEAKCHECK_API}&query={query}")
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def check_dehashed(query):
    try:
        r = requests.get(
            f"https://api.dehashed.com/search?query={query}",
            auth=(DEHASHED_USER, DEHASHED_PASS)
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def check_truecaller(phone_number):
    print(f"[!] Проверь Truecaller вручную: https://www.truecaller.com/search/ru/{phone_number}")

def check_telegram(phone_number):
    print(f"[!] Проверь Telegram вручную или через импорт контакта в приложении")

def check_whatsapp(phone_number):
    print(f"[!] Проверь WhatsApp: https://wa.me/{phone_number}")

def search_all(number_or_email):
    print(f"\n\033[1;36mПоиск информации для: {number_or_email}\033[0m")

    print("\n\033[1;34m[LeakCheck]\033[0m")
    print(check_leakcheck(number_or_email))

    print("\n\033[1;34m[Dehashed]\033[0m")
    print(check_dehashed(number_or_email))

    print("\n\033[1;34m[Truecaller / Telegram / WhatsApp]\033[0m")
    check_truecaller(number_or_email)
    check_telegram(number_or_email)
    check_whatsapp(number_or_email)

if __name__ == "__main__":
    query = input("Введите номер или email: ").strip()
    search_all(query)
