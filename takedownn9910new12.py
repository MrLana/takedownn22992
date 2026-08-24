# ================================================================
# TAKEDOWN INSTAGRAM - VERSI PALING MURNI
# 100% TANPA ChromeDriver - TANPA Selenium - TANPA API
# Cukup Input Username -> Spam Report Sampai Hilang!
# Untuk Yang Mulia Putri Incha
# ================================================================

import requests
import time
import random
from datetime import datetime

# ================================================================
# TIDAK ADA KONFIGURASI APAPUN
# ================================================================

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] {msg}")
    with open("takedown_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{t}] {msg}\n")

def cek_akun(username):
    """
    Cek apakah akun masih ada - TANPA login, TANPA API
    """
    try:
        url = f"https://www.instagram.com/{username}/"
        resp = requests.get(url, timeout=10)
        
        # Jika redirect ke login, akun masih ada
        if "login" in resp.url:
            return True
        
        # Jika ada teks "private" atau "posts", akun masih ada
        if "private" in resp.text.lower() or "posts" in resp.text.lower():
            return True
        
        # Jika ada "Sorry" atau "Page Not Found", akun hilang
        if "sorry" in resp.text.lower() or "page not found" in resp.text.lower():
            return False
        
        return True
    except:
        return True

def send_report(username):
    """
    Kirim laporan ke Instagram - TANPA login, TANPA email, TANPA API
    """
    try:
        # Data minimal
        data = {
            "username": username,
            "reason": "Impersonation",
            "description": f"Laporkan akun @{username} karena melanggar aturan Instagram."
        }
        
        # Kirim ke form bantuan Instagram
        resp = requests.post(
            "https://help.instagram.com/contact/165475033626097",
            data=data,
            timeout=15
        )
        
        if resp.status_code in [200, 201, 202, 204]:
            return True
        return False
    except:
        return False

def main():
    print("\n" + "="*60)
    print("   🔥 TAKEDOWN INSTAGRAM - MURNI 🔥")
    print("   TANPA ChromeDriver - TANPA Login - TANPA API")
    print("   Untuk Yang Mulia Putri Incha")
    print("="*60 + "\n")
    
    target = input("Masukkan username Instagram target: ").strip()
    if not target:
        print("❌ Username tidak boleh kosong!")
        return
    
    log(f"🎯 Target: @{target}")
    
    # Cek akun
    log("🔍 Mengecek akun target...")
    if not cek_akun(target):
        log("❌ AKUN TIDAK DITEMUKAN!")
        return
    log("✅ AKUN TERKONFIRMASI ADA!")
    
    # Spam report
    log("\n🚀 MEMULAI SPAM REPORT...")
    log("="*60)
    
    loop = 0
    success = 0
    failed = 0
    
    while True:
        loop += 1
        log(f"\n--- PUTARAN KE-{loop} ---")
        
        # Cek target masih ada?
        if not cek_akun(target):
            log("\n" + "🎉"*35)
            log("🎉🎉🎉 SELAMAT, YANG MULIA! 🎉🎉🎉")
            log("AKUN TARGET TELAH TAKEDOWN/HILANG!")
            log("🎉"*35)
            log(f"📊 Total laporan: {success+failed} | Berhasil: {success} | Gagal: {failed}")
            log("✅ AKUN SUDAH TIDAK BISA DICARI!")
            break
        
        # Kirim 3-10 laporan
        jumlah = random.randint(3, 10)
        log(f"📤 Mengirim {jumlah} laporan...")
        
        for i in range(jumlah):
            log(f"  [{i+1}/{jumlah}] Mengirim...")
            if send_report(target):
                success += 1
            else:
                failed += 1
            time.sleep(random.uniform(2, 5))
        
        log(f"📊 Statistik: ✅ {success} berhasil | ❌ {failed} gagal")
        log(f"⏳ Istirahat 3-5 menit...")
        time.sleep(random.randint(180, 300))

if __name__ == "__main__":
    main()