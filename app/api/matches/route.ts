import { NextResponse } from 'next/server';

// Vercel serverless ortamında SQLite çalışmadığı için
// geçici olarak mock data kullanıyoruz.
// Gerçek deployment için Vercel Postgres, Supabase veya
// başka bir cloud database kullanılmalı.

export async function GET() {
  try {
    console.log('📂 API: Maçlar istendi (mock data)');
    
    // Şimdilik boş array dön - gerçek veri için database entegrasyonu gerekli
    return NextResponse.json({ 
      success: true,
      matches: [],
      count: 0,
      message: 'Database entegrasyonu için lütfen Vercel Postgres veya Supabase kullanın.'
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
