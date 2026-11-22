"""
OCR ile screenshot'tan bahis oranlarını okuma ve analiz etme modülü
"""

import re
import numpy as np
from PIL import Image
import pytesseract
from typing import Dict, List, Optional

class OCRAnalyzer:
    def __init__(self):
        """
        OCR Analyzer başlatma
        
        NOT: Tesseract'ın yüklü olması gerekiyor:
        Windows: https://github.com/UB-Mannheim/tesseract/releases
        İndirip kurun ve aşağıdaki path'i düzenleyin
        """
        # Windows için Tesseract path
        # Tesseract kurulumundan sonra bu satırı aktif edin:
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        except:
            print("⚠️ Tesseract path ayarlanamadı. Varsayılan path kullanılacak.")
    
    def analyze_screenshot(self, image_path: str) -> Optional[Dict]:
        """
        Screenshot'tan bahis bilgilerini çıkar
        
        Args:
            image_path: Screenshot dosya yolu
            
        Returns:
            {
                'home_team': str,
                'away_team': str,
                'odd_1': float,
                'odd_x': float,
                'odd_2': float,
                'raw_text': str,
                'confidence': float
            }
        """
        try:
            # Resmi aç
            image = Image.open(image_path)
            original_image = image.copy()  # Orijinali sakla
            
            # Görüntü ön işleme - DENGELİ
            from PIL import ImageEnhance, ImageFilter, ImageOps
            
            # RGB'den grayscale'e çevir
            if image.mode != 'L':
                image = image.convert('L')
            
            # Hafif kontrast artırma
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            # Hafif keskinleştirme
            image = image.filter(ImageFilter.SHARPEN)
            
            # DEBUG: Resmi kaydet
            debug_path = "debug_ocr_preprocessed.png"
            image.save(debug_path)
            print(f"🖼️ İşlenmiş resim kaydedildi: {debug_path}")
            
            # 2. Versiyon: INVERT dene (beyaz yazı → siyah yazı)
            image_inverted = ImageOps.invert(image)
            debug_path2 = "debug_ocr_inverted.png"
            image_inverted.save(debug_path2)
            print(f"🖼️ Tersine çevrilmiş resim: {debug_path2}")
            
            # 3. Versiyon: ORİJİNAL (hiç işlem yapma!)
            if original_image.mode != 'L':
                original_gray = original_image.convert('L')
            else:
                original_gray = original_image
            debug_path3 = "debug_ocr_original.png"
            original_gray.save(debug_path3)
            print(f"🖼️ Orijinal resim: {debug_path3}")
            
            # Birden fazla OCR config dene
            configs = [
                r'--oem 3 --psm 6',   # PSM 6: Tek blok, whitelist YOK
                r'--oem 3 --psm 11',  # PSM 11: Dağınık text
                r'--oem 3 --psm 7',   # PSM 7: Tek satır
                r'--oem 1 --psm 6',   # OEM 1: LSTM
            ]
            
            text_numbers = None
            best_result = ""
            
            # 3 FARKLI RESİM DENE
            test_images = [
                ('original', original_gray),
                ('processed', image),
                ('inverted', image_inverted)
            ]
            
            # Her config'i dene, en çok nokta içereni al (en iyi oran tespiti)
            for idx, cfg in enumerate(configs):
                for img_name, test_img in test_images:
                    try:
                        result = pytesseract.image_to_string(test_img, lang='eng', config=cfg)
                        
                        # Sadece rakam/nokta/boşluk bırak (sonradan temizle)
                        result_clean = ''.join(c for c in result if c.isdigit() or c in '. \n')
                        
                        if result_clean.strip():
                            print(f"📊 Config {idx+1} {img_name}: {result_clean.strip()[:60]}")
                        
                        # Scoring: Nokta sayısı * 10 + karakter uzunluğu
                        score = result_clean.count('.') * 10 + len(result_clean.strip())
                        best_score = best_result.count('.') * 10 + len(best_result.strip())
                        
                        if score > best_score:
                            best_result = result_clean
                    except Exception as e:
                        continue
            
            text_numbers = best_result if best_result else ""
            
            # Sonra normal OCR (takım isimleri için)
            text_full = pytesseract.image_to_string(image, lang='tur+eng')
            
            print(f"📄 OCR çıktısı (RAKAMLAR):")
            print(text_numbers)
            print("="*50)
            print(f"📄 OCR çıktısı (TAM):")
            print(text_full)
            print("="*50)
            
            # Önce rakam OCR'ını dene
            result = self._parse_betting_text(text_numbers, prefer_numbers=True)
            
            # Başarısızsa tam text'i dene
            if not result or result['odd_1'] == 0.0:
                result = self._parse_betting_text(text_full, prefer_numbers=False)
            
            if result:
                result['raw_text'] = text_full
                return result
            
            return None
            
        except Exception as e:
            print(f"❌ OCR hatası: {e}")
            return None
    
    def _parse_betting_text(self, text: str, prefer_numbers: bool = False) -> Optional[Dict]:
        """
        OCR text'inden bahis bilgilerini çıkar
        
        Desteklenen formatlar:
        - "Fenerbahçe - Galatasaray"
        - "MS1: 2.10  MSX: 3.40  MS2: 3.20"
        - "1: 2.10  X: 3.40  2: 3.20"
        - "Ev Sahibi: 2.10  Beraberlik: 3.40  Deplasman: 3.20"
        """
        
        # Text'i satırlara böl
        lines = text.strip().split('\n')
        
        result = {
            'home_team': None,
            'away_team': None,
            'odd_1': 0.0,
            'odd_x': 0.0,
            'odd_2': 0.0,
            'confidence': 0.0
        }
        
        # Takım isimlerini bul
        team_patterns = [
            r'(.+?)\s*[-–—vs]\s*(.+)',  # "Fenerbahçe - Galatasaray"
            r'(.+?)\s+(?:ile|karşı)\s+(.+)',  # "Fenerbahçe ile Galatasaray"
        ]
        
        for line in lines:
            for pattern in team_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    result['home_team'] = match.group(1).strip()
                    result['away_team'] = match.group(2).strip()
                    break
            if result['home_team']:
                break
        
        # Oranları bul - Çeşitli formatlar
        odds_patterns = [
            # Format 1: "MS1: 2.10  MSX: 3.40  MS2: 3.20"
            r'MS1[:\s]+(\d+[.,]\d+).*?MSX[:\s]+(\d+[.,]\d+).*?MS2[:\s]+(\d+[.,]\d+)',
            
            # Format 2: "1: 2.10  X: 3.40  2: 3.20" veya "1: 2.10  0: 3.40  2: 3.20"
            r'1[:\s]+(\d+[.,]\d+).*?(?:X|0)[:\s]+(\d+[.,]\d+).*?2[:\s]+(\d+[.,]\d+)',
            
            # Format 3: Sadece 3 sayı grubu (noktasız da olabilir) "260 330 202"
            r'(\d{2,4})\s+(\d{2,4})\s+(\d{2,4})',
            
            # Format 4: Sadece sayılar yan yana noktalı "2.10  3.40  3.20"
            r'(\d+[.,]\d+)\s+(\d+[.,]\d+)\s+(\d+[.,]\d+)',
            
            # Format 5: "Ev: 2.10  Ber: 3.40  Dep: 3.20"
            r'Ev[:\s]+(\d+[.,]\d+).*?(?:Ber|X)[:\s]+(\d+[.,]\d+).*?Dep[:\s]+(\d+[.,]\d+)',
            
            # Format 6: Satır satır "2.60" "3.30" "2.80"
            r'(\d+[.,]\d+)\s*\n?\s*(\d+[.,]\d+)\s*\n?\s*(\d+[.,]\d+)',
        ]
        
        # Text'i temizle - tüm gürültü karakterlerini kaldır
        full_text = ' '.join(lines)
        # Noise karakterleri temizle
        noise_chars = ['[', ']', '(', ')', '{', '}', '@', '#', '$', '&', '*', '|']
        for char in noise_chars:
            full_text = full_text.replace(char, ' ')
        
        # Harfleri de temizle, sadece rakamları ve boşlukları bırak (oran tespiti için)
        import string
        odds_text = ''.join(c if c.isdigit() or c in [' ', '.', ',', '\n'] else ' ' for c in full_text)
        
        print(f"🧹 Temizlenmiş text (sadece rakamlar): {odds_text[:150]}")
        
        # Eğer prefer_numbers=True ise, önce basit noktalı rakamları bul
        if prefer_numbers:
            # Strateji 1: Noktalı rakamlar varsa direkt al
            simple_match = re.findall(r'(\d+[.,]\d+)', odds_text)
            if len(simple_match) >= 3:
                try:
                    result['odd_1'] = float(simple_match[0].replace(',', '.'))
                    result['odd_x'] = float(simple_match[1].replace(',', '.'))
                    result['odd_2'] = float(simple_match[2].replace(',', '.'))
                    
                    if all(1.01 <= odd <= 50.0 for odd in [result['odd_1'], result['odd_x'], result['odd_2']]):
                        print(f"✅ Oran bulundu (noktalı pattern): {result['odd_1']}/{result['odd_x']}/{result['odd_2']}")
                        result['confidence'] = 1.0
                        return result
                except:
                    pass
            
            # Strateji 2: NOKTASIZ 3 haneli rakamlar - İddaa mantığı
            # "260 324 202" gibi - Otomatik nokta ekle
            print(f"🔍 Noktasız rakam aranıyor: {odds_text[:100]}")
            
            # 2-4 haneli sayıları bul
            digit_groups = re.findall(r'\b(\d{2,4})\b', odds_text)
            print(f"🔢 Bulunan rakam grupları: {digit_groups}")
            
            # İlk 3 haneli rakamı al (100-999 arası veya 2-3 hane)
            valid_odds = []
            for num_str in digit_groups:
                num = int(num_str)
                # 2-4 haneli sayılar (10-9999 arası)
                if 10 <= num <= 9999:
                    # Noktayı ekle: 260 → 2.60, 324 → 3.24
                    if len(num_str) == 2:
                        odd_val = float(f"{num_str[0]}.{num_str[1]}")
                    elif len(num_str) == 3:
                        odd_val = float(f"{num_str[0]}.{num_str[1:]}")
                    elif len(num_str) == 4:
                        odd_val = float(f"{num_str[0:2]}.{num_str[2:]}")
                    else:
                        continue
                    
                    # Oran mantıklı aralıkta mı? (1.01 - 50.00)
                    if 1.01 <= odd_val <= 50.0:
                        valid_odds.append(odd_val)
                        print(f"  ✅ {num_str} → {odd_val}")
            
            # En az 3 oran bulunduysa kullan
            if len(valid_odds) >= 3:
                result['odd_1'] = valid_odds[0]
                result['odd_x'] = valid_odds[1]
                result['odd_2'] = valid_odds[2]
                print(f"✅ Oran bulundu (noktasız pattern): {result['odd_1']}/{result['odd_x']}/{result['odd_2']}")
                result['confidence'] = 1.0
                return result
        
        for idx, pattern in enumerate(odds_patterns):
            # İlk 3 pattern için temizlenmiş text, diğerleri için orijinal
            search_text = odds_text if idx in [2, 3, 5] else full_text
            match = re.search(pattern, search_text, re.IGNORECASE | re.DOTALL)
            if match:
                try:
                    # Virgülleri noktaya çevir ve rakamları düzelt
                    odd1_str = match.group(1).replace(',', '.')
                    odd2_str = match.group(2).replace(',', '.')
                    odd3_str = match.group(3).replace(',', '.')
                    
                    # Eğer nokta yoksa ve 2-4 haneliyse ekle (örn: "260" → "2.60")
                    if '.' not in odd1_str and len(odd1_str) >= 2:
                        if len(odd1_str) == 2:
                            odd1_str = odd1_str[0] + '.' + odd1_str[1:]  # 26 -> 2.6
                        else:
                            odd1_str = odd1_str[:-2] + '.' + odd1_str[-2:]  # 260 -> 2.60
                    
                    if '.' not in odd2_str and len(odd2_str) >= 2:
                        if len(odd2_str) == 2:
                            odd2_str = odd2_str[0] + '.' + odd2_str[1:]
                        else:
                            odd2_str = odd2_str[:-2] + '.' + odd2_str[-2:]
                    
                    if '.' not in odd3_str and len(odd3_str) >= 2:
                        if len(odd3_str) == 2:
                            odd3_str = odd3_str[0] + '.' + odd3_str[1:]
                        else:
                            odd3_str = odd3_str[:-2] + '.' + odd3_str[-2:]
                    
                    result['odd_1'] = float(odd1_str)
                    result['odd_x'] = float(odd2_str)
                    result['odd_2'] = float(odd3_str)
                    
                    # Oranlar mantıklı aralıkta mı?
                    if all(1.01 <= odd <= 50.0 for odd in [result['odd_1'], result['odd_x'], result['odd_2']]):
                        print(f"✅ Oran bulundu (pattern {idx+1}): {result['odd_1']}/{result['odd_x']}/{result['odd_2']}")
                        break
                    else:
                        print(f"⚠️ Oran aralık dışı (pattern {idx+1}): {result['odd_1']}/{result['odd_x']}/{result['odd_2']}")
                        result['odd_1'] = result['odd_x'] = result['odd_2'] = 0.0
                except Exception as e:
                    print(f"⚠️ Pattern {idx+1} parse hatası: {e}")
                    continue
        
        # Güven skoru hesapla
        confidence = 0.0
        if result['home_team'] and result['away_team']:
            confidence += 0.5
        if result['odd_1'] > 0 and result['odd_x'] > 0 and result['odd_2'] > 0:
            confidence += 0.5
        
        result['confidence'] = confidence
        
        # Minimum güven skoru kontrolü
        if confidence >= 0.5:
            return result
        
        return None
    
    def get_match_recommendation(self, ocr_result: Dict, db_history: List) -> tuple:
        """
        OCR sonucu ve geçmiş verilerle öneri oluştur
        
        Args:
            ocr_result: OCR'dan çıkan bahis bilgileri
            db_history: Veritabanından gelen geçmiş karşılaşmalar
            
        Returns:
            (message, keyboard): Telegram mesajı ve inline keyboard
        """
        if not ocr_result:
            return ("❌ OCR ile oran okunamadı", None)
        
        message = f"""
📱 <b>OKUNAN ORANLAR:</b>
MS1: {ocr_result['odd_1']:.2f} | MSX: {ocr_result['odd_x']:.2f} | MS2: {ocr_result['odd_2']:.2f}
"""
        
        keyboard = None  # Inline keyboard
        
        # Yeni format: dict with 'exact' and 'similar' keys
        if db_history and isinstance(db_history, dict):
            exact_matches = db_history.get('exact', [])
            similar_matches = db_history.get('similar', [])
            total_matches = db_history.get('total_count', 0)
            
            if total_matches > 0:
                message += f"\n📊 <b>BENZER ORANLI MAÇLAR ({total_matches} bulundu):</b>\n\n"
                
                # AYNI ORANLAR
                if exact_matches:
                    message += f"🎯 <b>AYNI ORANLAR ({len(exact_matches)} maç)</b>\n"
                    message += f"%100 oran eşleşmesi\n\n"
                    
                    for i, h in enumerate(exact_matches[:5], 1):  # İlk 5 göster
                        score = h.get('score', '').strip()
                        h_odd1 = h.get('odd_1', 0)
                        h_oddx = h.get('odd_x', 0)
                        h_odd2 = h.get('odd_2', 0)
                        message += f"📅 Skor: <b>{score if score else '?'}</b> | {h_odd1:.2f}/{h_oddx:.2f}/{h_odd2:.2f}\n"
                    
                    message += "\n"
                
                # YAKIN ORANLAR
                if similar_matches:
                    message += f"📊 <b>YAKIN ORANLAR ({len(similar_matches)} maç)</b>\n"
                    message += f"%98+ oran benzerliği\n\n"
                    
                    for i, h in enumerate(similar_matches[:5], 1):  # İlk 5 göster
                        score = h.get('score', '').strip()
                        h_odd1 = h.get('odd_1', 0)
                        h_oddx = h.get('odd_x', 0)
                        h_odd2 = h.get('odd_2', 0)
                        message += f"📅 Skor: <b>{score if score else '?'}</b> | {h_odd1:.2f}/{h_oddx:.2f}/{h_odd2:.2f}\n"
                    
                    message += "\n"
                
                # İstatistikler (tüm maçlar için)
                all_matches = exact_matches + similar_matches
                home_wins = 0
                draws = 0
                away_wins = 0
                kg_var = 0
                kg_yok = 0
                
                for h in all_matches:
                    score = h.get('score', '').strip()
                    if score and '-' in score:
                        try:
                            parts = score.split('-')
                            if len(parts) == 2:
                                home_score = int(parts[0].strip())
                                away_score = int(parts[1].strip())
                                
                                if home_score > away_score:
                                    home_wins += 1
                                elif home_score == away_score:
                                    draws += 1
                                else:
                                    away_wins += 1
                                
                                if home_score > 0 and away_score > 0:
                                    kg_var += 1
                                else:
                                    kg_yok += 1
                        except:
                            pass
                
                total_valid = home_wins + draws + away_wins
                if total_valid > 0:
                    message += f"━━━━━━━━━━━━━━━━━━━━━\n"
                    message += f"📊 <b>{total_valid} maç sonucu:</b>\n"
                    message += f"🏠 Ev Sahibi: <b>{home_wins}</b> galibiyet\n"
                    message += f"🤝 Beraberlik: <b>{draws}</b>\n"
                    message += f"✈️ Deplasman: <b>{away_wins}</b> galibiyet\n"
                    
                    kg_total = kg_var + kg_yok
                    if kg_total > 0:
                        message += f"\n⚽ <b>Karşılıklı Gol:</b>\n"
                        message += f"✅ Var: <b>{kg_var}</b>\n"
                        message += f"❌ Yok: <b>{kg_yok}</b>\n"
                    
                    message += f"\n💡 <b>ANALİZ SONUCU:</b>\n"
                    
                    max_result = max(home_wins, draws, away_wins)
                    
                    if max_result == home_wins and home_wins > 0:
                        message += f"   Benzer oranlı {total_valid} maçta ev sahibi {home_wins} kez kazandı\n"
                        message += f"   MS1 Oranı: <b>{ocr_result['odd_1']:.2f}</b>\n"
                            
                    elif max_result == away_wins and away_wins > 0:
                        message += f"   Benzer oranlı {total_valid} maçta deplasman {away_wins} kez kazandı\n"
                        message += f"   MS2 Oranı: <b>{ocr_result['odd_2']:.2f}</b>\n"
                            
                    elif max_result == draws and draws > 0:
                        message += f"   Benzer oranlı {total_valid} maçta {draws} beraberlik oldu\n"
                        message += f"   MSX Oranı: <b>{ocr_result['odd_x']:.2f}</b>\n"
                    else:
                        message += f"   Veriler yetersiz, net analiz yapılamadı\n"
                    
                    callback_data = f"ht_{ocr_result['odd_1']:.2f}_{ocr_result['odd_x']:.2f}_{ocr_result['odd_2']:.2f}"
                    
                    keyboard = {
                        'inline_keyboard': [[
                            {'text': '🔍 İlk Yarı Detayları', 'callback_data': callback_data}
                        ]]
                    }
                    
                else:
                    message += "\n⚠️ Skorlar eksik, istatistik çıkarılamadı"
            else:
                # Maç bulunamadı
                message += f"\n❌ <b>Benzer oranlı maç bulunamadı</b>\n\n"
                message += f"🔍 <b>Aranan Oranlar:</b>\n"
                message += f"   MS1: {ocr_result['odd_1']:.2f} | MSX: {ocr_result['odd_x']:.2f} | MS2: {ocr_result['odd_2']:.2f}\n\n"
                message += f"📊 <b>Neden bulunamadı?</b>\n"
                message += f"   • Bu oran kombinasyonu veritabanımızda yok\n"
                message += f"   • ±0.01 ve ±0.02 toleransla arandı\n"
                message += f"   • Nadir bir oran olabilir\n\n"
                message += f"💡 <b>Öneriler:</b>\n"
                message += f"   • Farklı bir maç deneyin\n"
                message += f"   • Daha yaygın oranlar daha fazla sonuç verir\n"
                message += f"   • Sistem sürekli yeni verilerle güncelleniyor"
        else:
            # Maç bulunamadı - Detaylı açıklama
            message += f"\n❌ <b>Benzer oranlı maç bulunamadı</b>\n\n"
            message += f"🔍 <b>Aranan Oranlar:</b>\n"
            message += f"   MS1: {ocr_result['odd_1']:.2f} | MSX: {ocr_result['odd_x']:.2f} | MS2: {ocr_result['odd_2']:.2f}\n\n"
            message += f"📊 <b>Neden bulunamadı?</b>\n"
            message += f"   • Bu oran kombinasyonu veritabanımızda yok\n"
            message += f"   • ±0.03 ve ±0.05 toleransla arandı\n"
            message += f"   • Nadir bir oran olabilir\n\n"
            message += f"💡 <b>Öneriler:</b>\n"
            message += f"   • Farklı bir maç deneyin\n"
            message += f"   • Daha yaygın oranlar daha fazla sonuç verir\n"
            message += f"   • Sistem sürekli yeni verilerle güncelleniyor"
        
        return (message, keyboard)


# Test için
if __name__ == "__main__":
    analyzer = OCRAnalyzer()
    
    print("""
📸 OCR TESTİ

Test için bir bahis screenshot'ı gerekli.
Screenshot şunları içermeli:
- Takım isimleri
- MS1, MSX, MS2 oranları

Örnek: "screenshot.png" dosyasını bu klasöre koyun
    """)
