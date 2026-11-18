// The Odds API Test
// Sign up: https://the-odds-api.com/
// Get free API key

const API_KEY = 'c10fe9e5201853c678da754cdf7e28c7'; // The Odds API Key

async function testTheOddsAPI() {
  console.log('⚽ Testing The Odds API...\n');
  
  try {
    // Soccer odds
    const response = await fetch(
      `https://api.the-odds-api.com/v4/sports/soccer_epl/odds?apiKey=${API_KEY}&regions=eu&markets=h2h`,
      {
        method: 'GET'
      }
    );

    console.log(`Status: ${response.status}\n`);
    
    if (!response.ok) {
      const text = await response.text();
      console.log('Error:', text);
      return;
    }

    const data = await response.json();
    console.log(`✅ Found ${data.length} matches\n`);
    
    if (data.length > 0) {
      const match = data[0];
      console.log(`📊 First match:`);
      console.log(`  ${match.home_team} vs ${match.away_team}`);
      console.log(`  Start: ${match.commence_time}`);
      
      if (match.bookmakers && match.bookmakers.length > 0) {
        const bookmaker = match.bookmakers[0];
        console.log(`\n  Bookmaker: ${bookmaker.title}`);
        
        const h2h = bookmaker.markets.find(m => m.key === 'h2h');
        if (h2h) {
          console.log(`  Odds:`);
          h2h.outcomes.forEach(o => {
            console.log(`    ${o.name}: ${o.price}`);
          });
        }
      }
      
      console.log('\n✅ The Odds API çalışıyor!');
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

console.log('📝 Adımlar:');
console.log('1. https://the-odds-api.com/ adresine git');
console.log('2. "Get a Free API Key" butonuna tıkla');
console.log('3. Email ile kayıt ol');
console.log('4. API key\'i al ve bu dosyaya yapıştır');
console.log('5. node test_the_odds_api.js komutunu çalıştır\n');

if (API_KEY === 'YOUR_API_KEY_HERE') {
  console.log('⚠️  Önce API key almalısın!');
} else {
  testTheOddsAPI();
}
