"""
BetSmart Web API - Flask Backend
Oran analizi için endpoint sağlar
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
import traceback

app = Flask(__name__)
CORS(app)  # Cross-origin requests için (Next.js'den gelen istekler)

db = Database()

@app.route('/api/analyze-odds', methods=['POST'])
def analyze_odds():
    """
    Oran analizi endpoint'i
    
    Request Body:
    {
        "odd_1": 2.65,
        "odd_x": 2.80,
        "odd_2": 2.00,
        "home_team": "Ukebo",  # Optional
        "away_team": "Sabadell"  # Optional
    }
    
    Response:
    {
        "success": true,
        "total_count": 50,
        "exact": [...],
        "similar": [...],
        "statistics": {
            "home_wins": 15,
            "draws": 10,
            "away_wins": 25,
            "gg_yes": 30,
            "gg_no": 20,
            "total_valid": 50
        },
        "recommendation": {
            "type": "MS2",
            "odds": 2.00,
            "confidence": "Yüksek",
            "reason": "Benzer oranlı 50 maçta deplasman 25 kez kazandı (%50)"
        }
    }
    """
    try:
        data = request.get_json()
        
        # Parametreleri al
        odd_1 = float(data.get('odd_1', 0))
        odd_x = float(data.get('odd_x', 0))
        odd_2 = float(data.get('odd_2', 0))
        home_team = data.get('home_team', '')
        away_team = data.get('away_team', '')
        
        # Validasyon
        if odd_1 <= 0 or odd_x <= 0 or odd_2 <= 0:
            return jsonify({
                'success': False,
                'error': 'Geçersiz oran değerleri'
            }), 400
        
        print(f"📊 Analiz başlatıldı: {odd_1} / {odd_x} / {odd_2}")
        
        # Veritabanında benzer oranları ara
        results = db.search_by_odds_range(
            home_team=home_team,
            away_team=away_team,
            odd_1=odd_1,
            odd_x=odd_x,
            odd_2=odd_2,
            limit=100  # Max 100 maç
        )
        
        # İstatistikleri hesapla
        all_matches = results['exact'] + results['similar']
        statistics = calculate_statistics(all_matches)
        
        # Öneri oluştur
        recommendation = generate_recommendation(
            odd_1, odd_x, odd_2,
            statistics,
            results['total_count']
        )
        
        print(f"✅ Analiz tamamlandı: {results['total_count']} maç bulundu")
        
        return jsonify({
            'success': True,
            'total_count': results['total_count'],
            'exact': results['exact'][:20],  # İlk 20 göster
            'similar': results['similar'][:20],  # İlk 20 göster
            'statistics': statistics,
            'recommendation': recommendation
        })
        
    except Exception as e:
        print(f"❌ Analiz hatası: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def calculate_statistics(matches):
    """Maç istatistiklerini hesapla"""
    stats = {
        'home_wins': 0,
        'draws': 0,
        'away_wins': 0,
        'gg_yes': 0,
        'gg_no': 0,
        'total_valid': 0
    }
    
    for match in matches:
        score = match.get('score', '').strip()
        if score and '-' in score:
            try:
                parts = score.split('-')
                if len(parts) == 2:
                    home_score = int(parts[0].strip())
                    away_score = int(parts[1].strip())
                    
                    stats['total_valid'] += 1
                    
                    # Maç sonucu
                    if home_score > away_score:
                        stats['home_wins'] += 1
                    elif home_score == away_score:
                        stats['draws'] += 1
                    else:
                        stats['away_wins'] += 1
                    
                    # Karşılıklı gol
                    if home_score > 0 and away_score > 0:
                        stats['gg_yes'] += 1
                    else:
                        stats['gg_no'] += 1
            except:
                continue
    
    return stats


def generate_recommendation(odd_1, odd_x, odd_2, stats, total_count):
    """İstatistiklere göre öneri oluştur"""
    
    if total_count == 0 or stats['total_valid'] == 0:
        return {
            'type': None,
            'odds': None,
            'confidence': 'Yok',
            'reason': 'Benzer oranlı maç bulunamadı. Farklı bir maç deneyin.'
        }
    
    total_valid = stats['total_valid']
    home_wins = stats['home_wins']
    draws = stats['draws']
    away_wins = stats['away_wins']
    
    # En çok olan sonucu bul
    results = {
        'MS1': (home_wins, odd_1),
        'MSX': (draws, odd_x),
        'MS2': (away_wins, odd_2)
    }
    
    best_result = max(results.items(), key=lambda x: x[1][0])
    result_type = best_result[0]
    result_count = best_result[1][0]
    result_odds = best_result[1][1]
    
    # Yüzde hesapla
    percentage = (result_count / total_valid) * 100
    
    # Güven seviyesi
    if percentage >= 60:
        confidence = 'Çok Yüksek'
    elif percentage >= 50:
        confidence = 'Yüksek'
    elif percentage >= 40:
        confidence = 'Orta'
    else:
        confidence = 'Düşük'
    
    # Açıklama
    result_names = {
        'MS1': 'Ev sahibi',
        'MSX': 'Beraberlik',
        'MS2': 'Deplasman'
    }
    
    reason = f"Benzer oranlı {total_valid} maçta {result_names[result_type].lower()} {result_count} kez gerçekleşti (%{percentage:.0f})"
    
    return {
        'type': result_type,
        'odds': result_odds,
        'confidence': confidence,
        'reason': reason,
        'percentage': round(percentage, 1)
    }


@app.route('/api/smart-coupon', methods=['POST'])
def smart_coupon():
    """
    Akıllı kupon önerisi - Tüm maçları analiz eder
    
    Request Body:
    {
        "matches": [
            {
                "id": 1,
                "home_team": "Barcelona",
                "away_team": "Real Madrid",
                "odd_1": 2.10,
                "odd_x": 3.20,
                "odd_2": 3.50
            },
            ...
        ]
    }
    
    Response:
    {
        "success": true,
        "analyzed_count": 87,
        "recommended_count": 3,
        "recommendations": [
            {
                "match": {...},
                "exact_matches": 45,
                "win_rate": 78.5,
                "recommendation": "MS1",
                "confidence": "Çok Yüksek"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        matches = data.get('matches', [])
        
        if not matches:
            return jsonify({
                'success': False,
                'error': 'Maç listesi boş'
            }), 400
        
        print(f"🤖 Akıllı kupon analizi başlatıldı: {len(matches)} maç")
        
        recommendations = []
        analyzed_count = 0
        
        for match in matches:
            try:
                odd_1 = float(match.get('odd_1', 0))
                odd_x = float(match.get('odd_x', 0))
                odd_2 = float(match.get('odd_2', 0))
                
                # Geçersiz oranları atla
                if odd_1 <= 0 or odd_x <= 0 or odd_2 <= 0:
                    continue
                
                analyzed_count += 1
                
                # Sadece ±0.01 toleransta ara (Exact Match)
                results = db.search_by_odds_range(
                    home_team=match.get('home_team', ''),
                    away_team=match.get('away_team', ''),
                    odd_1=odd_1,
                    odd_x=odd_x,
                    odd_2=odd_2,
                    limit=100
                )
                
                exact_matches = results['exact']
                
                # Sadece exact match varsa devam et
                if len(exact_matches) == 0:
                    continue
                
                # İstatistikleri hesapla
                stats = calculate_statistics(exact_matches)
                
                if stats['total_valid'] == 0:
                    continue
                
                # En iyi sonucu bul
                total_valid = stats['total_valid']
                home_wins = stats['home_wins']
                draws = stats['draws']
                away_wins = stats['away_wins']
                
                results_data = {
                    'MS1': (home_wins, odd_1),
                    'MSX': (draws, odd_x),
                    'MS2': (away_wins, odd_2)
                }
                
                best_result = max(results_data.items(), key=lambda x: x[1][0])
                result_type = best_result[0]
                result_count = best_result[1][0]
                result_odds = best_result[1][1]
                
                # Kazanma oranı hesapla
                win_rate = (result_count / total_valid) * 100
                
                # %75+ olanları öner
                if win_rate >= 75:
                    recommendations.append({
                        'match': match,
                        'exact_matches': len(exact_matches),
                        'total_analyzed': total_valid,
                        'win_rate': round(win_rate, 1),
                        'recommendation': result_type,
                        'recommended_odds': result_odds,
                        'statistics': {
                            'home_wins': home_wins,
                            'draws': draws,
                            'away_wins': away_wins,
                            'gg_yes': stats['gg_yes'],
                            'gg_no': stats['gg_no']
                        }
                    })
                    
                    print(f"✅ Öneri bulundu: {match.get('home_team')} vs {match.get('away_team')} - {result_type} (%{win_rate:.1f})")
            
            except Exception as e:
                print(f"⚠️ Maç analiz hatası: {e}")
                continue
        
        # Kazanma oranına göre sırala (en yüksek önce)
        recommendations.sort(key=lambda x: x['win_rate'], reverse=True)
        
        print(f"🎯 Analiz tamamlandı: {analyzed_count} maç analiz edildi, {len(recommendations)} öneri bulundu")
        
        return jsonify({
            'success': True,
            'analyzed_count': analyzed_count,
            'recommended_count': len(recommendations),
            'recommendations': recommendations
        })
        
    except Exception as e:
        print(f"❌ Akıllı kupon hatası: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Sağlık kontrolü"""
    return jsonify({
        'status': 'ok',
        'service': 'BetSmart API',
        'version': '1.0.0'
    })


@app.route('/api/odds-changes', methods=['POST'])
def get_odds_changes():
    """
    Belirli bir maç için oran değişiklik geçmişini getir
    
    Request Body:
    {
        "home_team": "Fenerbahce",
        "away_team": "Galatasaray",
        "match_datetime": "2024-11-21 19:00"  # Optional
    }
    
    Response:
    {
        "success": true,
        "changes": [
            {
                "detected_at": "2024-11-21 10:15",
                "old_odd_1": 2.00,
                "new_odd_1": 2.10,
                "change_1": 5.0,
                "old_odd_x": 3.50,
                "new_odd_x": 3.45,
                "change_x": -1.4,
                "old_odd_2": 3.20,
                "new_odd_2": 3.25,
                "change_2": 1.6,
                "total_change": 8.0
            }
        ]
    }
    """
    try:
        from supabase_sync import get_supabase_client
        
        data = request.get_json()
        home_team = data.get('home_team', '')
        away_team = data.get('away_team', '')
        match_datetime = data.get('match_datetime', '')
        
        if not home_team or not away_team:
            return jsonify({
                'success': False,
                'error': 'home_team ve away_team gerekli'
            }), 400
        
        print(f"📊 Oran değişiklikleri sorgulanıyor: {home_team} vs {away_team}")
        
        client = get_supabase_client()
        
        # Supabase'den oran değişikliklerini çek
        query = client.table('odds_changes').select('*').eq('home_team', home_team).eq('away_team', away_team)
        
        if match_datetime:
            query = query.eq('match_datetime', match_datetime)
        
        result = query.order('detected_at', desc=True).execute()
        
        changes = result.data if result.data else []
        
        print(f"✅ {len(changes)} değişiklik bulundu")
        
        return jsonify({
            'success': True,
            'changes': changes
        })
        
    except Exception as e:
        print(f"❌ Oran değişiklikleri hatası: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 BetSmart API başlatılıyor...")
    print("📊 Endpoint: http://localhost:5000/api/analyze-odds")
    print("🏥 Health: http://localhost:5000/health")
    app.run(host='0.0.0.0', port=5000, debug=True)
