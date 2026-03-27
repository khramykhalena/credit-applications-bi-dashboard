# Data Dictionary

Ниже описаны ключевые поля финальной витрины. Уровень витрины — `1 строка = 1 текущая заявка`.

| Field | Source | Type | Meaning | Level | Missing / Notes |
|---|---|---|---|---|---|
| SK_ID_CURR | application_train | int | Идентификатор клиента / текущей заявки | текущая заявка | ключ витрины |
| TARGET | application_train | int | Флаг проблем с выплатой кредита | текущая заявка | 0 = нет, 1 = были трудности |
| NAME_CONTRACT_TYPE | application_train | category | Тип кредитного продукта | текущая заявка | категориальное поле |
| CODE_GENDER | application_train | category | Пол клиента | текущая заявка | категориальное поле |
| FLAG_OWN_CAR | application_train | category | Наличие автомобиля | текущая заявка | Y/N |
| FLAG_OWN_REALTY | application_train | category | Наличие недвижимости | текущая заявка | Y/N |
| CNT_CHILDREN | application_train | int | Количество детей | текущая заявка | возможны редкие выбросы |
| CNT_FAM_MEMBERS | application_train | float | Размер семьи | текущая заявка | возможны пропуски |
| AMT_INCOME_TOTAL | application_train | float | Общий доход клиента | текущая заявка | возможны выбросы |
| AMT_CREDIT | application_train | float | Сумма кредита | текущая заявка | ключевой финансовый показатель |
| AMT_ANNUITY | application_train | float | Размер аннуитетного платежа | текущая заявка | есть пропуски |
| AMT_GOODS_PRICE | application_train | float | Стоимость товара / объекта | текущая заявка | есть пропуски |
| EXT_SOURCE_1 | application_train | float | Внешний скоринговый признак 1 | текущая заявка | есть пропуски |
| EXT_SOURCE_2 | application_train | float | Внешний скоринговый признак 2 | текущая заявка | используется в анализе риска |
| EXT_SOURCE_3 | application_train | float | Внешний скоринговый признак 3 | текущая заявка | есть пропуски |
| DAYS_BIRTH | application_train | int | Возраст в днях с отрицательным знаком | текущая заявка | техническое поле-источник |
| DAYS_EMPLOYED | application_train | int | Стаж в днях с отрицательным знаком | текущая заявка | значение 365243 — техническая аномалия |
| age_years | derived from DAYS_BIRTH | float | Возраст клиента в годах | текущая заявка | `-DAYS_BIRTH / 365` |
| employment_years | derived from DAYS_EMPLOYED | float | Стаж клиента в годах | текущая заявка | для 365243 ставится `NaN` |
| days_employed_anom_flag | derived from DAYS_EMPLOYED | int | Флаг технической аномалии стажа | текущая заявка | 1 = `DAYS_EMPLOYED = 365243` |
| credit_income_ratio | derived | float | Отношение кредита к доходу | текущая заявка | защита от деления на ноль |
| annuity_income_ratio | derived | float | Отношение аннуитета к доходу | текущая заявка | защита от деления на ноль |
| credit_goods_ratio | derived | float | Отношение кредита к стоимости товара | текущая заявка | защита от деления на ноль |
| employment_age_ratio | derived | float | Отношение стажа к возрасту | текущая заявка | интерпретировать осторожно |
| bureau_records_count | bureau | int | Число записей внешней кредитной истории | агрегат по клиенту | строится после groupby |
| bureau_active_credit_count | bureau | int | Число активных внешних кредитов | агрегат по клиенту | `CREDIT_ACTIVE = Active` |
| bureau_closed_credit_count | bureau | int | Число закрытых внешних кредитов | агрегат по клиенту | `CREDIT_ACTIVE = Closed` |
| bureau_bad_debt_credit_count | bureau | int | Число кредитов со статусом bad debt | агрегат по клиенту | категориальный агрегат |
| bureau_sold_credit_count | bureau | int | Число проданных долгов | агрегат по клиенту | категориальный агрегат |
| bureau_overdue_credit_count | bureau | int | Число кредитов с просрочкой | агрегат по клиенту | по `CREDIT_DAY_OVERDUE > 0` |
| bureau_total_credit_sum | bureau | float | Сумма внешних кредитов | агрегат по клиенту | `sum(AMT_CREDIT_SUM)` |
| bureau_total_credit_debt_sum | bureau | float | Сумма внешнего долга | агрегат по клиенту | `sum(AMT_CREDIT_SUM_DEBT)` |
| bureau_total_credit_overdue_sum | bureau | float | Суммарная просроченная сумма | агрегат по клиенту | `sum(AMT_CREDIT_SUM_OVERDUE)` |
| bureau_total_credit_limit_sum | bureau | float | Суммарный доступный лимит | агрегат по клиенту | есть пропуски в источнике |
| bureau_total_annuity_sum | bureau | float | Суммарный аннуитет по внешним кредитам | агрегат по клиенту | высокая доля пропусков в источнике |
| bureau_debt_to_credit_ratio | bureau | float | Отношение внешнего долга к сумме внешних кредитов | агрегат по клиенту | осторожная интерпретация |
| prev_app_count | previous_application | int | Число прошлых заявок клиента | агрегат по клиенту | `count(SK_ID_PREV)` |
| prev_approved_count | previous_application | int | Число прошлых одобрений | агрегат по клиенту | статус `Approved` |
| prev_refused_count | previous_application | int | Число прошлых отказов | агрегат по клиенту | статус `Refused` |
| prev_amt_application_sum | previous_application | float | Сумма прошлых заявок | агрегат по клиенту | `sum(AMT_APPLICATION)` |
| prev_amt_credit_sum | previous_application | float | Сумма прошлых кредитов | агрегат по клиенту | `sum(AMT_CREDIT)` |
| prev_amt_annuity_sum | previous_application | float | Сумма аннуитетов по прошлым заявкам | агрегат по клиенту | в источнике есть пропуски |
| prev_hour_appr_mean | previous_application | float | Средний час оформления прошлых заявок | агрегат по клиенту | `mean(HOUR_APPR_PROCESS_START)` |
| prev_rate_down_payment_mean | previous_application | float | Средняя ставка первоначального взноса | агрегат по клиенту | высокая доля пропусков |
| prev_days_decision_mean | previous_application | float | Средняя глубина истории прошлых решений | агрегат по клиенту | `mean(DAYS_DECISION)` |
| prev_approval_rate | previous_application | float | Доля прошлых одобрений | агрегат по клиенту | `prev_approved_count / prev_app_count` |
