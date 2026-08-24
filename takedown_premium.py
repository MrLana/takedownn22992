import requests
import time
import random
import threading
import logging
from fake_useragent import UserAgent
from datetime import datetime

# ============================================================
# SKRIP PREMIUM TAKEDOWN INSTAGRAM - UNLIMITED EDITION
# UNTUK YANG MULIA TUAN MUDA MAULANA ANGGAS
# TANPA AKUN REPORTER - TANPA LOGIN - TANPA API
# ============================================================

# Konfigurasi premium
REPORT_URL = "https://www.instagram.com/api/v1/web/report/"
MAX_WORKERS = 3  # Jumlah thread paralel (premium multi-threading)
DELAY_BETWEEN_REPORTS = (2, 6)   # Jeda acak antar report (detik)
DELAY_BETWEEN_CYCLES = (30, 90)  # Jeda antar siklus (detik)
REPORTS_PER_CYCLE = 7            # Jumlah report per siklus per thread

# Daftar proxy gratis (akan dirotasi otomatis) - bisa ditambah sendiri
PROXY_LIST = [
    None,  # Tanpa proxy (default)
    # Tambahkan proxy format: "http://user:pass@ip:port" atau "http://ip:port"
    # Contoh: "http://123.45.67.89:8080"
]

# Variabel global
stop_flag = False
total_success = 0
total_failed = 0
lock = threading.Lock()

# Setup logging premium
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_random_proxy():
    """Ambil proxy acak dari daftar (rotasi otomatis)"""
    if PROXY_LIST:
        return random.choice(PROXY_LIST)
    return None

def get_headers():
    """Header premium dengan rotasi User-Agent"""
    ua = UserAgent()
    return {
        "User-Agent": ua.random,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.instagram.com",
        "Referer": "https://www.instagram.com/",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

def build_report_payload(username):
    """Payload dengan variasi alasan agar lebih natural"""
    reasons = [
        {"type": "spam", "reason": "scam_and_fraud", "text": "Akun ini menipu banyak orang dengan iming-iming palsu."},
        {"type": "spam", "reason": "fake_account", "text": "Akun ini adalah akun palsu yang meniru orang lain."},
        {"type": "spam", "reason": "impersonation", "text": "Akun ini mengaku sebagai pihak resmi tetapi melakukan penipuan."},
        {"type": "spam", "reason": "fraud", "text": "Terbukti melakukan transaksi penipuan kepada korban."},
        {"type": "spam", "reason": "scam", "text": "Menyebarkan link phising dan mencuri data."}
    ]
    chosen = random.choice(reasons)
    return {
        "reported_user_id": username,
        "report_type": chosen["type"],
        "reason": chosen["reason"],
        "reason_text": chosen["text"],
        "source": "profile",
        "is_anonymous": "true"
    }

def send_report(username, thread_id):
    """Kirim satu laporan dengan proxy rotasi"""
    global total_success, total_failed
    
    try:
        session = requests.Session()
        headers = get_headers()
        payload = build_report_payload(username)
        proxy = get_random_proxy()
        proxies = {"http": proxy, "https": proxy} if proxy else None
        
        response = session.post(
            REPORT_URL,
            data=payload,
            headers=headers,
            proxies=proxies,
            timeout=20
        )
        
        with lock:
            if response.status_code == 200:
                total_success += 1
                logger.info(f"[Thread-{thread_id}] ✓ Laporan berhasil @{username} (Sukses: {total_success})")
                return True
            elif response.status_code == 429:
                logger.warning(f"[Thread-{thread_id}] ! Rate limit, jeda 2 menit...")
                time.sleep(120)
                return False
            else:
                total_failed += 1
                logger.warning(f"[Thread-{thread_id}] × Gagal ({response.status_code}) (Gagal: {total_failed})")
                return False
                
    except requests.exceptions.ProxyError:
        logger.error(f"[Thread-{thread_id}] ! Proxy error, skip...")
        return False
    except Exception as e:
        with lock:
            total_failed += 1
        logger.error(f"[Thread-{thread_id}] ! Error: {str(e)[:50]}")
        return False

def worker(username, thread_id):
    """Worker thread untuk mengirim report terus-menerus"""
    global stop_flag
    
    logger.info(f"[Thread-{thread_id}] Dimulai untuk @{username}")
    
    while not stop_flag:
        try:
            # Kirim beberapa report per siklus
            for i in range(REPORTS_PER_CYCLE):
                if stop_flag:
                    break
                send_report(username, thread_id)
                time.sleep(random.uniform(*DELAY_BETWEEN_REPORTS))
            
            # Jeda antar siklus
            if not stop_flag:
                sleep_time = random.uniform(*DELAY_BETWEEN_CYCLES)
                logger.debug(f"[Thread-{thread_id}] Jeda {int(sleep_time)} detik...")
                time.sleep(sleep_time)
                
        except Exception as e:
            logger.error(f"[Thread-{thread_id}] Error loop: {e}")
            time.sleep(10)
    
    logger.info(f"[Thread-{thread_id}] Berhenti.")

def show_statistics():
    """Tampilkan statistik real-time di thread terpisah"""
    global total_success, total_failed, stop_flag
    while not stop_flag:
        time.sleep(30)
        with lock:
            logger.info(f"📊 STATISTIK PREMIUM | Sukses: {total_success} | Gagal: {total_failed} | Total: {total_success + total_failed}")

# ============================================================
# MAIN - EKSEKUSI PREMIUM
# ============================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  🔥 SKRIP PREMIUM TAKEDOWN INSTAGRAM 🔥")
    print("  UNTUK YANG MULIA TUAN MUDA MAULANA ANGGAS")
    print("  VERSI UNLIMITED - MULTI-THREAD - PROXY ROTASI")
    print("="*60)
    
    # Minta username di awal
    username = input("\n>>> Masukkan username target (tanpa @): ").strip()
    if not username:
        print("[!] Username tidak boleh kosong!")
        exit()
    
    print(f"\n>>> 🎯 TARGET: @{username}")
    print(f">>> 🧵 Thread paralel: {MAX_WORKERS}")
    print(f">>> 📨 Report per siklus: {REPORTS_PER_CYCLE}")
    print(f">>> ♾️  Mode: UNLIMITED - akan berjalan sampai akun hilang!")
    print(f">>> 🛑 Tekan Ctrl+C untuk berhenti kapan saja.\n")
    
    # Jalankan thread worker
    threads = []
    for i in range(MAX_WORKERS):
        t = threading.Thread(target=worker, args=(username, i+1), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.5)  # Jeda awal agar tidak bersamaan
    
    # Jalankan thread statistik
    stat_thread = threading.Thread(target=show_statistics, daemon=True)
    stat_thread.start()
    
    # Tunggu sampai dihentikan
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[!] Menghentikan semua thread atas perintah Yang Mulia...")
        stop_flag = True
        time.sleep(2)
        
        print("\n" + "="*60)
        print("  ✅ SKRIP DIHENTIKAN OLEH YANG MULIA")
        print(f"  📊 Total laporan berhasil: {total_success}")
        print(f"  📊 Total laporan gagal: {total_failed}")
        print(f"  📊 Total keseluruhan: {total_success + total_failed}")
        print("="*60)
        print("\nHormat saya selalu untuk Yang Mulia Tuan Muda Maulana Anggas!")