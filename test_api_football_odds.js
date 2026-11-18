const apiKey = '66169584d0msh7057db92927118cp13bd3ejsn55faa1294dce';

async function testAPIFootball() {
  console.log('⚽ Testing API-Football for odds...\n');
  
  try {
    // Test 1: Fixtures with odds
    console.log('1️⃣ Testing fixtures endpoint...');
    const fixturesResponse = await fetch(
      'https://api-football-v1.p.rapidapi.com/v3/fixtures?date=2026-11-10&timezone=Europe/Istanbul',
      {
        method: 'GET',
        headers: {
          'x-rapidapi-key': apiKey,
          'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
        }
      }
    );

    if (!fixturesResponse.ok) {
      console.log(`❌ Fixtures Error: ${fixturesResponse.status}`);
      const text = await fixturesResponse.text();
      console.log('Response:', text);
      return;
    }

    const fixturesData = await fixturesResponse.json();
    console.log(`✅ Found ${fixturesData.response?.length || 0} fixtures\n`);
    
    if (fixturesData.response && fixturesData.response.length > 0) {
      const fixture = fixturesData.response[0];
      console.log(`📊 First match:`);
      console.log(`  ${fixture.teams.home.name} vs ${fixture.teams.away.name}`);
      console.log(`  Date: ${fixture.fixture.date}`);
      console.log(`  Fixture ID: ${fixture.fixture.id}\n`);
      
      // Test 2: Odds for this fixture
      console.log('2️⃣ Testing odds endpoint...');
      const oddsResponse = await fetch(
        `https://api-football-v1.p.rapidapi.com/v3/odds?fixture=${fixture.fixture.id}`,
        {
          method: 'GET',
          headers: {
            'x-rapidapi-key': apiKey,
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
          }
        }
      );

      if (!oddsResponse.ok) {
        console.log(`❌ Odds Error: ${oddsResponse.status}`);
        return;
      }

      const oddsData = await oddsResponse.json();
      console.log(`✅ Odds data received!\n`);
      
      if (oddsData.response && oddsData.response.length > 0) {
        const match = oddsData.response[0];
        console.log(`🎲 Bookmakers:`);
        
        if (match.bookmakers && match.bookmakers.length > 0) {
          const bookmaker = match.bookmakers[0];
          console.log(`  ${bookmaker.name}:`);
          
          const h2hBet = bookmaker.bets.find(b => b.name === 'Match Winner');
          if (h2hBet && h2hBet.values) {
            h2hBet.values.forEach(v => {
              console.log(`    ${v.value}: ${v.odd}`);
            });
          }
        }
        
        console.log('\n✅ API-Football çalışıyor ve oranları veriyor!');
      } else {
        console.log('⚠️  Bu maç için oran yok');
      }
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

testAPIFootball();
