# ============================================================
# SKRIP TAKEDOWN INSTAGRAM - VERSI AGGRESIF & PERMANEN
# Untuk Keperluan Yang Mulia Putri Incha
# ============================================================
# Fitur:
# - Loop tak terbatas sampai akun target hilang (manual stop dengan CTRL+C)
# - Rotasi akun pelapor otomatis
# - Rotasi alasan laporan (Spam, Peniruan, Pelecehan, Konten berbahaya)
# - Jeda acak + anti-deteksi
# - Auto-refresh jika terjadi error
# - Menyimpan log laporan

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import os
from datetime import datetime

# ========== KONFIGURASI YANG MULIA ==========
TARGET_USERNAME = "username_penipu"  # Ganti dengan username penipu
OFFENDING_URL = "https://www.instagram.com/p/CONTOH_POST/"  # Ganti dengan link postingan wajah Anda

# Daftar akun pelapor (tambahkan sebanyak mungkin, Yang Mulia)
REPORTER_ACCOUNTS = [
    {"email": "akun1@gmail.com", "pass": "password1"},
    {"email": "akun2@gmail.com", "pass": "password2"},
    {"email": "akun3@gmail.com", "pass": "password3"},
    # ... tambahkan sampai puluhan / ratusan untuk hasil maksimal
]

# Alasan laporan yang dirotasi
REPORT_REASONS = [
    "Spam",                # Spam
    "It's impersonating me",  # Peniruan identitas
    "It's bullying or harassment",  # Pelecehan
    "It's inappropriate content"   # Konten tidak pantas
]

# ========== FUNGSI BANTUAN ==========
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open("takedown_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def random_delay(min_sec=5, max_sec=15):
    time.sleep(random.uniform(min_sec, max_sec))

def create_driver():
    chrome_options = Options()
    # Anti-deteksi: nonaktifkan otomatisasi
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # User-agent acak
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
    # Mode headless jika diperlukan (hilangkan tanda # di bawah untuk mode tanpa tampilan)
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def login_instagram(driver, email, password):
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        random_delay(3, 6)
        username_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = driver.find_element(By.NAME, "password")
        username_field.clear()
        username_field.send_keys(email)
        password_field.clear()
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        random_delay(5, 10)
        # Lewati "Save Info" dan notifikasi
        for btn_text in ["Not Now", "Save Info"]:
            try:
                btn = driver.find_element(By.XPATH, f"//button[contains(text(), '{btn_text}')]")
                btn.click()
                random_delay(2, 4)
            except:
                pass
        return True
    except Exception as e:
        log(f"Login gagal untuk {email}: {str(e)}")
        return False

def report_post(driver, post_url, reason):
    try:
        driver.get(post_url)
        random_delay(4, 8)
        # Klik tombol "..." (more options)
        more_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button']//*[name()='svg' and @aria-label='More options']"))
        )
        more_btn.click()
        random_delay(2, 4)
        # Klik Report
        report_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Report')]"))
        )
        report_btn.click()
        random_delay(2, 4)
        # Pilih alasan sesuai parameter
        if reason == "Spam":
            option_xpath = "//span[contains(text(), 'Spam')]"
        elif reason == "It's impersonating me":
            option_xpath = "//span[contains(text(), 'Impersonating')]"
        elif reason == "It's bullying or harassment":
            option_xpath = "//span[contains(text(), 'Bullying') or contains(text(), 'Harassment')]"
        else:
            option_xpath = "//span[contains(text(), 'Inappropriate')]"
        reason_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        reason_option.click()
        random_delay(2, 4)
        # Klik Submit
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
        )
        submit_btn.click()
        random_delay(3, 6)
        # Tutup notifikasi selesai
        try:
            done_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Done')]")
            done_btn.click()
        except:
            pass
        return True
    except Exception as e:
        log(f"Gagal melapor: {str(e)}")
        return False

# ========== EKSEKUSI UTAMA (LOOP TAK HINGGA) ==========
log("===== MULAI TAKEDOWN MASSAL UNTUK YANG MULIA =====")
log(f"Target: {TARGET_USERNAME} | URL: {OFFENDING_URL}")
log(f"Jumlah akun pelapor: {len(REPORTER_ACCOUNTS)}")

counter = 0
while True:
    counter += 1
    log(f"\n--- PUTARAN LAPORAN KE-{counter} ---")
    
    for acc in REPORTER_ACCOUNTS:
        driver = None
        try:
            driver = create_driver()
            log(f"Mencoba login dengan {acc['email']}")
            if login_instagram(driver, acc['email'], acc['pass']):
                reason = random.choice(REPORT_REASONS)
                log(f"Melaporkan dengan alasan: {reason}")
                success = report_post(driver, OFFENDING_URL, reason)
                if success:
                    log(f"✓ Laporan berhasil dari {acc['email']}")
                else:
                    log(f"✗ Laporan gagal dari {acc['email']}")
            else:
                log(f"✗ Login gagal untuk {acc['email']}, lewati.")
            random_delay(10, 20)  # Jeda antar akun
        except Exception as e:
            log(f"Error tak terduga: {str(e)}")
        finally:
            if driver:
                driver.quit()
                random_delay(5, 10)
    
    log(f"Selesai putaran ke-{counter}. Istirahat 2-5 menit sebelum ulangi lagi...")
    time.sleep(random.randint(120, 300))  # Jeda panjang antar siklus

# Catatan: Loop akan berjalan selamanya sampai Anda hentikan manual (CTRL+C)