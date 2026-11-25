import asyncio
import threading
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from database import Database
from ocr_analyzer import OCRAnalyzer
import re
import os
import json
import pyperclip
from hybrid_fetch import fetch_matches_hybrid
from supabase_sync import sync_matches_to_supabase

class TelegramBotManager:
    def __init__(self):
        self.db = Database()
        self.ocr = OCRAnalyzer()
        
        # Önce config.json'dan oku, yoksa veritabanından
        self.bot_token, self.chat_id = self._load_credentials()
        
        self.app = None
        self.bot = None
        self.is_running = False
        
        # Rate limiting için son istek zamanı
        self.last_yeniveri_time = 0
        self.yeniveri_cooldown = 30  # 30 saniye cooldown (test için)
    
    def _load_credentials(self):
        """Telegram bilgilerini config.json'dan veya veritabanından yükle"""
        # Önce config.json'u dene
        config_path = 'config.json'
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    bot_token = config.get('telegram', {}).get('bot_token')
                    chat_id = config.get('telegram', {}).get('chat_id')
                    
                    if bot_token and chat_id:
                        # Veritabanına da kaydet (senkronizasyon için)
                        self.db.save_setting('telegram_bot_token', bot_token)
                        self.db.save_setting('telegram_chat_id', chat_id)
                        print("✅ Telegram ayarları config.json'dan yüklendi")
                        return bot_token, chat_id
            except Exception as e:
                print(f"⚠️ config.json okunamadı: {e}")
        
        # config.json yoksa veya okunamazsa veritabanından oku
        bot_token = self.db.get_setting('telegram_bot_token')
        chat_id = self.db.get_setting('telegram_chat_id')
        print("ℹ️ Telegram ayarları veritabanından yüklendi")
        return bot_token, chat_id
    
    def update_credentials(self, bot_token, chat_id):
        """Bot bilgilerini güncelle"""
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.db.save_setting('telegram_bot_token', bot_token)
        self.db.save_setting('telegram_chat_id', chat_id)
        
        # config.json'a da kaydet (kalıcı olması için)
        config_path = 'config.json'
        config = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except:
                pass
        
        config['telegram'] = {
            'bot_token': bot_token,
            'chat_id': chat_id
        }
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            print("✅ Telegram ayarları config.json'a kaydedildi")
        except Exception as e:
            print(f"⚠️ config.json yazılamadı: {e}")
        
        if self.bot:
            self.bot = Bot(token=bot_token)
    
    def is_configured(self):
        """Bot yapılandırılmış mı?"""
        return bool(self.bot_token and self.chat_id)
    
    async def send_message_async(self, message, reply_markup=None):
        """Mesaj gönder (async)"""
        if not self.is_configured():
            return False
        
        try:
            if not self.bot:
                self.bot = Bot(token=self.bot_token)
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            return True
        except Exception as e:
            print(f"Telegram mesaj hatası: {e}")
            return False
    
    def send_message(self, message, reply_markup=None):
        """Mesaj gönder (sync wrapper)"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.send_message_async(message, reply_markup))
            loop.close()
            return result
        except Exception as e:
            print(f"Mesaj gönderme hatası: {e}")
            return False
    
    def send_bulletin_notification(self, match_count):
        """Bülten yüklendiğinde bildirim gönder"""
        message = f"""
📋 <b>YENİ BÜLTEN YÜKLENDİ</b>

✅ {match_count} maç veritabanına eklendi

