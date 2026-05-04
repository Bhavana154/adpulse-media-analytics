# AdPulse — All DAX Measures
# Copy each measure into Power BI: Modeling → New Measure

# ════════════════════════════════════════════════════
# HOW TO CREATE MEASURES IN POWER BI
# ════════════════════════════════════════════════════
# 1. Home tab → Enter Data → Name it "_Measures" → Load
# 2. Click "_Measures" table in Fields pane
# 3. Modeling → New Measure
# 4. Paste the DAX below (one measure at a time)
# 5. Press Enter or click checkmark
# 6. Right-click measure → Display folder → type folder name
# ════════════════════════════════════════════════════


-- ────────────────────────────────────────────────
-- FOLDER: 01 Sales
-- ────────────────────────────────────────────────

Total Revenue =
SUM(fact_sales[revenue_lakhs])

Total Cost =
SUM(fact_sales[cost_lakhs])

Gross Profit =
SUM(fact_sales[gross_profit_lakhs])

Gross Margin % =
DIVIDE([Gross Profit], [Total Revenue], 0)

Total Target =
SUM(fact_sales[target_lakhs])

Revenue Achievement % =
DIVIDE([Total Revenue], [Total Target], 0)

Total Deals =
DISTINCTCOUNT(fact_sales[sale_id])

Avg Deal Size =
DIVIDE([Total Revenue], [Total Deals], 0)

Total Sellers =
DISTINCTCOUNT(fact_sales[seller_id])

Total Clients =
DISTINCTCOUNT(fact_sales[client_id])


-- ────────────────────────────────────────────────
-- FOLDER: 02 MoM
-- ────────────────────────────────────────────────

Revenue PM =
CALCULATE(
    [Total Revenue],
    DATEADD(dim_date[date], -1, MONTH)
)

MoM Growth Abs =
[Total Revenue] - [Revenue PM]

MoM Growth % =
DIVIDE([MoM Growth Abs], [Revenue PM], 0)

MoM Arrow =
VAR pct = [MoM Growth %]
RETURN
    IF(
        ISBLANK([Revenue PM]),
        "—",
        IF(pct >= 0,
           "▲ " & FORMAT(pct, "0.0%"),
           "▼ " & FORMAT(ABS(pct), "0.0%")
        )
    )

MoM Color =
IF([MoM Growth %] >= 0, "#2ECC71", "#E74C3C")


-- ────────────────────────────────────────────────
-- FOLDER: 03 YoY
-- ────────────────────────────────────────────────

Revenue PY =
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(dim_date[date])
)

YoY Growth % =
DIVIDE([Total Revenue] - [Revenue PY], [Revenue PY], 0)

YoY Growth Abs =
[Total Revenue] - [Revenue PY]

YoY Arrow =
VAR pct = [YoY Growth %]
RETURN
    IF(
        ISBLANK([Revenue PY]),
        "—",
        IF(pct >= 0,
           "▲ " & FORMAT(pct, "0.0%"),
           "▼ " & FORMAT(ABS(pct), "0.0%")
        )
    )


-- ────────────────────────────────────────────────
-- FOLDER: 04 Time Intelligence
-- ────────────────────────────────────────────────

Revenue YTD =
TOTALYTD([Total Revenue], dim_date[date])

Revenue QTD =
TOTALQTD([Total Revenue], dim_date[date])

Revenue MTD =
TOTALMTD([Total Revenue], dim_date[date])

Revenue 3M Rolling Avg =
DIVIDE(
    CALCULATE(
        [Total Revenue],
        DATESINPERIOD(
            dim_date[date],
            LASTDATE(dim_date[date]),
            -3,
            MONTH
        )
    ),
    3
)

Revenue Last 30 Days =
CALCULATE(
    [Total Revenue],
    DATESINPERIOD(
        dim_date[date],
        MAX(dim_date[date]),
        -30,
        DAY
    )
)

Target YTD =
TOTALYTD([Total Target], dim_date[date])


-- ────────────────────────────────────────────────
-- FOLDER: 05 P&L
-- ────────────────────────────────────────────────

PL Revenue =
SUM(fact_pl[revenue_lakhs])

PL Target =
SUM(fact_pl[revenue_target_lakhs])

Publisher Payout =
SUM(fact_pl[publisher_payout_lakhs])

PL Gross Profit =
SUM(fact_pl[gross_profit_lakhs])

PL Gross Margin % =
DIVIDE([PL Gross Profit], [PL Revenue], 0)

Platform Cost =
SUM(fact_pl[platform_cost_lakhs])

Sales Expense =
SUM(fact_pl[sales_expense_lakhs])

