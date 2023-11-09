SELECT
    day,
    --finalizeAggregation(u) AS uniqByDay,
    uniqMerge(u) OVER (ORDER BY day ASC RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS wau
FROM
(
    SELECT
        toDate(timestamp) AS day,
        uniqState(user_id) AS u
    FROM default.churn_submits
    GROUP BY day
)


WAU (weekly active users) – количество активных пользователей в неделю.

Вам предоставлен доступ к таблице default.churn_submits. В ней находятся данные по активности пользователей нашего Симулятора. Одна строка = одна попытка решения каким-то студентом какой-то задачи. 

churn_submits состоит из колонок: 

    submit_id – id события-попытки
    timestamp – время попытки
    user_id  – id пользователя
    task_id  – id задания
    submit – номер попытки
    score – балл за задание
    is_solved – решил/не решил

Задание

1. Напишите запрос с расчётом WAU за весь период скользящим окном в неделю с шагом в 1 день, при этом текущая дата должна включаться в расчет.
Например, для даты 07.09.2022 нужно рассчитать WAU за период с 01.09.2022 по 07.09.2022.

2. Название столбцов должно быть day и wau. Столбы должны идти именно в таком порядке.

3. Сохраните SQL-запрос в файл query.sql и загрузить его в форму ниже.

(также попробуйте вывести дашборд в Redash с полученной динамикой wau)
