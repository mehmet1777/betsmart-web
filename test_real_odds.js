const apiKey = '66169584d0msh7057db92927118cp13bd3ejsn55faa1294dce';
const apiHost = 'free-api-live-football-data.p.rapidapi.com';

async function testRealOdds() {
  console.log('🎲 Testing Real Odds Endpoint...\n');
  
  try {
    // 7 gün kontrol et
    for (let i = 0; i < 7; i++) {
      const checkDate = new Date();
      checkDate.setDate(checkDate.getDate() + i);
      const dateStr = checkDate.toISOString().split('T')[0].replace(/-/g, '');
      
      console.log(`📅 Checking: ${dateStr}...`);
      
      const matchesResponse = await fetch(
        `https://${apiHost}/football-get-matches-by-date?date=${dateStr}`,
        {
          method: 'GET',
          headers: {
            'x-rapidapi-key': apiKey,
            'x-rapidapi-host': apiHost
          }
        }
      );

      const matchesData = await matchesResponse.json();
      const matches = matchesData.response?.matches || [];
      
      if (matches.length > 0) {
        const firstMatch = matches[0];
        console.log(`\n✅ Found match: ${firstMatch.home?.name} vs ${firstMatch.away?.name}`);
        console.log(`   Match ID: ${firstMatch.id}`);
        console.log(`   Event ID: ${firstMatch.id}\n`);
        
        // Şimdi bu maç için odds alalım
        console.log('🎲 Getting odds...\n');
        
        const oddsResponse = await fetch(
          `https://${apiHost}/football-event-odds?eventId=${firstMatch.id}`,
          {
            method: 'GET',
            headers: {
              'x-rapidapi-key': apiKey,
              'x-rapidapi-host': apiHost
            }
          }
        );

        console.log(`Odds Status: ${oddsResponse.status}`);
        const oddsData = await oddsResponse.json();
        console.log('\n📊 Odds Response:');
        console.log(JSON.stringify(oddsData, null, 2).substring(0, 500));
        return;
      }
    }
    
    console.log('\n❌ No matches found in 7 days');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

testRealOdds();
