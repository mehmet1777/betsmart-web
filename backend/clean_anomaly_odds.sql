-- Clean up anomaly records from odds_changes table
-- Realistic filtering: Each odd can change max ±50%
-- Check each odd separately, not the total

DELETE FROM odds_changes
WHERE 
  -- Individual percentage changes (max ±50% per odd)
  (change_1 > 50 OR change_1 < -50) OR
  (change_x > 50 OR change_x < -50) OR
  (change_2 > 50 OR change_2 < -50) OR
  
  -- Placeholder odds (like 17.10, 25.50)
  old_odd_1 > 15 OR old_odd_x > 15 OR old_odd_2 > 15 OR
  new_odd_1 > 15 OR new_odd_x > 15 OR new_odd_2 > 15 OR
  
  -- Error/zero odds
  old_odd_1 < 1.01 OR old_odd_x < 1.01 OR old_odd_2 < 1.01 OR
  new_odd_1 < 1.01 OR new_odd_x < 1.01 OR new_odd_2 < 1.01;
