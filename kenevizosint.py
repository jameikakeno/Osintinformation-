import time
import os
import sys
import subprocess
import platform
import socket
import requests
import phonenumbers
import phonenumbers.timezone
import phonenumbers.carrier
import phonenumbers.geocoder
import whois
import random
import threading
import concurrent.futures
import hashlib
import uuid

KIRMIZI = '\033[91m'
YESIL = '\033[92m'
SARI = '\033[93m'
MAVI = '\033[94m'
MOR = '\033[95m'
CAM = '\033[96m'
BEYAZ = '\033[97m'
KALIN = '\033[1m'
RENK_SIFIRLA = '\033[0m'

def temizle():
    os.system('cls' if os.name == 'nt' else 'clear')

def keneviz_banner():
    
    temizle()
    print(f"""
{YESIL}{KALIN}            _  __      {KIRMIZI}OSINT Information Tool{YESIL}    _         
{YESIL}           | |/ /   ___   _ __     ___  __   __ (_)  ____  
{YESIL}           | ' /   / _ \\ | '_ \\   / _ \\ \\ \\ / / | | |_  /  
{YESIL}           | . \\  |  __/ | | | | |  __/  \\ V /  | |  / /   
{YESIL}           |_|\\_\\  \\___| |_| |_|  \\___|   \\_/   |_| /___|  
{CAM}                           Dev : Keneviz
{YESIL}══════════════════════════════════════════════════════════════{RENK_SIFIRLA}
    """)

def keneviz_menu():
    print(f"""
{YESIL}[1]{BEYAZ} Telefon Numarası Sorgula
{YESIL}[2]{BEYAZ} Domain/Web Sitesi Sorgula
{YESIL}[3]{BEYAZ} Kullanıcı Adı Sorgula
{YESIL}[4]{BEYAZ} IP Adresi Sorgula
{YESIL}[5]{BEYAZ} Veritabanında Ara
{YESIL}[6]{BEYAZ} MAC Adresi Sorgula
{KIRMIZI}[7]{BEYAZ} Çıkış
{SARI}══════════════════════════════════════════════════════════════{RENK_SIFIRLA}
    """)

def telefon_sorgula():
    telefon = input(f"{CAM}[?] Telefon numarası girin (uluslararası format): {RENK_SIFIRLA}")
    
    try:
        parsed = phonenumbers.parse(telefon, None)
        
        if not phonenumbers.is_valid_number(parsed):
            print(f"{KIRMIZI}[-] Geçersiz telefon numarası!{RENK_SIFIRLA}")
            return
        
        operator = phonenumbers.carrier.name_for_number(parsed, "tr")
        ulke = phonenumbers.geocoder.description_for_number(parsed, "tr")
        bolge = phonenumbers.geocoder.description_for_number(parsed, "en")
        formatli = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        gecerli = phonenumbers.is_valid_number(parsed)
        olasilik = phonenumbers.is_possible_number(parsed)
        saat_dilimi = phonenumbers.timezone.time_zones_for_number(parsed)
        
        print(f"""
{YESIL}[+] Telefon: {formatli}
[+] Ülke: {ulke}
[+] Bölge: {bolge}
[+] Operatör: {operator}
[+] Geçerli: {gecerli}
[+] Olası: {olasilik}
[+] Saat Dilimi: {saat_dilimi}
[+] Telegram: https://t.me/{telefon}
[+] WhatsApp: https://wa.me/{telefon}
{RENK_SIFIRLA}""")
        
    except Exception as e:
        print(f"{KIRMIZI}[-] Hata: {e}{RENK_SIFIRLA}")

def domain_sorgula():
    domain = input(f"{CAM}[?] Domain adı girin (ornek.com): {RENK_SIFIRLA}")
    
    try:
        domain_info = whois.whois(domain)
        
        print(f"""
{YESIL}[+] Domain: {domain_info.domain_name}
[+] Oluşturulma: {domain_info.creation_date}
[+] Bitiş: {domain_info.expiration_date}
[+] Kayıt Sahibi: {domain_info.registrant_name}
[+] Organizasyon: {domain_info.registrant_organization}
[+] Ülke: {domain_info.registrant_country}
[+] DNS Sunucuları: {domain_info.name_servers}
{RENK_SIFIRLA}""")
        
    except Exception as e:
        print(f"{KIRMIZI}[-] Hata: {e}{RENK_SIFIRLA}")

