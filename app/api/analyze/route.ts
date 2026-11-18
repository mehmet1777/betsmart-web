import { NextRequest, NextResponse } from 'next/server';

// Python backend URL (local development)
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:5000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { odd_1, odd_x, odd_2, home_team, away_team } = body;

    console.log('📊 API: Analiz isteği alındı:', { odd_1, odd_x, odd_2, home_team, away_team });

    // Validasyon
    if (!odd_1 || !odd_x || !odd_2 || odd_1 <= 0 || odd_x <= 0 || odd_2 <= 0) {
      console.warn('⚠️ Geçersiz oranlar:', { odd_1, odd_x, odd_2 });
      return NextResponse.json(
        { 
          success: false, 
          error: 'Oranlar eksik veya geçersiz',
          details: { odd_1, odd_x, odd_2 }
        },
        { status: 400 }
      );
    }

    // Python backend'e istek gönder (SQLite veritabanı sorgusu için)
    try {
      const pythonResponse = await fetch(`${PYTHON_API_URL}/api/analyze-odds`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          odd_1: parseFloat(odd_1),
          odd_x: parseFloat(odd_x),
          odd_2: parseFloat(odd_2),
          home_team: home_team || '',
          away_team: away_team || ''
        }),
        signal: AbortSignal.timeout(10000) // 10 saniye timeout
      });

      if (pythonResponse.ok) {
        const pythonData = await pythonResponse.json();
        console.log('✅ Python backend yanıtı:', pythonData);
        return NextResponse.json({
          success: true,
          ...pythonData
        });
      } else {
        console.warn('⚠️ Python backend hatası:', pythonResponse.status);
      }
    } catch (pythonError) {
      console.warn('⚠️ Python backend bağlantı hatası:', pythonError);
    }

    // Fallback: Python backend yoksa veya hata verdiyse
    console.log('ℹ️ Fallback: Mock data döndürülüyor');
    return NextResponse.json({
      success: true,
      total_count: 0,
      exact: [],
      similar: [],
      statistics: {
        home_wins: 0,
        draws: 0,
        away_wins: 0,
        gg_yes: 0,
        gg_no: 0,
        total_valid: 0
      },
      message: '⚠️ Benzer oranlı maç bulunamadı veya backend bağlantısı yok'
    });
  } catch (error) {
    console.error('❌ API hatası:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: 'Sunucu hatası',
        details: error instanceof Error ? error.message : 'Bilinmeyen hata'
      },
      { status: 500 }
    );
  }
}
