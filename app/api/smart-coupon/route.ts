import { NextRequest, NextResponse } from 'next/server';

const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:5000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { matches } = body;

    console.log('🤖 Akıllı kupon isteği alındı:', matches?.length, 'maç');

    if (!matches || matches.length === 0) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Maç listesi boş'
        },
        { status: 400 }
      );
    }

    // Python backend'e istek gönder
    try {
      const pythonResponse = await fetch(`${PYTHON_API_URL}/api/smart-coupon`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ matches }),
        signal: AbortSignal.timeout(30000) // 30 saniye timeout (çok maç varsa)
      });

      if (pythonResponse.ok) {
        const pythonData = await pythonResponse.json();
        console.log('✅ Akıllı kupon sonucu:', pythonData.recommended_count, 'öneri');
        return NextResponse.json({
          success: true,
          ...pythonData
        });
      } else {
        const errorData = await pythonResponse.json().catch(() => ({}));
        console.warn('⚠️ Python backend hatası:', pythonResponse.status, errorData);
        return NextResponse.json(
          { 
            success: false, 
            error: errorData.error || 'Backend hatası'
          },
          { status: pythonResponse.status }
        );
      }
    } catch (pythonError) {
      console.error('❌ Python backend bağlantı hatası:', pythonError);
      return NextResponse.json(
        { 
          success: false, 
          error: 'Analiz servisi bağlantı hatası'
        },
        { status: 503 }
      );
    }
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
