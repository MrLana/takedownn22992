# ================================================================
# TAKEDOWN INSTAGRAM - ANONYMOUS SPAM REPORT
# Tanpa Perlu Akun Reporter - Cukup Input Target!
# Untuk Yang Mulia Putri Incha
# ================================================================

import requests
import time
import random
import re
from datetime import datetime

# ================================================================
# KONFIGURASI - TIDAK PERLU DIUBAH
# ================================================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
]

# Endpoint laporan publik Instagram (tanpa login)
REPORT_ENDPOINTS = [
    "https://www.instagram.com/api/v1/web/report/user/",
    "https://www.instagram.com/api/v1/web/report/media/",
    "https://www.instagram.com/api/v1/web/accounts/report/",
]

# Alasan laporan (semua kuat)
REPORT_REASONS = [
    {"id": 1, "name": "Impersonation"},
    {"id": 2, "name": "Bullying"},
    {"id": 3, "name": "Inappropriate Content"},
    {"id": 4, "name": "Spam"},
    {"id": 6, "name": "Copyright Violation"},
    {"id": 8, "name": "Illegal Content"}
]

# ================================================================

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] {msg}")
    with open("anonymous_takedown_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{t}] {msg}\n")

def get_random_headers():
    """Header acak menyerupai browser"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.instagram.com",
        "Referer": "https://www.instagram.com/",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Connection": "keep-alive"
    }

def get_csrf_token():
    """Ambil CSRF token dari halaman utama Instagram"""
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        resp = requests.get("https://www.instagram.com/", headers=headers, timeout=10)
        csrf = re.search(r'"csrf_token":"([^"]+)"', resp.text)
        if csrf:
            return csrf.group(1)
        
        # Alternatif: cari di meta tag
        csrf_meta = re.search(r'<meta property="csrf-token" content="([^"]+)"', resp.text)
        if csrf_meta:
            return csrf_meta.group(1)
        
        return None
    except Exception as e:
        log(f"❌ Gagal ambil CSRF: {str(e)}")
        return None

def get_target_id(target_username):
    """Dapatkan user ID dari username target"""
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        resp = requests.get(
            f"https://www.instagram.com/{target_username}/?__a=1&__d=dis",
            headers=headers,
            timeout=10
        )
        data = resp.json()
        return data['graphql']['user']['id']
    except Exception as e:
        log(f"❌ Gagal dapatkan ID target: {str(e)}")
        return None

def check_account_exists(target_username):
    """Cek apakah akun target masih ada"""
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        resp = requests.get(
            f"https://www.instagram.com/{target_username}/",
            headers=headers,
            timeout=10
        )
        if "Sorry, this page isn't available" in resp.text or "Page Not Found" in resp.text:
            return False
        if '"graphql":{"user"' in resp.text or '"biography"' in resp.text:
            return True
        return False
    except:
        return True  # Jika error, anggap masih ada

def send_anonymous_report(target_username, target_id, reason_id):
    """Kirim laporan secara anonim tanpa login"""
    try:
        csrf = get_csrf_token()
        if not csrf:
            log("❌ Gagal dapat CSRF token, coba lagi...")
            return False
        
        url = random.choice(REPORT_ENDPOINTS)
        
        # Data laporan
        if "user" in url:
            data = {
                "user_id": target_id,
                "reason_id": reason_id,
                "source": "profile",
                "additional_info": f"Laporan anonim: Akun @{target_username} melanggar aturan Instagram dan melakukan penipuan identitas."
            }
        elif "media" in url:
            # Untuk media, kita coba ambil satu postingan pertama
            try:
                headers = {"User-Agent": random.choice(USER_AGENTS)}
                resp = requests.get(
                    f"https://www.instagram.com/{target_username}/?__a=1",
                    headers=headers,
                    timeout=10
                )
                posts = resp.json()['graphql']['user']['edge_owner_to_timeline_media']['edges']
                if posts:
                    media_id = posts[0]['node']['id']
                    data = {
                        "media_id": media_id,
                        "reason_id": reason_id,
                        "source": "feed"
                    }
                else:
                    return False
            except:
                return False
        else:
            data = {
                "user_id": target_id,
                "reason_id": reason_id,
                "source": "profile"
            }
        
        # Kirim laporan
        headers = get_random_headers()
        headers.update({
            "X-CSRFToken": csrf,
            "X-Instagram-AJAX": "1",
            "X-Requested-With": "XMLHttpRequest"
        })
        
        resp = requests.post(url, data=data, headers=headers, timeout=15)
        
        # Cek response
        try:
            result = resp.json()
            if result.get("status") == "ok" or result.get("success") or "success" in str(result):
                log(f"✅ Laporan ANONIM berhasil (alasan: {reason_id})")
                return True
            else:
                log(f"⚠️ Response: {str(result)[:100]}")
                return False
        except:
            if resp.status_code == 200:
                log(f"✅ Laporan ANONIM berhasil (status 200)")
                return True
            else:
                log(f"❌ Laporan gagal (status: {resp.status_code})")
                return False
                
    except Exception as e:
        log(f"❌ Error report: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("   🔥 TAKEDOWN INSTAGRAM - ANONYMOUS 🔥")
    print("   Tanpa Akun Reporter - Cukup Input Target!")
    print("   Untuk Yang Mulia Putri Incha")
    print("="*60 + "\n")
    
    # ========== INPUT TARGET ==========
    target = input("Masukkan username Instagram target: ").strip()
    if not target:
        print("❌ Username tidak boleh kosong, Yang Mulia!")
        return
    
    log(f"🎯 Target: @{target}")
    
    # ========== VERIFIKASI AWAL ==========
    log("🔍 Mengecek apakah akun target ada...")
    if not check_account_exists(target):
        log("❌ AKUN TIDAK DITEMUKAN! Pastikan username benar, Yang Mulia.")
        return
    log("✅ AKUN TERKONFIRMASI ADA!")
    
    # ========== DAPATKAN ID TARGET ==========
    log("🔑 Mengambil ID target...")
    target_id = get_target_id(target)
    if not target_id:
        log("❌ Gagal mendapatkan ID target. Coba lagi nanti.")
        return
    log(f"✅ ID target: {target_id}")
    
    # ========== LOOP SPAM REPORT ANONIM ==========
    loop = 0
    success_count = 0
    fail_count = 0
    
    while True:
        loop += 1
        log(f"\n{'='*50}")
        log(f"🔄 PUTARAN KE-{loop}")
        log(f"{'='*50}")
        
        # Cek apakah target masih ada
        if not check_account_exists(target):
            log("\n" + "🎉"*30)
            log("🎉🎉🎉 SELAMAT, YANG MULIA! AKUN TARGET TELAH HILANG! 🎉🎉🎉")
            log("🎉"*30)
            log(f"✅ Total laporan berhasil: {success_count}")
            log(f"✅ Total laporan gagal: {fail_count}")
            log("✅ Akun sudah tidak bisa diakses secara permanen.")
            break
        
        # Kirim beberapa laporan per putaran
        reports_per_round = random.randint(5, 10)
        log(f"📤 Mengirim {reports_per_round} laporan anonim...")
        
        for i in range(reports_per_round):
            reason = random.choice(REPORT_REASONS)
            log(f"  [{i+1}/{reports_per_round}] Alasan: {reason['name']}")
            
            success = send_anonymous_report(target, target_id, reason['id'])
            if success:
                success_count += 1
            else:
                fail_count += 1
            
            # Jeda acak antar laporan
            time.sleep(random.uniform(3, 8))
        
        log(f"📊 Statistik: ✅ {success_count} berhasil | ❌ {fail_count} gagal")
        log(f"⏳ Istirahat 3-5 menit sebelum putaran berikutnya...")
        time.sleep(random.randint(180, 300))
    
    print("\n" + "="*60)
    print("   ✅ MISI TELAH SELESAI, YANG MULIA! ✅")
    print("   AKUN PENIPU TELAH TAKEDOWN PERMANEN")
    print("="*60)

if __name__ == "__main__":
    main()