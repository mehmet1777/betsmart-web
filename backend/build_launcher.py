"""
BetSmart Launcher'ı EXE'ye dönüştür
"""
import PyInstaller.__main__
import os

# Icon dosyası (yoksa atla)
icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
icon_option = ['--icon', icon_path] if os.path.exists(icon_path) else []

PyInstaller.__main__.run([
    'launcher.py',
    '--name=BetSmart',
    '--onefile',
    '--windowed',  # CMD penceresi yok
    '--clean',
    '--noupx',  # UPX kullanma (temp sorunu için)
    '--log-level=ERROR',  # Sadece hataları göster
    *icon_option,
    '--add-data', 'start_api.bat;.',
    '--add-data', 'start_web.bat;.',
    '--add-data', 'start_odds_tracker.bat;.',
])

print("\n✅ BetSmart.exe oluşturuldu!")
print("📂 Konum: dist/BetSmart.exe")
print("\n📌 Bu dosyayı masaüstüne kopyalayabilirsin!")