/bulten komutu ile bugünün maçlarını görebilirsiniz.
"""
        return self.send_message(message)
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bot başlatma komutu"""
        await update.message.reply_text(
            "🎯 <b>BetSmart Bot'a Hoş Geldiniz!</b>\n\n"
            "📋 <b>Komutlar:</b>\n"
            "/durum - Sistem durumunu kontrol et\n"
            "/yeniveri - Güncel maç verilerini çek\n\n"
            "📸 <b>Screenshot Analizi:</b>\n"
            "Bahis sitesinden screenshot atın,\n"
            "oranları okuyup analiz edelim!\n\n"
            "💡 /yeniveri ile 2 günlük maçları otomatik çekin!",
            parse_mode='HTML'
        )
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Sistem durumunu göster"""
        # Toplam maç sayısını al
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM matches')
        total_matches = cursor.fetchone()[0]
        conn.close()
        
        # Durum mesajı
        message = "✅ <b>SİSTEM DURUMU</b>\n\n"
        message += "🟢 Sistem sorunsuz çalışıyor\n\n"
        message += f"📊 Veritabanında <b>{total_matches:,}</b> maç kayıtlı\n\n"
        message += "🍀 Bol şanslar!"
        
        await update.message.reply_text(
            message,
            parse_mode='HTML'
        )
    
    async def cmd_yeniveri(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Veri kaynağından tam otomatik veri çek"""
        try:
            # Cooldown kontrolü
            import time
            current_time = time.time()
            time_since_last = current_time - self.last_yeniveri_time
            
            # Günlük kullanım sayacı (basit versiyon - her gün sıfırlanır)
            today = time.strftime("%Y-%m-%d")
            usage_key = f"yeniveri_usage_{today}"
            
            # Basit counter (gerçek uygulamada veritabanında tutulmalı)
            if not hasattr(self, 'daily_usage'):
                self.daily_usage = {}
            
            if usage_key not in self.daily_usage:
                self.daily_usage = {usage_key: 0}  # Yeni gün, sıfırla
            
            current_usage = self.daily_usage.get(usage_key, 0)
            remaining = 3 - current_usage
            
            # Son çekme zamanı
            if time_since_last < 60:
                last_time_text = f"{int(time_since_last)} saniye önce"
            else:
                last_time_text = f"{int(time_since_last // 60)} dakika önce"
            
            # Onay mesajı göster
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Evet, Başlat", callback_data="yeniveri_confirm"),
                    InlineKeyboardButton("❌ İptal", callback_data="yeniveri_cancel")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"🔄 <b>Veri Güncelleme</b>\n\n"
                f"📊 2 günlük maç verisi çekilecek\n"
                f"⏱️ Süre: Yaklaşık 1 dakika\n"
                f"🎯 Kalan hak: {remaining}/3 (günlük)\n\n"
                f"⚠️ <b>Neden sınırlı?</b>\n"
                f"Aşırı kullanımda veri kaynağı tarafından\n"
                f"engellenme riski var. Sağlıklı çalışma için\n"
                f"günlük limit koyuyoruz.\n\n"
                f"💡 Son çekme: {last_time_text if self.last_yeniveri_time > 0 else 'Henüz çekilmedi'}\n\n"
                f"Devam etmek istiyor musunuz?",
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Hata</b>\n\n{str(e)}",
                parse_mode='HTML'
            )
    
    async def handle_yeniveri_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Yeniveri onay/iptal butonları"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "yeniveri_cancel":
            await query.edit_message_text(
                "❌ <b>İşlem İptal Edildi</b>\n\n"
                "Veri güncelleme iptal edildi.",
                parse_mode='HTML'
            )
            return
        
        # Onaylandı, veri çekme işlemini başlat
        try:
            import time
            current_time = time.time()
            
            # Günlük kullanım kontrolü
            today = time.strftime("%Y-%m-%d")
            usage_key = f"yeniveri_usage_{today}"
            
            if not hasattr(self, 'daily_usage'):
                self.daily_usage = {}
            
            if usage_key not in self.daily_usage:
                self.daily_usage = {usage_key: 0}
            
            current_usage = self.daily_usage.get(usage_key, 0)
            
            if current_usage >= 3:
                await query.edit_message_text(
                    "⛔ <b>Günlük Limit Doldu</b>\n\n"
                    "Bugün için 3 çekme hakkınız doldu.\n"
                    "Yarın tekrar deneyebilirsiniz.",
                    parse_mode='HTML'
                )
                return
            
            status_msg = await query.edit_message_text(
                "🌐 <b>Veri kaynağından bilgiler alınıyor...</b>\n\n"
                "📅 2 günlük maç takvimi kontrol ediliyor...\n"
                "⏳ Lütfen bekleyin...",
                parse_mode='HTML'
            )
            
            # Son istek zamanını güncelle
            self.last_yeniveri_time = current_time
            self.daily_usage[usage_key] = current_usage + 1
            
            # Callback fonksiyonu - durum güncellemeleri için
            day_names = ["Bugün", "Yarın"]
            day_counts = [0, 0]  # Her günün maç sayısı
            
            async def update_status(status):
                if status.startswith("date_") and "_trying_time_view" in status:
                    await status_msg.edit_text(
                        "🔍 <b>Lig Bazlı Liste:</b> Maç bulunamadı\n"
                        "   💡 Liglere göre gruplandırma\n\n"
                        "🔄 <b>Saat Bazlı Liste:</b> Kontrol ediliyor...\n"
                        "   ⏰ Saate göre sıralama\n\n"
                        "⏳ <b>Tahmini süre:</b> ~1 dakika\n"
                        "⚠️ Lütfen başka işlem yapmayın...",
                        parse_mode='HTML'
                    )
                elif status.startswith("day_"):
                    # day_0_150 formatında geliyor (gün indexi ve maç sayısı)
                    parts = status.split("_")
                    day_idx = int(parts[1])
                    match_count = int(parts[2])
                    day_counts[day_idx] = match_count
                    
                    # Mesajı oluştur
                    msg = "📅 <b>Veri kaynağından bilgiler alınıyor...</b>\n\n"
                    
                    for i in range(len(day_names)):
                        if i < day_idx:
                            # Tamamlanmış gün
                            msg += f"✅ <b>{day_names[i]}:</b> {day_counts[i]} maç bulundu\n"
                        elif i == day_idx:
                            # Şu anki gün (yeni tamamlandı)
                            msg += f"✅ <b>{day_names[i]}:</b> {day_counts[i]} maç bulundu\n"
                        else:
                            # Henüz başlanmamış
                            msg += f"⚪ <b>{day_names[i]}:</b> Bekliyor...\n"
                    
                    # Eğer son gün değilse "kontrol ediliyor" ekle
                    if day_idx < len(day_names) - 1:
                        msg += f"\n🔄 <b>{day_names[day_idx + 1]}</b> kontrol ediliyor...\n"
                        msg += "⏳ Lütfen bekleyin..."
                    
                    await status_msg.edit_text(msg, parse_mode='HTML')
            
                elif status.startswith("day_"):
                    # day_0_150 formatında geliyor (gün indexi ve maç sayısı)
                    parts = status.split("_")
                    day_idx = int(parts[1])
                    match_count = int(parts[2])
                    day_counts[day_idx] = match_count
                    
                    # Mesajı oluştur
                    msg = "📅 <b>Veri kaynağından bilgiler alınıyor...</b>\n\n"
                    
                    for i in range(len(day_names)):
                        if i < day_idx:
                            # Tamamlanmış gün
                            msg += f"✅ <b>{day_names[i]}:</b> {day_counts[i]} maç bulundu\n"
                        elif i == day_idx:
                            # Şu anki gün (yeni tamamlandı)
                            msg += f"✅ <b>{day_names[i]}:</b> {day_counts[i]} maç bulundu\n"
                        else:
                            # Henüz başlanmamış
                            msg += f"⚪ <b>{day_names[i]}:</b> Bekliyor...\n"
                    
                    # Eğer son gün değilse "kontrol ediliyor" ekle
                    if day_idx < len(day_names) - 1:
                        msg += f"\n🔄 <b>{day_names[day_idx + 1]}</b> kontrol ediliyor...\n"
                        msg += "⏳ Lütfen bekleyin..."
                    
                    await status_msg.edit_text(msg, parse_mode='HTML')
            
            # Hybrid API'den veri çek (Sahadan → Mackolik fallback)
            import asyncio
            loop = asyncio.get_event_loop()
            success, matches, error, source = await loop.run_in_executor(
                None, 
                lambda: fetch_matches_hybrid(days_ahead=2, status_callback=lambda s: asyncio.run_coroutine_threadsafe(update_status(s), loop))
            )
            
            if not success:
                await status_msg.edit_text(
                    f"❌ <b>API Hatası</b>\n\n{error}",
                    parse_mode='HTML'
                )
                return
            
            if not matches:
                await status_msg.edit_text(
                    "⚠️ <b>Maç Bulunamadı</b>\n\n"
                    "Seçilen tarihlerde maç yok.\n"
                    "💡 Başka bir zaman tekrar deneyin.",
                    parse_mode='HTML'
                )
                return
            
            # Benzersiz maç sayısını hesapla
            unique_matches = len(set(f"{m.get('datetime')}|{m.get('home_team')}|{m.get('away_team')}" for m in matches))
            
            await status_msg.edit_text(
                f"✅ <b>Maçlar Bulundu!</b>\n\n"
                f"📊 Toplam <b>{unique_matches}</b> maç\n"
                f"📅 2 günlük takvim\n\n"
                f"⚙️ Supabase'e kaydediliyor...",
                parse_mode='HTML'
            )
            
            # Supabase'e kaydet
            result = await loop.run_in_executor(None, lambda: sync_matches_to_supabase(matches))
            success_count = result[0]
            errors = result[1] if len(result) > 1 else 0
            cleanup_count = result[2] if len(result) > 2 else 0
            
            if success_count > 0:
                # Bugünkü ve yarınki maç sayısını hesapla
                from datetime import datetime, timedelta
                today = datetime.now().strftime("%d.%m.%Y")
                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
                
                today_matches = sum(1 for m in matches if m.get('datetime', '').startswith(today.split('.')[0] + '.' + today.split('.')[1]))
                tomorrow_matches = sum(1 for m in matches if m.get('datetime', '').startswith(tomorrow.split('.')[0] + '.' + tomorrow.split('.')[1]))
                
                # Temizlik mesajı (eğer temizlik yapıldıysa)
                cleanup_msg = ""
                if cleanup_count > 0:
                    cleanup_msg = f"🗑️  {cleanup_count} eski maç temizlendi\n"
                
                # Oran takipçisini tetikle (yeni oranları odds_changes'e kaydetsin)
                await status_msg.edit_text(
                    f"✅ <b>Maçlar Kaydedildi!</b>\n\n"
                    f"{cleanup_msg}"
                    f"📊 <b>{success_count}</b> maç kaydedildi\n\n"
                    f"🔄 İlk oranlar kaydediliyor...",
                    parse_mode='HTML'
                )
                
                # Match details fetch et (H2H ve form verileri)
                details_status = ""
                try:
                    from fetch_all_match_details import fetch_all_match_details_for_future_matches
                    
                    await status_msg.edit_text(
                        f"✅ <b>Maçlar Kaydedildi!</b>\n\n"
                        f"{cleanup_msg}"
                        f"📊 <b>{success_count}</b> maç kaydedildi\n\n"
                        f"🔄 İlk oranlar kaydediliyor...\n"
                        f"📊 Maç detayları çekiliyor (H2H, form)...",
                        parse_mode='HTML'
                    )
                    
                    # Match details fetch (thread'de çalıştır, 1-2 dakika sürebilir)
                    # Returns: (success_count, error_count, skipped_count)
                    details_result = await loop.run_in_executor(
                        None, 
                        fetch_all_match_details_for_future_matches
                    )
                    
                    # Tuple unpack
                    success_detail_count, failed_detail_count, skipped_count = details_result
                    
                    if success_detail_count > 0:
                        details_status = f"📊 {success_detail_count} maç detayı eklendi\n"
                        if failed_detail_count > 0:
                            details_status += f"⚠️ {failed_detail_count} maç detayı alınamadı\n"
                    elif failed_detail_count > 0:
                        details_status = f"⚠️ {failed_detail_count} maç detayı alınamadı\n"
                    else:
                        details_status = "⚠️ Maç detayları alınamadı\n"
                        
                except Exception as e:
                    print(f"Match details hatası: {e}")
                    import traceback
                    traceback.print_exc()
                    details_status = "⚠️ Maç detayı hatası\n"
                
                # İlk oranları odds_changes'e kaydet (Sahadan'dan tekrar çekmeden!)
                try:
                    def save_initial_odds():
                        """Yeni maçların ilk oranlarını odds_changes'e kaydet"""
                        from supabase_sync import get_supabase_client
                        from datetime import datetime
                        client = get_supabase_client()
                        
                        saved_count = 0
                        updated_count = 0
                        total = len(matches)
                        
                        print(f"\n🔄 İlk oranlar kaydediliyor... ({total} maç)")
                        
                        for idx, match in enumerate(matches, 1):
                            try:
                                # Kontrol et: Bu maç daha önce eklendi mi?
                                existing = client.table('odds_changes').select('*').eq(
                                    'home_team', match['home_team']
                                ).eq('away_team', match['away_team']).eq(
                                    'match_datetime', match['datetime']
                                ).execute()
                                
                                if existing.data and len(existing.data) > 0:
                                    # MEVCUT MAÇ - Sadece current_odd güncelle
                                    client.table('odds_changes').update({
                                        'current_odd_1': match.get('odd_1'),
                                        'current_odd_x': match.get('odd_x'),
                                        'current_odd_2': match.get('odd_2'),
                                        'last_updated_at': datetime.now().isoformat()
                                    }).eq('id', existing.data[0]['id']).execute()
                                    updated_count += 1
                                else:
                                    # YENİ MAÇ - İlk oranları kaydet
                                    client.table('odds_changes').insert({
                                        'match_datetime': match['datetime'],
                                        'home_team': match['home_team'],
                                        'away_team': match['away_team'],
                                        'league': match.get('league'),
                                        'first_odd_1': match.get('odd_1'),
                                        'first_odd_x': match.get('odd_x'),
                                        'first_odd_2': match.get('odd_2'),
                                        'current_odd_1': match.get('odd_1'),
                                        'current_odd_x': match.get('odd_x'),
                                        'current_odd_2': match.get('odd_2'),
                                        'change_1': 0,
                                        'change_x': 0,
                                        'change_2': 0,
                                        'change_direction': 'none',
                                        'total_change': 0,
                                        'telegram_sent': False,
                                        'first_detected_at': datetime.now().isoformat(),
                                        'last_updated_at': datetime.now().isoformat()
                                    }).execute()
                                    saved_count += 1
                                
                                # Progress bar
                                if idx % (total // 10) == 0 or idx == total:
                                    percentage = int((idx / total) * 100)
                                    filled = int((idx / total) * 10)
                                    bar = '▓' * filled + '░' * (10 - filled)
                                    print(f"   {bar} {percentage}% ({idx}/{total})")
                                    
                            except Exception as e:
                                # Sessizce devam et
                                continue
                        
                        print(f"✅ Tamamlandı: {saved_count} yeni, {updated_count} güncelleme\n")
                        return saved_count, updated_count
                    
                    # Thread'de çalıştır
                    saved, updated = await loop.run_in_executor(None, save_initial_odds)
                    
                    if saved > 0 or updated > 0:
                        odds_status = f"✅ İlk oranlar kaydedildi ({saved} yeni, {updated} güncelleme)"
                    else:
                        odds_status = "⚠️ Oran kaydı yapılamadı"
                        
                except Exception as e:
                    odds_status = f"⚠️ Oran kayıt hatası: {str(e)}"
                
                await status_msg.edit_text(
                    f"✅ <b>İşlem Tamamlandı!</b>\n\n"
                    f"{cleanup_msg}"
                    f"📊 <b>{success_count}</b> maç kaydedildi\n"
                    f"☁️ Supabase'e yüklendi\n"
                    f"🌐 Web sitesinde görünür\n"
                    f"{odds_status}\n"
                    f"{details_status}\n"
                    f"📅 <b>Tarih Dağılımı:</b>\n"
                    f"   • Bugün: {today_matches} maç\n"
                    f"   • Yarın: {tomorrow_matches} maç\n"
                    f"   • Diğer: {success_count - today_matches - tomorrow_matches} maç\n\n"
                    f"🔗 <a href='https://betsmart-web.vercel.app'>Web Sitesi</a>",
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )
            else:
                await status_msg.edit_text(
                    f"⚠️ <b>Kayıt Sorunu</b>\n\n"
                    f"📊 {len(matches)} maç bulundu\n"
                    f"❌ Supabase'e kaydedilemedi\n\n"
                    f"💡 Veritabanı bağlantısını kontrol edin.",
                    parse_mode='HTML'
                )
                
        except Exception as e:
            await query.message.reply_text(
                f"❌ <b>Hata</b>\n\n{str(e)}",
                parse_mode='HTML'
            )
    
    async def cmd_otocekim(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Veri kaynağından tam otomatik veri çek (Selenium)"""
        try:
            # Başlangıç mesajı
            status_msg = await update.message.reply_text(
                "🤖 <b>Otomatik Veri Çekme Başlatılıyor...</b>\n\n"
                "⏳ Bu işlem 15-20 saniye sürebilir.\n"
                "⚠️  Not: Selenium bazen LİG butonunu bulamayabilir.",
                parse_mode='HTML'
            )
            
            # Veri çek (blocking operation, thread'de çalışmalı)
            import asyncio
            loop = asyncio.get_event_loop()
            success, data, error = await loop.run_in_executor(None, scrape_mackolik_iddaa)
            
            if not success:
                await status_msg.edit_text(
                    f"❌ <b>Scraping Hatası</b>\n\n"
                    f"{error}\n\n"
                    f"💡 Manuel yöntem için /yeniveri kullanın",
                    parse_mode='HTML'
                )
                return
            
            # Durum güncelle
            await status_msg.edit_text(
                f"✅ <b>Veri Çekildi!</b>\n\n"
                f"📊 {len(data):,} karakter\n\n"
                f"⚙️ Veriler işleniyor...",
                parse_mode='HTML'
            )
            
            # Format algıla ve işle
            def process_data():
                """Veriyi işle ve Supabase'e kaydet"""
                try:
                    # Format algıla (ilk 50 satıra bak)
                    lines = data.split('\n')
                    has_league_headers = False
                    
                    # İlk 50 satırda lig başlığı formatını ara
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
                            break
                    
                    # Format'a göre parse et
                    if has_league_headers:
                        print("📋 Format: LİG görünümü")
                        matches = parse_league_view_format(data)
                    else:
                        print("📋 Format: SAAT görünümü")
                        matches = parse_new_mackolik_format(data)
                    
                    if not matches:
                        return False, 0, "Maç bulunamadı"
                    
                    # Tekrar eden maçları temizle
                    seen = set()
                    unique_matches = []
                    for match in matches:
                        key = f"{match['datetime']}|{match['home_team']}|{match['away_team']}"
                        if key not in seen:
                            seen.add(key)
                            unique_matches.append(match)
                    
                    matches = unique_matches
                    
                    # Supabase'e kaydet
                    success_count, errors = sync_matches_to_supabase(matches)
                    
                    if success_count > 0:
                        return True, success_count, f"✅ {success_count} maç kaydedildi"
                    else:
                        return False, len(matches), "Supabase kayıt hatası"
                    
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    return False, 0, f"İşleme hatası: {str(e)}"
            
            # Veriyi işle
            proc_success, match_count, proc_message = await loop.run_in_executor(None, process_data)
            
            if proc_success:
                await status_msg.edit_text(
                    f"✅ <b>İşlem Tamamlandı!</b>\n\n"
                    f"📊 <b>{match_count}</b> maç işlendi\n"
                    f"☁️ Supabase'e kaydedildi\n"
                    f"🌐 Web sitesinde görünür\n\n"
                    f"🔗 https://betsmart-web.vercel.app",
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )
            else:
                await status_msg.edit_text(
                    f"⚠️ <b>Kısmi Başarı</b>\n\n"
                    f"📊 {match_count} maç bulundu\n"
                    f"❌ {proc_message}",
                    parse_mode='HTML'
                )
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Beklenmeyen Hata</b>\n\n"
                f"Hata: {str(e)}",
                parse_mode='HTML'
            )
    
    async def cmd_yukle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clipboard'dan veri al ve işle"""
        try:
            status_msg = await update.message.reply_text(
                "📋 <b>Clipboard'dan veri okunuyor...</b>",
                parse_mode='HTML'
            )
            
            # Clipboard'dan oku
            import asyncio
            loop = asyncio.get_event_loop()
            
            def get_clipboard():
                import pyperclip
                return pyperclip.paste()
            
            data = await loop.run_in_executor(None, get_clipboard)
            
            if not data or len(data) < 100:
                await status_msg.edit_text(
                    "❌ <b>Clipboard Boş!</b>\n\n"
                    "Lütfen önce veri kaynağından kopyalayın:\n"
                    "1. Veri sayfasını açın\n"
                    "2. LİG butonuna tıkla\n"
                    "3. CTRL+A, CTRL+C\n"
                    "4. /yukle yaz",
                    parse_mode='HTML'
                )
                return
            
            await status_msg.edit_text(
                f"✅ <b>Veri Alındı!</b>\n\n"
                f"📊 {len(data):,} karakter\n\n"
                f"⚙️ İşleniyor...",
                parse_mode='HTML'
            )
            
            # Veriyi işle
            def process_clipboard_data():
                try:
                    # Format algıla
                    lines = data.split('\n')
                    has_league_headers = False
                    
                    for line in lines[:50]:
                        stripped = line.strip()
                        if len(stripped) > 10 and ' - ' in stripped:
                            skip_keywords = ['maç sonucu', 'çifte şans', 'altı', 'üstü', 'saat', 'canlı', 'arama', 'futbol', 'basketbol', 'haberler']
                            if any(keyword in stripped.lower() for keyword in skip_keywords):
                                continue
                            if len(stripped) <= 5 and stripped.replace(' ', '').isupper():
                                continue
                            has_league_headers = True
                            break
                    
                    # Parse et
                    if has_league_headers:
                        matches = parse_league_view_format(data)
                    else:
                        matches = parse_new_mackolik_format(data)
                    
                    if not matches:
                        return False, 0, "Maç bulunamadı"
                    
                    # Tekrarları temizle
                    seen = set()
                    unique_matches = []
                    for match in matches:
                        key = f"{match['datetime']}|{match['home_team']}|{match['away_team']}"
                        if key not in seen:
                            seen.add(key)
                            unique_matches.append(match)
                    
                    matches = unique_matches
                    
                    # Supabase'e kaydet
                    success_count, errors = sync_matches_to_supabase(matches)
                    
                    if success_count > 0:
                        return True, success_count, ""
                    else:
                        return False, len(matches), "Supabase hatası"
                        
                except Exception as e:
                    return False, 0, str(e)
            
            proc_success, match_count, error_msg = await loop.run_in_executor(None, process_clipboard_data)
            
            if proc_success:
                await status_msg.edit_text(
                    f"✅ <b>Başarılı!</b>\n\n"
                    f"📊 <b>{match_count}</b> maç kaydedildi\n"
                    f"☁️ Supabase'e yüklendi\n"
                    f"🌐 Web sitesinde görünür\n\n"
                    f"🔗 https://betsmart-web.vercel.app",
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )
            else:
                await status_msg.edit_text(
                    f"❌ <b>Hata</b>\n\n"
                    f"📊 {match_count} maç bulundu\n"
                    f"❌ {error_msg}",
                    parse_mode='HTML'
                )
                
        except Exception as e:
            await update.message.reply_text(
                f"❌ Hata: {str(e)}",
                parse_mode='HTML'
            )
            
            # Veri çek (blocking operation, thread'de çalışmalı)
            import asyncio
            loop = asyncio.get_event_loop()
            success, data, error = await loop.run_in_executor(None, scrape_mackolik_iddaa)
            
            if not success:
                await status_msg.edit_text(
                    f"❌ <b>Veri Çekme Hatası</b>\n\n"
                    f"Hata: {error}\n\n"
                    f"Lütfen daha sonra tekrar deneyin.",
                    parse_mode='HTML'
                )
                return
            
            # Durum güncelle
            await status_msg.edit_text(
                f"✅ <b>Veri Çekildi!</b>\n\n"
                f"📊 {len(data):,} karakter\n\n"
                f"⚙️ Veriler işleniyor...",
                parse_mode='HTML'
            )
            
            # Format algıla ve işle
            def process_data():
                """Veriyi işle ve Supabase'e kaydet"""
                try:
                    # Format algıla (ilk 50 satıra bak)
                    lines = data.split('\n')
                    has_league_headers = False
                    
                    # İlk 50 satırda lig başlığı formatını ara
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
                            break
                    
                    # Format'a göre parse et
                    if has_league_headers:
                        print("📋 Format: LİG görünümü")
                        matches = parse_league_view_format(data)
                    else:
                        print("📋 Format: SAAT görünümü")
                        matches = parse_new_mackolik_format(data)
                    
                    if not matches:
                        return False, 0, "Maç bulunamadı"
                    
                    # Tekrar eden maçları temizle
                    seen = set()
                    unique_matches = []
                    for match in matches:
                        key = f"{match['datetime']}|{match['home_team']}|{match['away_team']}"
                        if key not in seen:
                            seen.add(key)
                            unique_matches.append(match)
                    
                    matches = unique_matches
                    
                    # Supabase'e kaydet
                    success_count, errors = sync_matches_to_supabase(matches)
                    
                    if success_count > 0:
                        return True, success_count, f"✅ {success_count} maç kaydedildi"
                    else:
                        return False, len(matches), "Supabase kayıt hatası"
                    
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    return False, 0, f"İşleme hatası: {str(e)}"
            
            # Veriyi işle
            proc_success, match_count, proc_message = await loop.run_in_executor(None, process_data)
            
            if proc_success:
                await status_msg.edit_text(
                    f"✅ <b>İşlem Tamamlandı!</b>\n\n"
                    f"📊 <b>{match_count}</b> maç işlendi\n"
                    f"☁️ Supabase'e kaydedildi\n"
                    f"🌐 Web sitesinde görünür\n\n"
                    f"🔗 https://betsmart-web.vercel.app",
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )
            else:
                await status_msg.edit_text(
                    f"⚠️ <b>İşlem Tamamlandı Ama...</b>\n\n"
                    f"📊 {match_count} maç bulundu\n"
                    f"❌ Kayıt hatası: {proc_message}",
                    parse_mode='HTML'
                )
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Beklenmeyen Hata</b>\n\n"
                f"Hata: {str(e)}",
                parse_mode='HTML'
            )
    
    async def callback_analyze(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maç analizi callback"""
        query = update.callback_query
        await query.answer()
        
        # Match ID'yi al
        match_id = int(query.data.split('_')[1])
        
        # Analiz yap
        analysis = self.db.get_match_analysis(match_id)
        
        if not analysis:
            await query.edit_message_text("❌ Maç bulunamadı.")
            return
        
        match = analysis['match']
        history = analysis['history']
        
        message = f"""
⚽ <b>{match[4]} vs {match[5]}</b>
🏆 {match[3]} | ⏰ {match[2]}

📊 <b>ORANLAR:</b>
1: {match[8]} | X: {match[9]} | 2: {match[10]}
Alt: {match[11]} | Üst: {match[12]}

📈 <b>GEÇMİŞ KARŞILAŞMALAR:</b>
"""
        
        if history:
            for h in history:
                message += f"\n📅 {h[1]} | Skor: {h[6]} | İY: {h[7]}"
            
            # Basit istatistik
            home_wins = sum(1 for h in history if h[6] and h[6].split('-')[0] > h[6].split('-')[1])
            draws = sum(1 for h in history if h[6] and h[6].split('-')[0] == h[6].split('-')[1])
            away_wins = sum(1 for h in history if h[6] and h[6].split('-')[0] < h[6].split('-')[1])
            
            message += f"""

📊 <b>İSTATİSTİK:</b>
Ev Sahibi: {home_wins} galibiyet
Beraberlik: {draws}
Deplasman: {away_wins} galibiyet

💡 <b>TAVSİYE:</b>
"""
            if home_wins > away_wins:
                message += f"Ev sahibi avantajlı görünüyor."
            elif away_wins > home_wins:
                message += f"Deplasman takımı avantajlı."
            else:
                message += f"Dengeli bir maç bekleniyor."
        else:
            message += "\n❌ Geçmiş karşılaşma bulunamadı."
        
        # Geri butonu
        keyboard = [[InlineKeyboardButton("◀️ Geri", callback_data="back_to_bulletin")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Text mesaj handler - Nesine kupon linki algılama"""
        try:
            if not update.message or not update.message.text:
                print("⚠️ Mesaj veya text bulunamadı")
                return
            
            text = update.message.text
            print(f"📩 Text mesaj alındı: {text[:50]}...")
            
            # Nesine kupon linki mi? (hem tam link hem kısa link)
            # Format 1: https://nsn.li/XXXXX
            # Format 2: https://www.nesine.com/Iddaa/ViewCoupon?t=...
            # Format 3: https://www.nesine.com/kupon/XXXXX
            is_nesine_link = (
                'nsn.li' in text.lower() or
                ('nesine.com' in text.lower() and ('viewcoupon' in text.lower() or '/kupon/' in text.lower()))
            )
            
            if is_nesine_link:
                print(f"🔗 Nesine kupon linki algılandı: {text}")
                
                # URL'yi temizle (sadece ilk satırı al, boşlukları temizle)
                url = text.strip().split('\n')[0].split(' ')[0]
                
                # HTTP/HTTPS kontrolü
                if not url.startswith('http'):
                    url = 'https://' + url
                
                print(f"🌐 Temizlenmiş URL: {url}")
                
                # Kullanıcıya bilgi ver
                status_msg = await update.message.reply_text("🎯 Nesine kuponu parse ediliyor...")
                print("✅ Yanıt mesajı gönderildi")
                
                try:
                    # Selenium ile sayfayı aç ve içeriği al
                    from selenium import webdriver
                    from selenium.webdriver.chrome.service import Service
                    from selenium.webdriver.chrome.options import Options
                    from selenium.webdriver.common.keys import Keys
                    from selenium.webdriver.common.action_chains import ActionChains
                    import time
                    
                    # Chrome options
                    chrome_options = Options()
                    chrome_options.add_argument('--headless')  # Görünmez mod
                    chrome_options.add_argument('--no-sandbox')
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    
                    # WebDriver başlat
                    driver = webdriver.Chrome(options=chrome_options)
                    
                    try:
                        # Sayfayı aç
                        driver.get(url)
                        time.sleep(3)  # Sayfa yüklensin
                        
                        # Sayfanın tüm text içeriğini al
                        page_text = driver.find_element("tag name", "body").text
                        
                        # Debug: İlk 2000 karakteri logla
                        print(f"📄 Sayfa içeriği (ilk 2000 karakter):")
                        print(page_text[:2000])
                        print(f"\n... (toplam {len(page_text)} karakter)\n")
                        
                        driver.quit()
                        
                        if not page_text or len(page_text) < 100:
                            await status_msg.edit_text("❌ Sayfa içeriği alınamadı")
                            return
                        
                        # Parse et
                        await status_msg.edit_text("📋 Kupon parse ediliyor...")
                        
                        lines = [l.strip() for l in page_text.strip().split('\n') if l.strip()]
                        matches = []
                        sistem_info = None
                        nesine_total_odds = None
                        
                        # Toplam Oran'ı bul
                        for idx, line in enumerate(lines):
                            if 'toplam oran' in line.lower():
                                if idx + 1 < len(lines):
                                    next_line = lines[idx + 1].strip()
                                    next_line_clean = next_line.replace('.', '').replace(',', '.')
                                    try:
                                        if next_line_clean.replace('.', '').isdigit():
                                            nesine_total_odds = float(next_line_clean)
                                            print(f"💰 Toplam Oran: {nesine_total_odds}")
                                            break
                                    except:
                                        pass
                        
                        # Sistem bilgisi bul
                        sistem_found = False
                        for idx, line in enumerate(lines):
                            if 'sistem' in line.lower() and not sistem_found:
                                for j in range(1, min(6, len(lines) - idx)):
                                    next_line = lines[idx + j].strip()
                                    if ',' in next_line and len(next_line) < 30:
                                        clean_line = next_line.replace(' ', '').replace(',', '')
                                        if clean_line.isdigit():
                                            numbers = [int(x.strip()) for x in next_line.split(',') if x.strip().isdigit()]
                                            if len(numbers) >= 2 and all(2 <= n <= 8 for n in numbers):
                                                sistem_info = f"Sistem: {next_line}"
                                                print(f"📊 Sistem: {sistem_info}")
                                                sistem_found = True
                                                break
                                if sistem_found:
                                    break
                        
                        # Maçları parse et
                        i = 0
                        while i < len(lines):
                            line = lines[i]
                            
                            if ' - ' in line and 10 < len(line) < 50:
                                skip_patterns = [
                                    'copyright', 'nesine', 'iddaa', 'milli piyango', 'anasayfa',
                                    'kupondaş', 'at yarış', 'üye ol', 'müşteri', 'sponsorluk'
                                ]
                                
                                if any(pat in line.lower() for pat in skip_patterns):
                                    i += 1
                                    continue
                                
                                if line[0].isdigit() and ('.' in line or ':' in line):
                                    i += 1
                                    continue
                                
                                teams = line
                                mbs = None
                                bet_type = None
                                selection = None
                                oran = None
                                skor = None
                                ilk_yari_skor = None
                                
                                for j in range(1, min(25, len(lines) - i)):
                                    next_line = lines[i + j]
                                    
                                    if ' - ' in next_line and 10 < len(next_line) < 50 and j > 3:
                                        break
                                    
                                    if not mbs and len(next_line) == 1 and next_line.isdigit() and next_line != '0':
                                        mbs = next_line
                                    
                                    # Nesine'deki TÜM bahis türleri (Futbol, Basketbol, Voleybol, Tenis vs.)
                                    bet_keywords = [
                                        # Genel
                                        'sonucu', 'sonuc',
                                        'handikap', 'handikapl',
                                        'çifte şans', 'cifte sans',
                                        'tek', 'çift', 'cift',
                                        'alt', 'üst', 'ust',
                                        'var', 'yok',
                                        'beraberlik', ' x ',
                                        'ev sahibi', 'deplasman',
                                        
                                        # Futbol - Kombinasyon Bahisleri
                                        'gol', 'gül',
                                        'karşılıklı', 'karsilkli', 'kg',
                                        'ms&', 'ms &', 'ms&kg', 'ms & kg',
                                        '& kg', '&kg',
                                        'ms&toplam gol', 'ms&toplam gül',
                                        'ms&karşılıklı', 'ms&karsilkli',
                                        'ms&iy sonucu', 'ms&i̇y sonucu',
                                        'ms&çifte şans', 'ms&cifte sans',
                                        'ms&tek/çift', 'ms&tek/cift',
                                        'ms&ilk gol', 'ms&i̇lk gol',
                                        
                                        # İlk Yarı Kombinasyonları
                                        'iy&', 'i̇y&',
                                        'iy&toplam gol', 'i̇y&toplam gol',
                                        'iy&karşılıklı', 'i̇y&karşılıklı',
                                        
                                        # Temel Futbol
                                        'toplam gol', 'toplam gül',
                                        '1.y', 'ilk yarı', 'ilk yari', 'iy', 'i̇y',
                                        'ikinci yarı', 'ikinci yari',
                                        'ilk yarı / maç sonucu', 'ilk yari / mac sonucu',
                                        'iy/ms', 'i̇y/ms',
                                        'toplam gol sayısı', 'toplam gol sayisi',
                                        
                                        # Gol Bazlı
                                        'ilk gol', 'ilk gül',
                                        'ilk golü', 'ilk gülü',
                                        'gol atar', 'gol var/yok',
                                        'hangi yarıda', 'hangi yarida',
                                        'ilk yarı gol', 'ikinci yarı gol',
                                        'ilk yarı 1,5 gol', 'ikinci yarı 1,5 gol',
                                        'ilk yarı karşılıklı', 'ikinci yarı karşılıklı',
                                        'ev sahibi gol', 'deplasman gol',
                                        
                                        # Skor Tahminleri
                                        'skor tahmini',
                                        'ilk yarı skor', 'ikinci yarı skor',
                                        
                                        # Korner ve Kartlar
                                        'korner',
                                        'toplam korner',
                                        'kart', 'sarı', 'sari', 'kırmızı', 'kirmizi',
                                        'toplam kart',
                                        
                                        # Basketbol
                                        'sayı', 'sayi',
                                        'toplam sayı', 'toplam sayi',
                                        'çeyrek', 'ceyrek',
                                        '1.çeyrek', '1.ceyrek',
                                        '2.çeyrek', '2.ceyrek',
                                        '3.çeyrek', '3.ceyrek',
                                        '4.çeyrek', '4.ceyrek',
                                        '1.yarı', '1.yari',
                                        '2.yarı', '2.yari',
                                        
                                        # Voleybol
                                        'set',
                                        'toplam set',
                                        '1.set', '2.set', '3.set', '4.set', '5.set',
                                        
                                        # Tenis
                                        'game',
                                        'toplam game',
                                        'toplam gem'
                                    ]
                                    if not bet_type and 5 < len(next_line) < 80:  # Uzunluk sınırını 80'e çıkardık (uzun bahis isimleri için)
                                        # "Toplam Oran" değilse ve keyword varsa
                                        if 'toplam oran' not in next_line.lower() and any(kw in next_line.lower() for kw in bet_keywords):
                                            bet_type = next_line
                                    
                                    sel_keywords = ['& var', '& yok', '& üst', '& alt', 'var &', 'yok &']
                                    if not selection and 3 < len(next_line) < 20:
                                        if any(kw in next_line.lower() for kw in sel_keywords):
                                            selection = next_line
                                    
                                    if not oran and '.' in next_line and len(next_line) <= 6:
                                        parts = next_line.replace(',', '.').split('.')
                                        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                                            oran = next_line
                                    
                                    if not skor and '-' in next_line and len(next_line) <= 5:
                                        parts = next_line.split('-')
                                        if len(parts) == 2:
                                            try:
                                                int(parts[0])
                                                int(parts[1])
                                                skor = next_line
                                            except:
                                                pass
                                    
                                    if not ilk_yari_skor and ('iy' in next_line.lower() or '(' in next_line):
                                        if '-' in next_line and len(next_line) <= 12:
                                            if '(' in next_line and ')' in next_line:
                                                inside = next_line[next_line.find('(')+1:next_line.find(')')]
                                                inside = inside.replace('İY:', '').replace('IY:', '').strip()
                                                if '-' in inside:
                                                    parts = inside.split('-')
                                                    if len(parts) == 2:
                                                        try:
                                                            int(parts[0].strip())
                                                            int(parts[1].strip())
                                                            ilk_yari_skor = inside
                                                        except:
                                                            pass
                                
                                if oran or bet_type or selection:
                                    matches.append({
                                        'teams': teams,
                                        'mbs': mbs,
                                        'tahmin': bet_type,
                                        'selection': selection,
                                        'oran': oran,
                                        'skor': skor,
                                        'ilk_yari_skor': ilk_yari_skor
                                    })
                            
                            i += 1
                        
                        if not matches:
                            await status_msg.edit_text("❌ Kuponda maç bulunamadı")
                            return
                        
                        # Veritabanına kaydet
                        from datetime import datetime
                        
                        # Toplam oran hesapla
                        if nesine_total_odds:
                            total_odds = nesine_total_odds
                        else:
                            total_odds = 1.0
                            for match in matches:
                                if match['oran']:
                                    try:
                                        total_odds *= float(match['oran'].replace(',', '.'))
                                    except:
                                        pass
                        
                        # Kuponu kaydet
                        coupon_id = self.db.save_nesine_coupon(
                            coupon_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            total_odds=round(total_odds, 2),
                            match_count=len(matches),
                            sistem_info=sistem_info
                        )
                        
                        # Maçları kaydet
                        for idx, match in enumerate(matches):
                            print(f"🔍 Maç {idx+1} kaydediliyor:")
                            print(f"   Teams: {match.get('teams')}")
                            print(f"   MBS: {match.get('mbs')}")
                            print(f"   Tahmin: {match.get('tahmin')}")
                            print(f"   Selection: {match.get('selection')}")
                            print(f"   Oran: {match.get('oran')}")
                            print(f"   Skor: {match.get('skor')}")
                            print(f"   İlk Yarı: {match.get('ilk_yari_skor')}")
                            
                            self.db.save_nesine_match(
                                coupon_id=coupon_id,
                                teams=match['teams'],
                                mbs=match['mbs'],
                                tahmin=match['tahmin'],
                                selection=match['selection'],
                                oran=match['oran'],
                                mac_saati=None,
                                skor=match['skor'],
                                ilk_yari_skor=match['ilk_yari_skor'],
                                match_order=idx + 1
                            )
                        
                        # Sonuç mesajı
                        result_text = f"✅ Nesine kuponu kaydedildi!\n\n"
                        result_text += f"📊 Toplam Maç: {len(matches)}\n"
                        result_text += f"💰 Toplam Oran: {total_odds:.2f}\n"
                        if sistem_info:
                            result_text += f"🎯 {sistem_info}\n"
                        
                        await status_msg.edit_text(result_text)
                        
                    except Exception as e:
                        driver.quit()
                        raise e
                        
                except Exception as e:
                    print(f"❌ Parse hatası: {e}")
                    import traceback
                    traceback.print_exc()
                    await status_msg.edit_text(f"❌ Kupon parse edilemedi: {str(e)}")
            else:
                print(f"ℹ️ Nesine linki değil, göz ardı edildi")
            
        except Exception as e:
            print(f"❌ Text handler hatası: {e}")
            import traceback
            traceback.print_exc()
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Screenshot analizi"""
        print("="*60)
        print("📸 PHOTO HANDLER ÇAĞRILDI!")
        print(f"Chat ID: {update.message.chat_id}")
        print(f"Message ID: {update.message.message_id}")
        print(f"Photo Count: {len(update.message.photo)}")
        print("="*60)
        
        await update.message.reply_text("📸 Screenshot alındı! Analiz ediliyor...")
        
        try:
            # En büyük fotoğrafı al
            photo = update.message.photo[-1]
            print(f"✅ Fotoğraf alındı: {photo.file_id}")
            
            # Dosyayı indir
            file = await context.bot.get_file(photo.file_id)
            file_path = f"temp_screenshot_{update.message.chat_id}.jpg"
            await file.download_to_drive(file_path)
            print(f"✅ Dosya indirildi: {file_path}")
            
            # OCR analizi
            print("🔍 OCR analizi başlıyor...")
            ocr_result = self.ocr.analyze_screenshot(file_path)
            print(f"✅ OCR tamamlandı: {ocr_result}")
            
            if not ocr_result or ocr_result['confidence'] < 0.5:
                print(f"❌ OCR güven skoru düşük: {ocr_result}")
                print(f"📄 HAM METIN:\n{ocr_result.get('raw_text', 'YOK') if ocr_result else 'OCR NULL'}")
                await update.message.reply_text(
                    "❌ Screenshot'tan oran okunamadı.\n\n"
                    "📝 <b>İpuçları:</b>\n"
                    "- Oranlar net ve büyük olsun\n"
                    "- MS1, MSX, MS2 görünsün\n"
                    "- Ekran parlaklığı yeterli olsun\n"
                    "- Çok fazla yazı karmaşa yaratabilir",
                    parse_mode='HTML'
                )
                return
            
            # Veritabanından SADECE ORANLARA GÖRE benzer maçları bul (KADEMELİ)
            print(f"🔍 Veritabanında aranıyor: {ocr_result['odd_1']}/{ocr_result['odd_x']}/{ocr_result['odd_2']}")
            history = self.db.search_by_odds_range(
                ocr_result['home_team'],
                ocr_result['away_team'],
                ocr_result['odd_1'],
                ocr_result['odd_x'],
                ocr_result['odd_2'],
                limit=50  # En fazla 50 maç al
            )
            print(f"✅ Bulunan maç sayısı: {len(history)}")
            
            # Analiz mesajı oluştur
            print("📝 Mesaj oluşturuluyor...")
            message, keyboard = self.ocr.get_match_recommendation(ocr_result, history)
            print(f"✅ Mesaj hazır, gönderiliyor...")
            
            # Inline keyboard oluştur (eğer varsa)
            reply_markup = None
            if keyboard:
                reply_markup = InlineKeyboardMarkup(keyboard['inline_keyboard'])
            
            await update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)
            print("✅ Mesaj gönderildi!")
            
            # Temp dosyayı sil
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️ Temp dosya silindi")
                
        except Exception as e:
            print(f"❌ Photo handler hatası: {e}")
            import traceback
            traceback.print_exc()
            await update.message.reply_text(
                f"❌ Bir hata oluştu: {str(e)}\n\n"
                "Lütfen tekrar deneyin."
            )
    
    async def callback_back(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Geri butonu"""
        query = update.callback_query
        await query.answer()
        
        # Bülteni tekrar göster
        matches = self.db.get_today_matches()
    
    async def handle_halftime_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """İlk yarı detayları butonu"""
        query = update.callback_query
        await query.answer()
        
        try:
            # Callback data'dan oranları al (format: "ht_1.47_3.76_4.09")
            data = query.data
            
            # Parse et
            parts = data.split('_')
            if len(parts) != 4 or parts[0] != 'ht':
                await query.edit_message_text("❌ Geçersiz veri formatı")
                return
            
            odd_1 = float(parts[1])
            odd_x = float(parts[2])
            odd_2 = float(parts[3])
            
            print(f"🔍 İlk yarı detayları isteniyor: {odd_1}/{odd_x}/{odd_2}")
            
            # Aynı oranlarla tekrar ara
            results = self.db.search_by_odds_range('', '', odd_1, odd_x, odd_2, limit=50)
            
            # Yeni format: dict with exact and similar
            if not results or results.get('total_count', 0) == 0:
                await query.edit_message_text("❌ Maç verisi bulunamadı")
                return
            
            # Tüm maçları birleştir (exact + similar)
            history = results.get('exact', []) + results.get('similar', [])
            
            # İLK YARI DETAYLARI mesajı oluştur
            display_count = min(10, len(history))
            message = f"🏟️ <b>İLK YARI DETAYLARI ({len(history)} maç bulundu, ilk {display_count} gösteriliyor):</b>\n\n"
            
            # İlk yarı istatistikleri - TÜM MAÇLARDAN
            ht_home_lead = 0  # İlk yarı ev sahibi önde
            ht_draw = 0       # İlk yarı beraberlik
            ht_away_lead = 0  # İlk yarı deplasman önde
            ht_draw_0_0 = 0   # 0-0 beraberlik
            ht_draw_scored = 0  # Gollü beraberlik (1-1, 2-2, vb)
            ht_btts_yes = 0   # İY karşılıklı gol VAR
            ht_btts_no = 0    # İY karşılıklı gol YOK
            ht_total_goals = 0  # Toplam gol sayısı
            ht_valid_count = 0  # Geçerli ilk yarı skoru olan maç sayısı
            
            # ÖNCE TÜM MAÇLARI İSTATİSTİĞE DAHIL ET
            for h in history:  # TÜM history (50 maç)
                half_score = h.get('half_score', '').strip()
                
                if half_score and '-' in half_score:
                    try:
                        parts = half_score.split('-')
                        if len(parts) == 2:
                            ht_home = int(parts[0].strip())
                            ht_away = int(parts[1].strip())
                            ht_valid_count += 1
                            
                            # Toplam gol
                            ht_total_goals += (ht_home + ht_away)
                            
                            # Karşılıklı gol
                            if ht_home > 0 and ht_away > 0:
                                ht_btts_yes += 1
                            else:
                                ht_btts_no += 1
                            
                            # Maç durumu
                            if ht_home > ht_away:
                                ht_home_lead += 1
                            elif ht_home == ht_away:
                                ht_draw += 1
                                # Beraberlik tipi
                                if ht_home == 0 and ht_away == 0:
                                    ht_draw_0_0 += 1
                                else:
                                    ht_draw_scored += 1
                            else:
                                ht_away_lead += 1
                    except:
                        pass
            
            # SONRA İLK 10 MAÇI GÖSTER
            for i, h in enumerate(history[:display_count], 1):
                score = h.get('score', '').strip()
                half_score = h.get('half_score', '').strip()
                h_odd1 = h.get('odd_1', 0)
                h_oddx = h.get('odd_x', 0)
                h_odd2 = h.get('odd_2', 0)
                
                # Maç bilgisi
                message += f"📅 <b>MS:</b> {score if score else '?'} | "
                message += f"<b>İY:</b> {half_score if half_score else '?'} | "
                message += f"{h_odd1:.2f}/{h_oddx:.2f}/{h_odd2:.2f}\n"
            
            # İlk yarı istatistik özeti
            ht_total = ht_home_lead + ht_draw + ht_away_lead
            if ht_total > 0:
                message += f"\n━━━━━━━━━━━━━━━━━━━━━\n"
                message += f"📊 <b>İLK YARI İSTATİSTİK ({ht_total} maç):</b>\n"
                message += f"🏠 Ev Sahibi Önde: <b>{ht_home_lead}</b>\n"
                message += f"🤝 Beraberlik: <b>{ht_draw}</b>\n"
                
                # Beraberlik detayı
                if ht_draw > 0:
                    message += f"   └ 0-0: <b>{ht_draw_0_0}</b> | Gollü: <b>{ht_draw_scored}</b>\n"
                
                message += f"✈️ Deplasman Önde: <b>{ht_away_lead}</b>\n"
                
                # Karşılıklı Gol
                if ht_btts_yes + ht_btts_no > 0:
                    message += f"\n⚽ <b>İY Karşılıklı Gol:</b>\n"
                    message += f"✅ Var: <b>{ht_btts_yes}</b>\n"
                    message += f"❌ Yok: <b>{ht_btts_no}</b>\n"
                
                # Ortalama gol
                if ht_valid_count > 0:
                    avg_goals = ht_total_goals / ht_valid_count
                    message += f"\n🎯 <b>Ortalama İY Gol:</b> <b>{avg_goals:.2f}</b>\n"
                    message += f"   Toplam: {ht_total_goals} gol / {ht_valid_count} maç\n"
            
            # Geri dönüş butonu - oranları tekrar gönder
            back_callback = f"back_{odd_1:.2f}_{odd_x:.2f}_{odd_2:.2f}"
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Ana Analiz", callback_data=back_callback)
            ]])
            
            await query.edit_message_text(message, parse_mode='HTML', reply_markup=keyboard)
            print("✅ İlk yarı detayları gönderildi")
            
        except Exception as e:
            print(f"❌ Callback hatası: {e}")
            import traceback
            traceback.print_exc()
            await query.edit_message_text(f"❌ Hata: {str(e)}")
    
    async def handle_back_to_main(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ana analize geri dön butonu"""
        query = update.callback_query
        await query.answer()
        
        try:
            # Callback data'dan oranları al (format: "back_1.47_3.76_4.09")
            data = query.data
            parts = data.split('_')
            
            if len(parts) != 4 or parts[0] != 'back':
                await query.edit_message_text("❌ Geçersiz veri formatı")
                return
            
            odd_1 = float(parts[1])
            odd_x = float(parts[2])
            odd_2 = float(parts[3])
            
            print(f"🔙 Ana analize dönülüyor: {odd_1}/{odd_x}/{odd_2}")
            
            # Aynı oranlarla tekrar ara
            history = self.db.search_by_odds_range('', '', odd_1, odd_x, odd_2, limit=50)
            
            # OCR result simüle et (sadece oranlar)
            ocr_result = {
                'home_team': 'None',
                'away_team': 'None',
                'odd_1': odd_1,
                'odd_x': odd_x,
                'odd_2': odd_2
            }
            
            # Ana analiz mesajını oluştur
            message, keyboard = self.ocr.get_match_recommendation(ocr_result, history)
            
            # Inline keyboard oluştur
            reply_markup = None
            if keyboard:
                reply_markup = InlineKeyboardMarkup(keyboard['inline_keyboard'])
            
            await query.edit_message_text(message, parse_mode='HTML', reply_markup=reply_markup)
            print("✅ Ana analize dönüldü")
            
        except Exception as e:
            print(f"❌ Geri dönüş hatası: {e}")
            import traceback
            traceback.print_exc()
            await query.edit_message_text(f"❌ Hata: {str(e)}")
    
    def start_bot(self):
        """Bot'u başlat (arka planda)"""
        if not self.is_configured():
            print("⚠️ Telegram bot yapılandırılmamış!")
            return False
        
        # Eğer bot zaten çalışıyorsa, önce durdur
        if self.is_running:
            print("⚠️ Bot zaten çalışıyor, yeniden başlatılıyor...")
            self.stop_bot()
            import time
            time.sleep(1)  # Kısa bir bekleme
        
        def run_bot():
            try:
                # Yeni event loop oluştur
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Bot uygulamasını oluştur
                self.app = Application.builder().token(self.bot_token).build()
                
                # Komutları ekle
                self.app.add_handler(CommandHandler("start", self.cmd_start))
                self.app.add_handler(CommandHandler("durum", self.cmd_status))
                self.app.add_handler(CommandHandler("yeniveri", self.cmd_yeniveri))
                
                # Photo handler ekle (screenshot analizi)
                self.app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
                
                # Text message handler ekle (Nesine kupon linki)
                self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
                
                # Callback handler'ları ekle
                self.app.add_handler(CallbackQueryHandler(self.callback_analyze, pattern="^analyze_"))
                self.app.add_handler(CallbackQueryHandler(self.callback_back, pattern="^back_to_bulletin$"))
                self.app.add_handler(CallbackQueryHandler(self.handle_halftime_callback, pattern="^ht_"))
                self.app.add_handler(CallbackQueryHandler(self.handle_back_to_main, pattern="^back_"))
                self.app.add_handler(CallbackQueryHandler(self.handle_yeniveri_callback, pattern="^yeniveri_"))
                
                self.is_running = True
                print("✅ Telegram bot başlatıldı!")
                
                self.app.run_polling(drop_pending_updates=True)  # Eski update'leri atla
                
            except Exception as e:
                import traceback
                error_msg = str(e)
                
                # Timezone hatası bilinen bir sorun, kullanıcıyı bilgilendir
                if "Only timezones from the pytz library" in error_msg:
                    print("⚠️  Telegram bot timezone uyumsuzluğu nedeniyle devre dışı.")
                    print("ℹ️  Mackolik parser ve diğer özellikler normal çalışmaya devam ediyor.")
                elif "proxies" in error_msg.lower():
                    print("⚠️  Telegram bot kütüphanesi güncelleme sorunu. Bot devre dışı.")
                else:
                    print(f"❌ Bot çalıştırılırken hata: {error_msg}")
                    traceback.print_exc()
                
                self.is_running = False
            finally:
                try:
                    loop.close()
                except:
                    pass
        
        # Arka planda çalıştır
        thread = threading.Thread(target=run_bot, daemon=True)
        thread.start()
        
        return True
    
    def stop_bot(self):
        """Bot'u durdur"""
        try:
            if self.app and self.is_running:
                print("🛑 Telegram bot durduruluyor...")
                
                # Önce flag'i değiştir
                self.is_running = False
                
                # Bot'u durdur (async değil, direkt durdur)
                if hasattr(self.app, 'stop'):
                    try:
                        self.app.stop()
                    except:
                        pass
                
                # App referansını temizle
                self.app = None
                print("✅ Telegram bot durduruldu!")
                
        except Exception as e:
            print(f"⚠️ Bot durdurulurken hata (göz ardı edildi): {str(e)}")
            self.is_running = False
            self.app = None

if __name__ == '__main__':
    print("🤖 BetSmart Telegram Bot Başlatılıyor...")
    bot = TelegramBotManager()
    
    if not bot.is_configured():
        print("❌ Bot yapılandırılmamış!")
        print("config.json dosyasına telegram ayarlarını ekleyin:")
        print("""
{
  "telegram": {
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  }
}
""")
    else:
        print("✅ Bot yapılandırması bulundu")
        bot.start_bot()
        
        # Bot başlaması için kısa bekleme
        import time
        time.sleep(2)
        
        if bot.is_running:
            print("\n" + "="*50)
            print("✅ BOT ÇALIŞIYOR!")
            print("="*50)
            print("\n📱 Telegram'dan şu komutları kullanabilirsiniz:")
            print("   /start - Bot'u başlat")
            print("   /durum - Sistem durumu")
            print("   /yeniveri - Güncel maçları çek (2 günlük)")
            print("\n⏸️  Durdurmak için CTRL+C yapın")
            print("="*50 + "\n")
        
        # Sonsuz döngü - bot çalışsın diye
        try:
            while bot.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Bot durduruluyor...")
            bot.stop_bot()
            print("👋 Görüşürüz!")
