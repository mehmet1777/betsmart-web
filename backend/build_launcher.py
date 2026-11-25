"""
BetSmart Launcher'ı EXE'ye dönüştür
"""
import PyInstaller.__main__
import os

# Icon dosyası (yoksa atla)
icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
icon_option = ['--icon', icon_path] if os.path.exists(icon_path) else []

PyInstaller.__main__.run([
    'app.py',
    '--name=BetSmart',
    '--onefile',  # Tekrar onefile - daha hızlı
    '--windowed',
    '--clean',
    '--add-data', 'templates;templates',
])

print("\n✅ BetSmart.exe oluşturuldu!")
print("📂 Konum: dist/BetSmart.exe")
print("\n📌 Bu dosyayı masaüstüne kopyalayabilirsin!")
