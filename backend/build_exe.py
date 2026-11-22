from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = [
        'app.py',                    # Ana Python dosyası
        '--onefile',                 # Tek bir exe dosyası oluştur
        '--add-data=templates;templates',  # Template klasörünü dahil et
        '--add-data=uploads;uploads',      # Uploads klasörünü dahil et
        '--hidden-import=pandas',          # Gerekli gizli importları ekle
        '--hidden-import=openpyxl',
        '--hidden-import=PyQt5',
        '--hidden-import=PyQtWebEngine',
        '--name=ExcelViewer',        # Exe dosyasının adı
        '--noconsole',               # Konsol penceresi gösterme
        '--icon=NONE'                # Varsayılan icon kullan
    ]
    
    run(opts)
