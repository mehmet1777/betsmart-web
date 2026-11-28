import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export const revalidate = 600; // 10 dakikada bir cache yenile

export async function GET() {
  try {
    // Backend'den oluşturulan JSON dosyasını oku
    const filePath = path.join(process.cwd(), 'backend', 'score_predictions.json');
    
    // Dosya var mı kontrol et
    if (!fs.existsSync(filePath)) {
      return NextResponse.json({
        total_matches: 0,
        matches_with_details: 0,
        predictions: [],
        timestamp: new Date().toISOString(),
        error: 'Henüz tahmin verisi oluşturulmadı'
      });
    }
    
    // JSON dosyasını oku
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const data = JSON.parse(fileContent);
    
    return NextResponse.json(data);
    
  } catch (error) {
    console.error('Score predictions API error:', error);
    return NextResponse.json(
      { 
        error: 'Tahminler yüklenirken hata oluştu',
        total_matches: 0,
        matches_with_details: 0,
        predictions: []
      },
      { status: 500 }
    );
  }
}
