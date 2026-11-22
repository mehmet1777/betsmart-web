#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# app.py'deki 1043-1310 arası eski kodu sil

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1043. satır: "        @pyqtSlot(str)" (yanlış, eski kodun başı)
# Bu satırdan MainWindow class'ına kadar olan kısmı sil

# MainWindow class'ını bul
mainwindow_line = -1
for i in range(1043, len(lines)):
    if 'class MainWindow' in lines[i]:
        mainwindow_line = i
        print(f'MainWindow class bulundu: satır {i}')
        break

if mainwindow_line > 0:
    # 1043'ten mainwindow_line'a kadar sil
    new_lines = lines[:1043] + lines[mainwindow_line:]
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f'✅ {mainwindow_line - 1043} satır eski kod silindi')
    print(f'Yeni dosya: {len(new_lines)} satır')
else:
    print('❌ MainWindow class bulunamadı!')
