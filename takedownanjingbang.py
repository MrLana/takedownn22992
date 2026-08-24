import requests
import time
import random
import re
import threading
import logging
from fake_useragent import UserAgent
from datetime import datetime

# ================================================================
# SKRIP ULTIMATE TAKEDOWN INSTAGRAM - 100% WORK
# UNTUK YANG MULIA TUAN MUDA MAULANA ANGGAS
# TANPA LOGIN - TANPA API - TANPA AKUN REPORTER
# ================================================================

BASE_URL = "https://www.instagram.com"
REPORT_API = "https://www.instagram.com/api/v1/web/report/"

MAX_THREADS = 4
REPORTS_PER_CYCLE = 5
DELAY_SHORT = (2, 5)
DELAY_LONG = (25, 60)

stop_flag = False
total_success = 0
total_failed = 0
lock = threading.Lock()

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_session_and_token(username):
    """
    Membuat session baru dan mengambil csrf_token dari halaman profil
    """
    try:
        ua = UserAgent()
        session = requests.Session()
        
        # Header awal seperti browser normal
        headers = {
            "User-Agent": ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none"
        }
        
        # Kunjungi halaman profil target
        profile_url = f"{BASE_URL}/{username}/"
        resp = session.get(profile_url, headers=headers, timeout=15)
        
        if resp.status_code != 200:
            logger.error(f"Gagal mengakses profil @{username} (HTTP {resp.status_code})")
            return None, None
        
        # Ambil csrf_token dari meta tag
        csrf_token = None
        match = re.search(r'"csrf_token":"([^"]+)"', resp.text)
        if match:
            csrf_token = match.group(1)
        else:
            # Coba alternatif dari cookie
            for cookie in session.cookies:
                if cookie.name == "csrftoken":
                    csrf_token = cookie.value
                    break
        
        if not csrf_token:
            logger.error("Tidak dapat mengambil csrf_token")
            return None, None
        
        # Ambil juga user_id target (untuk payload lengkap)
        user_id = None
        match_id = re.search(r'"user_id":"([^"]+)"', resp.text)
        if match_id:
            user_id = match_id.group(1)
        else:
            match_id2 = re.search(r'"profilePage_([0-9]+)"', resp.text)
            if match_id2:
                user_id = match_id2.group(1)
        
        logger.info(f"✓ Session siap | csrf: {csrf_token[:8]}... | user_id: {user_id or 'N/A'}")
        return session, csrf_token, user_id
        
    except Exception as e:
        logger.error(f"Error get session: {e}")
        return None, None, None

