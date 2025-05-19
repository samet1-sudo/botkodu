from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Giriş bilgilerin
USERNAME = "sametgungor767@gmail.com"
PASSWORD = "discord1234"
EPISODE_URL = "https://anm.cx/titles/66/one-piece/season/1/episode/950"

# Tarayıcı ayarları
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Giriş sayfasına git
driver.get("https://anm.cx/login")

# E-posta ve şifre alanlarını doldur
email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "login-email"))
)
email_input.send_keys(USERNAME)

password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "login-password"))
)
password_input.send_keys(PASSWORD)

# Giriş yap
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
)
login_button.click()
print("🔐 Giriş yapılıyor...")

# Giriş sonrası bekle
time.sleep(5)

# Bölüm sayfasına git
driver.get(EPISODE_URL)
print("🎬 Bölüm sayfasına gidildi.")

# Şimdi İzle butonuna tıkla
try:
    now_watch_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@mattooltip='Şimdi İzle']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", now_watch_button)
    time.sleep(1)
    ActionChains(driver).move_to_element(now_watch_button).click().perform()
    print("✅ 'Şimdi izle' butonuna tıklandı.")

    # Otomatik geçiş tuşu kontrolü
    time.sleep(5)
    auto_next_toggle = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "mat-slide-toggle-3"))
    )

    if "mat-checked" not in auto_next_toggle.get_attribute("class"):
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", auto_next_toggle)
        time.sleep(1)
        auto_next_toggle.click()
        print("🔁 Otomatik geçiş açıldı.")
    else:
        print("🔁 Otomatik geçiş zaten açık.")

except Exception as e:
    print("❌ Hata oluştu:", str(e))

# 5 dakikada bir 'Sonraki Bölüm' tuşuna tıklama döngüsü
try:
    print("⏳ 5 dakikada bir 'Sonraki Bölüm'e geçilecek.")
    while True:
        time.sleep(300)  # 5 dakika bekle (300 saniye)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-grad') and contains(text(), '')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
            time.sleep(1)
            next_button.click()
            print("➡️ 5 dakika doldu, 'Sonraki Bölüm'e geçildi.")
        except Exception as inner_e:
            print("⚠️ 'Sonraki Bölüm' butonuna tıklanamadı:", str(inner_e))

except KeyboardInterrupt:
    print("🛑 Otomasyon durduruldu.")

