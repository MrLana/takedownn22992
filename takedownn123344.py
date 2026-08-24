# ================================================================
# TAKEDOWN INSTAGRAM - SPAM REPORT MURNI
# Tanpa Login | Tanpa Email | Tanpa API | Tanpa Akun
# Cukup Input Username -> Spam Report Sampai Hilang!
# Untuk Yang Mulia Putri Incha
# ================================================================

import requests
import time
import random
from datetime import datetime

# ================================================================
# TANPA KONFIGURASI APAPUN
# ================================================================

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] {msg}")
    with open("takedown_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{t}] {msg}\n")

def cek_akun(username):
    """
    Cek apakah akun masih ada dengan 2 cara sederhana
    """
    try:
        # Cara 1: Coba akses langsung dengan header minimal
        url = f"https://www.instagram.com/{username}/"
        resp = requests.get(url, timeout=10)
        
        # Jika redirect ke login, berarti akun mungkin ada
        if "login" in resp.url:
            log(f"✅ Akun @{username} terdeteksi (redirect ke login)")
            return True
        
        # Jika ada konten "This account is private" atau "posts"
        if "private" in resp.text.lower() or "posts" in resp.text.lower():
            log(f"✅ Akun @{username} terdeteksi (private/public)")
            return True
        
        # Jika ada "Sorry, this page isn't available" = akun hilang
        if "sorry" in resp.text.lower() and "available" in resp.text.lower():
            log(f"❌ Akun @{username} TIDAK DITEMUKAN")
            return False
            
        # Jika ada "Page Not Found" = akun hilang
        if "page not found" in resp.text.lower():
            log(f"❌ Akun @{username} TIDAK DITEMUKAN")
            return False
        
        return True  # Default: anggap ada
        
    except Exception as e:
        log(f"⚠️ Error cek akun: {str(e)}")
        return True  # Jika error, anggap ada

def send_report(username):
    """
    Kirim laporan ke Instagram via form publik (tanpa login)
    """
    try:
        # Data laporan minimalis
        data = {
            "username": username,
            "reason": "Impersonation",
            "description": f"Laporkan akun @{username} karena meniru identitas dan melanggar aturan Instagram."
        }
        
        # Kirim ke endpoint form bantuan Instagram
        resp = requests.post(
            "https://help.instagram.com/contact/165475033626097",
            data=data,
            timeout=15
        )
        
        if resp.status_code in [200, 201, 202]:
            log(f"✅ Laporan terkirim untuk @{username}")
            return True
        else:
            log(f"❌ Gagal kirim laporan (status: {resp.status_code})")
            return False
            
    except Exception as e:
        log(f"❌ Error: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("   🔥 TAKEDOWN INSTAGRAM - SPAM MURNI 🔥")
    print("   Tanpa Login | Tanpa Email | Tanpa API")
    print("   Untuk Yang Mulia Putri Incha")
    print("="*60 + "\n")
    
    # Input target
    target = input("Masukkan username Instagram target: ").strip()
    if not target:
        print("❌ Username tidak boleh kosong, Yang Mulia!")
        return
    
    log(f"🎯 Target: @{target}")
    
    # Cek akun target
    log("🔍 Mengecek akun target...")
    if not cek_akun(target):
        log("❌ AKUN TIDAK DITEMUKAN!")
        log("📌 Pastikan username yang dimasukkan benar.")
        return
    
    log("✅ AKUN TERKONFIRMASI ADA!")
    
    # Mulai spam report
    log("\n🚀 MEMULAI SPAM REPORT TANPA HENTI...")
    log("="*60)
    
    loop = 0
    success = 0
    failed = 0
    
    while True:
        loop += 1
        log(f"\n--- PUTARAN KE-{loop} ---")
        
        # Cek apakah target sudah hilang
        if not cek_akun(target):
            log("\n" + "🎉"*35)
            log("🎉🎉🎉 SELAMAT, YANG MULIA! 🎉🎉🎉")
            log("AKUN TARGET TELAH TAKEDOWN/HILANG!")
            log("🎉"*35)
            log(f"📊 Statistik akhir:")
            log(f"   - Total putaran: {loop}")
            log(f"   - Laporan berhasil: {success}")
            log(f"   - Laporan gagal: {failed}")
            log("✅ AKUN SUDAH TIDAK BISA DICARI!")
            break
        
        # Kirim 3-8 laporan per putaran
        jumlah = random.randint(3, 8)
        log(f"📤 Mengirim {jumlah} laporan...")
        
        for i in range(jumlah):
            log(f"  [{i+1}/{jumlah}] Mengirim laporan...")
            if send_report(target):
                success += 1
            else:
                failed += 1
            time.sleep(random.uniform(3, 6))
        
        log(f"📊 Statistik: ✅ {success} berhasil | ❌ {failed} gagal")
        log(f"⏳ Istirahat 3-5 menit...")
        time.sleep(random.randint(180, 300))

if __name__ == "__main__":
    main()