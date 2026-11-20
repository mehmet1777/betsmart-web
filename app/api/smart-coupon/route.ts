import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

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

    const supabase = createClient(supabaseUrl, supabaseKey);
    
    const recommendations = [];
    let analyzedCount = 0;

    // Her maçı analiz et
    for (const match of matches) {
      try {
        const odd1 = parseFloat(match.odd_1 || 0);
        const oddX = parseFloat(match.odd_x || 0);
        const odd2 = parseFloat(match.odd_2 || 0);

        if (odd1 <= 0 || oddX <= 0 || odd2 <= 0) continue;

        analyzedCount++;

        // Supabase'den benzer oranlı tarihi maçları çek (±0.01 tolerans)
        const { data: historicalMatches, error } = await supabase
          .from('matches')
          .select('*')
          .gte('odd_1', odd1 - 0.01)
          .lte('odd_1', odd1 + 0.01)
          .gte('odd_x', oddX - 0.01)
          .lte('odd_x', oddX + 0.01)
          .gte('odd_2', odd2 - 0.01)
          .lte('odd_2', odd2 + 0.01)
          .not('score', 'is', null)
          .limit(100);

        if (error || !historicalMatches || historicalMatches.length === 0) {
          continue;
        }

        // İstatistikleri hesapla
        const stats = {
          homeWins: 0,
          draws: 0,
          awayWins: 0,
          ggYes: 0,
          ggNo: 0,
          totalValid: 0
        };

        for (const hMatch of historicalMatches) {
          const score = hMatch.score?.trim();
          if (!score || !score.includes('-')) continue;

          const parts = score.split('-');
          if (parts.length !== 2) continue;

          const homeScore = parseInt(parts[0].trim());
          const awayScore = parseInt(parts[1].trim());

          if (isNaN(homeScore) || isNaN(awayScore)) continue;

          stats.totalValid++;

          // Maç sonucu
          if (homeScore > awayScore) stats.homeWins++;
          else if (homeScore === awayScore) stats.draws++;
          else stats.awayWins++;

          // Karşılıklı gol
          if (homeScore > 0 && awayScore > 0) stats.ggYes++;
          else stats.ggNo++;
        }

        if (stats.totalValid === 0) continue;

        // En iyi sonucu bul
        const results = {
          'MS1': { count: stats.homeWins, odds: odd1 },
          'MSX': { count: stats.draws, odds: oddX },
          'MS2': { count: stats.awayWins, odds: odd2 }
        };

        const bestResult = Object.entries(results).reduce((best, [type, data]) => 
          data.count > best[1].count ? [type, data] : best
        );

        const [resultType, resultData] = bestResult as [string, { count: number; odds: number }];
        const winRate = (resultData.count / stats.totalValid) * 100;

        // Filtreleme kriterleri:
        // 1. Minimum %75 kazanma oranı
        // 2. Minimum 3 benzer maç
        // 3. Minimum 1.30 oran
        const MIN_WIN_RATE = 75;
        const MIN_MATCHES = 3;
        const MIN_ODDS = 1.30;

        if (
          winRate >= MIN_WIN_RATE && 
          stats.totalValid >= MIN_MATCHES &&
          resultData.odds >= MIN_ODDS
        ) {
          recommendations.push({
            match,
            exact_matches: historicalMatches.length,
            total_analyzed: stats.totalValid,
            win_rate: Math.round(winRate * 10) / 10,
            recommendation: resultType,
            recommended_odds: resultData.odds,
            statistics: {
              home_wins: stats.homeWins,
              draws: stats.draws,
              away_wins: stats.awayWins,
              gg_yes: stats.ggYes,
              gg_no: stats.ggNo
            }
          });

          console.log(`✅ Öneri: ${match.home_team} vs ${match.away_team} - ${resultType} (${winRate.toFixed(1)}% | ${resultData.odds} | ${stats.totalValid} maç)`);
        } else {
          console.log(`⏭️ Reddedildi: ${match.home_team} vs ${match.away_team} - Kriter: Win=${winRate.toFixed(1)}%, Maç=${stats.totalValid}, Oran=${resultData.odds}`);
        }
      } catch (matchError) {
        console.error('⚠️ Maç analiz hatası:', matchError);
        continue;
      }
    }

    // Kazanma oranına göre sırala
    recommendations.sort((a, b) => b.win_rate - a.win_rate);

    console.log(`🎯 Analiz tamamlandı: ${analyzedCount} maç, ${recommendations.length} öneri`);

    return NextResponse.json({
      success: true,
      analyzed_count: analyzedCount,
      recommended_count: recommendations.length,
      recommendations
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
