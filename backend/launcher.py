import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk
import threading

class ModernLauncher:
    def __init__(self):
        # Eski Python process'lerini kapat (BetSmart ile ilgili olanlar)
        self.kill_existing_processes()
        
        self.root = tk.Tk()
        self.root.title("BetSmart Launcher")
        
        # Pencere boyutu ve konumu
        window_width = 600
        window_height = 450
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        
        # Çerçevesiz pencere
        self.root.overrideredirect(True)
        
        # Ana frame - Koyu arkaplan
        self.main_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.main_frame.pack(fill="both", expand=True)
        
        # Üst bar (başlık + butonlar)
        self.create_title_bar()
        
        # İçerik
        self.create_content()
        
        # Sürükle-bırak
        self.x = 0
        self.y = 0
        
    def create_title_bar(self):
        """Üst başlık barı"""
        title_bar = tk.Frame(self.main_frame, bg="#16161e", height=40)
        title_bar.pack(fill="x", side="top")
        title_bar.pack_propagate(False)
        
        # Başlık
        title_label = tk.Label(
            title_bar, 
            text="⚡ BetSmart Launcher",
            bg="#16161e",
            fg="#00D9FF",
            font=("Segoe UI", 11, "bold")
        )
        title_label.pack(side="left", padx=15)
        
        # Close butonu
        close_btn = tk.Button(
            title_bar,
            text="✕",
            bg="#16161e",
            fg="white",
            font=("Arial", 12, "bold"),
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            activebackground="#ff4757",
            activeforeground="white",
            command=self.root.destroy
        )
        close_btn.pack(side="right")
        
        # Minimize butonu
        min_btn = tk.Button(
            title_bar,
            text="─",
            bg="#16161e",
            fg="white",
            font=("Arial", 12, "bold"),
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            activebackground="#2d2d3d",
            activeforeground="white",
            command=self.root.iconify
        )
        min_btn.pack(side="right")
        
        # Sürükle-bırak için bind
        title_bar.bind("<Button-1>", self.start_drag)
        title_bar.bind("<B1-Motion>", self.on_drag)
        title_label.bind("<Button-1>", self.start_drag)
        title_label.bind("<B1-Motion>", self.on_drag)
    
    def create_content(self):
        """Ana içerik"""
        content_frame = tk.Frame(self.main_frame, bg="#1e1e2e")
        content_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Logo
        logo_label = tk.Label(
            content_frame,
            text="🎯",
            bg="#1e1e2e",
            fg="white",
            font=("Segoe UI Emoji", 70)
        )
        logo_label.pack(pady=(20, 10))
        
        # Başlık
        title = tk.Label(
            content_frame,
            text="BetSmart",
            bg="#1e1e2e",
            fg="white",
            font=("Arial", 42, "bold")
        )
        title.pack(pady=(5, 5))
        
        # Alt başlık
        subtitle = tk.Label(
            content_frame,
            text="Akıllı Bahis Analiz Sistemi",
            bg="#1e1e2e",
            fg="#b0b0b0",
            font=("Arial", 13)
        )
        subtitle.pack(pady=(0, 30))
        
        # BAŞLAT butonu
        self.start_btn = tk.Button(
            content_frame,
            text="▶  BAŞLAT",
            bg="#00D9FF",
            fg="black",
            font=("Arial", 14, "bold"),
            bd=0,
            padx=50,
            pady=15,
            cursor="hand2",
            activebackground="#00F0FF",
            activeforeground="black",
            command=self.start_application
        )
        self.start_btn.pack(pady=(0, 15))
        
        # Hover efekti
        self.start_btn.bind("<Enter>", lambda e: self.start_btn.config(bg="#00F0FF"))
        self.start_btn.bind("<Leave>", lambda e: self.start_btn.config(bg="#00D9FF"))
        
        # Durum label
        self.status_label = tk.Label(
            content_frame,
            text="",
            bg="#1e1e2e",
            fg="white",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=(0, 20))
        
        # Progress bar (başlangıçta gizli)
        self.progress = ttk.Progressbar(
            content_frame,
            mode='indeterminate',
            length=300
        )
        
        # Version
        version = tk.Label(
            content_frame,
            text="Version 2.0",
            bg="#1e1e2e",
            fg="#707070",
            font=("Arial", 9)
        )
        version.pack(side="bottom", pady=(20, 0))
    
    def kill_existing_processes(self):
        """Eski BetSmart process'lerini kapat"""
        try:
            import psutil
            current_pid = os.getpid()
            app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # Python process'i mi?
                    if proc.info['name'] and 'python' in proc.info['name'].lower():
                        # Bu launcher değil mi?
                        if proc.info['pid'] != current_pid:
                            # Komut satırında app.py var mı?
                            cmdline = proc.info.get('cmdline', [])
                            if cmdline and any('app.py' in str(arg) for arg in cmdline):
                                print(f"🔴 Eski process sonlandırılıyor: PID {proc.info['pid']}")
                                proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except ImportError:
            # psutil yoksa, Windows komutunu kullan
            if sys.platform == 'win32':
                try:
                    import subprocess
                    # Sadece bu dizindeki app.py çalıştıran process'leri bul ve öldür
                    result = subprocess.run(
                        ['powershell', '-Command', 
                         f"Get-Process python -ErrorAction SilentlyContinue | Where-Object {{$_.CommandLine -like '*app.py*'}} | Stop-Process -Force"],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        print("🔴 Eski process'ler temizlendi")
                except Exception as e:
                    print(f"⚠️ Process temizleme hatası: {e}")
    
    def start_drag(self, event):
        """Sürüklemeye başla"""
        self.x = event.x
        self.y = event.y
    
    def on_drag(self, event):
        """Pencereyi sürükle"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def start_application(self):
        """Ana uygulamayı başlat"""
        try:
            self.start_btn.config(state="disabled")
            self.start_btn.pack_forget()  # Butonu gizle
            self.progress.pack(pady=(0, 15))  # Progress bar göster
            self.progress.start(10)
            
            # Başlat
            def launch():
                import time
                
                # 1. API başlat
                self.root.after(0, lambda: self.status_label.config(text="⚙️ Python API başlatılıyor...", fg="#00D9FF"))
                if sys.platform == 'win32':
                    api_bat = os.path.join(os.path.dirname(__file__), "start_api.bat")
                    if os.path.exists(api_bat):
                        subprocess.Popen([api_bat], 
                                       creationflags=subprocess.CREATE_NO_WINDOW,
                                       cwd=os.path.dirname(__file__))
                time.sleep(1)
                self.root.after(0, lambda: self.status_label.config(text="✅ Python API başlatıldı", fg="#00E676"))
                time.sleep(0.5)
                
                # 2. Web başlat
                self.root.after(0, lambda: self.status_label.config(text="🌐 Web arayüzü başlatılıyor...", fg="#00D9FF"))
                if sys.platform == 'win32':
                    web_bat = os.path.join(os.path.dirname(__file__), "start_web.bat")
                    if os.path.exists(web_bat):
                        subprocess.Popen([web_bat],
                                       creationflags=subprocess.CREATE_NO_WINDOW,
                                       cwd=os.path.dirname(__file__))
                time.sleep(1)
                self.root.after(0, lambda: self.status_label.config(text="✅ Web arayüzü başlatıldı", fg="#00E676"))
                time.sleep(0.5)
                
                # 3. Birleşik Takip Sistemi başlat (Oran + Maç Detay)
                self.root.after(0, lambda: self.status_label.config(text="📊 Takip sistemleri başlatılıyor...", fg="#00D9FF"))
                
                # Sabit path kullan (EXE temp klasör sorununu çöz)
                backend_path = r"C:\Users\worda\Desktop\BetSmart\backend"
                unified_script = os.path.join(backend_path, "unified_tracker.py")
                
                if os.path.exists(unified_script):
                    # Tek terminalde tüm tracker'ları çalıştır
                    subprocess.Popen(['python', unified_script],
                                   cwd=backend_path,
                                   creationflags=subprocess.CREATE_NEW_CONSOLE)
                    print("✅ Birleşik takip sistemi başlatıldı")
                else:
                    print(f"⚠️ unified_tracker.py bulunamadı: {unified_script}")
                
                time.sleep(1)
                self.root.after(0, lambda: self.status_label.config(text="✅ Takip sistemleri başlatıldı", fg="#00E676"))
                time.sleep(0.5)
                
                # 4. GUI açılıyor (Telegram bot GUI içinde otomatik başlayacak)
                self.root.after(0, lambda: self.status_label.config(text="🎯 Masaüstü uygulaması açılıyor...", fg="#00D9FF"))
                time.sleep(0.5)
                
                # 5. Masaüstü GUI'yi başlat
                # EXE nerede olursa olsun, sabit path kullan
                backend_path = r"C:\Users\worda\Desktop\BetSmart\backend"
                app_script = os.path.join(backend_path, "app.py")
                
                print(f"🔍 app.py aranıyor: {app_script}")
                
                if os.path.exists(app_script):
                    subprocess.Popen(['python', app_script],
                                   cwd=backend_path)
                    print("✅ GUI başlatıldı")
                else:
                    print(f"❌ app.py bulunamadı: {app_script}")
                    self.root.after(0, lambda: self.status_label.config(text="⚠️ GUI bulunamadı, diğer servisler çalışıyor", fg="#FFA726"))
                
                time.sleep(1)
                self.root.after(0, lambda: self.status_label.config(text="✅ BetSmart hazır! (Telegram bot GUI'de aktif)", fg="#00E676"))
                
                # Launcher'ı kapat
                time.sleep(1)
                self.root.after(0, self.root.destroy)
            
            thread = threading.Thread(target=launch, daemon=True)
            thread.start()
            
        except Exception as e:
            self.status_label.config(text=f"❌ Hata: {str(e)}", fg="#ff4757")
            self.progress.stop()
            self.progress.pack_forget()
            self.start_btn.pack()
            self.start_btn.config(state="normal")
    
    def run(self):
        """Pencereyi başlat"""
        # Fade-in efekti
        self.root.attributes('-alpha', 0.0)
        self.root.update()
        
        def fade_in(alpha=0.0):
            if alpha < 1.0:
                alpha += 0.05
                self.root.attributes('-alpha', alpha)
                self.root.after(20, lambda: fade_in(alpha))
        
        self.root.after(50, fade_in)
        
        # PyInstaller temp cleanup uyarısını gizle
        if getattr(sys, 'frozen', False):
            import warnings
            warnings.filterwarnings("ignore")
        
        self.root.mainloop()

if __name__ == '__main__':
    app = ModernLauncher()
    app.run()
