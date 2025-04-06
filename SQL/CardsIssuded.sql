SELECT 
card_name, 
max(issued_amount) - min(issued_amount) as difference
FROM monthly_cards_issued
GROUP BY 
card_name
ORDER BY 
max(issued_amount) - min(issued_amount) DESC
;