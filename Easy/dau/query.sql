select toDate(timestamp) as day, uniq(user_id) as dau
from default.churn_submits
group by day
