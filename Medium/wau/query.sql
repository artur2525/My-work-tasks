select count(user_id)
from default.churn_submits
group by toYearWeek(timestamp)
