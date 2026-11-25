import sys
import os
import json
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenuBar, QMenu, QAction, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtWebChannel import QWebChannel
import time
import traceback
from database import Database
from telegram_bot import TelegramBotManager
from scraper import BulletinScraper
from browser_window import BrowserWindow

# Excel Worker Thread
class ExcelLoaderThread(QThread):
    finished = pyqtSignal(int, int)  # saved_count, total_count
    error = pyqtSignal(str)
    
    def __init__(self, file_path, db, telegram):
        super().__init__()
        self.file_path = file_path
        self.db = db
        self.telegram = telegram
    
    def run(self):
        try:
            print(f"📂 Excel yükleniyor: {self.file_path}")
            
            # Excel oku
            df = pd.read_excel(self.file_path, header=None, skiprows=3)
            df = df.fillna("")
            print(f"✅ {len(df)} satır okundu")
            
            # Parse et
            matches_data = []
            print(f"🔄 Satırlar parse ediliyor...")
            
            for idx, row in df.iterrows():
                try:
                    if len(row) < 11:
                        continue
                    
                    odd_1 = float(row.iloc[8]) if pd.notna(row.iloc[8]) and str(row.iloc[8]).replace('.','').replace(',','').isdigit() else 0
                    odd_x = float(row.iloc[9]) if pd.notna(row.iloc[9]) and str(row.iloc[9]).replace('.','').replace(',','').isdigit() else 0
                    odd_2 = float(row.iloc[10]) if pd.notna(row.iloc[10]) and str(row.iloc[10]).replace('.','').replace(',','').isdigit() else 0
                    
                    if odd_1 > 0 and odd_x > 0 and odd_2 > 0:
                        match = {
                            'date': '',
                            'time': str(row.iloc[0]) if pd.notna(row.iloc[0]) else '',
                            'league': str(row.iloc[2]) if pd.notna(row.iloc[2]) else '',
                            'mbs': row.iloc[3] if pd.notna(row.iloc[3]) else 0,
                            'home_team': str(row.iloc[4]) if pd.notna(row.iloc[4]) else '',
                            'score': str(row.iloc[5]) if pd.notna(row.iloc[5]) else '',
                            'away_team': str(row.iloc[6]) if pd.notna(row.iloc[6]) else '',
                            'half_score': str(row.iloc[7]) if pd.notna(row.iloc[7]) else '',
                            'odd_1': odd_1,
                            'odd_x': odd_x,
                            'odd_2': odd_2,
                            'over': 0,
                            'under': 0,
                            'gg_yes': 0,
                            'gg_no': 0,
                            'over_1': 0,
                            'under_1': 0,
                            'over_2': 0,
                            'under_2': 0,
                        }
                        matches_data.append(match)
                        
                        # Her 5000 satırda bir progress göster
                        if len(matches_data) % 5000 == 0:
                            print(f"⏳ {len(matches_data)} maç işlendi...")
                            
                except Exception as e:
                    if idx < 5:
                        print(f"⚠️ Satır {idx} hatası: {e}")
                    continue
            
            print(f"✅ Parse tamamlandı: {len(matches_data)} maç bulundu")
            
            # Veritabanına kaydet
            print(f"💾 Veritabanına kaydediliyor...")
            saved_count = self.db.save_matches(matches_data)
            print(f"✅ {saved_count} maç kaydedildi")
            
            # Telegram bildirim
            if saved_count > 0:
                try:
                    print(f"📱 Telegram bildirimi gönderiliyor...")
                    self.telegram.send_bulletin_notification(saved_count)
                    print(f"✅ Telegram bildirimi gönderildi")
                except Exception as e:
                    print(f"⚠️ Telegram hatası: {e}")
            
            # Signal gönder
            print(f"📡 Signal gönderiliyor: finished({saved_count}, {len(matches_data)})")
            self.finished.emit(saved_count, len(matches_data))
            print(f"✅ Signal gönderildi!")
            
        except Exception as e:
            print(f"❌ THREAD HATASI: {e}")
            import traceback
            traceback.print_exc()
            self.error.emit(str(e))

