// Maç tipi
export interface Match {
  id: number;
  leagueId: number;
  leagueName?: string; // API'den gelen lig ismi
  time: string;
  home: {
    id: number;
    name: string;
    score?: number;
  };
  away: {
    id: number;
    name: string;
    score?: number;
  };
  status: {
    finished: boolean;
    started: boolean;
    scoreStr?: string;
  };
  odds?: {
    home: string;
    draw: string;
    away: string;
  };
}

// Kupon seçimi
export interface BetSelection {
  matchId: number;
  match: Match;
  prediction: '1' | 'X' | '2'; // 1: Ev sahibi, X: Beraberlik, 2: Deplasman
}

// Kupon
export interface BetSlip {
  selections: BetSelection[];
  createdAt: string;
}

// Oran analizi sonucu
export interface OddsAnalysis {
  totalMatches: number; // Toplam benzer maç sayısı
  homeWins: number;     // Ev sahibi galibiyeti
  draws: number;        // Beraberlik
  awayWins: number;     // Deplasman galibiyeti
  winProbability: number; // Kazanma olasılığı %
  similarBets: Array<{
    match: string;
    result: string;
    date: string;
    odds: string;
  }>;
}

// Lig isimleri
export const LEAGUE_NAMES: Record<number, string> = {
  // Türkiye
  1000001862: '🇹🇷 Süper Lig',
  1000001750: '🇹🇷 1. Lig',
  1000001751: '🇹🇷 2. Lig',
  1000001752: '🇹🇷 3. Lig',
  
  // Avrupa Kupaları
  943230: '🏆 Şampiyonlar Ligi',
  943229: '🏆 Avrupa Ligi',
  943231: '🏆 Konferans Ligi',
  1000001457: '👦 Gençlik Ligi U19',
  943324: '🏆 UEFA Kupası',
  943368: '🏆 Şampiyonlar Ligi Eleme',
  943369: '🏆 Avrupa Ligi Eleme',
  
  // İngiltere
  8: '🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier Lig',
  9: '🏴󠁧󠁢󠁥󠁮󠁧󠁿 Championship',
  10: '🏴󠁧󠁢󠁥󠁮󠁧󠁿 League One',
  11: '🏴󠁧󠁢󠁥󠁮󠁧󠁿 League Two',
  940374: '🏴󠁧󠁢󠁥󠁮󠁧󠁿 National League',
  953430: '🏴󠁧󠁢󠁥󠁮󠁧󠁿 Southern League',
  940355: '🏴󠁧󠁢󠁥󠁮󠁧󠁿 FA Kupası',
  940451: '🏴󠁧󠁢󠁥󠁮󠁧󠁿 EFL Kupası',
  940452: '🏴󠁧󠁢󠁥󠁮󠁧󠁿 EFL Trophy',
  
  // İspanya
  87: '🇪🇸 La Liga',
  88: '🇪🇸 La Liga 2',
  138: '🇪🇸 Primera RFEF',
  938653: '🇪🇸 Segunda RFEF',
  938777: '👩 Kadınlar La Liga',
  938778: '🇪🇸 Kral Kupası',
  938779: '🇪🇸 Süper Kupa',
  
  // Almanya
  35: '🇩🇪 Bundesliga',
  36: '🇩🇪 2. Bundesliga',
  111: '🇩🇪 3. Liga',
  9676: '👩 Kadınlar Bundesliga',
  
  // İtalya
  135: '🇮🇹 Serie A',
  136: '🇮🇹 Serie B',
  942846: '🇮🇹 Serie C Grup A',
  942852: '🇮🇹 Serie C Grup B',
  942853: '🇮🇹 Serie C Grup C',
  942844: '🇮🇹 İtalya Kupası',
  
  // Fransa
  34: '🇫🇷 Ligue 1',
  60: '🇫🇷 Ligue 2',
  522: '🇫🇷 National',
  
  // Portekiz
  63: '🇵🇹 Portekiz Ligi',
  185: '🇵🇹 Portekiz 2. Lig',
  1000001242: '🇵🇹 Portekiz 3. Lig',
  1000001243: '🇵🇹 Portekiz Şampiyonası',
  
  // Hollanda
  37: '🇳🇱 Hollanda Ligi',
  38: '🇳🇱 Hollanda 2. Lig',
  
  // İskandinav Ülkeleri
  59: '🇳🇴 Norveç Ligi',
  51: '🇩🇰 Danimarka Ligi',
  936592: '🇩🇰 Danimarka 2. Lig',
  939688: '👩 Kadınlar Ligi (Danimarka)',
  57: '🇸🇪 İsveç Ligi',
  951425: '🇸🇪 İsveç 2. Lig',
  344: '🇫🇮 Finlandiya Ligi',
  
  // Diğer Avrupa
  32: '🇧🇪 Belçika Ligi',
  50: '🇨🇭 İsviçre Ligi',
  56: '🇦🇹 Avusturya Ligi',
  62: '🇬🇷 Yunanistan Ligi',
  66: '🇵🇱 Polonya Ligi',
  345: '🇨🇿 Çekya Ligi',
  179: '🏴󠁧󠁢󠁳󠁣󠁴󠁿 İskoçya Premier Lig',
  177: '🏴󠁧󠁢󠁳󠁣󠁴󠁿 İskoçya Championship',
  232: '🇮🇪 İrlanda Ligi',
  
  // Doğu Avrupa
  77: '🇷🇺 Rusya Ligi',
  333: '🇺🇦 Ukrayna Ligi',
  210: '🇭🇷 Hırvatistan Ligi',
  266: '🇷🇸 Sırbistan Ligi',
  183: '🇧🇬 Bulgaristan Ligi',
  938428: '🇷🇴 Romanya Ligi',
  942122: '🇷🇴 Romanya 2. Lig',
  
  // Güney Amerika
  325: '🇧🇷 Brasileirão',
  326: '🇧🇷 Brezilya 2. Lig',
  1000001212: '🇧🇷 Brezilya 3. Lig',
  332: '🇦🇷 Arjantin Ligi',
  1000001591: '🇦🇷 Arjantin 2. Lig',
  341: '🇲🇽 Meksika Ligi',
  10342: '🇺🇾 Uruguay Ligi',
  335: '🇨🇱 Şili Ligi',
  336: '🇨🇴 Kolombiya Ligi',
  337: '🇵🇪 Peru Ligi',
  1000001253: '🇪🇨 Ekvador Ligi',
  516: '🇵🇾 Paraguay Ligi',
  439: '🇧🇴 Bolivya Ligi',
  540: '🇻🇪 Venezuela Ligi',
  
  // Kuzey Amerika
  332: '🇺🇸 MLS',
  8935: '🇺🇸 USL Championship',
  8972: '🇺🇸 USL League One',
  9089: '🇨🇦 Kanada Premier Ligi',
  
  // Asya
  355: '🇯🇵 J1 Ligi',
  356: '🇯🇵 J2 Ligi',
  357: '🇰🇷 K Ligi 1',
  9096: '🇰🇷 K Ligi 2',
  318: '🇨🇳 Çin Süper Ligi',
  9136: '🇨🇳 Çin 2. Lig',
  9195: '🇨🇳 Çin 3. Lig',
  9227: '🇮🇳 Hindistan Süper Ligi',
  9634: '🇮🇳 I-League',
  
  // Avustralya
  268: '🇦🇺 A-League',
  10289: '🇦🇺 Kadınlar A-League',
  10308: '🇦🇺 NPL',
  
  // Orta Doğu
  955: '🇸🇦 Suudi Arabistan Ligi',
  950: '🇦🇪 BAE Ligi',
  956: '🇶🇦 Katar Ligi',
  938187: '🇮🇱 İsrail Ligi',
  
  // Afrika
  288: '🇿🇦 Güney Afrika Ligi',
  9941: '🇪🇬 Mısır Ligi',
  959: '🇹🇳 Tunus Ligi',
  960: '🇲🇦 Fas Ligi',
  961: '🇩🇿 Cezayir Ligi',
  
  // Daha Az Bilinen Ligler (Generic isimler)
  914609: '⚽ Lig 914609',
  915708: '⚽ Lig 915708',
  920741: '⚽ Turnuva Grubu A',
  920742: '⚽ Turnuva Grubu B',
  920743: '⚽ Turnuva Grubu C',
  920744: '⚽ Turnuva Grubu D',
  920745: '⚽ Turnuva Grubu E',
  920746: '⚽ Turnuva Grubu F',
  920747: '⚽ Turnuva Grubu G',
  920748: '⚽ Turnuva Grubu H',
  920749: '⚽ Turnuva Eleme 1',
  920750: '⚽ Turnuva Eleme 2',
  920751: '⚽ Turnuva Çeyrek Final',
  920752: '⚽ Turnuva Yarı Final',
  920753: '⚽ Turnuva Final',
  920754: '⚽ Turnuva 3. Yer',
  922761: '⚽ Dostluk Maçları',
  937668: '⚽ Bölgesel Lig A',
  937670: '⚽ Bölgesel Lig B',
  937672: '⚽ Bölgesel Lig C',
  938005: '⚽ Alt Lig Turnuvası',
  938215: '⚽ Amatör Lig',
  938226: '👦 Gençlik Ligi A',
  938228: '👦 Gençlik Ligi B',
  938229: '👦 Gençlik Ligi C',
  938230: '👦 Gençlik Ligi D',
  938235: '👦 U21 Ligi',
  938236: '👦 U19 Ligi',
  938237: '👦 U18 Ligi',
  938238: '👦 U17 Ligi',
  938239: '👦 U16 Ligi',
  938240: '👦 U15 Ligi',
  938241: '👦 Gençlik Kupası A',
  938242: '👦 Gençlik Kupası B',
  938243: '👦 Gençlik Kupası C',
  938244: '👦 Gençlik Kupası D',
  938245: '👦 Gençlik Kupası E',
  938246: '👦 Gençlik Turnuvası',
  938371: '⚽ Bölgesel Kupa',
  938416: '⚽ Rezerv Ligi',
  938422: '⚽ İkinci Takımlar Ligi',
  938628: '⚽ Alt Lig Playoff',
  938638: '⚽ 4. Lig A',
  938639: '⚽ 4. Lig B',
  938783: '🏆 Lig Kupası',
  938792: '🏆 Süper Kupa',
  938793: '🏆 Federasyon Kupası',
  938794: '🏆 Bölge Kupası A',
  938796: '🏆 Bölge Kupası B',
  938854: '⚽ Amatör Playoff',
  940360: '⚽ Kupa Eleme',
  940450: '⚽ Lig Playoff',
  940469: '⚽ Yükselme Playoff',
  941109: '⚽ Alt Lig 1',
  941116: '⚽ Alt Lig 2',
  941117: '⚽ Alt Lig 3',
  941118: '⚽ Alt Lig 4',
  941122: '⚽ Grup Maçları A',
  941123: '⚽ Grup Maçları B',
  941124: '⚽ Grup Maçları C',
  941125: '⚽ Grup Maçları D',
  941129: '⚽ Eleme Turu',
  941168: '⚽ Playoff Turu',
  941466: '⚽ Bölgesel Turnuva',
  942146: '⚽ Alt Kupa',
  945430: '⚽ 5. Lig',
  945923: '⚽ 6. Lig',
  948410: '⚽ 7. Lig',
  948423: '⚽ 8. Lig',
  949112: '⚽ Playoff A',
  949115: '⚽ Playoff B',
  949116: '⚽ Playoff C',
  949117: '⚽ Playoff D',
  949731: '⚽ Sezon Sonu Turnuvası',
  951107: '⚽ Yaz Ligi',
  951108: '⚽ Kış Ligi',
  951233: '⚽ Bahar Sezonu',
  951356: '⚽ Güz Sezonu',
  955706: '⚽ Hazırlık Maçları',
  955997: '⚽ Özel Turnuva',
  956080: '⚽ Lig Kupası Eleme',
  956085: '⚽ Federasyon Kupası Eleme',
  956109: '⚽ Süper Kupa Eleme',
  957031: '⚽ Bölge Ligi',
  957972: '⚽ Şehir Ligi',
  943876: '🏆 Kupa Grup A',
  943877: '🏆 Kupa Grup B',
  943878: '🏆 Kupa Grup C',
  943879: '🏆 Kupa Grup D',
  943880: '🏆 Kupa Grup E',
  943881: '🏆 Kupa Grup F',
  943882: '🏆 Kupa Grup G',
  943883: '🏆 Kupa Grup H',
  943884: '🏆 Kupa Çeyrek Final',
  943885: '🏆 Kupa Yarı Final',
  943886: '🏆 Kupa Final',
  943887: '🏆 Kupa 3.Lük Maçı',
  944340: '⚽ Özel Lig',
  1000001064: '⚽ Alt Lig X',
  1000001204: '⚽ Bölge Ligi A',
  1000001205: '⚽ Bölge Ligi B',
  1000001207: '⚽ Bölge Ligi C',
  1000001208: '⚽ Bölge Ligi D',
  1000001235: '⚽ Alt Kategoriler',
  1000001249: '⚽ Genç Kategoriler',
  1000001403: '⚽ Yerel Lig A',
  1000001407: '⚽ Yerel Lig B',
  1000001415: '⚽ Yerel Lig C',
  1000001425: '⚽ Yerel Lig D',
  1000001461: '⚽ Alt Bölge Ligi',
  1000001465: '⚽ İl Ligi',
  1000001473: '⚽ Amatör Kategori',
  1000001474: '⚽ Karma Lig',
  1000001483: '⚽ Özel Kategori',
  1000001491: '⚽ Turnuva Kategorisi',
  1000001497: '⚽ Sezonluk Lig',
  1000001499: '⚽ Yıllık Turnuva',
  1000001513: '⚽ Özel Organizasyon',
  1000001595: '⚽ Alt Yapı Ligi',
  1000001643: '⚽ Genç Takımlar',
  1000001644: '⚽ B Takımları',
  1000001681: '⚽ Rezerv Kategorisi',
  1000001696: '⚽ Yan Lig',
  1000001703: '⚽ Paralel Lig',
  1000001709: '⚽ Alternatif Lig',
  1000001771: '⚽ Ek Turnuva',
  1000001825: '⚽ Sezon Ortası Kupası',
  1000001831: '⚽ Kış Kupası',
  1000001844: '⚽ Yaz Turnuvası',
};

