"""
AdPulse Media Analytics — Sample Data Generator
Domain : Ad-tech / Media Sales (InMobi-style)
Output : excel_data/AdPulse_Analytics.xlsx  (7 sheets)
Run    : python generate_data.py
"""

import pandas as pd
import numpy as np
import random
import os
from datetime import date, datetime, timedelta

try:
    from faker import Faker
    fake = Faker("en_IN")
    Faker.seed(42)
except ImportError:
    print("Run: pip install faker pandas openpyxl numpy")
    raise

np.random.seed(42)
random.seed(42)

OUT_DIR = "excel_data"
os.makedirs(OUT_DIR, exist_ok=True)

# ════════════════════════════════════════════════════════════
# DIM: Sellers  (20 reps across 4 teams)
# ════════════════════════════════════════════════════════════
TEAMS = ["Enterprise", "Mid-Market", "SMB", "International"]
REGIONS = ["North India", "South India", "West India", "East India", "APAC"]
TIERS = ["Senior", "Mid", "Junior"]
MONTHLY_TARGETS = {"Senior": 40, "Mid": 25, "Junior": 15}

sellers = []
for i in range(1, 21):
    tier = random.choice(TIERS)
    sellers.append({
        "seller_id":            f"S{i:03d}",
        "seller_name":          fake.name(),
        "team":                 random.choice(TEAMS),
        "region":               random.choice(REGIONS),
        "manager":              fake.name(),
        "tier":                 tier,
        "target_monthly_lakhs": MONTHLY_TARGETS[tier],
    })
df_sellers = pd.DataFrame(sellers)

# ════════════════════════════════════════════════════════════
# DIM: Clients  (50 advertisers)
# ════════════════════════════════════════════════════════════
INDUSTRIES = [
    "E-commerce", "BFSI", "Gaming", "Entertainment",
    "FMCG", "EdTech", "HealthTech", "Travel", "Retail", "Auto",
]
clients = []
for i in range(1, 51):
    clients.append({
        "client_id":    f"C{i:03d}",
        "client_name":  fake.company(),
        "industry":     random.choice(INDUSTRIES),
        "region":       random.choice(REGIONS),
        "tier":         random.choice(["Tier 1", "Tier 2", "Tier 3"]),
        "onboard_date": fake.date_between(
            start_date=date(2021, 1, 1),
            end_date=date(2023, 6, 30),
        ).strftime("%Y-%m-%d"),
    })
df_clients = pd.DataFrame(clients)

# ════════════════════════════════════════════════════════════
# DIM: Ad Products  (8 ad formats)
# ════════════════════════════════════════════════════════════
products = [
    {"product_id": "P001", "product_name": "Display Ads",   "category": "Performance", "sub_category": "Banner",      "base_cpm": 120},
    {"product_id": "P002", "product_name": "Video Ads",     "category": "Brand",       "sub_category": "In-Stream",   "base_cpm": 280},
    {"product_id": "P003", "product_name": "Native Ads",    "category": "Performance", "sub_category": "Native",      "base_cpm": 150},
    {"product_id": "P004", "product_name": "CPI Campaigns", "category": "Performance", "sub_category": "App Install",  "base_cpm": 200},
    {"product_id": "P005", "product_name": "Rewarded Video","category": "Brand",       "sub_category": "Rewarded",    "base_cpm": 320},
    {"product_id": "P006", "product_name": "Interstitial",  "category": "Performance", "sub_category": "Full-Screen",  "base_cpm": 180},
    {"product_id": "P007", "product_name": "Rich Media",    "category": "Brand",       "sub_category": "Interactive", "base_cpm": 240},
    {"product_id": "P008", "product_name": "Programmatic",  "category": "Performance", "sub_category": "RTB",         "base_cpm": 130},
]
df_products = pd.DataFrame(products)

# ════════════════════════════════════════════════════════════
# FACT: Sales  (~1,600 rows  |  2023–2024  |  grain: deal)
# ════════════════════════════════════════════════════════════
SEASONALITY = {
    1: 0.75, 2: 0.80, 3: 0.85,
    4: 0.90, 5: 0.92, 6: 0.95,
    7: 0.93, 8: 0.95, 9: 1.00,
    10: 1.05, 11: 1.10, 12: 1.20,
}

