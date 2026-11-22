from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class BrowserWindow:
    def __init__(self):
        self.driver = None
    
    def open_browser(self, url="https://www.sahadan.com/iddaa-programi"):
        """Browser'ı aç"""
        try:
            # Chrome seçenekleri
            chrome_options = Options()
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Driver'ı başlat
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Sayfa yükle
            self.driver.get(url)
            
            print(f"✅ Browser açıldı: {url}")
            return True
            
        except Exception as e:
            print(f"❌ Browser açma hatası: {e}")
            return False
    
    def click_next_day(self, days=1):
        """Sonraki güne git"""
        try:
            for _ in range(days):
                # "İleri" veya ">" butonunu bul
                # Sahadan'da genelde sağ ok butonu var
                next_button = None
                
                # Farklı selector'lar dene
                selectors = [
                    "//button[contains(@class, 'next')]",
                    "//button[contains(@aria-label, 'next')]",
                    "//button[contains(@title, 'sonraki')]",
                    "//a[contains(@class, 'next')]",
                    "//i[contains(@class, 'arrow-right')]/..",
                    "//*[contains(@class, 'calendar')]//button[last()]"
                ]
                
                for selector in selectors:
                    try:
                        next_button = self.driver.find_element(By.XPATH, selector)
                        if next_button:
                            next_button.click()
                            print(f"✅ Sonraki güne geçildi")
                            time.sleep(2)  # Sayfa yüklensin
                            return True
                    except:
                        continue
                
                # Buton bulunamadıysa JavaScript ile tarih değiştir
                print("⚠️ Tarih değiştirme butonu bulunamadı, JavaScript deneniyor...")
                self.driver.execute_script("""
                    // Tarih input'unu bul ve değiştir
                    let dateInputs = document.querySelectorAll('input[type="date"], input[type="datetime-local"]');
                    if (dateInputs.length > 0) {
                        let today = new Date();
                        today.setDate(today.getDate() + 1);
                        dateInputs[0].value = today.toISOString().split('T')[0];
                        dateInputs[0].dispatchEvent(new Event('change', { bubbles: true }));
                    }
                """)
                time.sleep(2)
                print("✅ JavaScript ile tarih değiştirildi")
                return True
            
        except Exception as e:
            print(f"❌ Tarih değiştirme hatası: {e}")
            return False
    
    def find_matches_on_page(self):
        """Sayfada maç var mı kontrol et"""
        try:
            # Maç elementlerini ara
            match_elements = self.driver.find_elements(By.XPATH, 
                "//*[contains(@class, 'match') or contains(@class, 'game') or contains(@class, 'event')]")
            
            if len(match_elements) > 0:
                print(f"✅ Sayfada {len(match_elements)} maç elementi bulundu")
                return True
            
            # Alternatif: "maç yok" mesajı var mı?
            no_match_texts = ["maç yok", "no match", "no games", "henüz maç yok"]
            page_text = self.driver.page_source.lower()
            
            for text in no_match_texts:
                if text in page_text:
                    print(f"⚠️ Sayfada '{text}' mesajı bulundu")
                    return False
            
            # Belirsiz durum
            print("❓ Maç durumu belirsiz")
            return None
            
        except Exception as e:
            print(f"❌ Maç kontrol hatası: {e}")
            return None
    
    def auto_find_matches(self, max_days=7):
        """Otomatik olarak maç bulan güne git"""
        print(f"🔍 Maç aranıyor (maksimum {max_days} gün)")
        
        for day in range(max_days):
            if day == 0:
                print(f"📅 Bugün kontrol ediliyor...")
            else:
                print(f"📅 {day} gün sonrası kontrol ediliyor...")
                if not self.click_next_day(1):
                    print("❌ Tarih değiştirilemedi")
                    return False
            
            time.sleep(3)  # Sayfa yüklensin
            
            has_matches = self.find_matches_on_page()
            
            if has_matches:
                print(f"✅ Maçlar bulundu! ({day} gün sonrası)")
                return True
            elif has_matches is False:
                print(f"⏭️ Maç yok, sonraki güne geçiliyor...")
                continue
            else:
                # Belirsiz, HTML'i al gene de
                print(f"❓ Belirsiz durum, HTML alınacak")
                return True
        
        print(f"❌ {max_days} gün içinde maç bulunamadı")
        return False
    
    def get_page_html(self):
        """Sayfanın HTML'ini al"""
        if self.driver:
            try:
                # Sayfanın yüklenmesini bekle
                time.sleep(2)
                return self.driver.page_source
            except Exception as e:
                print(f"❌ HTML alma hatası: {e}")
                return None
        return None
    
    def wait_and_get_html(self, wait_seconds=5):
        """Kullanıcı işlemlerini bekle ve HTML'i al"""
        if self.driver:
            print(f"⏳ {wait_seconds} saniye bekleniyor (JavaScript yükleniyor)...")
            time.sleep(wait_seconds)
            
            # Sayfa yüklenene kadar bekle
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda d: d.execute_script('return document.readyState') == 'complete'
                )
                print("✅ Sayfa tamamen yüklendi")
            except:
                print("⚠️ Sayfa yükleme timeout")
            
            return self.get_page_html()
        return None
    
    def close(self):
        """Browser'ı kapat"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("✅ Browser kapatıldı")
