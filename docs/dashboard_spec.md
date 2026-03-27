# Dashboard Spec

Ниже — готовая структура дашборда для Power BI. Минимум 3 страницы.

## Page 1. Overview
### Цель
Дать быстрый обзор объёма заявок, уровня риска и ключевых финансовых метрик.

### Карточки
- `Applications Count` = `COUNT(SK_ID_CURR)`
- `Default Rate` = `AVERAGE(TARGET)`
- `Avg Income` = `AVERAGE(AMT_INCOME_TOTAL)`
- `Avg Credit` = `AVERAGE(AMT_CREDIT)`
- `Avg Annuity` = `AVERAGE(AMT_ANNUITY)`
- `Avg Bureau Records` = `AVERAGE(bureau_records_count)`
- `Avg Previous Applications` = `AVERAGE(prev_app_count)`

### Графики
- столбчатая диаграмма: число заявок по `TARGET`
- гистограмма: распределение `AMT_INCOME_TOTAL`
- гистограмма: распределение `AMT_CREDIT`
- столбчатая диаграмма: `Default Rate` по `NAME_INCOME_TYPE`
- столбчатая диаграмма: `Default Rate` по `CODE_GENDER`

## Page 2. Client Profile & Risk
### Цель
Показать, как риск связан с профилем клиента, финансовой нагрузкой и внешними признаками.

### Визуалы
- bar chart: `Default Rate` по `NAME_EDUCATION_TYPE`
- bar chart: `Default Rate` по `NAME_FAMILY_STATUS`
- bar chart: `Default Rate` по `NAME_HOUSING_TYPE`
- histogram: `age_years`
- histogram: `employment_years`
- scatter / binned chart: `credit_income_ratio` vs `TARGET`
- scatter / binned chart: `annuity_income_ratio` vs `TARGET`
- scatter / binned chart: `EXT_SOURCE_1` vs `TARGET`
- scatter / binned chart: `EXT_SOURCE_2` vs `TARGET`
- scatter / binned chart: `EXT_SOURCE_3` vs `TARGET`
- scatter / binned chart: `bureau_records_count` vs `TARGET`
- scatter / binned chart: `prev_app_count` vs `TARGET`
- scatter / binned chart: `prev_approval_rate` vs `TARGET`

### Срезы
- `CODE_GENDER`
- `NAME_INCOME_TYPE`
- `NAME_EDUCATION_TYPE`
- `NAME_FAMILY_STATUS`

## Page 3. Data Quality
### Цель
Показать ограничения данных, которые влияют на интерпретацию аналитики.

### Карточки
- число записей с `days_employed_anom_flag = 1`
- доля строк с пустым `EXT_SOURCE_1`
- доля строк с пустым `EXT_SOURCE_3`
- среднее число записей `bureau` на клиента
- среднее число прошлых заявок на клиента

### Таблица пропусков
Рекомендуемые поля:
- `AMT_ANNUITY`
- `AMT_GOODS_PRICE`
- `EXT_SOURCE_1`
- `EXT_SOURCE_2`
- `EXT_SOURCE_3`
- `employment_years`
- `bureau_total_credit_debt_sum`
- `prev_days_decision_mean`

### Поясняющий блок текстом
- `DAYS_EMPLOYED = 365243` — техническая заглушка
- `bureau` и `previous_application` — связи `1:N`
- прямой join без агрегации приводит к дублированию строк
- часть полей не включена в основной слой из-за высокой доли пропусков

## Полезные меры Power BI
### 1. Applications Count
```DAX
Applications Count = COUNT('datamart_sample'[SK_ID_CURR])
```

### 2. Default Rate
```DAX
Default Rate = AVERAGE('datamart_sample'[TARGET])
```

### 3. Avg Income
```DAX
Avg Income = AVERAGE('datamart_sample'[AMT_INCOME_TOTAL])
```

### 4. Avg Credit
```DAX
Avg Credit = AVERAGE('datamart_sample'[AMT_CREDIT])
```

### 5. Avg Annuity
```DAX
Avg Annuity = AVERAGE('datamart_sample'[AMT_ANNUITY])
```

### 6. Avg Bureau Records
```DAX
Avg Bureau Records = AVERAGE('datamart_sample'[bureau_records_count])
```

### 7. Avg Previous Applications
```DAX
Avg Previous Applications = AVERAGE('datamart_sample'[prev_app_count])
```

### 8. Employment Anomaly Count
```DAX
Employment Anomaly Count = SUM('datamart_sample'[days_employed_anom_flag])
```

### 9. Missing EXT_SOURCE_1 Rate
```DAX
Missing EXT_SOURCE_1 Rate =
DIVIDE(
    COUNTROWS(
        FILTER('datamart_sample', ISBLANK('datamart_sample'[EXT_SOURCE_1]))
    ),
    COUNTROWS('datamart_sample')
)
```