sales_rows = []
sale_id = 1
for year in [2023, 2024]:
    for month in range(1, 13):
        for seller in sellers:
            n_deals = random.randint(2, 4)
            for _ in range(n_deals):
                client  = random.choice(clients)
                product = random.choice(products)
                base    = seller["target_monthly_lakhs"] * SEASONALITY[month]
                revenue = round((base / n_deals) * random.uniform(0.6, 1.4), 2)
                cost    = round(revenue * random.uniform(0.55, 0.70), 2)
                gp      = round(revenue - cost, 2)
                target  = round(seller["target_monthly_lakhs"] / n_deals, 2)

                sales_rows.append({
                    "sale_id":             f"SAL{sale_id:05d}",
                    "date":                date(year, month, random.randint(1, 28)).strftime("%Y-%m-%d"),
                    "year":                year,
                    "month":               month,
                    "month_name":          datetime(year, month, 1).strftime("%b"),
                    "month_year":          datetime(year, month, 1).strftime("%b %Y"),
                    "quarter":             f"Q{(month - 1) // 3 + 1}",
                    "seller_id":           seller["seller_id"],
                    "seller_name":         seller["seller_name"],
                    "team":                seller["team"],
                    "region":              seller["region"],
                    "tier":                seller["tier"],
                    "client_id":           client["client_id"],
                    "client_name":         client["client_name"],
                    "industry":            client["industry"],
                    "product_id":          product["product_id"],
                    "product_name":        product["product_name"],
                    "category":            product["category"],
                    "sub_category":        product["sub_category"],
                    "revenue_lakhs":       revenue,
                    "cost_lakhs":          cost,
                    "gross_profit_lakhs":  gp,
                    "target_lakhs":        target,
                    "achievement_pct":     round((revenue / target) * 100, 1),
                })
                sale_id += 1

df_sales = pd.DataFrame(sales_rows)

# ════════════════════════════════════════════════════════════
# FACT: Sales Pipeline  (300 deals  |  2024 OKRs)
# ════════════════════════════════════════════════════════════
STAGES = ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
PROB   = {"Prospecting": 10, "Qualification": 25, "Proposal": 50,
          "Negotiation": 75, "Closed Won": 100, "Closed Lost": 0}
OKR_QUARTERS = ["Q1 FY2024", "Q2 FY2024", "Q3 FY2024", "Q4 FY2024"]

pipeline_rows = []
for pid in range(1, 301):
    seller = random.choice(sellers)
    client = random.choice(clients)
    stage  = random.choice(STAGES)
    value  = round(random.uniform(2, 60), 2)
    prob   = PROB[stage]

    pipeline_rows.append({
        "pipeline_id":         f"PIPE{pid:04d}",
        "deal_name":           f"{client['client_name'][:20]} — Campaign",
        "seller_id":           seller["seller_id"],
        "seller_name":         seller["seller_name"],
        "team":                seller["team"],
        "region":              seller["region"],
        "client_id":           client["client_id"],
        "client_name":         client["client_name"],
        "industry":            client["industry"],
        "stage":               stage,
        "deal_value_lakhs":    value,
        "probability_pct":     prob,
        "weighted_value_lakhs":round(value * prob / 100, 2),
        "okr_quarter":         random.choice(OKR_QUARTERS),
        "expected_close_date": fake.date_between(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
        ).strftime("%Y-%m-%d"),
        "created_date":        fake.date_between(
            start_date=date(2023, 10, 1),
            end_date=date(2024, 9, 30),
        ).strftime("%Y-%m-%d"),
    })

df_pipeline = pd.DataFrame(pipeline_rows)

