const apiKey = '66169584d0msh7057db92927118cp13bd3ejsn55faa1294dce';
const apiHost = 'free-api-live-football-data.p.rapidapi.com';

async function checkRawOdds() {
  const today = new Date();
  today.setDate(today.getDate() + 1); // Yarın
  const dateStr = today.toISOString().split('T')[0].replace(/-/g, '');
  
  console.log(`📅 Checking date: ${dateStr}\n`);
  
  const response = await fetch(
    `https://${apiHost}/football-get-matches-by-date?date=${dateStr}`,
    {
      method: 'GET',
      headers: {
        'x-rapidapi-key': apiKey,
        'x-rapidapi-host': apiHost
      }
    }
  );

  const data = await response.json();
  const matches = data.response?.matches || [];
  
  console.log(`📊 Total matches: ${matches.length}\n`);
  
  if (matches.length > 0) {
    console.log('🔍 First 3 matches with odds:\n');
    
    matches.slice(0, 3).forEach((match, i) => {
      console.log(`Maç ${i + 1}: ${match.home?.name} vs ${match.away?.name}`);
      console.log(`  League ID: ${match.leagueId}`);
      console.log(`  Time: ${match.time}`);
      console.log(`  Odds Object:`, match.odds);
      console.log(`  Has odds: ${!!match.odds}`);
      if (match.odds) {
        console.log(`    home: ${match.odds.home}`);
        console.log(`    draw: ${match.odds.draw}`);
        console.log(`    away: ${match.odds.away}`);
      }
      console.log('');
    });
  } else {
    console.log('❌ No matches found for today');
  }
}

checkRawOdds().catch(console.error);
