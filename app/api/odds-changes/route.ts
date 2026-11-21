import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Python API'ye proxy et
    const pythonApiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
    
    const response = await fetch(`${pythonApiUrl}/api/odds-changes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Odds changes API error:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch odds changes' },
      { status: 500 }
    );
  }
}
