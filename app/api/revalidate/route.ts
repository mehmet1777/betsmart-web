import { NextRequest, NextResponse } from 'next/server';
import { revalidatePath } from 'next/cache';

// Edge Runtime - CPU limiti sayılmaz! ⚡
export const runtime = 'edge';

export async function POST(request: NextRequest) {
  try {
    // Secret token kontrolü (güvenlik için)
    const { searchParams } = new URL(request.url);
    const secret = searchParams.get('secret');
    
    // .env'den secret al
    if (secret !== process.env.REVALIDATE_SECRET) {
      return NextResponse.json({ 
        success: false, 
        message: 'Invalid secret' 
      }, { status: 401 });
    }
    
    // Cache'i temizle
    revalidatePath('/');
    revalidatePath('/api/matches');
    
    console.log('✅ Cache temizlendi:', new Date().toISOString());
    
    return NextResponse.json({ 
      success: true, 
      revalidated: true,
      message: 'Cache başarıyla temizlendi',
      timestamp: new Date().toISOString()
    });
    
  } catch (error: any) {
    console.error('❌ Revalidation error:', error);
    return NextResponse.json({ 
      success: false, 
      message: error.message 
    }, { status: 500 });
  }
}
