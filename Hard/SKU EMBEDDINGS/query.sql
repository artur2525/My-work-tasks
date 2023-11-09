select * 
from 
(select user_id, item_id,  sum(units) as qty
from default.karpov_express_orders
WHERE toDate(timestamp) >= toDate(%(start_date)s) AND toDate(timestamp) <= toDate(%(end_date)s)
group by item_id, user_id
) as out 

inner JOIN (select item_id, round(avg(price),2) as price
            from default.karpov_express_orders
            WHERE toDate(timestamp) >= toDate(%(start_date)s) AND toDate(timestamp) <= toDate(%(end_date)s)
            group by item_id) as tab
            
using (item_id)
order by user_id, item_id