def kullanici_sorgula():
    nick = input(f"{CAM}[?] Kullanıcı adı girin: {RENK_SIFIRLA}")
    
    siteler = {
        "Instagram": f"https://www.instagram.com/{nick}",
        "TikTok": f"https://www.tiktok.com/@{nick}",
        "Twitter": f"https://twitter.com/{nick}",
        "Facebook": f"https://www.facebook.com/{nick}",
        "YouTube": f"https://www.youtube.com/@{nick}",
        "Telegram": f"https://t.me/{nick}",
        "Roblox": f"https://www.roblox.com/user.aspx?username={nick}",
        "Twitch": f"https://www.twitch.tv/{nick}",
        "GitHub": f"https://github.com/{nick}",
        "Reddit": f"https://www.reddit.com/user/{nick}",
        "Pinterest": f"https://www.pinterest.com/{nick}",
        "Spotify": f"https://open.spotify.com/user/{nick}"
    }
    
    print(f"\n{SARI}[*] {len(siteler)} platform taranıyor...{RENK_SIFIRLA}\n")
    
    for site, url in siteler.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"{YESIL}[+] {site}: {url}{RENK_SIFIRLA}")
            else:
                print(f"{KIRMIZI}[-] {site}: Bulunamadı (HTTP {response.status_code}){RENK_SIFIRLA}")
        except:
            print(f"{KIRMIZI}[-] {site}: Hata{RENK_SIFIRLA}")

def ip_sorgula():
    ip = input(f"{CAM}[?] IP adresi girin: {RENK_SIFIRLA}")
    
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        data = response.json()
        
        if data.get("status") == "fail":
            print(f"{KIRMIZI}[-] Hata: {data.get('message', 'Bilinmeyen hata')}{RENK_SIFIRLA}")
            return
        
        print(f"""
{YESIL}[+] IP: {data.get('query')}
[+] Ülke: {data.get('country')}
[+] Ülke Kodu: {data.get('countryCode')}
[+] Bölge: {data.get('regionName')} ({data.get('region')})
[+] Şehir: {data.get('city')}
[+] Posta Kodu: {data.get('zip')}
[+] Enlem: {data.get('lat')}
[+] Boylam: {data.get('lon')}
[+] ISP: {data.get('isp')}
[+] Organizasyon: {data.get('org')}
[+] AS: {data.get('as')}
{RENK_SIFIRLA}""")
        
    except Exception as e:
        print(f"{KIRMIZI}[-] Hata: {e}{RENK_SIFIRLA}")

def veritabaninda_ara():
    path = input(f"{CAM}[?] Veritabanı dosya yolu: {RENK_SIFIRLA}")
    aranan = input(f"{CAM}[?] Aranacak metin: {RENK_SIFIRLA}")
    
    kodlamalar = ['utf-8', 'cp1254', 'latin-1', 'iso-8859-9']
    bulundu = False
    
    for encoding in kodlamalar:
        try:
            with open(path, 'r', encoding=encoding) as f:
                for satir in f:
                    if aranan.lower() in satir.lower():
                        print(f"{YESIL}[+] Bulundu: {satir.strip()}{RENK_SIFIRLA}")
                        bulundu = True
                        break
                if bulundu:
                    break
        except:
            continue
    
    if not bulundu:
        print(f"{KIRMIZI}[-] Metin bulunamadı!{RENK_SIFIRLA}")

def mac_sorgula():
    mac = input(f"{CAM}[?] MAC adresi girin (XX:XX:XX:XX:XX:XX formatında): {RENK_SIFIRLA}")
    
    try:
        # MAC adresini formatla
        mac_clean = mac.upper().replace(':', '').replace('-', '')
        
        if len(mac_clean) != 12:
            print(f"{KIRMIZI}[-] Geçersiz MAC adresi formatı!{RENK_SIFIRLA}")
            return
        
        url = f"https://api.macvendors.com/{mac_clean}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"{YESIL}[+] MAC: {mac}")
            print(f"[+] Üretici: {response.text.strip()}{RENK_SIFIRLA}")
        else:
            print(f"{KIRMIZI}[-] MAC adresi bilgisi bulunamadı!{RENK_SIFIRLA}")
            
    except Exception as e:
        print(f"{KIRMIZI}[-] Hata: {e}{RENK_SIFIRLA}")

def keneviz_ana_menu():
    while True:
        try:
            keneviz_banner()
            keneviz_menu()
            
            secim = input(f"{CAM}[?] Seçiminiz: {RENK_SIFIRLA}")
            
            if secim == "1":
                telefon_sorgula()
            elif secim == "2":
                domain_sorgula()
            elif secim == "3":
                kullanici_sorgula()
            elif secim == "4":
                ip_sorgula()
            elif secim == "5":
                veritabaninda_ara()
            elif secim == "6":
                mac_sorgula()
            elif secim == "7":
                print(f"\n{YESIL}Keneviz OSINT Tool kullandığınız için teşekkürler!{RENK_SIFIRLA}")
                sys.exit()
            else:
                print(f"\n{KIRMIZI}Geçersiz seçenek!{RENK_SIFIRLA}")
            
            input(f"\n{CAM}[?] Devam etmek için ENTER'e basın...{RENK_SIFIRLA}")
            
        except KeyboardInterrupt:
            print(f"\n\n{KIRMIZI}Çıkış yapılıyor...{RENK_SIFIRLA}")
            sys.exit()

if __name__ == "__main__":
    keneviz_ana_menu()
