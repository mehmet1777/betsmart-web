const apiKey = '66169584d0msh7057db92927118cp13bd3ejsn55faa1294dce';
const apiHost = 'free-api-live-football-data.p.rapidapi.com';

async function checkLeagues() {
  const today = new Date();
  const allMatches = [];
  
  // 7 gün kontrol et
  for (let i = 0; i < 7; i++) {
    const checkDate = new Date(today);
    checkDate.setDate(today.getDate() + i);
    const dateStr = checkDate.toISOString().split('T')[0].replace(/-/g, '');
    
    console.log(`Checking ${dateStr}...`);
    
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
    allMatches.push(...matches);
  }
  
  console.log(`\n✅ Total matches: ${allMatches.length}`);
  
  if (allMatches.length > 0) {
    console.log('\n🔍 First match structure:');
    console.log(JSON.stringify(allMatches[0], null, 2));
  }
  
  console.log('\n📋 All unique league IDs and names:');
  const leaguesMap = new Map();
  
  allMatches.forEach(match => {
    const leagueId = match.leagueId;
    const leagueName = match.league || match.leagueName || 'Unknown';
    
    if (!leaguesMap.has(leagueId)) {
      leaguesMap.set(leagueId, leagueName);
    }
  });
  
  // Sort by ID
  const sortedLeagues = Array.from(leaguesMap.entries()).sort((a, b) => a[0] - b[0]);
  
  console.log('\n// Add these to LEAGUE_NAMES:');
  sortedLeagues.forEach(([id, name]) => {
    console.log(`  ${id}: '⚽ ${name}',`);
  });
}

checkLeagues();