try:
    class Bridge(QObject):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.main_window = parent
            self.db = Database()
            self.telegram = TelegramBotManager()
            self.scraper = BulletinScraper()
            self.browser = None
            self.is_testing = False  # Test durumu için flag

        @pyqtSlot(str)
        def handleFileUpload(self, _):
            try:
                # Dosya seç
                file_path, _ = QFileDialog.getOpenFileName(
                    self.main_window,
                    "Excel Dosyası Seç",
                    "",
                    "Excel Files (*.xlsx *.xls)"
                )
                
                if not file_path:
                    print("İptal edildi")
                    return
                
                # Loading göster
                loading_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'loading.html')
                self.main_window.web_view.setUrl(QUrl.fromLocalFile(loading_path))
                
                # Thread başlat
                self.excel_thread = ExcelLoaderThread(file_path, self.db, self.telegram)
                self.excel_thread.finished.connect(self.onExcelFinished)
                self.excel_thread.error.connect(self.onExcelError)
                self.excel_thread.start()
                
                print(f"📂 Excel thread başlatıldı: {file_path}")
                    
            except Exception as e:
                print(f"❌ Hata: {e}")
                traceback.print_exc()
        
        @pyqtSlot(int, int)
        def onExcelFinished(self, saved_count, total_count):
            """Excel yükleme tamamlandı"""
            print(f"🎉 Excel yükleme tamamlandı: {saved_count}/{total_count}")
            
            # Ana ekrana dön
            index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'index.html')
            self.main_window.web_view.setUrl(QUrl.fromLocalFile(index_path))
            
            # Popup göster
            msg = QMessageBox(self.main_window)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Başarılı!")
            msg.setText(f"✅ Excel yükleme tamamlandı")
            msg.setInformativeText(f"{saved_count} yeni maç veritabanına kaydedildi.\n\nToplam işlenen: {total_count} kayıt")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1e1e1e;
                    color: white;
                }
                QLabel {
                    color: white;
                    font-size: 13px;
                }
                QPushButton {
                    background-color: #0d7377;
                    color: white;
                    border: none;
                    padding: 8px 20px;
                    border-radius: 4px;
                    font-size: 12px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #14FFEC;
                    color: black;
                }
            """)
            msg.exec_()
        
        @pyqtSlot(str)
        def onExcelError(self, error_msg):
            """Excel yükleme hatası"""
            print(f"❌ Hata: {error_msg}")
            
            # Ana ekrana dön
            index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'index.html')
            self.main_window.web_view.setUrl(QUrl.fromLocalFile(index_path))
            
            # Hata popup'ı
            msg = QMessageBox(self.main_window)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Hata!")
            msg.setText("❌ Excel yüklenirken bir hata oluştu")
            msg.setInformativeText(error_msg)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        
        @pyqtSlot()
        def minimizeWindow(self):
            """Pencereyi küçült"""
            try:
                self.main_window.showMinimized()
            except KeyboardInterrupt:
                print("ℹ️ Minimize işlemi iptal edildi")
            except Exception as e:
                print(f"❌ Minimize hatası: {str(e)}")
        
        @pyqtSlot()
        def closeWindow(self):
            """Pencereyi kapat"""
            try:
                self.main_window.close()
            except KeyboardInterrupt:
                print("ℹ️ Close işlemi iptal edildi")
            except Exception as e:
                print(f"❌ Close hatası: {str(e)}")
        
        @pyqtSlot()
        def openSettings(self):
            """Telegram ayarları ekranını aç"""
            try:
                settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'settings.html')
                self.main_window.web_view.setUrl(QUrl.fromLocalFile(settings_path))
            except Exception as e:
                print(f"❌ Ayarlar açılırken hata: {str(e)}")
                import traceback
                traceback.print_exc()
        
        @pyqtSlot()
        def openMackolikParser(self):
            """Mackolik parser sayfasını aç"""
            try:
                parser_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'mackolik_parser_v2.html')
                self.main_window.web_view.setUrl(QUrl.fromLocalFile(parser_path))
            except Exception as e:
                print(f"❌ Parser açılırken hata: {str(e)}")
                import traceback
                traceback.print_exc()
        
        @pyqtSlot()
        def openNesineParser(self):
            """Nesine parser sayfasını aç"""
            try:
                parser_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'nesine_parser.html')
                self.main_window.web_view.setUrl(QUrl.fromLocalFile(parser_path))
            except Exception as e:
                print(f"❌ Parser açılırken hata: {str(e)}")
                import traceback
                traceback.print_exc()
        
        @pyqtSlot(str)
        def parseNesineCoupon(self, coupon_data):
            """Nesine kupon verisini parse et"""
            try:
                print("🎯 Nesine kuponu parse ediliyor...")
                print(f"📋 Veri uzunluğu: {len(coupon_data)} karakter")
                
                lines = [l.strip() for l in coupon_data.strip().split('\n') if l.strip()]
                matches = []
                sistem_info = None
                
                # Sistem bilgisini bul (örn: "11 Sistem")
                for line in lines:
                    if 'sistem' in line.lower() and any(c.isdigit() for c in line):
                        # "11 Sistem" veya "2, 3, 4" gibi formatlar
                        sistem_info = line.strip()
                        print(f"📊 Sistem bulundu: {sistem_info}")
                        break
                
                # Strategi: Takım isimleri bir satırda, hemen ardından rakamsal veriler (MBS, oran, skor)
                i = 0
                while i < len(lines):
                    line = lines[i]
                    
                    # Takım ismi pattern'i: "X - Y" formatı, uzunluk 10-50 karakter arası
                    if ' - ' in line and 10 < len(line) < 50:
                        
                        # Kesinlikle ATLANMASI gerekenler
                        skip_patterns = [
                            'copyright', 'nesine', 'iddaa', 'milli piyango', 'spor toto',
                            'anasayfa', 'yardım', 'iletişim', 'hakkımızda', 'bülten',
                            'kupondaş', 'canlı', 'oyunlar', 'şans', 'at yarış', 'kariyer',
                            'üye ol', 'giriş yap', 'müşteri', 'kullanım şart', 'politika',
                            'sponsorluk', 'bizi takip', 'footer', 'header', 'yasal',
                            'at mı', 'nal mı', 'lana cross', 'altın nal', 'tazılar',
                            'jokey', 'bingola', 'define', 'ejder', 'kozmik', 'magma',
                            'şans perisi', 'külçeler', 'amazon', 'serbest vuruş', 'pro lig',
                            'sanal lig', 'basketbol', 'amerikan futbol', 'euroleague',
                            'editörler', 'dakika bahis', 'kazanan', 'nesine tv',
                            'extra', 'para yatır', 'para çek', 'çerez', 'kişisel veri',
                            'güvenlik', 'toplumu hizmet', 'sorumlu oyun', 'united racing',
                            'sayısal oyun', 'secure', 'site güven', 'bayi', 'haklar',
                            'store', 'indirin', 'huawei', 'google', 'app store',
                            'facebook', 'twitter', 'instagram', 'youtube', 'ngaming'
                        ]
                        
                        if any(pat in line.lower() for pat in skip_patterns):
                            i += 1
                            continue
                        
                        # Tarih/saat formatı değil mi? (25.11.2026 gibi)
                        if line[0].isdigit() and ('.' in line or ':' in line):
                            i += 1
                            continue
                        
                        # Potansiyel takım ismi
                        teams = line
                        
                        # Sonraki 25 satırı tara, maç bilgilerini bul
                        mbs = None
                        tahmin = None
                        oran = None
                        mac_saati = None
                        skor = None
                        ilk_yari_skor = None
                        
                        look_ahead = 25
                        for j in range(1, min(look_ahead, len(lines) - i)):
                            next_line = lines[i + j]
                            
                            # Başka bir takım ismi görüldüyse dur (bir sonraki maça geçtik)
                            if ' - ' in next_line and 10 < len(next_line) < 50 and j > 3:
                                break
                            
                            # MBS: tek basamaklı rakam (1-9)
                            if not mbs and len(next_line) == 1 and next_line.isdigit() and next_line != '0':
                                mbs = next_line
                            
                            # Tahmin: MS, KG, Toplam, Üst, Alt, Var içerenler
                            tahmin_keywords = ['ms&', 'ms ', '& kg', 'toplam', 'üst', 'alt', 'var', 'yok', 'gol']
                            if not tahmin and 3 < len(next_line) < 60:
                                if any(kw in next_line.lower() for kw in tahmin_keywords):
                                    tahmin = next_line
                            
                            # Oran: 1.XX veya 2.XX formatı (iki basamaklı noktalı sayı)
                            if not oran and '.' in next_line and len(next_line) <= 6:
                                parts = next_line.replace(',', '.').split('.')
                                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                                    oran = next_line
                            
                            # Maç Saati: Sadece "MS" yazısı
                            if not mac_saati and next_line.upper() == 'MS':
                                mac_saati = 'MS'
                            
                            # Skor: X-X formatı (0-0, 1-1, 3-0 gibi) - İLK BULDUĞUMUZ ana skor
                            if not skor and '-' in next_line and len(next_line) <= 5:
                                parts = next_line.split('-')
                                if len(parts) == 2:
                                    try:
                                        int(parts[0])
                                        int(parts[1])
                                        skor = next_line
                                    except:
                                        pass
                            
                            # İlk yarı skoru: (İY: 0-2) formatı veya parantez içinde
                            if not ilk_yari_skor and ('iy' in next_line.lower() or '(' in next_line):
                                # (İY: 0-2) veya (0-2) formatı
                                if '-' in next_line and len(next_line) <= 12:
                                    # Parantez içindeki skoru al
                                    if '(' in next_line and ')' in next_line:
                                        inside_parens = next_line[next_line.find('(')+1:next_line.find(')')]
                                        # İY: prefix'ini temizle
                                        inside_parens = inside_parens.replace('İY:', '').replace('IY:', '').strip()
                                        if '-' in inside_parens:
                                            parts = inside_parens.split('-')
                                            if len(parts) == 2:
                                                try:
                                                    int(parts[0].strip())
                                                    int(parts[1].strip())
                                                    ilk_yari_skor = inside_parens
                                                except:
                                                    pass
                        
                        # En az oran bilgisi varsa maç olarak kaydet
                        if oran or tahmin:
                            match_info = {
                                'teams': teams,
                                'mbs': mbs,
                                'tahmin': tahmin,
                                'oran': oran,
                                'mac_saati': mac_saati,
                                'skor': skor,
                                'ilk_yari_skor': ilk_yari_skor
                            }
                            matches.append(match_info)
                            
                            print(f"\n  ✅ {len(matches)}. {teams}")
                            if mbs:
                                print(f"     MBS: {mbs}")
                            if tahmin:
                                print(f"     Tahmin: {tahmin}")
                            if oran:
                                print(f"     Oran: {oran}")
                            if mac_saati:
                                print(f"     Durum: {mac_saati} (Maç Sonu)")
                            if skor:
                                print(f"     Skor: {skor}")
                            if ilk_yari_skor:
                                print(f"     İlk Yarı: {ilk_yari_skor}")
                    
                    i += 1
                
                print(f"\n✅ Toplam {len(matches)} maç bulundu")
                if sistem_info:
                    print(f"📊 Sistem: {sistem_info}")
                
                if len(matches) > 0:
                    # Supabase'e kaydet
                    print("💾 Supabase'e kaydediliyor...")
                    try:
                        from supabase_sync import get_supabase_client
                        client = get_supabase_client()
                        
                        # Toplam oran hesapla
                        total_odds = 1.0
                        for match in matches:
                            if match['oran']:
                                try:
                                    total_odds *= float(match['oran'].replace(',', '.'))
                                except:
                                    pass
                        
                        # Kupon kaydı oluştur
                        coupon_data = {
                            'match_count': len(matches),
                            'total_odds': round(total_odds, 2),
                            'status': 'pending',
                            'featured': False,
                            'sistem_info': sistem_info  # Sistem bilgisi ekle
                        }
                        
                        coupon_result = client.table('nesine_coupons').insert(coupon_data).execute()
                        
                        if coupon_result.data and len(coupon_result.data) > 0:
                            coupon_id = coupon_result.data[0]['id']
                            print(f"✅ Kupon oluşturuldu: {coupon_id}")
                            
                            # Maçları kaydet
                            match_records = []
                            for idx, match in enumerate(matches):
                                match_records.append({
                                    'coupon_id': coupon_id,
                                    'teams': match['teams'],
                                    'mbs': match.get('mbs'),
                                    'tahmin': match.get('tahmin'),
                                    'oran': match.get('oran'),
                                    'mac_saati': match.get('mac_saati'),
                                    'skor': match.get('skor'),
                                    'ilk_yari_skor': match.get('ilk_yari_skor'),  # İlk yarı skoru ekle
                                    'match_order': idx + 1
                                })
                            
                            matches_result = client.table('nesine_coupon_matches').insert(match_records).execute()
                            print(f"✅ {len(matches)} maç kaydedildi")
                            
                            # JavaScript'e success callback gönder
                            js_code = f"onSuccess({len(matches)});"
                            self.main_window.web_view.page().runJavaScript(js_code)
                        else:
                            raise Exception("Kupon kaydedilemedi")
                        
                    except Exception as db_error:
                        print(f"❌ Veritabanı hatası: {db_error}")
                        import traceback
                        traceback.print_exc()
                        
                        # Yine de başarılı olarak göster (parse başarılı oldu)
                        js_code = f"onSuccess({len(matches)});"
                        self.main_window.web_view.page().runJavaScript(js_code)
                else:
                    js_code = "onError('Maç bulunamadı! Nesine kupon sayfasını tamamen kopyalayıp yapıştırın (Ctrl+A, Ctrl+C, Ctrl+V)');"
                    self.main_window.web_view.page().runJavaScript(js_code)
                
            except Exception as e:
                error_msg = str(e).replace("'", "\\'")
                print(f"❌ Parse hatası: {error_msg}")
                import traceback
                traceback.print_exc()
                
                js_code = f"onError('{error_msg}');"
                self.main_window.web_view.page().runJavaScript(js_code)
        
        @pyqtSlot()
        def goBack(self):
            """Ana ekrana dön"""
            try:
                index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'index.html')
                self.main_window.web_view.setUrl(QUrl.fromLocalFile(index_path))
            except Exception as e:
                print(f"❌ Ana ekrana dönülürken hata: {str(e)}")
                import traceback
                traceback.print_exc()
        
        @pyqtSlot()
        def loadTelegramSettings(self):
            """Telegram ayarlarını yükle"""
            bot_token = self.db.get_setting('telegram_bot_token') or ''
            chat_id = self.db.get_setting('telegram_chat_id') or ''
            
            js_code = f"setTelegramSettings('{bot_token}', '{chat_id}');"
            self.main_window.web_view.page().runJavaScript(js_code)
        
        @pyqtSlot(str, str)
        def saveTelegramSettings(self, bot_token, chat_id):
            """Telegram ayarlarını kaydet"""
            try:
                print("💾 Telegram ayarları kaydediliyor...")
                
                # Ayarları güncelle
                self.telegram.update_credentials(bot_token, chat_id)
                
                # Mesaj göster
                js_code = "showSaveResult(true, '✅ Ayarlar kaydedildi! Değişikliklerin geçerli olması için programı yeniden başlatın.');"
                self.main_window.web_view.page().runJavaScript(js_code)
                
                print("✅ Ayarlar kaydedildi. Yeni ayarların aktif olması için programı yeniden başlatın.")
                
            except KeyboardInterrupt:
                print("ℹ️ Kaydetme işlemi iptal edildi")
                js_code = "showSaveResult(false, '⚠️ İşlem iptal edildi');"
                self.main_window.web_view.page().runJavaScript(js_code)
            except Exception as e:
                print(f"❌ Kaydetme hatası: {str(e)}")
                import traceback
                traceback.print_exc()
                js_code = f"showSaveResult(false, '❌ Hata: {str(e)}');"
                self.main_window.web_view.page().runJavaScript(js_code)
        
        @pyqtSlot(str, str)
        def testTelegram(self, bot_token, chat_id):
            """Telegram bağlantısını test et"""
            # Eğer test zaten çalışıyorsa, ikinci testi engelle
            if self.is_testing:
                print("⚠️ Test zaten çalışıyor, lütfen bekleyin")
                js_code = "showTestResult(false, '⚠️ Test zaten çalışıyor, bekleyin...');"
                self.main_window.web_view.page().runJavaScript(js_code)
                return
            
            try:
                self.is_testing = True
                print("🔍 Telegram bağlantı testi başlatılıyor...")
                
                # Geçici bot oluştur
                temp_telegram = TelegramBotManager()
                temp_telegram.update_credentials(bot_token, chat_id)
                
                # Test mesajı gönder
                result = temp_telegram.send_message("🎯 BetSmart bağlantı testi başarılı!")
                
                if result:
                    print("✅ Test başarılı")
                    js_code = "showTestResult(true, '✅ Bağlantı başarılı! Test mesajı gönderildi.');"
                else:
                    print("❌ Test başarısız")
                    js_code = "showTestResult(false, '❌ Mesaj gönderilemedi. Bilgileri kontrol edin.');"
                
                self.main_window.web_view.page().runJavaScript(js_code)
                
            except KeyboardInterrupt:
                print("ℹ️ Test işlemi iptal edildi")
                js_code = "showTestResult(false, '⚠️ Test iptal edildi');"
                self.main_window.web_view.page().runJavaScript(js_code)
            except Exception as e:
                print(f"❌ Test hatası: {str(e)}")
                import traceback
                traceback.print_exc()
                js_code = f"showTestResult(false, '❌ Hata: {str(e)}');"
                self.main_window.web_view.page().runJavaScript(js_code)
            finally:
                # Test bittiğinde flag'i sıfırla
                self.is_testing = False
        
        @pyqtSlot(str, str)
        def processMackolikData(self, left_data, odds_data):
            """Mackolik verilerini parse et ve Excel oluştur (eski versiyon - iki alan)"""
            try:
                print("🔄 Mackolik verileri işleniyor (iki alan)...")
                self._process_mackolik_internal(left_data, odds_data)
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Parse hatası: {error_msg}")
                import traceback
                traceback.print_exc()
                import json
                js_code = f"onError({json.dumps(error_msg)});"
                self.main_window.web_view.page().runJavaScript(js_code)
        
        @pyqtSlot(str)
        def processMackolikDataSingle(self, all_data):
            """Mackolik verilerini parse et (tek alan - tümü birlikte)"""
            try:
                print("🔄 Mackolik verileri işleniyor (tek alan)...")
                print("=" * 50)
                
                # "1	X	2	2,5A	2,5Ü" satırını bul - ayırıcı
                lines = all_data.split('\n')
                separator_index = -1
                
                for i, line in enumerate(lines):
                    # Oran başlıklarını ara
                    if '1' in line and 'X' in line and '2' in line and ('2,5A' in line or '2,5Ü' in line):
                        separator_index = i
                        print(f"📍 Ayırıcı bulundu: Satır {i}")
                        break
                
                if separator_index == -1:
                    raise Exception("Oran başlıkları bulunamadı! Format hatalı olabilir.")
                
                # Verileri ayır
                left_data = '\n'.join(lines[:separator_index])
                odds_data = '\n'.join(lines[separator_index + 1:])
                
                print(f"📊 Maç verileri: {len(left_data)} karakter")
                print(f"🎲 Oran verileri: {len(odds_data)} karakter")
                
                # Mevcut fonksiyona gönder
                self._process_mackolik_internal(left_data, odds_data)
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Parse hatası: {error_msg}")
                import traceback
                traceback.print_exc()
                import json
                js_code = f"onError({json.dumps(error_msg)});"
                self.main_window.web_view.page().runJavaScript(js_code)
        
        def _process_mackolik_internal(self, left_data, odds_data):
            """Mackolik verilerini parse et ve Excel oluştur (internal)"""
            try:
                print("=" * 50)
                
                # Satırlara ayır ve temizle
                left_lines = [line.strip() for line in left_data.split('\n') if line.strip()]
                odds_lines = [line.strip() for line in odds_data.split('\n') if line.strip()]
                
                print(f"📊 Sol kısım: {len(left_lines)} satır")
                print(f"🎲 Oranlar: {len(odds_lines)} satır")
                
                # Debug: İlk 20 satırı göster
                print("\n📋 SOL KISIM İLK 20 SATIR:")
                print("-" * 50)
                for i in range(min(20, len(left_lines))):
                    print(f"Satır {i}: '{left_lines[i]}'")
                print("-" * 50)
                
                # Oranları grupla - ALT ALTA FORMAT
                # Her maç için 5 satır + "Diğer" satırı
                odds_groups = []
                temp_numbers = []
                
                print("\n🔍 ORAN PARSE DEBUG (Alt Alta Format):")
                print("-" * 50)
                
                # Oranlar direkt sayılarla başlıyor - başlık aramaya gerek yok
                parsing_odds = True  # Direkt parse'a başla
                
                i = 0
                while i < len(odds_lines):
                    line = odds_lines[i].strip()
                    
                    # Boş satır atla
                    if not line:
                        i += 1
                        continue
                    
                    # Footer/reklam bölümünü görünce dur
                    if 'İlginizi Çekebilir' in line or 'Welder' in line or 'İletişim' in line or \
                       'Künye' in line or 'mackolik.com' in line.lower() or 'Hakkı Saklı' in line:
                        print(f"🛑 Footer/reklam bölümü başladı (satır {i}), oran parse durdu")
                        break
                    
                    # Başlık satırlarını atla (1, X, 2, 2,5A, 2,5Ü gibi)
                    if line in ['1', 'X', '2', '2,5A', '2,5Ü', '2.5A', '2.5Ü']:
                        print(f"❌ Satır {i}: '{line}' (başlık, atlandı)")
                        i += 1
                        continue
                    
                    # "Diğer" satırını gördüğünde grubu tamamla
                    if 'diğer' in line.lower() or 'diger' in line.lower():
                        if len(temp_numbers) >= 3:  # En az 3 sayı (1, X, 2)
                            # Eksik oranları doldur
                            while len(temp_numbers) < 5:
                                temp_numbers.append(1.01)
                            
                            odds_groups.append({
                                'odd_1': temp_numbers[0],
                                'odd_x': temp_numbers[1],
                                'odd_2': temp_numbers[2],
                                'under_25': temp_numbers[3],  # Mackolik'te 4. sıra = 2.5A (Alt)
                                'over_25': temp_numbers[4]     # Mackolik'te 5. sıra = 2.5Ü (Üst)
                            })
                            print(f"✅ Grup {len(odds_groups)}: {temp_numbers} (Diğer ile sonlandı)")
                            temp_numbers = []
                        i += 1
                        continue
                    
                    # Sayı mı kontrol et
                    try:
                        num = float(line.replace(',', '.'))
                        temp_numbers.append(num)
                        print(f"➕ Satır {i}: {num} eklendi (toplam: {len(temp_numbers)})")
                        
                        # 5 sayı toplandıysa otomatik kaydet
                        if len(temp_numbers) == 5:
                            odds_groups.append({
                                'odd_1': temp_numbers[0],
                                'odd_x': temp_numbers[1],
                                'odd_2': temp_numbers[2],
                                'under_25': temp_numbers[3],  # Mackolik'te 4. sıra = 2.5A (Alt)
                                'over_25': temp_numbers[4]     # Mackolik'te 5. sıra = 2.5Ü (Üst)
                            })
                            print(f"✅ Grup {len(odds_groups)}: {temp_numbers} (5 sayı - otomatik)")
                            temp_numbers = []
                        
                        # 3 sayı toplandıysa ve sonraki satır sayı DEĞİLSE, grubu kaydet
                        elif len(temp_numbers) == 3 and i + 1 < len(odds_lines):
                            next_line = odds_lines[i + 1].strip()
                            try:
                                float(next_line.replace(',', '.'))
                                # Sonraki sayı, devam et
                            except:
                                # Sonraki sayı değil, bu grup sadece 3 sayılı
                                while len(temp_numbers) < 5:
                                    temp_numbers.append(1.01)
                                odds_groups.append({
                                    'odd_1': temp_numbers[0],
                                    'odd_x': temp_numbers[1],
                                    'odd_2': temp_numbers[2],
                                    'over_25': temp_numbers[3],
                                    'under_25': temp_numbers[4]
                                })
                                print(f"✅ Grup {len(odds_groups)}: {temp_numbers} (3 sayı - sonraki sayı değil)")
                                temp_numbers = []
                        
                    except:
                        # Sayı değilse ve grupta veri varsa grubu kaydet
                        if len(temp_numbers) >= 3:
                            while len(temp_numbers) < 5:
                                temp_numbers.append(1.01)
                            odds_groups.append({
                                'odd_1': temp_numbers[0],
                                'odd_x': temp_numbers[1],
                                'odd_2': temp_numbers[2],
                                'under_25': temp_numbers[3],  # Mackolik'te 4. sıra = 2.5A (Alt)
                                'over_25': temp_numbers[4]     # Mackolik'te 5. sıra = 2.5Ü (Üst)
                            })
                            print(f"✅ Grup {len(odds_groups)}: {temp_numbers} (sayı değil ile sonlandı)")
                            temp_numbers = []
                        print(f"⚠️ Satır {i}: '{line[:50]}' (sayı değil, atlandı)")
                    
                    i += 1
                
                # Son grubu da ekle (eğer varsa)
                if len(temp_numbers) >= 3:
                    while len(temp_numbers) < 5:
                        temp_numbers.append(1.01)
                    odds_groups.append({
                        'odd_1': temp_numbers[0],
                        'odd_x': temp_numbers[1],
                        'odd_2': temp_numbers[2],
                        'over_25': temp_numbers[3],
                        'under_25': temp_numbers[4]
                    })
                    print(f"✅ Son grup {len(odds_groups)}: {temp_numbers} (son grup)")
                
                print("-" * 50)
                print(f"✅ TOPLAM: {len(odds_groups)} oran grubu oluşturuldu")
                
                # Son 5 oran grubunu göster (debug)
                print("\n📊 SON 5 ORAN GRUBU:")
                for i in range(max(0, len(odds_groups)-5), len(odds_groups)):
                    odds = odds_groups[i]
                    print(f"  Grup {i+1}: 1={odds['odd_1']:.2f} X={odds['odd_x']:.2f} 2={odds['odd_2']:.2f}")
                print()
                
                # Sol kısmı parse et - SKOR BAZLI
                # Format: Takım1, Skor, Takım2, İY Skoru
                matches_data = []
                
                print("\n🔍 SOL KISIM PARSE DEBUG (Skor Bazlı):")
                print("-" * 50)
                print(f"Toplam satır: {len(left_lines)}")
                
                # İLK 100 SATIRI GÖSTER (Debug) - Oman FC ve Saham maçlarını bul
                print("\n📋 İLK 100 SATIR (Oman FC ve Saham için):")
                for idx in range(min(100, len(left_lines))):
                    line = left_lines[idx].strip()
                    if line:
                        # Oman veya Saham içeren satırları vurgula
                        marker = "🔴" if ('Oman' in line or 'Saham' in line or 'Dhofor' in line or 'Al Seeb' in line) else "  "
                        print(f"{marker} [{idx:3d}] {line[:100]}")
                print()
                
                i = 0
                postponed_match_count = 0
                while i < len(left_lines):
                    line = left_lines[i].strip()
                    
                    # Ertelenmiş maç tespiti (P - P)
                    is_postponed = False
                    if 'P - P' in line or 'P-P' in line:
                        is_postponed = True
                        score = 'P-P'
                        print(f"⏸️ ERTELENMİŞ MAÇ TESPİT EDİLDİ: {line}")
                    
                    # Skor satırı mı? (1-1, 0-0, 2-1 gibi)
                    elif '-' in line and len(line) <= 25:  # Sınırı biraz daha artır
                        parts = line.split('-')
                        if len(parts) == 2:
                            try:
                                # Parantezleri temizle (hem başta hem sonda)
                                # (1) 0 - 0 (0) → 0 - 0
                                left_part = parts[0].strip()
                                right_part = parts[1].strip()
                                
                                # Sol tarafta parantez varsa temizle
                                if '(' in left_part:
                                    # Son parantezden sonraki kısmı al
                                    if ')' in left_part:
                                        left_part = left_part.split(')')[-1].strip()
                                
                                # Sağ tarafta parantez varsa temizle
                                if '(' in right_part:
                                    right_part = right_part.split('(')[0].strip()
                                
                                int(left_part)
                                int(right_part)
                                
                                # Bu bir skor!
                                score = f"{left_part} - {right_part}"
                                is_postponed = False
                                print(f"⚽ Skor tespit edildi: '{line}' → '{score}'")
                            except:
                                # Sayı değil, atla
                                i += 1
                                continue
                    else:
                        # Skor değil, atla
                        i += 1
                        continue
                    
                    # Buraya gelinmişse ya normal skor ya P-P var
                    home_team = ""
                    away_team = ""
                    time = ""
                    half_score = ""
                    
                    # Önceki satırlarda takım ve saat ara (geriye 5 satır)
                    for j in range(max(0, i-5), i):
                        prev_line = left_lines[j].strip()
                        # Saat mi? (XX:XX)
                        if ':' in prev_line and len(prev_line.split(':')[0]) <= 2:
                            time = prev_line.split()[0]
                    
                    # Hemen önceki satır ev sahibi takım
                    if i > 0:
                        home_team = left_lines[i-1].strip()
                    
                    # Hemen sonraki satır deplasman takım
                    if i + 1 < len(left_lines):
                        away_team = left_lines[i+1].strip()
                    
                    # İY skoru 2 satır sonra (deplasman + boşluk/takım karşılaştırma)
                    for j in range(i+2, min(i+5, len(left_lines))):
                        next_line = left_lines[j].strip()
                        
                        # "Takım Karşılaştırma" metnini temizle
                        if 'Takım Karşılaştırma' in next_line or 'Takım Karşılaştırma' in next_line:
                            next_line = next_line.split('Takım')[0].strip()
                                    
                        # Skor formatında mı?
                        if '-' in next_line and len(next_line) <= 10:
                            try:
                                int(next_line.split('-')[0].strip())
                                int(next_line.split('-')[1].strip())
                                half_score = next_line
                                print(f"  🎯 İY skoru bulundu: {half_score}")
                                break
                            except:
                                pass
                    
                    # Kaydet
                    if home_team and away_team:
                        matches_data.append({
                            'time': time if time else '??:??',
                            'home_team': home_team,
                            'score': score,
                            'away_team': away_team,
                            'half_score': half_score,
                            'is_postponed': is_postponed
                        })
                        
                        # Log (insert yapmıyoruz artık!)
                        if is_postponed:
                            postponed_match_count += 1
                            print(f"⏸️ Ertelenmiş Maç {len(matches_data)}: {time} {home_team} P-P {away_team} (Oranlar atlanacak)")
                        else:
                            print(f"✅ Maç {len(matches_data)}: {time} {home_team} {score} {away_team} (İY: {half_score})")
                    
                    i += 1
                
                print("-" * 50)
                print(f"✅ {len(matches_data)} maç bulundu ({postponed_match_count} ertelenmiş)")
                
                # Son 5 maçı göster (debug)
                print("\n📊 SON 5 MAÇ:")
                for i in range(max(0, len(matches_data)-5), len(matches_data)):
                    match = matches_data[i]
                    postponed_tag = " [ERTELENMİŞ]" if match.get('is_postponed', False) else ""
                    print(f"  Maç {i+1}: {match['time']} {match['home_team']} {match['score']} {match['away_team']}{postponed_tag}")
                print()
                
                print(f"\n{'='*60}")
                print(f"✅ {len(matches_data)} MAÇ BULUNDU ({postponed_match_count} ERTELENMİŞ)")
                print(f"✅ {len(odds_groups)} ORAN GRUBU VAR")
                print(f"💡 NOT: Mackolik ertelenmiş maçlar için de oran gösteriyor")
                print(f"{'='*60}\n")
                
                # Eşleştirme kontrolü - Mackolik ertelenmiş maçlar için de oran gösteriyor!
                if len(odds_groups) != len(matches_data):
                    print(f"\n⚠️ UYARI: Oran sayısı eşleşmiyor!")
                    print(f"Maçlar: {len(matches_data)}, Oranlar: {len(odds_groups)}")
                    
                    print(f"\n🔍 DETAYLI KARŞILAŞTIRMA:")
                    print("=" * 100)
                    
                    # TÜM maçları karşılaştır (hangisi uyumsuz bul)
                    for i in range(min(len(matches_data), len(odds_groups))):
                        match = matches_data[i]
                        odds = odds_groups[i]
                        
                        # Her 10 maçta bir yazdır (çok uzun olmasın)
                        if i < 20 or i % 10 == 0 or i >= len(matches_data) - 5:
                            print(f"#{i+1:2d} | {match['time']} {match['home_team'][:15]:15s} {match['score']:5s} {match['away_team'][:15]:15s} | 1:{odds['odd_1']:5.2f} X:{odds['odd_x']:.2f} 2:{odds['odd_2']:5.2f}")
                    
                    # Eğer fazla oran varsa
                    if len(odds_groups) > len(matches_data):
                        print("\n⚠️ FAZLA ORAN GRUPLARI:")
                        for i in range(len(matches_data), len(odds_groups)):
                            odds = odds_groups[i]
                            print(f"Oran #{i+1}: 1:{odds['odd_1']:.2f} X:{odds['odd_x']:.2f} 2:{odds['odd_2']:.2f} ← FAZLA!")
                    
                    print("=" * 100)
                    print(f"\n💡 İPUCU: Footer'dan fazla oran gelmiş olabilir.")
                    print(f"   Yukarıdaki listede hangi maçta oranlar mantıksızsa o noktada kayma var.")
                    
                    import json
                    error_msg = f"Veri sayilari eslesmedi! {len(matches_data)} mac, {len(odds_groups)} oran."
                    # JSON ile escape et
                    safe_msg = json.dumps(error_msg)
                    js_code = f"onError({safe_msg});"
                    self.main_window.web_view.page().runJavaScript(js_code)
                    return
                
                # Oranları ve ek bilgileri ekle - DİREKT EŞLEŞTIR (ertelenmiş maçların da oranı var!)
                for i, match in enumerate(matches_data):
                    print(f"\n🔗 Maç {i+1} işleniyor...")
                    
                    # Lig ve Mbs bilgileri
                    match['lig'] = 'STD'
                    match['mbs'] = '3'
                    
                    # Oranları direkt ata (ertelenmiş olsa da oranı var)
                    if i < len(odds_groups):
                        match['odd_1'] = odds_groups[i]['odd_1']
                        match['odd_x'] = odds_groups[i]['odd_x']
                        match['odd_2'] = odds_groups[i]['odd_2']
                        match['over_25'] = odds_groups[i]['over_25']
                        match['under_25'] = odds_groups[i]['under_25']
                        
                        postponed_tag = " [ERTELENMİŞ]" if match.get('is_postponed', False) else ""
                        print(f"✅ Maç {i+1} → Oran Grubu {i+1} eşleştirildi{postponed_tag}")
                    else:
                        # Oran yok - dummy
                        match['odd_1'] = 1.01
                        match['odd_x'] = 1.01
                        match['odd_2'] = 1.01
                        match['over_25'] = 1.01
                        match['under_25'] = 1.01
                        print(f"❌ Maç {i+1} için oran yok!")
                    
                    # Var/Yok oranları (1.01 sabit)
                    match['var'] = 1.01
                    match['yok'] = 1.01
                    
                    # Ekstra Alt/Üst oranları (1.5, 3.5)
                    match['over_15'] = 1.01
                    match['under_15'] = 1.01
                    match['over_35'] = 1.01
                    match['under_35'] = 1.01
                
                if not matches_data:
                    error_msg = "Hic mac parse edilemedi! Lutfen formati kontrol edin."
                    print(f"❌ {error_msg}")
                    import json
                    safe_msg = json.dumps(error_msg)
                    js_code = f"onError({safe_msg});"
                    self.main_window.web_view.page().runJavaScript(js_code)
                    return
                
                # Excel oluştur
                print(f"📝 Excel oluşturuluyor: {len(matches_data)} maç")
                
                # Sütun sırasını kontrol et
                print("\n📋 İLK MAÇ VERİSİ:")
                if matches_data:
                    print(matches_data[0])
                
                # DataFrame oluştur ve sütun sırasını ayarla
                df = pd.DataFrame(matches_data)
                
                # Sütun sıralaması (örnek Excel'e göre)
                column_order = [
                    'time', 'lig', 'mbs', 'home_team', 'score', 'away_team', 'half_score',
                    'odd_1', 'odd_x', 'odd_2', 'over_25', 'var', 'yok', 'under_25',
                    'over_15', 'under_15', 'over_35', 'under_35'
                ]
                df = df[column_order]
                
                # Sütun başlıklarını Türkçeleştir
                df.columns = [
                    'Saat', 'Lig', 'Mbs', 'Ev Sahibi', 'MS', 'Deplasman', 'İY',
                    '1', '0', '2', '2.5Ü', 'Var', 'Yok', '2.5A',
                    '1.5Ü', '1.5A', '3.5Ü', '3.5A'
                ]
                
                # Sütunları kontrol et
                print(f"\n📊 EXCEL SÜTUNLARI: {list(df.columns)}")
                print(f"\n📄 İLK 3 SATIR:")
                print(df.head(3))
                print(f"\n🔍 İLK SATIR VERİLERİ:")
                if len(df) > 0:
                    first_row = df.iloc[0]
                    for col in df.columns:
                        print(f"  {col}: {first_row[col]}")
                
                # Dosya seçim penceresi aç
                from PyQt5.QtWidgets import QFileDialog
                file_dialog = QFileDialog()
                selected_file, _ = file_dialog.getOpenFileName(
                    None,
                    "Hangi Excel dosyasına eklemek istersiniz? (İptal = Yeni dosya oluştur)",
                    os.path.join(os.path.expanduser('~'), 'Desktop'),
                    "Excel Dosyaları (*.xlsx *.xls)"
                )
                
                desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                
                if selected_file:
                    # Mevcut dosyaya ekle
                    print(f"📂 Mevcut dosya seçildi: {selected_file}")
                    
                    try:
                        # Mevcut dosyayı oku
                        from openpyxl import load_workbook
                        from openpyxl.styles import numbers
                        wb = load_workbook(selected_file)
                        ws = wb.active
                        
                        # En son dolu satırı bul
                        last_row = ws.max_row
                        print(f"📊 Mevcut dosyada {last_row} satır var")
                        
                        # Yeni verileri en alta ekle
                        print(f"\n🔍 EKLENEN İLK SATIR DEBUG:")
                        start_row = last_row + 1
                        
                        for idx in range(len(df)):
                            row_values = df.iloc[idx].values.tolist()
                            current_row = start_row + idx
                            
                            # İlk sütunu yaz (Saat - A sütunu)
                            cell = ws.cell(row=current_row, column=1)
                            cell.value = row_values[0]
                            if isinstance(row_values[0], str):
                                cell.number_format = '@'
                            
                            # B sütununu atla (boş bırak)
                            
                            # Geri kalan sütunları 1 sütun kaydırarak yaz (C'den başla)
                            for col_idx in range(1, len(row_values)):
                                cell = ws.cell(row=current_row, column=col_idx + 2)  # +2 çünkü B'yi atlıyoruz
                                value = row_values[col_idx]
                                
                                # String değerleri TEXT formatında kaydet
                                if isinstance(value, str):
                                    cell.value = value
                                    cell.number_format = '@'
                                else:
                                    cell.value = value
                            
                            if idx == 0:
                                print(f"  İlk satır sütun yapısı:")
                                print(f"    A: {row_values[0]} (Saat)")
                                print(f"    B: (boş bırakıldı)")
                                for col_idx in range(1, min(5, len(row_values))):
                                    col_letter = chr(65 + col_idx + 1)  # C, D, E, ...
                                    print(f"    {col_letter}: {row_values[col_idx]}")
                        
                        wb.save(selected_file)
                        print(f"✅ {len(df)} maç mevcut dosyaya eklendi!")
                        print(f"💡 Sütun yapısı: A=Saat, B=Boş, C=Lig, D=Mbs, E=Ev Sahibi, ...")
                        filepath = selected_file
                        filename = os.path.basename(selected_file)
                        
                    except Exception as e:
                        print(f"❌ Mevcut dosyaya eklerken hata: {str(e)}")
                        import traceback
                        traceback.print_exc()
                        print("⚠️ Yeni dosya oluşturuluyor...")
                        selected_file = None  # Yeni dosya oluştur
                
                if not selected_file:
                    # Yeni dosya oluştur
                    filename = f"mackolik_data_{timestamp}.xlsx"
                    filepath = os.path.join(desktop, filename)
                    print(f"📝 Yeni dosya oluşturuluyor: {filepath}")
                    
                    # Excel Writer ile kaydet (formatları ayarlamak için)
                    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                        # BAŞLIK SATIRI OLMADAN kaydet (header=False)
                        df.to_excel(writer, index=False, sheet_name='Maçlar', header=False)
                        
                        # Worksheet'i al
                        worksheet = writer.sheets['Maçlar']
                        
                        # Sütun genişliklerini ayarla
                        column_widths = {
                            'A': 8,   # Saat
                            'B': 6,   # Lig
                            'C': 6,   # Mbs
                            'D': 25,  # Ev Sahibi
                            'E': 8,   # MS
                            'F': 25,  # Deplasman
                            'G': 8,   # İY
                            'H': 6,   # 1
                            'I': 6,   # 0
                            'J': 6,   # 2
                            'K': 7,   # 2.5Ü
                            'L': 6,   # Var
                            'M': 6,   # Yok
                            'N': 7,   # 2.5A
                            'O': 7,   # 1.5Ü
                            'P': 7,   # 1.5A
                            'Q': 7,   # 3.5Ü
                            'R': 7    # 3.5A
                        }
                        
                        for col, width in column_widths.items():
                            worksheet.column_dimensions[col].width = width
                        
                        # Lig (B) ve Mbs (C) sütunlarını TEXT formatında kaydet
                        from openpyxl.styles import numbers
                        for row in worksheet.iter_rows(min_row=1, max_row=worksheet.max_row, min_col=2, max_col=3):
                            for cell in row:
                                cell.number_format = numbers.FORMAT_TEXT
                    
                    print(f"✅ Yeni Excel oluşturuldu!")
                
                print(f"✅ Excel kaydedildi: {filepath}")
                print("=" * 50)
                
                # Başarı mesajı gönder
                js_code = f"onSuccess('{filename}', {len(matches_data)});"
                self.main_window.web_view.page().runJavaScript(js_code)
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Parse hatası: {error_msg}")
                import traceback
                traceback.print_exc()
                
                import json
                safe_msg = json.dumps(error_msg)
                js_code = f"onError({safe_msg});"
                self.main_window.web_view.page().runJavaScript(js_code)
        
        @pyqtSlot(str)
        def processFutureMatches(self, all_data):
            """Mackolik'ten gelecek maçları parse et ve veritabanına kaydet - OTOMATİK FORMAT"""
            try:
                print("🔄 Gelecek maçlar işleniyor...")
                print("=" * 50)
                
                # FORMAT ALGILAMA: LİG view mi, SAAT view mi?
                future_matches = []
                
                # LİG view formatını dene - lig başlıklarını ara
                lines = all_data.split('\n')
                has_league_headers = False
                
                # İlk 50 satırda (daha fazla) lig başlığı formatını ara
                for line in lines[:50]:
                    stripped = line.strip()
                    # Lig başlığı: En az 10 karakter, tire içeren
                    if len(stripped) > 10 and ' - ' in stripped:
                        # Header/menu satırlarını atla
                        skip_keywords = ['maç sonucu', 'çifte şans', 'altı', 'üstü', 'saat', 'canlı', 'arama', 'futbol', 'basketbol', 'haberler']
                        if any(keyword in stripped.lower() for keyword in skip_keywords):
                            continue
                        # Sadece büyük harflerden oluşan kısa kodları atla (PRD, CAF, UWC)
                        if len(stripped) <= 5 and stripped.replace(' ', '').isupper():
                            continue
                        # Bu bir lig başlığı!
                        has_league_headers = True
                        print(f"🎯 Lig başlığı bulundu: '{stripped}'")
                        break
                
                if has_league_headers:
                    print("📋 Format: LİG görünümü (tam lig isimleri)")
                    from process_future_matches_league_view import parse_league_view_format
                    future_matches = parse_league_view_format(all_data)
                else:
                    print("📋 Format: SAAT görünümü (lig kodları)")
                    from process_future_matches_new import parse_new_mackolik_format
                    future_matches = parse_new_mackolik_format(all_data)
                
                print(f"\n✅ {len(future_matches)} gelecek maç bulundu")
                
                # TEKRAR EDEN MAÇLARI TEMİZLE
                seen = set()
                unique_matches = []
                for match in future_matches:
                    key = f"{match['datetime']}|{match['home_team']}|{match['away_team']}"
                    if key not in seen:
                        seen.add(key)
                        unique_matches.append(match)
                
                future_matches = unique_matches
                print(f"✅ {len(future_matches)} unique maç kaldı")
                
                # Veritabanına kaydet
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                # future_matches tablosunu oluştur
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS future_matches (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        datetime TEXT NOT NULL,
                        home_team TEXT NOT NULL,
                        away_team TEXT NOT NULL,
                        league TEXT,
                        odd_1 REAL,
                        odd_x REAL,
                        odd_2 REAL,
                        over_25 REAL,
                        under_25 REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(datetime, home_team, away_team)
                    )
                ''')
                
                # Maçları kaydet
                saved_count = 0
                for match in future_matches:
                    try:
                        cursor.execute('''
                            INSERT OR REPLACE INTO future_matches 
                            (datetime, home_team, away_team, league, odd_1, odd_x, odd_2, over_25, under_25)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            match['datetime'],
                            match['home_team'],
                            match['away_team'],
                            match['league'],
                            match['odd_1'],
                            match['odd_x'],
                            match['odd_2'],
                            match['over_25'],
                            match['under_25']
                        ))
                        saved_count += 1
                    except Exception as e:
                        print(f"❌ Kayıt hatası: {e}")
                        print(f"   Maç: {match['home_team']} vs {match['away_team']}")
                
                conn.commit()
                conn.close()
                
                print(f"✅ {saved_count} gelecek maç yerel veritabanına kaydedildi")
                
                # Supabase'e senkronize et
                try:
                    from supabase_sync import sync_matches_to_supabase
                    success, errors = sync_matches_to_supabase(future_matches)
                    
                    # JavaScript callback ile loading'i kapat
                    import json
                    if success > 0:
                        msg = f"✅ {saved_count} maç yerel DB'ye kaydedildi\n☁️ {success} maç Supabase'e yüklendi"
                        js_code = f"onSuccess('future_matches', {success});"
                        self.main_window.web_view.page().runJavaScript(js_code)
                        
                        QMessageBox.information(
                            None,
                            "Başarılı",
                            f"{msg}\n\nWeb sitesinde görüntülemek için:\nhttps://betsmart-web.vercel.app"
                        )
                    else:
                        error_msg = f"✅ {saved_count} maç yerel DB'ye kaydedildi\n⚠️ Supabase senkronizasyonu başarısız"
                        safe_msg = json.dumps(error_msg)
                        js_code = f"onError({safe_msg});"
                        self.main_window.web_view.page().runJavaScript(js_code)
                        
                        QMessageBox.warning(
                            None,
                            "Kısmi Başarı",
                            f"{error_msg}\n\nİnternet bağlantınızı kontrol edin."
                        )
                except Exception as sync_error:
                    print(f"⚠️ Supabase sync hatası: {sync_error}")
                    import json
                    error_msg = f"✅ {saved_count} maç yerel DB'ye kaydedildi\n⚠️ Cloud senkronizasyonu başarısız: {sync_error}"
                    safe_msg = json.dumps(error_msg)
                    js_code = f"onError({safe_msg});"
                    self.main_window.web_view.page().runJavaScript(js_code)
                    
                    QMessageBox.warning(
                        None,
                        "Kısmi Başarı",
                        f"{error_msg}\n\nYerel veri kaydedildi ama web sitesinde görünmeyebilir."
                    )
                
                print("=" * 50)
                
            except Exception as e:
                print(f"❌ HATA: {e}")
                import traceback
                traceback.print_exc()
                
                # JavaScript callback ile loading'i kapat
                import json
                error_msg = f"Gelecek maçlar işlenirken hata oluştu: {str(e)}"
                safe_msg = json.dumps(error_msg)
                js_code = f"onError({safe_msg});"
                self.main_window.web_view.page().runJavaScript(js_code)
                
                QMessageBox.critical(
                    None,
                    "Hata",
                    error_msg
                )
        
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Bet Smart")
            self.setGeometry(100, 100, 1100, 850)
            
            # Frameless pencere - Beyaz başlık çubuğunu kaldır
            self.setWindowFlags(Qt.FramelessWindowHint)
            
            # Menu bar KALDIRILDI - HTML'deki ayarlar butonu yeterli

            # WebEngineView oluştur
            self.web_view = QWebEngineView()
            
            # Bridge nesnesini oluştur ve kaydet
            self.bridge = Bridge(self)
            self.channel = QWebChannel()
            self.channel.registerObject("bridge", self.bridge)
            self.web_view.page().setWebChannel(self.channel)

            # Index.html'i yükle
            index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'index.html')
            self.web_view.setUrl(QUrl.fromLocalFile(index_path))
            
            self.setCentralWidget(self.web_view)
            
            # Telegram bot'u BAŞLATMA
            # Not: Bot isteğe bağlı olarak ayarlardan başlatılabilir
            # Otomatik başlatma - Telegram bot
            if self.bridge.telegram.is_configured():
                print("🤖 Telegram bot başlatılıyor...")
                self.bridge.telegram.start_bot()
                print("✅ Telegram bot otomatik başlatıldı")
                print("📸 Telegram'dan screenshot göndererek analiz yapabilirsiniz!")
            else:
                print("ℹ️ Telegram bot yapılandırılmamış")
                print("ℹ️ Ayarlardan Telegram bilgilerini girebilirsiniz")
            
            # Pencereyi taşımak için değişkenler
            self.dragging = False
            self.offset = None
        
        def mousePressEvent(self, event):
            """Pencereyi sürükle"""
            if event.button() == Qt.LeftButton:
                self.dragging = True
                self.offset = event.pos()
        
        def mouseMoveEvent(self, event):
            """Pencereyi taşı"""
            if self.dragging:
                self.move(self.mapToGlobal(event.pos() - self.offset))
        
        def mouseReleaseEvent(self, event):
            """Sürüklemeyi bırak"""
            self.dragging = False

    if __name__ == '__main__':
        try:
            app = QApplication(sys.argv)
            window = MainWindow()
            
            # Pencereyi ekranın ortasına yerleştir
            screen_geometry = app.desktop().availableGeometry()
            x = (screen_geometry.width() - window.width()) // 2
            y = (screen_geometry.height() - window.height()) // 2
            window.move(x, y)
            
            window.show()
            sys.exit(app.exec_())
        except Exception as e:
            with open('error_log.txt', 'w') as f:
                f.write(f"Error: {str(e)}\n")
                f.write(traceback.format_exc())
            print(f"Error: {str(e)}")
            print(traceback.format_exc())
            sys.exit(1)
except Exception as e:
    with open('error_log.txt', 'w') as f:
        f.write(f"Startup Error: {str(e)}\n")
        f.write(traceback.format_exc())
    print(f"Startup Error: {str(e)}")
    print(traceback.format_exc())
    sys.exit(1)
