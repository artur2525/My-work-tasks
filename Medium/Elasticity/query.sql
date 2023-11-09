Select dates, price, count(user) as qty, sku 
from transactions
group by sku, dates, price