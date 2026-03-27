from pathlib import Path
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def safe_divide(numerator, denominator):
    return np.where((denominator.notna()) & (denominator != 0), numerator / denominator, np.nan)


def load_data():
    application = pd.read_csv(RAW_DIR / "application_train.csv")
    bureau = pd.read_csv(RAW_DIR / "bureau.csv")
    previous = pd.read_csv(RAW_DIR / "previous_application.csv")
    return application, bureau, previous


def build_application_layer(application: pd.DataFrame) -> pd.DataFrame:
    base_cols = [
        "SK_ID_CURR", "TARGET", "NAME_CONTRACT_TYPE", "CODE_GENDER",
        "FLAG_OWN_CAR", "FLAG_OWN_REALTY", "CNT_CHILDREN", "AMT_INCOME_TOTAL",
        "AMT_CREDIT", "AMT_ANNUITY", "AMT_GOODS_PRICE", "NAME_INCOME_TYPE",
        "NAME_EDUCATION_TYPE", "NAME_FAMILY_STATUS", "NAME_HOUSING_TYPE",
        "REGION_POPULATION_RELATIVE", "DAYS_BIRTH", "DAYS_EMPLOYED",
        "DAYS_REGISTRATION", "DAYS_ID_PUBLISH", "CNT_FAM_MEMBERS",
        "REGION_RATING_CLIENT", "REGION_RATING_CLIENT_W_CITY",
        "WEEKDAY_APPR_PROCESS_START", "HOUR_APPR_PROCESS_START",
        "ORGANIZATION_TYPE", "EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3",
        "DAYS_LAST_PHONE_CHANGE", "AMT_REQ_CREDIT_BUREAU_YEAR"
    ]

    df = application[base_cols].copy()

    df["age_years"] = (-df["DAYS_BIRTH"] / 365).round(1)
    df["days_employed_anom_flag"] = (df["DAYS_EMPLOYED"] == 365243).astype(int)

    df["employment_years"] = np.where(
        df["DAYS_EMPLOYED"] == 365243,
        np.nan,
        -df["DAYS_EMPLOYED"] / 365
    )
    df["employment_years"] = np.round(df["employment_years"], 1)

    df["credit_income_ratio"] = safe_divide(df["AMT_CREDIT"], df["AMT_INCOME_TOTAL"])
    df["annuity_income_ratio"] = safe_divide(df["AMT_ANNUITY"], df["AMT_INCOME_TOTAL"])
    df["credit_goods_ratio"] = safe_divide(df["AMT_CREDIT"], df["AMT_GOODS_PRICE"])
    df["employment_age_ratio"] = safe_divide(df["employment_years"], df["age_years"])

    return df


