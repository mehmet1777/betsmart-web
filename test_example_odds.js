const apiKey = '66169584d0msh7057db92927118cp13bd3ejsn55faa1294dce';
const apiHost = 'free-api-live-football-data.p.rapidapi.com';

async function testExampleOdds() {
  console.log('🎲 Testing with example event ID from docs...\n');
  
  // Screenshot'tan gelen örnek ID
  const exampleEventId = '46216244';
  
  try {
    const oddsResponse = await fetch(
      `https://${apiHost}/football-event-odds?eventId=${exampleEventId}&countryCode=BR`,
      {
        method: 'GET',
        headers: {
          'x-rapidapi-key': apiKey,
          'x-rapidapi-host': apiHost
        }
      }
    );

    console.log(`Status: ${oddsResponse.status} ${oddsResponse.statusText}\n`);
    
    const oddsData = await oddsResponse.json();
    console.log('📊 Odds Response:');
    console.log(JSON.stringify(oddsData, null, 2));
    
    if (oddsData.response) {
      console.log('\n✅ API gerçek oranları veriyor!');
      console.log('🎯 Şimdi bu endpoint\'i projeye entegre edelim!');
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

testExampleOdds();