export function getLeagueName(leagueId: number, apiLeagueName?: string): string {
  // Önce API'den gelen lig adını kontrol et (Mackolik lig kodu)
  if (apiLeagueName && apiLeagueName.length >= 2 && apiLeagueName.length <= 10) {
    // Kısa kod (PRD, COC, J-C vs.) - direkt kullan
    return apiLeagueName;
  }
  
  // Uzun lig adı varsa
  if (apiLeagueName && apiLeagueName !== 'Unknown' && apiLeagueName !== 'undefined' && !apiLeagueName.includes('undefined')) {
    const cleaned = apiLeagueName
      .replace(/^[^a-zA-ZÀ-ž0-9]+/, '')
      .replace(/\s+/g, ' ')
      .trim();
    
    if (cleaned.length > 3) {
      return `⚽ ${cleaned}`;
    }
  }
  
  // Mapping'e bak
  if (LEAGUE_NAMES[leagueId]) {
    return LEAGUE_NAMES[leagueId];
  }
  
  // Son çare
  if (leagueId >= 1000000000) {
    return `⚽ Özel Turnuva ${leagueId}`;
  } else if (leagueId >= 900000) {
    return `⚽ Bölgesel Lig ${leagueId}`;
  } else if (leagueId >= 500000) {
    return `⚽ Alt Kategori ${leagueId}`;
  } else {
    return `⚽ Lig ${leagueId}`;
  }
}
