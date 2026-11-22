"""
Mackolik match ID'lerin parse edilip edilmediğini kontrol et
"""

from mackolik_api import fetch_mackolik_matches

print("="*80)
print("MACKOLIK MATCH ID PARSE TEST")
print("="*80)

success, matches, error = fetch_mackolik_matches(days_ahead=1)

if success and matches:
    print(f"\n✅ {len(matches)} maç çekildi")
    
    # Match ID'li maçları say
    with_id = [m for m in matches if m.get('mackolik_match_id')]
    without_id = [m for m in matches if not m.get('mackolik_match_id')]
    
    print(f"\n📊 İSTATİSTİK:")
    print(f"   Match ID var: {len(with_id)}")
    print(f"   Match ID yok: {len(without_id)}")
    
    if len(with_id) > 0:
        print(f"\n✅ BAŞARILI! İlk 5 maç:")
        for i, match in enumerate(with_id[:5], 1):
            mackolik_id = match['mackolik_match_id']
            print(f"\n{i}. {match['home_team']} vs {match['away_team']}")
            print(f"   Lig: {match['league']}")
            print(f"   Mackolik ID: {mackolik_id}")
            print(f"   H2H Link: https://arsiv.mackolik.com/Match/Head2Head.aspx?id={mackolik_id}&s=1")
    else:
        print(f"\n❌ BAŞARISIZ! Hiçbir maçta Match ID yok")
        print(f"\n💡 NEDEN?")
        print(f"   • HTML yapısı değişmiş olabilir")
        print(f"   • /mac/MATCHID/ formatı kullanılmıyor olabilir")
        print(f"   • Regex pattern yanlış")
        
        print(f"\n🔍 İlk maçın detayını göster:")
        if matches:
            first = matches[0]
            print(f"   Keys: {list(first.keys())}")
            for key, value in first.items():
                print(f"   {key}: {value}")
    
    if len(without_id) > 0:
        print(f"\n⚠️ ID olmayan ilk 3 maç:")
        for i, match in enumerate(without_id[:3], 1):
            print(f"   {i}. {match['home_team']} vs {match['away_team']} ({match['league']})")
else:
    print(f"\n❌ Maç çekilemedi: {error}")

print("\n" + "="*80)