def build_bureau_agg(bureau: pd.DataFrame) -> pd.DataFrame:
    bureau = bureau.copy()

    bureau["is_active_credit"] = (bureau["CREDIT_ACTIVE"] == "Active").astype(int)
    bureau["is_closed_credit"] = (bureau["CREDIT_ACTIVE"] == "Closed").astype(int)
    bureau["is_bad_debt_credit"] = (bureau["CREDIT_ACTIVE"] == "Bad debt").astype(int)
    bureau["is_sold_credit"] = (bureau["CREDIT_ACTIVE"] == "Sold").astype(int)
    bureau["is_overdue_credit"] = (bureau["CREDIT_DAY_OVERDUE"] > 0).astype(int)

    bureau_agg = bureau.groupby("SK_ID_CURR").agg(
        bureau_records_count=("SK_ID_BUREAU", "count"),
        bureau_active_credit_count=("is_active_credit", "sum"),
        bureau_closed_credit_count=("is_closed_credit", "sum"),
        bureau_bad_debt_credit_count=("is_bad_debt_credit", "sum"),
        bureau_sold_credit_count=("is_sold_credit", "sum"),
        bureau_overdue_credit_count=("is_overdue_credit", "sum"),
        bureau_credit_day_overdue_max=("CREDIT_DAY_OVERDUE", "max"),
        bureau_credit_day_overdue_mean=("CREDIT_DAY_OVERDUE", "mean"),
        bureau_total_credit_sum=("AMT_CREDIT_SUM", "sum"),
        bureau_total_credit_debt_sum=("AMT_CREDIT_SUM_DEBT", "sum"),
        bureau_total_credit_overdue_sum=("AMT_CREDIT_SUM_OVERDUE", "sum"),
        bureau_total_credit_limit_sum=("AMT_CREDIT_SUM_LIMIT", "sum"),
        bureau_total_annuity_sum=("AMT_ANNUITY", "sum"),
        bureau_total_prolong_sum=("CNT_CREDIT_PROLONG", "sum"),
        bureau_total_max_overdue_sum=("AMT_CREDIT_MAX_OVERDUE", "sum"),
        bureau_days_credit_mean=("DAYS_CREDIT", "mean"),
        bureau_days_credit_min=("DAYS_CREDIT", "min"),
        bureau_days_credit_max=("DAYS_CREDIT", "max"),
        bureau_days_credit_update_mean=("DAYS_CREDIT_UPDATE", "mean"),
        bureau_future_enddate_mean=("DAYS_CREDIT_ENDDATE", "mean"),
        bureau_unique_credit_types=("CREDIT_TYPE", "nunique"),
        bureau_unique_currencies=("CREDIT_CURRENCY", "nunique")
    ).reset_index()

    bureau_agg["bureau_debt_to_credit_ratio"] = safe_divide(
        bureau_agg["bureau_total_credit_debt_sum"],
        bureau_agg["bureau_total_credit_sum"]
    )

    return bureau_agg


def build_previous_agg(previous: pd.DataFrame) -> pd.DataFrame:
    previous = previous.copy()

    previous["is_approved"] = (previous["NAME_CONTRACT_STATUS"] == "Approved").astype(int)
    previous["is_refused"] = (previous["NAME_CONTRACT_STATUS"] == "Refused").astype(int)

    prev_agg = previous.groupby("SK_ID_CURR").agg(
        prev_app_count=("SK_ID_PREV", "count"),
        prev_approved_count=("is_approved", "sum"),
        prev_refused_count=("is_refused", "sum"),
        prev_amt_application_sum=("AMT_APPLICATION", "sum"),
        prev_amt_credit_sum=("AMT_CREDIT", "sum"),
        prev_amt_annuity_sum=("AMT_ANNUITY", "sum"),
        prev_hour_appr_mean=("HOUR_APPR_PROCESS_START", "mean"),
        prev_rate_down_payment_mean=("RATE_DOWN_PAYMENT", "mean"),
        prev_days_decision_mean=("DAYS_DECISION", "mean")
    ).reset_index()

    prev_agg["prev_approval_rate"] = safe_divide(
        prev_agg["prev_approved_count"],
        prev_agg["prev_app_count"]
    )

    return prev_agg


def build_datamart():
    application, bureau, previous = load_data()

    app_layer = build_application_layer(application)
    bureau_agg = build_bureau_agg(bureau)
    prev_agg = build_previous_agg(previous)

    datamart = app_layer.merge(bureau_agg, on="SK_ID_CURR", how="left")
    datamart = datamart.merge(prev_agg, on="SK_ID_CURR", how="left")

    datamart.to_csv(PROCESSED_DIR / "datamart_full.csv", index=False)
    datamart.sample(min(100, len(datamart)), random_state=42).to_csv(
        PROCESSED_DIR / "datamart_sample.csv", index=False
    )

    print("Datamart full shape:", datamart.shape)
    print("Saved full datamart to:", PROCESSED_DIR / "datamart_full.csv")
    print("Saved sample datamart to:", PROCESSED_DIR / "datamart_sample.csv")


if __name__ == "__main__":
    build_datamart()
