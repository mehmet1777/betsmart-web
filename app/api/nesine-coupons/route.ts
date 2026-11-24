import { createClient } from '@supabase/supabase-js';
import { NextResponse } from 'next/server';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// Disable caching
export const dynamic = 'force-dynamic';
export const revalidate = 0;

export async function GET() {
  try {
    // Kuponları tarih sırasına göre çek (en yeni önce)
    const { data: coupons, error: couponsError } = await supabase
      .from('nesine_coupons')
      .select('*')
      .order('coupon_date', { ascending: false })
      .limit(50);

    if (couponsError) {
      console.error('Kuponlar çekilemedi:', couponsError);
      return NextResponse.json({ error: 'Kuponlar yüklenemedi' }, { status: 500 });
    }

    // Her kupon için maçları çek
    const couponsWithMatches = await Promise.all(
      coupons.map(async (coupon) => {
        const { data: matches, error: matchesError } = await supabase
          .from('nesine_coupon_matches')
          .select('*')
          .eq('coupon_id', coupon.id)
          .order('match_order', { ascending: true });

        if (matchesError) {
          console.error('Maçlar çekilemedi:', matchesError);
          return { ...coupon, matches: [] };
        }

        return {
          ...coupon,
          matches: matches || []
        };
      })
    );

    return NextResponse.json({ coupons: couponsWithMatches });
  } catch (error) {
    console.error('API Hatası:', error);
    return NextResponse.json({ error: 'Sunucu hatası' }, { status: 500 });
  }
}
