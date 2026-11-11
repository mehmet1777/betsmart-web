import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

// Supabase client
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

const supabase = createClient(supabaseUrl, supabaseKey);

function parseDateTime(dateTimeStr: string): Date {
  // "10/11/2026 21:00" formatını parse et
  try {
    const [datePart, timePart] = dateTimeStr.split(' ');
    const [day, month, year] = datePart.split('/');
    const [hours, minutes] = timePart.split(':');
    
    return new Date(
      parseInt(year),
      parseInt(month) - 1,
      parseInt(day),
      parseInt(hours),
      parseInt(minutes)
    );
  } catch (e) {
    return new Date();
  }
}

function formatDateTime(date: Date): string {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  
  return `${day}.${month}.${year} ${hours}:${minutes}`;
}

// Maçın canlı olup olmadığını kontrol et
function isMatchLive(datetime: string): boolean {
  try {
    const matchDate = parseDateTime(datetime);
    const now = new Date();
    const diffMinutes = (now.getTime() - matchDate.getTime()) / (1000 * 60);
    
    // Maç başladıysa ve 120 dakika geçmediyse canlı
    return diffMinutes >= 0 && diffMinutes <= 120;
  } catch (e) {
    return false;
  }
}

export async function GET() {
  try {
    console.log('📂 Supabase\'den maçlar çekiliyor...');
    
    const { data: matches, error } = await supabase
      .from('future_matches')
      .select('*')
      .order('id', { ascending: true });
    
    if (error) {
      console.error('❌ Supabase error:', error);
      throw error;
    }
    
    if (!matches || matches.length === 0) {
      return NextResponse.json({ 
        success: true,
        matches: [],
        count: 0,
        message: 'Henüz maç yok. Desktop uygulamasından Mackolik Parser ile maç ekleyin.'
      });
    }
    
    console.log(`✅ ${matches.length} maç bulundu`);
    
    // Maçları API formatına dönüştür
    const formattedMatches = matches.map((match: any) => {
      const matchDate = parseDateTime(match.datetime);
      const isLive = isMatchLive(match.datetime);
      
      return {
        id: match.id,
        leagueId: match.id,
        leagueName: match.league,  // Lig kodunu olduğu gibi göster (PRD, COC, J-C vs.)
        time: formatDateTime(matchDate),
        home: {
          id: match.id * 2,
          name: match.home_team,
          score: undefined
        },
        away: {
          id: match.id * 2 + 1,
          name: match.away_team,
          score: undefined
        },
        status: {
          finished: false,
          started: isLive
        },
        odds: {
          home: match.odd_1 > 1.01 ? match.odd_1.toFixed(2) : '-',
          draw: match.odd_x > 1.01 ? match.odd_x.toFixed(2) : '-',
          away: match.odd_2 > 1.01 ? match.odd_2.toFixed(2) : '-'
        },
        // Extra bilgiler (isteğe bağlı kullanım için)
        overUnder: {
          over: match.over_25 > 1.01 ? match.over_25.toFixed(2) : '-',
          under: match.under_25 > 1.01 ? match.under_25.toFixed(2) : '-'
        }
      };
    });
    
    console.log(`🎯 ${formattedMatches.length} maç frontend'e gönderiliyor`);
    
    return NextResponse.json({ 
      success: true,
      matches: formattedMatches,
      count: formattedMatches.length,
      source: 'supabase-cloud'
    });
    
  } catch (error: any) {
    console.error('❌ API error:', error);
    
    return NextResponse.json({ 
      success: false,
      matches: [],
      count: 0,
      error: error.message || 'Bilinmeyen hata'
    });
  }
}
