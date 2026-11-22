"""
Mackolik IDDAA sayfasından otomatik veri çekme modülü
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip

def scrape_mackolik_iddaa():
    """
    Mackolik IDDAA sayfasından maç verilerini otomatik çeker
    Returns: (success: bool, data: str, error_msg: str)
    """
    driver = None
    try:
        print("🌐 Chrome tarayıcısı başlatılıyor...")
        
        # Chrome ayarları
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')  # Headless mod
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.page_load_strategy = 'eager'  # Sayfa tamamen yüklenmesini bekleme
        
        # WebDriver başlat
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("📡 Mackolik sayfası açılıyor...")
        driver.get("https://www.mackolik.com/iddaa")
        
        # Sayfa yüklenene kadar bekle - explicit wait kullan
        print("⏳ Sayfa yükleniyor...")
        
        # SAAT/LİG butonlarının yüklenmesini bekle
        try:
            print("🔍 SAAT/LİG butonları bekleniyor...")
            # SAAT butonunun görünmesini bekle (ikisi de aynı anda yüklenir)
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("""
                    const btns = Array.from(document.querySelectorAll('button'));
                    return btns.some(b => b.textContent.trim() === 'SAAT');
                """)
            )
            print("✅ Butonlar yüklendi")
        except Exception as e:
            print(f"⚠️  Butonlar beklenirken timeout, devam ediliyor...")
        
        time.sleep(1)  # Kısa bekleme
        
        # LİG butonuna tıkla - JavaScript ile
        print("🎯 LİG görünümüne geçiliyor...")
        try:
            # Strategi 1: Direkt LİG text'i ara
            script = """
            const allButtons = document.querySelectorAll('button');
            for (let btn of allButtons) {
                const text = btn.textContent.trim();
                if (text === 'LİG') {
                    btn.click();
                    return 'clicked-direct';
                }
            }
            
            // Strategi 2: SAAT butonunu bul, sonraki kardeşi (sibling) LİG olmalı
            for (let btn of allButtons) {
                if (btn.textContent.trim() === 'SAAT') {
                    const parent = btn.parentElement;
                    if (parent) {
                        const ligBtn = Array.from(parent.querySelectorAll('button')).find(b => b.textContent.trim() === 'LİG');
                        if (ligBtn) {
                            ligBtn.click();
                            return 'clicked-sibling';
                        }
                    }
                }
            }
            
            return 'not-found';
            """
            result = driver.execute_script(script)
            
            if 'clicked' in result:
                print(f"✅ LİG butonuna tıklandı ({result})")
                time.sleep(5)  # LİG view yüklensin
            else:
                print(f"⚠️  LİG butonu bulunamadı: {result}")
                
        except Exception as e:
            print(f"⚠️  LİG butonuna tıklama hatası: {str(e)}")
        
        # Sayfayı kaydır (lazy loading için)
        print("📜 Sayfa kaydırılıyor...")
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        print("📋 Sayfa içeriği alınıyor...")
        
        # Body elementini bul ve tüm metni al
        body = driver.find_element(By.TAG_NAME, 'body')
        page_text = body.text
        
        print(f"✅ {len(page_text)} karakter veri çekildi")
        
        driver.quit()
        
        if not page_text or len(page_text) < 100:
            return False, "", "Sayfa içeriği çok kısa veya boş"
        
        return True, page_text, ""
        
    except Exception as e:
        if driver:
            try:
                driver.quit()
            except:
                pass
        error_msg = f"Scraping hatası: {str(e)}"
        print(f"❌ {error_msg}")
        return False, "", error_msg

def scrape_and_process():
    """
    Mackolik'ten veri çeker ve clipboard'a kopyalar
    """
    success, data, error = scrape_mackolik_iddaa()
    
    if success:
        # Clipboard'a kopyala
        pyperclip.copy(data)
        return True, f"✅ {len(data)} karakter veri çekildi ve clipboard'a kopyalandı"
    else:
        return False, f"❌ Hata: {error}"

if __name__ == "__main__":
    # Test için
    success, message = scrape_and_process()
    print(message)
