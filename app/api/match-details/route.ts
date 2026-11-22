import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const supabase = createClient(supabaseUrl, supabaseKey);

export async function POST(request: Request) {
  try {
    const { match_uuid } = await request.json();

    if (!match_uuid) {
      return NextResponse.json({ 
        success: false, 
        details: null,
        message: 'match_uuid gerekli' 
      });
    }

    // match_details tablosundan çek
    const { data, error } = await supabase
      .from('match_details')
      .select('*')
      .eq('match_uuid', match_uuid)
      .single();

    if (error || !data) {
      return NextResponse.json({ 
        success: false, 
        details: null 
      });
    }

    return NextResponse.json({ 
      success: true, 
      details: data 
    });

  } catch (error: any) {
    console.error('❌ match-details API error:', error);
    return NextResponse.json({ 
      success: false, 
      details: null,
      error: error.message 
    });
  }
}
