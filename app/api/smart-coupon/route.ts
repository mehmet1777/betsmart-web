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

        // TÜM SEÇENEKLERİ HESAPLA ve EN İYİSİNİ SEÇ
        const options = [
          // Maç Sonucu
          { type: 'MS1', label: 'Ev Sahibi', count: stats.homeWins, total: stats.totalValid, odds: odd1 },
          { type: 'MSX', label: 'Beraberlik', count: stats.draws, total: stats.totalValid, odds: oddX },
          { type: 'MS2', label: 'Deplasman', count: stats.awayWins, total: stats.totalValid, odds: odd2 },
          
          // Karşılıklı Gol
          { type: 'GG_YES', label: 'Karşılıklı Gol Var', count: stats.ggYes, total: stats.totalValid, odds: 0 },
          { type: 'GG_NO', label: 'Karşılıklı Gol Yok', count: stats.ggNo, total: stats.totalValid, odds: 0 },
          
          // Alt/Üst
          { type: 'OVER_15', label: '1.5 Üst', count: stats.over_15, total: stats.totalValid, odds: 0 },
          { type: 'OVER_25', label: '2.5 Üst', count: stats.over_25, total: stats.totalValid, odds: 0 },
          { type: 'OVER_35', label: '3.5 Üst', count: stats.over_35, total: stats.totalValid, odds: 0 },
          
          // İlk Yarı Alt/Üst (sadece ilk yarı verisi varsa)
          ...(stats.totalWithHalfTime >= 3 ? [
            { type: 'HT_OVER_05', label: 'İlk Yarı 0.5 Üst', count: stats.ht_over_05, total: stats.totalWithHalfTime, odds: 0 },
            { type: 'HT_OVER_15', label: 'İlk Yarı 1.5 Üst', count: stats.ht_over_15, total: stats.totalWithHalfTime, odds: 0 },
          ] : []),
          
          // İlk Yarı KG (sadece ilk yarı verisi varsa)
          ...(stats.totalWithHalfTime >= 3 ? [
            { type: 'HT_GG_YES', label: 'İlk Yarı KG Var', count: stats.ht_gg_yes, total: stats.totalWithHalfTime, odds: 0 }
          ] : [])
        ];

        // Her seçeneğin başarı oranını hesapla
        const optionsWithRate = options.map(opt => ({
          ...opt,
          rate: (opt.count / opt.total) * 100
        }));

        // En yüksek oranı bul
        const bestOption = optionsWithRate.reduce((best, current) => 
          current.rate > best.rate ? current : best
        );

        // Filtreleme kriterleri
        const MIN_WIN_RATE = 75;
        const MIN_MATCHES = 3;
        const MIN_ODDS = 1.30;

        // Eğer MS seçeneği ise oran kontrolü yap, diğerlerinde oran kontrolü yok
        const needsOddCheck = ['MS1', 'MSX', 'MS2'].includes(bestOption.type);
        const oddsOk = !needsOddCheck || bestOption.odds >= MIN_ODDS;

        if (
          bestOption.rate >= MIN_WIN_RATE && 
          bestOption.total >= MIN_MATCHES &&
          oddsOk
        ) {
          recommendations.push({
            match,
            exact_matches: historicalMatches.length,
            total_analyzed: bestOption.total,
            win_rate: Math.round(bestOption.rate * 10) / 10,
            recommendation: bestOption.type,
            recommendation_label: bestOption.label,
            recommended_odds: bestOption.odds || 0,
            statistics: {
              home_wins: stats.homeWins,
              draws: stats.draws,
              away_wins: stats.awayWins,
              gg_yes: stats.ggYes,
              gg_no: stats.ggNo,
              over_25: stats.over_25,
              over_35: stats.over_35
            }
          });

          console.log(`✅ Öneri: ${match.home_team} vs ${match.away_team} - ${bestOption.label} (${bestOption.rate.toFixed(1)}% | ${bestOption.count}/${bestOption.total})`);
        } else {
          console.log(`⏭️ Reddedildi: ${match.home_team} vs ${match.away_team} - En iyi: ${bestOption.label} (${bestOption.rate.toFixed(1)}%, ${bestOption.total} maç)`);
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