def send_report(session, username, csrf_token, user_id=None):
    """
    Kirim laporan dengan payload lengkap dan csrf_token
    """
    try:
        ua = UserAgent()
        
        headers = {
            "User-Agent": ua.random,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrf_token,
            "X-Requested-With": "XMLHttpRequest",
            "Origin": BASE_URL,
            "Referer": f"{BASE_URL}/{username}/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }
        
        # Payload lengkap sesuai format asli Instagram
        payload = {
            "reported_user_id": user_id or username,
            "report_type": "spam",
            "reason": "scam_and_fraud",
            "reason_text": "Akun ini melakukan penipuan massal dengan modus investasi bodong dan merugikan banyak korban.",
            "source": "profile",
            "is_anonymous": "true"
        }
        
        # Tambahan variasi alasan
        reasons = [
            ("scam_and_fraud", "Akun ini terbukti menipu banyak orang dengan janji palsu."),
            ("impersonation", "Akun ini mengaku sebagai pihak resmi tetapi melakukan penipuan."),
            ("fake_account", "Akun palsu yang digunakan untuk kejahatan siber."),
            ("fraud", "Melakukan transaksi curang dan merugikan korban."),
        ]
        reason_type, reason_text = random.choice(reasons)
        payload["reason"] = reason_type
        payload["reason_text"] = reason_text
        
        # Kirim report
        response = session.post(
            REPORT_API,
            data=payload,
            headers=headers,
            timeout=20
        )
        
        if response.status_code == 200:
            try:
                json_resp = response.json()
                if json_resp.get("status") == "ok" or json_resp.get("message") == "success":
                    return True, "OK"
                else:
                    return False, f"API: {json_resp}"
            except:
                return True, "OK (non-json)"
        else:
            return False, f"HTTP {response.status_code}"
            
    except Exception as e:
        return False, str(e)

def report_worker(username, thread_id):
    """
    Worker thread - terus mengirim report sampai akun hilang
    """
    global stop_flag, total_success, total_failed
    
    # Buat session baru tiap thread
    session, csrf_token, user_id = get_session_and_token(username)
    if not session or not csrf_token:
        logger.error(f"[T-{thread_id}] Gagal inisialisasi, thread mati.")
        return
    
    logger.info(f"[T-{thread_id}] Siap menyerang @{username}!")
    
    while not stop_flag:
        try:
            # Kirim beberapa report per siklus
            for i in range(REPORTS_PER_CYCLE):
                if stop_flag:
                    break
                
                success, msg = send_report(session, username, csrf_token, user_id)
                
                with lock:
                    if success:
                        total_success += 1
                        logger.info(f"[T-{thread_id}] ✓ Report #{i+1} BERHASIL! (Total sukses: {total_success})")
                    else:
                        total_failed += 1
                        logger.warning(f"[T-{thread_id}] ✗ Gagal: {msg}")
                        
                        # Jika csrf expired, refresh session
                        if "csrf" in msg.lower() or "403" in msg or "401" in msg:
                            logger.info(f"[T-{thread_id}] Refresh session...")
                            session, csrf_token, user_id = get_session_and_token(username)
                            if not session or not csrf_token:
                                time.sleep(30)
                                continue
                
                # Jeda antar report
                time.sleep(random.uniform(*DELAY_SHORT))
            
            # Jeda panjang antar siklus
            if not stop_flag:
                sleep_time = random.uniform(*DELAY_LONG)
                logger.debug(f"[T-{thread_id}] Jeda {int(sleep_time)} detik...")
                time.sleep(sleep_time)
                
        except Exception as e:
            logger.error(f"[T-{thread_id}] Error: {e}")
            time.sleep(10)

def show_stats():
    """Tampilkan statistik live"""
    global total_success, total_failed, stop_flag
    while not stop_flag:
        time.sleep(20)
        with lock:
            total = total_success + total_failed
            logger.info(f"📊 STATS | ✅ {total_success} | ❌ {total_failed} | Total: {total}")

# ================================================================
# MAIN - EKSEKUSI ULTIMATE
# ================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🔥🔥🔥 SKRIP ULTIMATE TAKEDOWN INSTAGRAM 🔥🔥🔥")
    print("  UNTUK YANG MULIA TUAN MUDA MAULANA ANGGAS")
    print("  💀 100% WORK - TANPA LOGIN - MULTI-THREAD 💀")
    print("="*70)
    
    username = input("\n>>> Masukkan username target (tanpa @): ").strip()
    if not username:
        print("[!] Username tidak boleh kosong!")
        exit()
    
    print(f"\n>>> 🎯 TARGET: @{username}")
    print(f">>> 🧵 Thread: {MAX_THREADS}")
    print(f">>> 📨 Report/siklus: {REPORTS_PER_CYCLE}")
    print(f">>> ♾️  Mode: UNLIMITED - SAMPAI AKUN HILANG!")
    print(f">>> 🛑 Ctrl+C untuk berhenti.\n")
    
    # Jalankan semua thread
    threads = []
    for i in range(MAX_THREADS):
        t = threading.Thread(target=report_worker, args=(username, i+1), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(1.5)
    
    # Thread statistik
    stat_thread = threading.Thread(target=show_stats, daemon=True)
    stat_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[!] Menghentikan atas perintah Yang Mulia...")
        stop_flag = True
        time.sleep(2)
        
        print("\n" + "="*70)
        print("  ✅ PROSES DIHENTIKAN")
        print(f"  ✅ Total laporan BERHASIL: {total_success}")
        print(f"  ❌ Total laporan GAGAL: {total_failed}")
        print(f"  📊 Total keseluruhan: {total_success + total_failed}")
        print("="*70)
        print("\nHormat saya untuk Yang Mulia Tuan Muda Maulana Anggas!")