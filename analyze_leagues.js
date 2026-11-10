const apiKey = '66169584d0msh7057db92927118cp13bd3ejsn55faa1294dce';
const apiHost = 'free-api-live-football-data.p.rapidapi.com';

async function analyzeAllLeagues() {
  const today = new Date();
  const allMatches = [];
  
  console.log('🔍 7 günlük maç verisi analiz ediliyor...\n');
  
  // 7 gün kontrol et
  for (let i = 0; i < 7; i++) {
    const checkDate = new Date(today);
    checkDate.setDate(today.getDate() + i);
    const dateStr = checkDate.toISOString().split('T')[0].replace(/-/g, '');
    
    process.stdout.write(`  ${checkDate.toISOString().split('T')[0]} kontrol ediliyor... `);
    
    try {
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
      console.log(`✅ ${matches.length} maç`);
    } catch (error) {
      console.log('❌ Hata');
    }
  }
  
  console.log(`\n✅ Toplam ${allMatches.length} maç bulundu\n`);
  
  // Mevcut LEAGUE_NAMES (types/index.ts'den)
  const EXISTING_LEAGUES = new Set([
    1000001212, 1000001591,
    1000001862, 1000001750, 1000001751, 1000001752,
    943230, 943229, 943231, 1000001457,
    8, 9, 10, 11, 940374, 953430,
    87, 88, 138, 938653,
    35, 36,
    135, 136, 942846, 942852,
    34, 60,
    63, 185, 1000001242, 1000001243,
    37, 38,
    59, 51, 936592, 57, 951425, 32, 50, 56, 62, 66, 345, 179,
    77, 333, 210, 266,
    325, 326, 332, 341, 355, 356, 357, 318, 268,
    955, 950, 956, 288,
    1000001253, 10342, 335, 336, 337,
    938428, 942122, 183, 938187,
    9941, 959, 960, 961,
    9676, 938777, 939688
  ]);
  
  // Tüm unique ligleri topla
  const leaguesMap = new Map();
  
  allMatches.forEach(match => {
    const leagueId = match.leagueId;
    const leagueName = match.league || match.leagueName || 'Unknown';
    
    if (!leaguesMap.has(leagueId)) {
      leaguesMap.set(leagueId, {
        id: leagueId,
        name: leagueName,
        matchCount: 0
      });
    }
    
    leaguesMap.get(leagueId).matchCount++;
  });
  
  // Eksik olanları bul
  const missingLeagues = [];
  const existingLeagues = [];
  
  Array.from(leaguesMap.values()).forEach(league => {
    if (!EXISTING_LEAGUES.has(league.id)) {
      missingLeagues.push(league);
    } else {
      existingLeagues.push(league);
    }
  });
  
  // Eksik ligleri maç sayısına göre sırala
  missingLeagues.sort((a, b) => b.matchCount - a.matchCount);
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('❌ EKSİK LİGLER (types/index.ts\'e eklenecek)');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  if (missingLeagues.length === 0) {
    console.log('✅ Tüm ligler tanımlı!\n');
  } else {
    console.log('// types/index.ts LEAGUE_NAMES içine ekle:\n');
    
    missingLeagues.forEach(league => {
      // Lig ismini temizle
      let cleanName = league.name
        .replace(/^[^a-zA-ZÀ-ž0-9]+/, '') // Başındaki garip karakterler
        .trim();
      
      if (cleanName === 'Unknown' || cleanName.length < 3) {
        cleanName = `Lig ${league.id}`;
      }
      
      // Bayrak tahmin et (ülke ismine göre)
      let flag = '⚽';
      const nameLower = cleanName.toLowerCase();
      
      if (nameLower.includes('brazil') || nameLower.includes('brasileiro')) flag = '🇧🇷';
      else if (nameLower.includes('argentin')) flag = '🇦🇷';
      else if (nameLower.includes('portugal') || nameLower.includes('portug')) flag = '🇵🇹';
      else if (nameLower.includes('spain') || nameLower.includes('españa')) flag = '🇪🇸';
      else if (nameLower.includes('england') || nameLower.includes('premier')) flag = '🏴󠁧󠁢󠁥󠁮󠁧󠁿';
      else if (nameLower.includes('italy') || nameLower.includes('serie')) flag = '🇮🇹';
      else if (nameLower.includes('germany') || nameLower.includes('bundesliga')) flag = '🇩🇪';
      else if (nameLower.includes('france') || nameLower.includes('ligue')) flag = '🇫🇷';
      else if (nameLower.includes('netherlands') || nameLower.includes('eredivisie')) flag = '🇳🇱';
      else if (nameLower.includes('belgium')) flag = '🇧🇪';
      else if (nameLower.includes('turkey') || nameLower.includes('türk')) flag = '🇹🇷';
      else if (nameLower.includes('mexico')) flag = '🇲🇽';
      else if (nameLower.includes('usa') || nameLower.includes('mls')) flag = '🇺🇸';
      else if (nameLower.includes('chile')) flag = '🇨🇱';
      else if (nameLower.includes('colombia')) flag = '🇨🇴';
      else if (nameLower.includes('uruguay')) flag = '🇺🇾';
      else if (nameLower.includes('peru')) flag = '🇵🇪';
      else if (nameLower.includes('ecuador')) flag = '🇪🇨';
      else if (nameLower.includes('greece')) flag = '🇬🇷';
      else if (nameLower.includes('romania')) flag = '🇷🇴';
      else if (nameLower.includes('poland')) flag = '🇵🇱';
      else if (nameLower.includes('czech')) flag = '🇨🇿';
      else if (nameLower.includes('austria')) flag = '🇦🇹';
      else if (nameLower.includes('switzerland')) flag = '🇨🇭';
      else if (nameLower.includes('sweden')) flag = '🇸🇪';
      else if (nameLower.includes('norway')) flag = '🇳🇴';
      else if (nameLower.includes('denmark')) flag = '🇩🇰';
      else if (nameLower.includes('scotland')) flag = '🏴󠁧󠁢󠁳󠁣󠁴󠁿';
      else if (nameLower.includes('ireland')) flag = '🇮🇪';
      else if (nameLower.includes('australia')) flag = '🇦🇺';
      else if (nameLower.includes('japan')) flag = '🇯🇵';
      else if (nameLower.includes('korea')) flag = '🇰🇷';
      else if (nameLower.includes('china')) flag = '🇨🇳';
      else if (nameLower.includes('india')) flag = '🇮🇳';
      else if (nameLower.includes('saudi')) flag = '🇸🇦';
      else if (nameLower.includes('egypt')) flag = '🇪🇬';
      else if (nameLower.includes('morocco')) flag = '🇲🇦';
      else if (nameLower.includes('tunisia')) flag = '🇹🇳';
      else if (nameLower.includes('algeria')) flag = '🇩🇿';
      else if (nameLower.includes('champions') || nameLower.includes('uefa')) flag = '🏆';
      else if (nameLower.includes('women') || nameLower.includes('kadın')) flag = '👩';
      else if (nameLower.includes('youth') || nameLower.includes('u19') || nameLower.includes('u21')) flag = '👦';
      
      console.log(`  ${league.id}: '${flag} ${cleanName}', // ${league.matchCount} maç`);
    });
    
    console.log(`\n📊 Toplam ${missingLeagues.length} eksik lig bulundu\n`);
  }
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('✅ MEVCUT LİGLER (zaten tanımlı)');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  existingLeagues
    .sort((a, b) => b.matchCount - a.matchCount)
    .slice(0, 10)
    .forEach(league => {
      console.log(`  ${league.id}: ${league.name} (${league.matchCount} maç)`);
    });
  
  console.log(`\n📊 Toplam ${existingLeagues.length} lig zaten tanımlı\n`);
}

analyzeAllLeagues().catch(console.error);
