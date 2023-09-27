select age, income, dependents, 
        has_property,has_car,credit_score,
        job_tenure,has_education,loan_amount, 
        dateDiff('day', toDateTime( loan_start ), toDateTime(loan_deadline)) as loan_period, 
        if(dateDiff('day', toDateTime(loan_deadline), toDateTime(loan_payed)) < 0,
          0,
          dateDiff('day', toDateTime(loan_deadline), toDateTime(loan_payed))) as delay_days
        
from default.loan_delay_days
order by id
