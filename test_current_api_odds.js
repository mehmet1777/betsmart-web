const apiKey = '66169584d0msh7057db92927118cp13bd3ejsn55faa1294dce';
const apiHost = 'free-api-live-football-data.p.rapidapi.com';

async function testOddsEndpoints() {
  console.log('🔍 Testing Free API Live Football Data for odds...\n');
  
  // Muhtemel odds endpoints
  const endpoints = [
    '/football-get-odds',
    '/odds',
    '/football-odds',
    '/betting-odds',
    '/match-odds',
    '/football-get-matches-odds'
  ];
  
  for (const endpoint of endpoints) {
    console.log(`Testing: ${endpoint}`);
    
    try {
      const response = await fetch(
        `https://${apiHost}${endpoint}`,
        {
          method: 'GET',
          headers: {
            'x-rapidapi-key': apiKey,
            'x-rapidapi-host': apiHost
          }
        }
      );
      
      if (response.ok) {
        console.log(`  ✅ FOUND! Status: ${response.status}`);
        const data = await response.json();
        console.log(`  Data:`, JSON.stringify(data).substring(0, 200));
        console.log('');
        return;
      } else {
        console.log(`  ❌ ${response.status} ${response.statusText}`);
      }
    } catch (error) {
      console.log(`  ❌ Error: ${error.message}`);
    }
  }
  
  console.log('\n⚠️  Bu API\'de odds endpoint\'i bulunamadı.');
  console.log('💡 Çözüm: API-FOOTBALL\'a subscribe olmalıyız.');
}

testOddsEndpoints();
