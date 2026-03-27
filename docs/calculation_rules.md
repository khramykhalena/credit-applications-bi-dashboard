# Calculation Rules

## 1. age_years
- Source fields: `DAYS_BIRTH`
- Formula: `-DAYS_BIRTH / 365`
- Missing logic: если `DAYS_BIRTH` пустой, результат `NaN`
- Interpretation: возраст клиента в годах

## 2. employment_years
- Source fields: `DAYS_EMPLOYED`
- Formula: `-DAYS_EMPLOYED / 365`
- Missing logic: если `DAYS_EMPLOYED = 365243`, заменить на `NaN`
- Interpretation: стаж клиента в годах без технической заглушки

## 3. days_employed_anom_flag
- Source fields: `DAYS_EMPLOYED`
- Formula: `1`, если `DAYS_EMPLOYED = 365243`, иначе `0`
- Interpretation: отдельный флаг технической аномалии стажа

## 4. credit_income_ratio
- Source fields: `AMT_CREDIT`, `AMT_INCOME_TOTAL`
- Formula: `AMT_CREDIT / AMT_INCOME_TOTAL`
- Division by zero: если доход `<= 0`, результат `NaN`
- Interpretation: долговая нагрузка относительно дохода

## 5. annuity_income_ratio
- Source fields: `AMT_ANNUITY`, `AMT_INCOME_TOTAL`
- Formula: `AMT_ANNUITY / AMT_INCOME_TOTAL`
- Division by zero: если доход `<= 0`, результат `NaN`
- Interpretation: размер платежа относительно дохода

## 6. credit_goods_ratio
- Source fields: `AMT_CREDIT`, `AMT_GOODS_PRICE`
- Formula: `AMT_CREDIT / AMT_GOODS_PRICE`
- Division by zero: если стоимость товара `<= 0`, результат `NaN`
- Interpretation: насколько сумма кредита соотносится со стоимостью объекта

## 7. employment_age_ratio
- Source fields: `employment_years`, `age_years`
- Formula: `employment_years / age_years`
- Division by zero: если `age_years <= 0`, результат `NaN`
- Interpretation: доля трудового стажа в возрасте клиента

## 8. bureau_records_count
- Source fields: `bureau.SK_ID_BUREAU`
- Formula: `count(SK_ID_BUREAU) by SK_ID_CURR`
- Interpretation: число записей внешней кредитной истории

## 9. bureau_active_credit_count
- Source fields: `bureau.CREDIT_ACTIVE`
- Formula: `count(CREDIT_ACTIVE == "Active") by SK_ID_CURR`
- Interpretation: число активных внешних кредитов

## 10. bureau_closed_credit_count
- Source fields: `bureau.CREDIT_ACTIVE`
- Formula: `count(CREDIT_ACTIVE == "Closed") by SK_ID_CURR`
- Interpretation: число закрытых внешних кредитов

## 11. bureau_overdue_credit_count
- Source fields: `bureau.CREDIT_DAY_OVERDUE`
- Formula: `count(CREDIT_DAY_OVERDUE > 0) by SK_ID_CURR`
- Interpretation: число кредитов с зафиксированной просрочкой

## 12. bureau_total_credit_sum
- Source fields: `bureau.AMT_CREDIT_SUM`
- Formula: `sum(AMT_CREDIT_SUM) by SK_ID_CURR`
- Interpretation: суммарный объём внешних кредитов

## 13. bureau_total_credit_debt_sum
- Source fields: `bureau.AMT_CREDIT_SUM_DEBT`
- Formula: `sum(AMT_CREDIT_SUM_DEBT) by SK_ID_CURR`
- Missing logic: пропуски игнорируются стандартным суммированием pandas
- Interpretation: суммарный внешний долг

## 14. bureau_debt_to_credit_ratio
- Source fields: `bureau_total_credit_debt_sum`, `bureau_total_credit_sum`
- Formula: `bureau_total_credit_debt_sum / bureau_total_credit_sum`
- Division by zero: если сумма кредитов `<= 0`, результат `NaN`
- Interpretation: отношение внешнего долга к сумме внешних кредитов

## 15. prev_app_count
- Source fields: `previous_application.SK_ID_PREV`
- Formula: `count(SK_ID_PREV) by SK_ID_CURR`
- Interpretation: число прошлых заявок клиента

## 16. prev_approved_count
- Source fields: `previous_application.NAME_CONTRACT_STATUS`
- Formula: `count(NAME_CONTRACT_STATUS == "Approved") by SK_ID_CURR`
- Interpretation: число прошлых одобрений

## 17. prev_refused_count
- Source fields: `previous_application.NAME_CONTRACT_STATUS`
- Formula: `count(NAME_CONTRACT_STATUS == "Refused") by SK_ID_CURR`
- Interpretation: число прошлых отказов

## 18. prev_amt_application_sum
- Source fields: `previous_application.AMT_APPLICATION`
- Formula: `sum(AMT_APPLICATION) by SK_ID_CURR`
- Interpretation: суммарный объём прошлых заявок

## 19. prev_amt_credit_sum
- Source fields: `previous_application.AMT_CREDIT`
- Formula: `sum(AMT_CREDIT) by SK_ID_CURR`
- Interpretation: суммарный объём прошлых кредитов

## 20. prev_days_decision_mean
- Source fields: `previous_application.DAYS_DECISION`
- Formula: `mean(DAYS_DECISION) by SK_ID_CURR`
- Interpretation: средняя глубина истории прошлых решений

## 21. prev_approval_rate
- Source fields: `prev_approved_count`, `prev_app_count`
- Formula: `prev_approved_count / prev_app_count`
- Division by zero: если `prev_app_count = 0`, результат `NaN`
- Interpretation: доля прошлых заявок со статусом `Approved`
