const apiKey = '66169584d0msh7057db92927118cp13bd3ejsn55faa1294dce';

async function testOddsAPI() {
  console.log('🎲 Testing Live Sports Odds API...\n');
  
  try {
    // Test endpoint
    const response = await fetch(
      'https://live-sports-odds.p.rapidapi.com/v4/sports/soccer_epl/odds',
      {
        method: 'GET',
        headers: {
          'x-rapidapi-key': apiKey,
          'x-rapidapi-host': 'live-sports-odds.p.rapidapi.com'
        }
      }
    );

    if (!response.ok) {
      console.log(`❌ Error: ${response.status} ${response.statusText}`);
      const text = await response.text();
      console.log('Response:', text);
      return;
    }

    const data = await response.json();
    console.log(`✅ Success! Found ${data.length || 0} matches\n`);
    
    if (data.length > 0) {
      console.log('📊 First match with odds:\n');
      const match = data[0];
      console.log(`Match: ${match.home_team} vs ${match.away_team}`);
      console.log(`Start time: ${match.commence_time}`);
      console.log(`\nBookmakers:`);
      
      if (match.bookmakers && match.bookmakers.length > 0) {
        const bookmaker = match.bookmakers[0];
        console.log(`  ${bookmaker.key}:`);
        
        const h2hMarket = bookmaker.markets.find(m => m.key === 'h2h');
        if (h2hMarket) {
          console.log(`    Home (1): ${h2hMarket.outcomes[0].price}`);
          console.log(`    Draw (X): ${h2hMarket.outcomes[1]?.price || 'N/A'}`);
          console.log(`    Away (2): ${h2hMarket.outcomes[2]?.price || h2hMarket.outcomes[1]?.price}`);
        }
      }
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

testOddsAPI();
