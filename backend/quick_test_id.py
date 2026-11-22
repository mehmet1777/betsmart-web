from mackolik_api import fetch_mackolik_matches

success, matches, error = fetch_mackolik_matches(days_ahead=1)

if success:
    with_id = [m for m in matches if m.get('mackolik_match_id')]
    print(f"Total matches: {len(matches)}")
    print(f"With Mackolik ID: {len(with_id)}")
    
    if with_id:
        print("\nFirst 3 matches with ID:")
        for m in with_id[:3]:
            mid = m.get('mackolik_match_id')
            print(f"{m['home_team']} vs {m['away_team']} | ID: {mid}")
            print(f"  H2H: https://arsiv.mackolik.com/Match/Head2Head.aspx?id={mid}&s=1")
    else:
        print("\nNO IDs FOUND! First match keys:")
        if matches:
            print(list(matches[0].keys()))
