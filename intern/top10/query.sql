select vendor, count(sku_type) as sku
from sku_dict_another_one
group by vendor
order by sku desc
limit 10


--select vendor, count(DISTINCT brand) as brand
--from sku_dict_another_one
--group by vendor
--order by brand desc
--limit 10


--select sku_type, count(DISTINCT vendor) as count_vendor
--from sku_dict_another_one
--group by sku_type
--order by count_vendor desc
--limit 10


--select brend, count(sku_type) as count_sku_type
--group by brend
--having brend != 0
--order by count_sku desc
--limit 10

