select cal_date AS days, SUM(cnt) AS sku
FROM transactions_another_one
GROUP by cal_date
