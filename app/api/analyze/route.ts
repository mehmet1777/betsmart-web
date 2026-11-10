import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { selections } = body;

    // Mock analiz sonucu
    const mockAnalysis = {
      totalMatches: Math.floor(Math.random() * 2000) + 500,
      homeWins: Math.floor(Math.random() * 600) + 200,
      draws: Math.floor(Math.random() * 400) + 100,
      awayWins: Math.floor(Math.random() * 500) + 150,
      winProbability: (Math.random() * 40 + 45).toFixed(1),
      similarBets: [
        {
          match: 'Galatasaray vs Fenerbahçe',
          result: '1',
          date: '2026-03-15',
          odds: '1.85'
        },
        {
          match: 'Beşiktaş vs Trabzonspor',
          result: '1',
          date: '2026-02-28',
          odds: '1.92'
        },
        {
          match: 'Real Madrid vs Barcelona',
          result: 'X',
          date: '2026-04-12',
          odds: '3.20'
        }
      ]
    };

    return NextResponse.json({
      success: true,
      analysis: mockAnalysis,
      message: 'Analiz tamamlandı'
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Analiz hatası' },
      { status: 500 }
    );
  }
}
