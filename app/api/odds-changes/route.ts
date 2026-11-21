import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { home_team, away_team } = body;
    
    if (!home_team || !away_team) {
      return NextResponse.json(
        { success: false, error: 'home_team ve away_team gerekli' },
        { status: 400 }
      );
    }

    // Supabase client oluştur
    const supabase = createClient(supabaseUrl, supabaseKey);

    // Oran değişikliklerini çek
    const { data, error } = await supabase
      .from('odds_changes')
      .select('*')
      .eq('home_team', home_team)
      .eq('away_team', away_team)
      .order('detected_at', { ascending: false });

    if (error) {
      console.error('Supabase error:', error);
      return NextResponse.json(
        { success: false, error: error.message },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      changes: data || []
    });

  } catch (error) {
    console.error('Odds changes API error:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch odds changes' },
      { status: 500 }
    );
  }
}
