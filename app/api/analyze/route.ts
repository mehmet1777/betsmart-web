import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { odd_1, odd_x, odd_2, home_team, away_team } = body;

    console.log('📊 Analiz isteği:', { odd_1, odd_x, odd_2, home_team, away_team });

    // Validasyon
    const odd1 = parseFloat(odd_1);
    const oddX = parseFloat(odd_x);
    const odd2 = parseFloat(odd_2);

    if (!odd1 || !oddX || !odd2 || odd1 <= 0 || oddX <= 0 || odd2 <= 0) {
      return NextResponse.json(
        { success: false, error: 'Geçersiz oran değerleri' },
        { status: 400 }
      );
    }

    const supabase = createClient(supabaseUrl, supabaseKey);

    // Exact match (±0.01 tolerans)
    const { data: exactMatches, error: exactError } = await supabase
      .from('matches')
      .select('*')
      .filter('odd_1', 'gte', odd1 - 0.01)
      .filter('odd_1', 'lte', odd1 + 0.01)
      .filter('odd_x', 'gte', oddX - 0.01)
      .filter('odd_x', 'lte', oddX + 0.01)
      .filter('odd_2', 'gte', odd2 - 0.01)
      .filter('odd_2', 'lte', odd2 + 0.01)
      .not('score', 'is', null)
      .limit(100);

    console.log('🔍 Exact query:', exactError ? `Error: ${exactError.message}` : `Found ${exactMatches?.length || 0} matches`);

    // Similar match (±0.03 tolerans)
    const { data: similarMatches, error: similarError } = await supabase
      .from('matches')
      .select('*')
      .filter('odd_1', 'gte', odd1 - 0.03)
      .filter('odd_1', 'lte', odd1 + 0.03)
      .filter('odd_x', 'gte', oddX - 0.03)
      .filter('odd_x', 'lte', oddX + 0.03)
      .filter('odd_2', 'gte', odd2 - 0.03)
      .filter('odd_2', 'lte', odd2 + 0.03)
      .not('score', 'is', null)
      .limit(100);

    console.log('🔍 Similar query:', similarError ? `Error: ${similarError.message}` : `Found ${similarMatches?.length || 0} matches`);

    const exact = exactMatches || [];
    const similar = (similarMatches || []).filter(
      m => !exact.some(e => e.id === m.id)
    );

    // İstatistikleri hesapla
    const allMatches = [...exact, ...similar];
    const stats = {
      home_wins: 0,
      draws: 0,
      away_wins: 0,
      gg_yes: 0,
      gg_no: 0,
      total_valid: 0
    };

    for (const match of allMatches) {
      const score = match.score?.trim();
      if (!score || !score.includes('-')) continue;

      const parts = score.split('-');
      if (parts.length !== 2) continue;

      const homeScore = parseInt(parts[0].trim());
      const awayScore = parseInt(parts[1].trim());

      if (isNaN(homeScore) || isNaN(awayScore)) continue;

      stats.total_valid++;

      if (homeScore > awayScore) stats.home_wins++;
      else if (homeScore === awayScore) stats.draws++;
      else stats.away_wins++;

      if (homeScore > 0 && awayScore > 0) stats.gg_yes++;
      else stats.gg_no++;
    }

    // Öneri oluştur
    let recommendation = null;
    if (stats.total_valid > 0) {
      const results = {
        'MS1': { count: stats.home_wins, odds: odd1 },
        'MSX': { count: stats.draws, odds: oddX },
        'MS2': { count: stats.away_wins, odds: odd2 }
      };

      const bestResult = Object.entries(results).reduce((best, [type, data]) => 
        data.count > best[1].count ? [type, data] : best
      );

      const [resultType, resultData] = bestResult as [string, { count: number; odds: number }];
      const percentage = (resultData.count / stats.total_valid) * 100;

      const confidence = percentage >= 60 ? 'Çok Yüksek' :
                        percentage >= 50 ? 'Yüksek' :
                        percentage >= 40 ? 'Orta' : 'Düşük';

      const resultNames: Record<string, string> = { 
        'MS1': 'Ev sahibi', 
        'MSX': 'Beraberlik', 
        'MS2': 'Deplasman' 
      };

      recommendation = {
        type: resultType,
        odds: resultData.odds,
        confidence,
        reason: `Benzer oranlı ${stats.total_valid} maçta ${resultNames[resultType]?.toLowerCase() || resultType} ${resultData.count} kez gerçekleşti (%${percentage.toFixed(0)})`,
        percentage: Math.round(percentage * 10) / 10
      };
    }

    console.log(`✅ Analiz tamamlandı: ${exact.length} exact, ${similar.length} similar`);

    return NextResponse.json({
      success: true,
      total_count: allMatches.length,
      exact,
      similar,
      statistics: stats,
      recommendation
    });

  } catch (error) {
    console.error('❌ Analiz hatası:', error);
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
