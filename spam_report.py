# ================================================================
# TAKEDOWN INSTAGRAM - SPAM REPORT TANPA LOGIN
# Tanpa User-Agent, Tanpa Email, Tanpa Akun
# Cukup Input Target -> Langsung Spam Report!
# Untuk Yang Mulia Putri Incha
# ================================================================

import requests
import time
import random
import re
from datetime import datetime

# ================================================================
# KONFIGURASI - TIDAK PERUBAH APA PUN
# ================================================================

# Headers DEFAULT (tanpa User-Agent khusus)
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://help.instagram.com",
    "Referer": "https://help.instagram.com/",
    "Connection": "keep-alive"
}

# ================================================================

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] {msg}")
    with open("spam_report_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{t}] {msg}\n")

def check_account_exists(username):
    """Cek apakah akun target masih ada (tanpa login)"""
    try:
        resp = requests.get(f"https://www.instagram.com/{username}/", timeout=10)
        if "Sorry, this page isn't available" in resp.text or "Page Not Found" in resp.text:
            return False
        if '"graphql":{"user"' in resp.text or '"biography"' in resp.text:
            return True
        return False
    except Exception as e:
        log(f"⚠️ Error cek akun: {str(e)}")
        return True

def get_csrf_token():
    """Ambil CSRF token dari halaman bantuan Instagram"""
    try:
        resp = requests.get("https://help.instagram.com/contact/", timeout=10)
        csrf = re.search(r'"csrf_token":"([^"]+)"', resp.text)
        if csrf:
            return csrf.group(1)
        # Alternatif
        csrf_meta = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
        if csrf_meta:
            return csrf_meta.group(1)
        return None
    except Exception as e:
        log(f"❌ Gagal ambil CSRF: {str(e)}")
        return None

def send_report(target_username):
    """
    Kirim laporan ke Instagram melalui form publik
    TANPA email, TANPA login, TANPA user-agent khusus
    """
    try:
        # Dapatkan CSRF token
        csrf = get_csrf_token()
        if not csrf:
            log("❌ Gagal dapat CSRF token, coba lagi...")
            return False
        
        # Data laporan (tanpa email, tanpa nama, tanpa telepon)
        # Menggunakan data kosong/minimal agar tetap terkirim
        report_data = {
            "username": target_username,
            "reason": "Impersonation",
            "description": f"""
            LAPORAN URGENT:
            Akun @{target_username} adalah akun penipuan.
            - Menggunakan identitas orang lain
            - Menyebarkan konten ilegal
            - Melanggar aturan Instagram
            - Merugikan banyak orang
            
            Saya meminta akun ini segera dihapus permanen.
            """,
            "source": "web_report",
            "csrf_token": csrf
        }
        
        # Kirim laporan ke endpoint publik
        resp = requests.post(
            "https://help.instagram.com/api/v1/web/contact/submit/",
            data=report_data,
            headers=HEADERS,
            timeout=15
        )
        
        if resp.status_code == 200:
            log(f"✅ Laporan terkirim! (target: @{target_username})")
            return True
        else:
            log(f"❌ Gagal kirim laporan (status: {resp.status_code})")
            return False
            
    except Exception as e:
        log(f"❌ Error: {str(e)}")
        return False

def spam_report_until_gone(target_username):
    """Loop spam report sampai akun hilang"""
    log(f"🎯 Target: @{target_username}")
    
    # Verifikasi awal
    log("🔍 Mengecek akun target...")
    if not check_account_exists(target_username):
        log("❌ AKUN TIDAK DITEMUKAN! Pastikan username benar.")
        return
    
    log("✅ AKUN TERKONFIRMASI ADA! Memulai spam report...")
    
    loop = 0
    success = 0
    failed = 0
    
    while True:
        loop += 1
        log(f"\n{'='*50}")
        log(f"🔄 PUTARAN KE-{loop}")
        log(f"{'='*50}")
        
        # Cek target masih ada?
        if not check_account_exists(target_username):
            log("\n" + "🎉"*30)
            log("🎉🎉🎉 AKUN TARGET TELAH HILANG! 🎉🎉🎉")
            log("🎉"*30)
            log(f"📊 Total: {success+failed} laporan | Berhasil: {success} | Gagal: {failed}")
            log("✅ MISI SELESAI, YANG MULIA!")
            break
        
        # Kirim 5-10 laporan per putaran
        jumlah = random.randint(5, 10)
        log(f"📤 Mengirim {jumlah} laporan...")
        
        for i in range(jumlah):
            log(f"  [{i+1}/{jumlah}] Mengirim laporan...")
            if send_report(target_username):
                success += 1
            else:
                failed += 1
            time.sleep(random.uniform(3, 7))  # Jeda antar laporan
        
        log(f"📊 Statistik: ✅ {success} berhasil | ❌ {failed} gagal")
        log(f"⏳ Istirahat 3-5 menit...")
        time.sleep(random.randint(180, 300))

# ================================================================
# PROGRAM UTAMA
# ================================================================

print("\n" + "="*60)
print("   🔥 SPAM REPORT INSTAGRAM - TANPA LOGIN 🔥")
print("   Tanpa User-Agent, Tanpa Email, Tanpa Akun")
print("   Untuk Yang Mulia Putri Incha")
print("="*60 + "\n")

target = input("Masukkan username Instagram target: ").strip()

if not target:
    print("❌ Username tidak boleh kosong!")
else:
    spam_report_until_gone(target)

print("\n" + "="*60)
print("   ✅ SKRIP SELESAI, YANG MULIA! ✅")
print("="*60)