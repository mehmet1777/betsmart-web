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

        // İstatistikleri hesapla - GENİŞLETİLMİŞ ANALİZ
        const stats = {
          // Maç Sonucu
          homeWins: 0,
          draws: 0,
          awayWins: 0,
          
          // Karşılıklı Gol
          ggYes: 0,
          ggNo: 0,
          
          // Alt/Üst
          over_05: 0,
          over_15: 0,
          over_25: 0,
          over_35: 0,
          over_45: 0,
          
          // İlk Yarı Alt/Üst
          ht_over_05: 0,
          ht_over_15: 0,
          ht_over_25: 0,
          
          // İlk Yarı KG
          ht_gg_yes: 0,
          ht_gg_no: 0,
          
          // İlk Yarı Sonuç
          ht_home_wins: 0,
          ht_draws: 0,
          ht_away_wins: 0,
          
          // Tek/Çift
          odd_goals: 0,
          even_goals: 0,
          
          // Toplam
          totalValid: 0,
          totalWithHalfTime: 0
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
          const totalGoals = homeScore + awayScore;

          // Maç sonucu
          if (homeScore > awayScore) stats.homeWins++;
          else if (homeScore === awayScore) stats.draws++;
          else stats.awayWins++;

          // Karşılıklı gol
          if (homeScore > 0 && awayScore > 0) stats.ggYes++;
          else stats.ggNo++;
          
          // Alt/Üst
          if (totalGoals > 0.5) stats.over_05++;
          if (totalGoals > 1.5) stats.over_15++;
          if (totalGoals > 2.5) stats.over_25++;
          if (totalGoals > 3.5) stats.over_35++;
          if (totalGoals > 4.5) stats.over_45++;
          
          // Tek/Çift
          if (totalGoals % 2 === 1) stats.odd_goals++;
          else stats.even_goals++;
          
          // İlk yarı analizi
          const halfScore = hMatch.half_score?.trim();
          if (halfScore && halfScore.includes('-')) {
            const htParts = halfScore.split('-');
            if (htParts.length === 2) {
              const htHome = parseInt(htParts[0].trim());
              const htAway = parseInt(htParts[1].trim());
              
              if (!isNaN(htHome) && !isNaN(htAway)) {
                stats.totalWithHalfTime++;
                const htTotal = htHome + htAway;
                
                // İlk yarı sonuç
                if (htHome > htAway) stats.ht_home_wins++;
                else if (htHome === htAway) stats.ht_draws++;
                else stats.ht_away_wins++;
                
                // İlk yarı alt/üst
                if (htTotal > 0.5) stats.ht_over_05++;
                if (htTotal > 1.5) stats.ht_over_15++;
                if (htTotal > 2.5) stats.ht_over_25++;
                
                // İlk yarı KG
                if (htHome > 0 && htAway > 0) stats.ht_gg_yes++;
                else stats.ht_gg_no++;
              }
            }
          }
        }

        if (stats.totalValid === 0) continue;

        // ANA ÖNERİ: Sadece Maç Sonucu (MS1, MSX, MS2)
        const msResults = {
          'MS1': { count: stats.homeWins, odds: odd1 },
          'MSX': { count: stats.draws, odds: oddX },
          'MS2': { count: stats.awayWins, odds: odd2 }
        };

        const bestMS = Object.entries(msResults).reduce((best, [type, data]) => 
          data.count > best[1].count ? [type, data] : best
        );

        const [msType, msData] = bestMS as [string, { count: number; odds: number }];
        const msWinRate = (msData.count / stats.totalValid) * 100;

        // Filtreleme kriterleri
        const MIN_WIN_RATE = 75;
        const MIN_MATCHES = 3;
        const MIN_ODDS = 1.30;

        if (
          msWinRate >= MIN_WIN_RATE && 
          stats.totalValid >= MIN_MATCHES &&
          msData.odds >= MIN_ODDS
        ) {
          // EK BİLGİLER: Diğer seçeneklerin istatistikleri
          const additionalInsights = [];

          // KG Var
          const ggYesRate = (stats.ggYes / stats.totalValid) * 100;
          if (ggYesRate >= 60) {
            additionalInsights.push({
              type: 'GG_YES',
              label: '⚽ Karşılıklı Gol Var',
              rate: Math.round(ggYesRate * 10) / 10,
              count: stats.ggYes,
              total: stats.totalValid
            });
          }

          // KG Yok
          const ggNoRate = (stats.ggNo / stats.totalValid) * 100;
          if (ggNoRate >= 60) {
            additionalInsights.push({
              type: 'GG_NO',
              label: '🚫 Karşılıklı Gol Yok',
              rate: Math.round(ggNoRate * 10) / 10,
              count: stats.ggNo,
              total: stats.totalValid
            });
          }

          // 2.5 Üst
          const over25Rate = (stats.over_25 / stats.totalValid) * 100;
          if (over25Rate >= 60) {
            additionalInsights.push({
              type: 'OVER_25',
              label: '📈 2.5 Üst',
              rate: Math.round(over25Rate * 10) / 10,
              count: stats.over_25,
              total: stats.totalValid
            });
          }

          // 3.5 Üst
          const over35Rate = (stats.over_35 / stats.totalValid) * 100;
          if (over35Rate >= 60) {
            additionalInsights.push({
              type: 'OVER_35',
              label: '📈 3.5 Üst',
              rate: Math.round(over35Rate * 10) / 10,
              count: stats.over_35,
              total: stats.totalValid
            });
          }

          // İlk Yarı 0.5 Üst
          if (stats.totalWithHalfTime >= 3) {
            const htOver05Rate = (stats.ht_over_05 / stats.totalWithHalfTime) * 100;
            if (htOver05Rate >= 60) {
              additionalInsights.push({
                type: 'HT_OVER_05',
                label: '🕐 İlk Yarı 0.5 Üst',
                rate: Math.round(htOver05Rate * 10) / 10,
                count: stats.ht_over_05,
                total: stats.totalWithHalfTime
              });
            }
          }

          // İlk Yarı 1.5 Üst
          if (stats.totalWithHalfTime >= 3) {
            const htOver15Rate = (stats.ht_over_15 / stats.totalWithHalfTime) * 100;
            if (htOver15Rate >= 60) {
              additionalInsights.push({
                type: 'HT_OVER_15',
                label: '🕐 İlk Yarı 1.5 Üst',
                rate: Math.round(htOver15Rate * 10) / 10,
                count: stats.ht_over_15,
                total: stats.totalWithHalfTime
              });
            }
          }

          // İlk Yarı KG Var
          if (stats.totalWithHalfTime >= 3) {
            const htGGRate = (stats.ht_gg_yes / stats.totalWithHalfTime) * 100;
            if (htGGRate >= 60) {
              additionalInsights.push({
                type: 'HT_GG_YES',
                label: '🕐⚽ İlk Yarı KG Var',
                rate: Math.round(htGGRate * 10) / 10,
                count: stats.ht_gg_yes,
                total: stats.totalWithHalfTime
              });
            }
          }

          recommendations.push({
            match,
            exact_matches: historicalMatches.length,
            total_analyzed: stats.totalValid,
            win_rate: Math.round(msWinRate * 10) / 10,
            recommendation: msType,
            recommended_odds: msData.odds,
            statistics: {
              home_wins: stats.homeWins,
              draws: stats.draws,
              away_wins: stats.awayWins,
              gg_yes: stats.ggYes,
              gg_no: stats.ggNo,
              over_25: stats.over_25,
              over_35: stats.over_35
            },
            additional_insights: additionalInsights
          });

          console.log(`✅ Öneri: ${match.home_team} vs ${match.away_team} - ${msType} (${msWinRate.toFixed(1)}% | ${msData.odds} | ${stats.totalValid} maç) + ${additionalInsights.length} ek bilgi`);
        } else {
          console.log(`⏭️ Reddedildi: ${match.home_team} vs ${match.away_team} - MS Kriter: Win=${msWinRate.toFixed(1)}%, Maç=${stats.totalValid}, Oran=${msData.odds}`);
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