# ════════════════════════════════════════════════════════════
# FACT: P&L  (monthly  |  2023–2024)
# ════════════════════════════════════════════════════════════
pl_rows = []
for year in [2023, 2024]:
    for month in range(1, 13):
        sub = df_sales[(df_sales["year"] == year) & (df_sales["month"] == month)]
        rev  = round(sub["revenue_lakhs"].sum(), 2)
        cost = round(sub["cost_lakhs"].sum(), 2)

        pub_payout   = round(cost * 0.70, 2)
        platform_cost= round(cost * 0.15, 2)
        sales_exp    = round(cost * 0.10, 2)
        ga_exp       = round(cost * 0.05, 2)

        gp           = round(rev - pub_payout, 2)
        opex         = round(platform_cost + sales_exp + ga_exp, 2)
        ebitda       = round(gp - opex, 2)
        rev_target   = round(rev * random.uniform(0.90, 1.15), 2)

        pl_rows.append({
            "year":                    year,
            "month":                   month,
            "month_name":              datetime(year, month, 1).strftime("%b"),
            "month_year":              datetime(year, month, 1).strftime("%b %Y"),
            "quarter":                 f"Q{(month - 1) // 3 + 1}",
            "revenue_lakhs":           rev,
            "revenue_target_lakhs":    rev_target,
            "publisher_payout_lakhs":  pub_payout,
            "gross_profit_lakhs":      gp,
            "gross_margin_pct":        round(gp / rev * 100, 1) if rev else 0,
            "platform_cost_lakhs":     platform_cost,
            "sales_expense_lakhs":     sales_exp,
            "ga_expense_lakhs":        ga_exp,
            "total_opex_lakhs":        opex,
            "ebitda_lakhs":            ebitda,
            "ebitda_margin_pct":       round(ebitda / rev * 100, 1) if rev else 0,
        })

df_pl = pd.DataFrame(pl_rows)

# ════════════════════════════════════════════════════════════
# DIM: Date  (2023-01-01 → 2024-12-31)
# ════════════════════════════════════════════════════════════
date_rows = []
cur = date(2023, 1, 1)
end = date(2024, 12, 31)
while cur <= end:
    m = cur.month
    fy_year = cur.year if m >= 4 else cur.year - 1
    fq = ((m - 4) % 12) // 3 + 1 if m >= 4 else ((m + 8) % 12) // 3 + 1
    date_rows.append({
        "date":           cur.strftime("%Y-%m-%d"),
        "day":            cur.day,
        "day_name":       cur.strftime("%A"),
        "week_of_year":   cur.isocalendar()[1],
        "month":          m,
        "month_name":     cur.strftime("%B"),
        "month_short":    cur.strftime("%b"),
        "month_year":     cur.strftime("%b %Y"),
        "quarter":        f"Q{(m - 1) // 3 + 1}",
        "year":           cur.year,
        "is_weekend":     cur.weekday() >= 5,
        "fiscal_year":    f"FY{fy_year}-{str(fy_year + 1)[2:]}",
        "fiscal_quarter": f"Q{fq}",
    })
    cur += timedelta(days=1)

df_date = pd.DataFrame(date_rows)

# ════════════════════════════════════════════════════════════
# Write single Excel workbook — 7 sheets
# ════════════════════════════════════════════════════════════
out_path = f"{OUT_DIR}/AdPulse_Analytics.xlsx"
with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    df_sales.to_excel(writer,    sheet_name="fact_sales",    index=False)
    df_pipeline.to_excel(writer, sheet_name="fact_pipeline", index=False)
    df_pl.to_excel(writer,       sheet_name="fact_pl",       index=False)
    df_sellers.to_excel(writer,  sheet_name="dim_seller",    index=False)
    df_clients.to_excel(writer,  sheet_name="dim_client",    index=False)
    df_products.to_excel(writer, sheet_name="dim_product",   index=False)
    df_date.to_excel(writer,     sheet_name="dim_date",      index=False)

print(f"\n✅  Written → {out_path}")
print(f"    fact_sales    : {len(df_sales):,} rows")
print(f"    fact_pipeline : {len(df_pipeline):,} rows")
print(f"    fact_pl       : {len(df_pl):,} rows")
print(f"    dim_seller    : {len(df_sellers):,} rows")
print(f"    dim_client    : {len(df_clients):,} rows")
print(f"    dim_product   : {len(df_products):,} rows")
print(f"    dim_date      : {len(df_date):,} rows")
print("\nNext → open Power BI Desktop → Get Data → Excel → AdPulse_Analytics.xlsx")