GA Expense =
SUM(fact_pl[ga_expense_lakhs])

Total OPEX =
SUM(fact_pl[total_opex_lakhs])

EBITDA =
SUM(fact_pl[ebitda_lakhs])

EBITDA Margin % =
DIVIDE([EBITDA], [PL Revenue], 0)

Revenue vs Budget % =
DIVIDE([PL Revenue] - [PL Target], [PL Target], 0)

Revenue vs Budget Abs =
[PL Revenue] - [PL Target]


-- ────────────────────────────────────────────────
-- FOLDER: 06 Pipeline
-- ────────────────────────────────────────────────

Total Pipeline Value =
SUM(fact_pipeline[deal_value_lakhs])

Weighted Pipeline =
SUM(fact_pipeline[weighted_value_lakhs])

Total Pipeline Deals =
COUNTROWS(fact_pipeline)

Closed Won Value =
CALCULATE(
    [Total Pipeline Value],
    fact_pipeline[stage] = "Closed Won"
)

Closed Lost Value =
CALCULATE(
    [Total Pipeline Value],
    fact_pipeline[stage] = "Closed Lost"
)

Win Rate =
DIVIDE(
    CALCULATE(COUNTROWS(fact_pipeline), fact_pipeline[stage] = "Closed Won"),
    CALCULATE(COUNTROWS(fact_pipeline), fact_pipeline[stage] IN {"Closed Won", "Closed Lost"}),
    0
)

Pipeline Coverage =
DIVIDE([Total Pipeline Value], [Total Target], 0)

Avg Deal Size Pipeline =
DIVIDE([Total Pipeline Value], [Total Pipeline Deals], 0)

Open Pipeline =
CALCULATE(
    [Total Pipeline Value],
    fact_pipeline[stage] IN {"Prospecting","Qualification","Proposal","Negotiation"}
)


-- ────────────────────────────────────────────────
-- FOLDER: 07 Seller
-- ────────────────────────────────────────────────

Sellers Hitting Target =
COUNTROWS(
    FILTER(
        VALUES(dim_seller[seller_id]),
        [Revenue Achievement %] >= 1
    )
)

Sellers Below Target =
[Total Sellers] - [Sellers Hitting Target]

Seller Rank =
RANKX(
    ALL(dim_seller[seller_name]),
    [Total Revenue],
    ,
    DESC,
    DENSE
)

Avg Revenue per Seller =
DIVIDE([Total Revenue], [Total Sellers], 0)

Top Seller Revenue =
CALCULATE(
    [Total Revenue],
    TOPN(1, ALL(dim_seller[seller_name]), [Total Revenue])
)


-- ────────────────────────────────────────────────
-- FOLDER: 08 Conditional Formatting
-- ────────────────────────────────────────────────

KPI Color YoY =
SWITCH(
    TRUE(),
    [YoY Growth %] >= 0.10, "#2ECC71",
    [YoY Growth %] >= 0,    "#F39C12",
    "#E74C3C"
)

Achievement Color =
SWITCH(
    TRUE(),
    [Revenue Achievement %] >= 1.05, "#2ECC71",
    [Revenue Achievement %] >= 0.90, "#F39C12",
    "#E74C3C"
)

EBITDA Color =
SWITCH(
    TRUE(),
    [EBITDA Margin %] >= 0.20, "#2ECC71",
    [EBITDA Margin %] >= 0.10, "#F39C12",
    "#E74C3C"
)


-- ────────────────────────────────────────────────
-- FOLDER: 09 What-If (create parameter first)
-- ────────────────────────────────────────────────

-- BEFORE creating these measures:
-- Modeling → New Parameter
-- Name: "Payout Rate"
-- Min: 55  Max: 75  Increment: 1  Default: 65
-- Click OK — Power BI creates the parameter + slicer

Simulated Gross Profit =
[PL Revenue] * (1 - ('Payout Rate'[Payout Rate Value] / 100))

Simulated GM % =
DIVIDE([Simulated Gross Profit], [PL Revenue], 0)

Simulated EBITDA =
[Simulated Gross Profit] - [Total OPEX]

Simulated EBITDA Margin % =
DIVIDE([Simulated EBITDA], [PL Revenue], 0)


-- ────────────────────────────────────────────────
-- DISPLAY FOLDER SETUP (after all measures created)
-- ────────────────────────────────────────────────
-- Select measure in Fields pane
-- Properties pane (right side) → Display folder
-- Type folder name exactly as above (01 Sales, 02 MoM, etc.)
-- Measures auto-group under folder in Fields pane
