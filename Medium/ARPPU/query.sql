select  avg(amount) as aov , (sum(amount) / count(DISTINCT email_id)) as arppu,  DATE_TRUNC('month', date)::DATE as time
from new_payments
where status = 'Confirmed' or status =  'confirmed'
group by time
order by time

