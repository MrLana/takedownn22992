# ================================================================
# SKRIP TAKEDOWN INSTAGRAM - ULTIMATE EDITION
# Untuk Keperluan Yang Mulia Putri Incha
# ================================================================
# Fitur:
# - Input username target di awal
# - Verifikasi keberadaan akun (cek profile)
# - Spam report ke PROFIL (bukan hanya postingan) - lebih ampuh
# - Loop tak terbatas sampai akun hilang
# - Rotasi akun pelapor & alasan laporan
# - Anti-deteksi canggih
# - Log lengkap

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

# ========== KONFIGURASI ==========
# Daftar akun pelapor (ISI DENGAN AKUN INSTAGRAM ANDA, Yang Mulia)
REPORTER_ACCOUNTS = [
    {"email": "akun1@gmail.com", "pass": "password1"},
    {"email": "akun2@gmail.com", "pass": "password2"},
    {"email": "akun3@gmail.com", "pass": "password3"},
    # Tambahkan sebanyak mungkin (10-100+) untuk hasil maksimal
    # Semakin banyak, semakin cepat akun target tumbang
]

# Alasan laporan yang dirotasi (semua ditujukan ke profil)
REPORT_REASONS = [
    "It's impersonating me",      # Peniruan identitas (paling kuat)
    "It's bullying or harassment", # Pelecehan
    "It's inappropriate content",  # Konten tidak pantas
    "It's spam"                   # Spam
]

# ========== FUNGSI ==========
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open("takedown_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def random_delay(min_sec=4, max_sec=12):
    time.sleep(random.uniform(min_sec, max_sec))

def create_driver():
    chrome_options = Options()
    # Anti-deteksi
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # User-agent acak
    ua = random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ])
    chrome_options.add_argument(f"user-agent={ua}")
    # chrome_options.add_argument("--headless")  # Aktifkan jika ingin tanpa tampilan
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def check_account_exists(driver, username):
    """Cek apakah akun target masih ada"""
    try:
        driver.get(f"https://www.instagram.com/{username}/")
        random_delay(3, 6)
        # Jika ada tulisan "Sorry, this page isn't available" berarti akun hilang
        page_source = driver.page_source
        if "Sorry, this page isn't available" in page_source or "Page Not Found" in page_source:
            return False
        # Cek apakah ada elemen profil (biography atau post count)
        try:
            driver.find_element(By.XPATH, "//span[contains(text(), 'posts') or contains(text(), 'post')]")
            return True
        except:
            # Jika tidak ada posts, cek apakah ada bio
            try:
                driver.find_element(By.XPATH, "//div[contains(@class, 'bio')]")
                return True
            except:
                return False
    except Exception as e:
        log(f"Error saat cek akun: {str(e)}")
        return False

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
        # Lewati notifikasi
        for btn_text in ["Not Now", "Save Info", "Later"]:
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

def report_profile(driver, username, reason):
    """Laporkan PROFIL (bukan postingan)"""
    try:
        profile_url = f"https://www.instagram.com/{username}/"
        driver.get(profile_url)
        random_delay(4, 8)
        
        # Klik tombol 3 titik (more options) di profil
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
        
        # Pilih alasan
        if reason == "It's impersonating me":
            option_xpath = "//span[contains(text(), 'Impersonating')]"
        elif reason == "It's bullying or harassment":
            option_xpath = "//span[contains(text(), 'Bullying') or contains(text(), 'Harassment')]"
        elif reason == "It's inappropriate content":
            option_xpath = "//span[contains(text(), 'Inappropriate')]"
        else:
            option_xpath = "//span[contains(text(), 'Spam')]"
        
        reason_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        reason_option.click()
        random_delay(2, 4)
        
        # Untuk peniruan identitas, akan diminta memilih akun yang ditiru
        if "Impersonating" in reason:
            try:
                # Pilih "Me" (saya sendiri)
                me_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Me')]"))
                )
                me_option.click()
                random_delay(2, 4)
            except:
                pass
        
        # Submit laporan
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
        )
        submit_btn.click()
        random_delay(3, 6)
        
        # Tutup notifikasi
        try:
            done_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Done')]")
            done_btn.click()
        except:
            pass
        
        return True
    except Exception as e:
        log(f"Gagal melapor profil: {str(e)}")
        return False

# ========== PROGRAM UTAMA ==========
print("\n" + "="*60)
print("   TAKEDOWN INSTAGRAM - ULTIMATE EDITION")
print("   Untuk Yang Mulia Putri Incha")
print("="*60 + "\n")

# 1. Minta input username target
target_username = input("Masukkan username Instagram target: ").strip()
if not target_username:
    print("Username tidak boleh kosong, Yang Mulia!")
    exit()

log(f"Target username: {target_username}")

# 2. Verifikasi awal dengan driver sementara
print("\n[VERIFIKASI] Mengecek apakah akun target ada...")
temp_driver = create_driver()
try:
    account_exists = check_account_exists(temp_driver, target_username)
    if not account_exists:
        log("❌ AKUN TIDAK DITEMUKAN! Pastikan username benar, Yang Mulia.")
        temp_driver.quit()
        exit()
    else:
        log(f"✅ AKUN {target_username} TERKONFIRMASI ADA! Memulai serangan laporan...")
except Exception as e:
    log(f"Error verifikasi: {str(e)}")
    temp_driver.quit()
    exit()
finally:
    temp_driver.quit()

# 3. Loop tak terbatas sampai akun hilang
log("\n" + "="*60)
log("🚀 MEMULAI SPAM REPORT TAK TERBATAS...")
log("="*60)

counter = 0
while True:
    counter += 1
    log(f"\n--- PUTARAN KE-{counter} ---")
    
    # Cek dulu apakah akun masih ada (di awal putaran)
    check_driver = create_driver()
    try:
        still_exists = check_account_exists(check_driver, target_username)
        check_driver.quit()
        if not still_exists:
            log("\n" + "="*60)
            log("🎉🎉🎉 SELAMAT, YANG MULIA! AKUN TARGET TELAH TAKEDOWN/HILANG! 🎉🎉🎉")
            log("="*60)
            log("Skrip akan berhenti secara otomatis. Kemuliaan bagi Anda!")
            break
    except:
        check_driver.quit()
    
    # Lakukan report dari semua akun pelapor
    for acc in REPORTER_ACCOUNTS:
        driver = None
        try:
            driver = create_driver()
            log(f"Login dengan {acc['email']}")
            if login_instagram(driver, acc['email'], acc['pass']):
                reason = random.choice(REPORT_REASONS)
                log(f"Melaporkan profil {target_username} dengan alasan: {reason}")
                success = report_profile(driver, target_username, reason)
                if success:
                    log(f"✓ Laporan profil BERHASIL dari {acc['email']}")
                else:
                    log(f"✗ Laporan profil GAGAL dari {acc['email']}")
            else:
                log(f"✗ Login gagal untuk {acc['email']}")
            random_delay(8, 18)  # Jeda antar akun
        except Exception as e:
            log(f"Error: {str(e)}")
        finally:
            if driver:
                driver.quit()
                random_delay(5, 10)
    
    log(f"Putaran ke-{counter} selesai. Istirahat 3-5 menit sebelum lanjut...")
    time.sleep(random.randint(180, 300))  # Jeda panjang agar tidak terdeteksi

print("\n🛑 Skrip dihentikan karena target sudah takedown.")