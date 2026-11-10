import { NextResponse } from 'next/server';
import sqlite3 from 'sqlite3';
import path from 'path';

// SQLite veritabanı yolu (parent directory'deki betsmart.db)
const DB_PATH = path.resolve(process.cwd(), '..', 'betsmart.db');

interface FutureMatch {
  id: number;
  datetime: string;
  home_team: string;
  away_team: string;
  league: string;
  odd_1: number;
  odd_x: number;
  odd_2: number;
  over_25: number;
  under_25: number;
  created_at: string;
}

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

// SQLite promise wrapper
function queryDatabase(query: string): Promise<FutureMatch[]> {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READONLY, (err) => {
      if (err) {
        console.error('❌ Database connection error:', err);
        reject(err);
        return;
      }
    });

    db.all(query, [], (err, rows) => {
      if (err) {
        console.error('❌ Query error:', err);
        db.close();
        reject(err);
        return;
      }

      db.close((closeErr) => {
        if (closeErr) {
          console.error('❌ Database close error:', closeErr);
        }
      });

      resolve(rows as FutureMatch[]);
    });
  });
}

export async function GET() {
  try {
    console.log('📂 SQLite veritabanından maçlar çekiliyor...');
    console.log('📍 DB Path:', DB_PATH);
    
    // Gelecek maçları çek
    const query = `
      SELECT 
        id, datetime, home_team, away_team, league, 
        odd_1, odd_x, odd_2, over_25, under_25, created_at
      FROM future_matches
      ORDER BY id ASC
    `;
    
    const matches = await queryDatabase(query);
    
    console.log(`✅ ${matches.length} maç bulundu`);
    
    if (matches.length === 0) {
      return NextResponse.json({ 
        success: true,
        matches: [],
        count: 0,
        message: 'Henüz maç yok. Desktop uygulamasından Mackolik Parser ile maç ekleyin.'
      });
    }
    
    // Maçları API formatına dönüştür
    const formattedMatches = matches.map((match, index) => {
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
      source: 'mackolik-sqlite'
    });
    
  } catch (error: any) {
    console.error('❌ SQLite error:', error);
    
    // Veritabanı yoksa veya hata varsa bilgilendirici mesaj
    if (error.code === 'SQLITE_CANTOPEN') {
      return NextResponse.json({ 
        success: false,
        matches: [],
        count: 0,
        error: 'Veritabanı bulunamadı. Desktop uygulamasından maç ekleyin.',
        message: 'betsmart.db dosyası bulunamadı. Lütfen önce Desktop uygulamadan Mackolik Parser ile maç ekleyin.'
      });
    }
    
    return NextResponse.json({ 
      success: false,
      matches: [],
      count: 0,
      error: error.message || 'Bilinmeyen hata'
    });
  }
}
