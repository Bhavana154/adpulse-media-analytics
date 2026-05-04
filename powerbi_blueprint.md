# AdPulse Media Analytics — Power BI Report Blueprint

> Reference: Ankita Nanglia (InMobi) resume dashboards
> Data source: Excel only (AdPulse_Analytics.xlsx)
> No SQL. No Azure. No Databricks.

---

## Report Overview

| Page | Name | Purpose |
|------|------|---------|
| 1 | Executive Summary | KPI tiles, MoM, revenue vs target |
| 2 | P&L Dashboard | Waterfall, margin trends, cost breakdown |
| 3 | Sales Pipeline & OKR | Funnel, weighted pipeline, win rate |
| 4 | Seller Performance | Ranking, effectiveness, drill-through |
| 5 | Client & Industry | Top clients, industry split |
| 6 | Product Analysis | Category drill-up/down, format mix |
| 7 | Monthly Trends | MoM, YoY, heatmap, 3M rolling avg |

---

## Step 1: Load Data into Power BI

```
Power BI Desktop
→ Get Data
→ Excel Workbook
→ Select: AdPulse_Analytics.xlsx
→ Check ALL 7 sheets (fact_sales, fact_pipeline, fact_pl, dim_seller, dim_client, dim_product, dim_date)
→ Load
```

---

## Step 2: Data Model (Relationships)

Build in Model View:

| From Table | From Column | To Table | To Column | Cardinality |
|-----------|------------|----------|-----------|-------------|
| fact_sales | date | dim_date | date | *:1 |
| fact_sales | seller_id | dim_seller | seller_id | *:1 |
| fact_sales | client_id | dim_client | client_id | *:1 |
| fact_sales | product_id | dim_product | product_id | *:1 |
| fact_pipeline | seller_id | dim_seller | seller_id | *:1 |
| fact_pipeline | client_id | dim_client | client_id | *:1 |

**Mark dim_date as Date Table:**
Modeling → Mark as Date Table → Column: `date`

**Sort columns:**
- `month_name` → sort by `month`
- `month_year` → sort by `month_year` (already chronological)
- `day_name` → sort by `day_of_week`

**Hide from report view:**
- All `*_id` columns on fact tables
- `base_cpm`, `created_at` technical fields

---

## Step 3: DAX Measures

Create a new table: `_Measures` (Enter Data → blank table → name it `_Measures`)
Put ALL measures here. Organize with display folders.

### Folder: Sales

```dax
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
```

### Folder: MoM

```dax
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
    IF(pct >= 0, "▲ " & FORMAT(pct, "0.0%"), "▼ " & FORMAT(ABS(pct), "0.0%"))
```

### Folder: YoY

```dax
Revenue PY =
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(dim_date[date])
)

YoY Growth % =
DIVIDE([Total Revenue] - [Revenue PY], [Revenue PY], 0)

YoY Growth Abs =
[Total Revenue] - [Revenue PY]
```

### Folder: Time Intelligence

```dax
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
        DATESINPERIOD(dim_date[date], LASTDATE(dim_date[date]), -3, MONTH)
    ),
    3
)

Revenue Last 30 Days =
CALCULATE(
    [Total Revenue],
    DATESINPERIOD(dim_date[date], MAX(dim_date[date]), -30, DAY)
)
```

### Folder: P&L

```dax
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

Total OPEX =
SUM(fact_pl[total_opex_lakhs])

EBITDA =
SUM(fact_pl[ebitda_lakhs])

EBITDA Margin % =
DIVIDE([EBITDA], [PL Revenue], 0)

Revenue vs Budget % =
DIVIDE([PL Revenue] - [PL Target], [PL Target], 0)
```

### Folder: Pipeline

```dax
Total Pipeline Value =
SUM(fact_pipeline[deal_value_lakhs])

Weighted Pipeline =
SUM(fact_pipeline[weighted_value_lakhs])

Total Deals in Pipeline =
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
```

### Folder: Seller

```dax
Total Sellers =
DISTINCTCOUNT(fact_sales[seller_id])

Sellers Hitting Target =
COUNTROWS(
    FILTER(
        VALUES(dim_seller[seller_id]),
        [Revenue Achievement %] >= 1
    )
)

Seller Rank =
RANKX(
    ALL(dim_seller[seller_name]),
    [Total Revenue],
    ,
    DESC
)

Avg Revenue per Seller =
DIVIDE([Total Revenue], [Total Sellers], 0)
```

### Folder: Conditional Formatting

```dax
KPI Color Revenue =
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
```

---

## Step 4: Hierarchies (right-click → Create hierarchy)

**Product Hierarchy** (dim_product):
```
Category → Sub-Category → Product Name
```

**Date Hierarchy** (dim_date):
```
Year → Quarter → Month → Day
```

**Seller Hierarchy** (dim_seller):
```
Team → Tier → Seller Name
```

**Geography Hierarchy** (dim_seller):
```
Region → Seller Name
```

---

## Step 5: Dashboard Pages

---

### PAGE 1: Executive Summary

**Layout (1280×720):**

```
┌────────────────────────────────────────────────────────────────────┐
│  AdPulse Media Analytics             [Year ▼] [Quarter ▼]         │
│  Executive Summary                   [Team ▼] [Region ▼]          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐│
│  │ REVENUE  │ │ GROSS    │ │ EBITDA   │ │ ACHIEVE  │ │ WIN      ││
│  │ ₹XX Lakh │ │ MARGIN % │ │ MARGIN % │ │ RATE %   │ │ RATE %   ││
│  │ ▲ MoM%   │ │          │ │          │ │          │ │          ││
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘│
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ Revenue vs Target (Monthly) │  │ Revenue by Team (Donut)    │  │
│  │ [Clustered column + line]   │  │ Enterprise/Mid-Market/SMB  │  │
│  │ Bars = Actual, Line = Target│  │ /International             │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ Top 10 Sellers              │  │ Revenue by Industry        │  │
│  │ [Bar chart + achievement %] │  │ [Bar chart]                │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

**Visuals:**

| Visual | Type | Fields |
|--------|------|--------|
| Revenue KPI | Card | `[Total Revenue]`, secondary `[MoM Arrow]` |
| Gross Margin | Card | `[Gross Margin %]` |
| EBITDA Margin | Card | `[EBITDA Margin %]` |
| Achievement | Card | `[Revenue Achievement %]` |
| Win Rate | Card | `[Win Rate]` |
| Revenue vs Target | Combo chart | X: `dim_date[month_year]`, Column: `[Total Revenue]`, Line: `[Total Target]` |
| Team donut | Donut | Legend: `dim_seller[team]`, Values: `[Total Revenue]` |
| Top Sellers | Bar | Y: `dim_seller[seller_name]`, X: `[Total Revenue]`, tooltips: `[Revenue Achievement %]` |
| Industry bar | Bar | Y: `dim_client[industry]`, X: `[Total Revenue]` |

---

### PAGE 2: P&L Dashboard

**Reference:** Ankita's "Profit & Loss dashboards reduced manual effort 50%"

```
┌────────────────────────────────────────────────────────────────────┐
│  P&L Dashboard                    [Year ▼] [Quarter ▼] [Month ▼]  │
├────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Revenue  │ │Publisher │ │ Gross    │ │ EBITDA   │             │
│  │          │ │ Payout   │ │ Profit   │ │          │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  P&L Waterfall Chart                                         │  │
│  │  Revenue → (−) Publisher Payout → Gross Profit              │  │
│  │  → (−) Platform Cost → (−) Sales Exp → (−) G&A → EBITDA    │  │
│  │  [Waterfall visual]                                          │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ Gross Margin % Trend        │  │ Cost Breakdown (Stacked)   │  │
│  │ [Line chart by month]       │  │ Pub Payout / Platform /    │  │
│  │ + target margin dotted line │  │ Sales Exp / G&A            │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Monthly P&L Table                                           │  │
│  │  Month | Revenue | Payout | GP | GP% | OPEX | EBITDA | EBITDA%│
│  │  [Matrix with conditional formatting on GP% and EBITDA%]    │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

**Waterfall Chart Setup:**
- Category: Revenue, Publisher Payout, Platform Cost, Sales Expense, G&A, EBITDA
- Values: respective DAX measures
- Revenue = Increase, costs = Decrease, EBITDA = Total

**DAX for Waterfall (individual cost lines):**
```dax
Publisher Payout = SUM(fact_pl[publisher_payout_lakhs])
Platform Cost = SUM(fact_pl[platform_cost_lakhs])
Sales Expense = SUM(fact_pl[sales_expense_lakhs])
GA Expense = SUM(fact_pl[ga_expense_lakhs])
```

---

### PAGE 3: Sales Pipeline & OKR

**Reference:** Ankita's "Sales pipeline dashboard for OKR setting & Pipeline tracking"

```
┌────────────────────────────────────────────────────────────────────┐
│  Sales Pipeline & OKR              [OKR Quarter ▼] [Team ▼]       │
├────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Total    │ │ Weighted │ │ Win Rate │ │ Pipeline │             │
│  │ Pipeline │ │ Pipeline │ │          │ │ Coverage │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ Pipeline Funnel by Stage    │  │ Deals by OKR Quarter       │  │
│  │ [Funnel chart]              │  │ [Stacked bar: stage mix]   │  │
│  │ Prospecting → Qualification │  │                            │  │
│  │ → Proposal → Negotiation    │  │                            │  │
│  │ → Closed Won                │  │                            │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ Pipeline by Team            │  │ Win/Loss by Industry       │  │
│  │ [Clustered bar]             │  │ [Clustered bar]            │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Pipeline Detail Table                                       │  │
│  │  Deal | Seller | Client | Industry | Stage | Value | Close  │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

**Funnel Chart Setup:**
- Group: `fact_pipeline[stage]`
- Values: `[Total Pipeline Value]`
- Sort stages manually: Prospecting → Qualification → Proposal → Negotiation → Closed Won

---

### PAGE 4: Seller Performance (Drill-Through)

**Reference:** Ankita's "Dashboard replicating seller-level insights, 5x faster"

```
┌────────────────────────────────────────────────────────────────────┐
│  Seller Performance           [Team ▼] [Region ▼] [Tier ▼]        │
│                               [Year ▼] [Quarter ▼]                │
├────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Sellers  │ │ Hitting  │ │ Avg Rev  │ │ Top      │             │
│  │ Total    │ │ Target   │ │ per Rep  │ │ Seller   │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Seller Leaderboard Table                                    │  │
│  │  Rank | Seller | Team | Revenue | Target | Achievement%      │  │
│  │  | Deals | Avg Deal | Rank Badge                             │  │
│  │  [Conditional formatting: green ≥100%, orange 80-99%, red]  │  │
│  │  [Drill-through enabled → Seller Detail page]               │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ Revenue by Team (Bar)       │  │ Achievement % Distribution │  │
│  │ Actual vs Target            │  │ [Histogram / bar bins]     │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

#### Drill-Through: Seller Detail Page

```
┌────────────────────────────────────────────────────────────────────┐
│  ← Back    Seller Detail: [Seller Name]                            │
├────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Revenue  │ │ Target   │ │ Achievmt │ │ Total    │             │
│  │ (YTD)    │ │ (YTD)    │ │ %        │ │ Deals    │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ Monthly Revenue Trend       │  │ Revenue by Product         │  │
│  │ [Line: Actual vs Target]    │  │ [Bar chart]                │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ Top Clients (this seller)   │  │ Pipeline (this seller)     │  │
│  │ [Bar chart]                 │  │ [Funnel]                   │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

**Drill-Through Setup:**
1. Create new page "Seller Detail"
2. Add `dim_seller[seller_name]` to drill-through field well
3. Back button auto-created by Power BI (Visualizations → Insert → Back button)
4. Right-click any seller name on Page 4 → Drill through → Seller Detail

---

### PAGE 5: Client & Industry Analysis

```
┌────────────────────────────────────────────────────────────────────┐
│  Client & Industry Analysis    [Industry ▼] [Region ▼] [Tier ▼]   │
├────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Active   │ │ Avg Rev  │ │ Top      │ │ New      │             │
│  │ Clients  │ │ per Clnt │ │ Industry │ │ Clients  │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ Top 20 Clients (Treemap)    │  │ Industry Revenue Split     │  │
│  │ [Treemap: size = revenue]   │  │ [Donut]                    │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ Revenue by Client Tier      │  │ New vs Existing Clients    │  │
│  │ [Bar: Tier 1/2/3]           │  │ [Stacked bar by month]     │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Client Detail Table                                         │  │
│  │  Client | Industry | Tier | Region | Revenue | Deals | YoY% │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

---

### PAGE 6: Product Analysis (Drill-Up / Drill-Down)

**Reference:** Ankita's category analysis + format performance

```
┌────────────────────────────────────────────────────────────────────┐
│  Product Analysis              [Category ▼] [Year ▼]              │
├────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Products │ │ Top      │ │ Brand vs │ │ Avg Rev  │             │
│  │ Active   │ │ Category │ │ Perf %   │ │ per Deal │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Product Hierarchy Bar Chart (DRILL-UP / DRILL-DOWN)         │  │
│  │  Level 1: Category (Performance vs Brand)                    │  │
│  │  Level 2: Sub-Category (↓ drill-down)                        │  │
│  │  Level 3: Product Name                                       │  │
│  │  [Bar chart with hierarchy — use ↑↓ drill arrows]           │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ Product Revenue Trend       │  │ Product Mix by Quarter     │  │
│  │ [Line chart]                │  │ [100% stacked bar]         │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Product Table                                               │  │
│  │  Product | Category | Revenue | Deals | Margin% | Rank      │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

**Drill-Up/Down Setup:**
1. Add `Product Hierarchy` to X-axis of bar chart
2. In visual header → enable drill icons (up ↑ / down ↓ arrows appear)
3. Click ↓ to drill down from Category → Sub-Category → Product
4. Click ↑ to drill up
5. OR: right-click bar → "Drill down"

---

### PAGE 7: Monthly Trends

**Reference:** Ankita's "Automated data manipulation reducing manual intervention 30%"

```
┌────────────────────────────────────────────────────────────────────┐
│  Monthly Trends                [Year ▼] [Team ▼] [Category ▼]     │
├────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Rev YTD  │ │ Rev QTD  │ │ MoM      │ │ YoY      │             │
│  │          │ │          │ │ Growth % │ │ Growth % │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Revenue: Actual vs PY vs 3M Rolling Avg                     │  │
│  │  [Line chart — 3 lines]                                      │  │
│  │  - Solid: Current Year                                       │  │
│  │  - Dotted: Prior Year                                        │  │
│  │  - Dashed: 3M Rolling Avg                                    │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│  │ MoM Growth % (bar chart)    │  │ Revenue Heatmap            │  │
│  │ Green bars = +ve growth     │  │ [Matrix: row=month,col=year│  │
│  │ Red bars = -ve growth       │  │  conditional formatting]   │  │
│  └─────────────────────────────┘  └────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Monthly Summary Table                                       │  │
│  │  Month | Revenue | PY Rev | YoY% | MoM% | Target | Achiev% │  │
│  │  [Conditional formatting on YoY% and MoM%]                  │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

**MoM Bar Color Conditional Formatting:**
```dax
MoM Color =
IF([MoM Growth %] >= 0, "#2ECC71", "#E74C3C")
```
Apply via: Format → Data colors → Conditional formatting → Field value → `[MoM Color]`

---

## Step 6: Global Slicers (Sync Across Pages)

View → Sync Slicers:

| Slicer | Field | Pages |
|--------|-------|-------|
| Year | `dim_date[year]` | All |
| Quarter | `dim_date[quarter]` | All |
| Month | `dim_date[month_name]` | All |
| Team | `dim_seller[team]` | 1,4,5,7 |
| Region | `dim_seller[region]` | 1,4,5 |
| Industry | `dim_client[industry]` | 1,5,6 |
| Category | `dim_product[category]` | 1,6,7 |
| OKR Quarter | `fact_pipeline[okr_quarter]` | 3 only |

---

## Step 7: Theme & Branding

**Color Palette (AdPulse):**
```
Primary:    #1A1A2E  (dark navy)
Secondary:  #E94560  (red accent)
Positive:   #2ECC71  (green)
Warning:    #F39C12  (orange)
Negative:   #E74C3C  (red)
Background: #F5F6FA  (light gray)
Text:       #2C3E50  (dark gray)
```

**Font:** Segoe UI throughout (native Power BI font)

**Apply Theme:**
View → Themes → Customize current theme → enter hex values above → Save

---

## Step 8: Interactivity Features

### Bookmarks
- "Reset All Filters" button (each page)
- "Current Year Only" toggle
- "2023 vs 2024 Compare" preset

**Setup:** View → Bookmarks → Add bookmark → clear all slicers → save as "Reset"

### Tooltips (Custom Tooltip Page)
Create small page (320×200):
- Set page type: Tooltip
- Add sparkline + KPIs
- Assign to visuals: Format → Tooltip → Report page

### What-If: Publisher Payout Slider
```
Modeling → New Parameter → Name: "Payout Rate" → Min: 55, Max: 75, Increment: 1, Default: 65
```

```dax
Simulated Gross Profit =
[PL Revenue] * (1 - ('Payout Rate'[Payout Rate Value] / 100))

Simulated GM % =
DIVIDE([Simulated Gross Profit], [PL Revenue], 0)
```

### Page Navigation Buttons
Insert → Buttons → Page navigation → style with icons

---

## Step 9: Publish Checklist

- [ ] All FK columns hidden from report
- [ ] dim_date marked as Date Table
- [ ] Sort columns set (month_name → month)
- [ ] All measures in `_Measures` table with display folders
- [ ] Theme applied consistently all 7 pages
- [ ] Slicers synced across pages
- [ ] Drill-through on Seller Detail page works
- [ ] Drill-up/down on Product page works
- [ ] Waterfall on P&L page correct (revenue → costs → EBITDA)
- [ ] Bookmarks (Reset Filters) added each page
- [ ] Mobile layout configured (View → Mobile Layout)
- [ ] File saved as `AdPulse_Analytics.pbix`
- [ ] Publish to Power BI Service (File → Publish → Your Workspace)
- [ ] Take screenshots of all 7 pages
- [ ] Record Loom walkthrough (3-5 min)
- [ ] Commit to GitHub

---

## Step 10: Business Insights to Write (insights.md)

After building — write 5-7 insights for README + LinkedIn:

> 1. **Q4 drives 28% of annual revenue** — seasonality index peaks in Dec (1.20x). Recommend front-loading sales hiring in Q3.
> 2. **Enterprise team 3x more productive per rep** than SMB despite same headcount — reallocate targets accordingly.
> 3. **Win rate at 34%** — Negotiation → Closed Won drop-off is biggest leak. Coaching opportunity.
> 4. **Video Ads highest margin product** at 42% GP vs Display at 28% — push upsell motion.
> 5. **Gaming + BFSI clients = 52% of revenue** from 15% of client base — protect these accounts.
> 6. **MoM growth stalled Jun-Aug** both years — summer slump. Plan retention campaigns for this window.
> 7. **Publisher payout averaging 65% of revenue** — even 1pp improvement = ₹X lakh annualized.

---

## File Structure

```
adpulse-bi-project/
├── generate_data.py
├── excel_data/
│   └── AdPulse_Analytics.xlsx        (7 sheets)
├── powerbi/
│   └── AdPulse_Analytics.pbix
├── screenshots/
│   ├── 01_executive.png
│   ├── 02_pl_dashboard.png
│   ├── 03_pipeline_okr.png
│   ├── 04_seller_performance.png
│   ├── 04b_seller_detail_drillthrough.png
│   ├── 05_client_industry.png
│   ├── 06_product_drilldown.png
│   └── 07_monthly_trends.png
├── docs/
│   ├── insights.md
│   └── dax_measures.md
├── powerbi_blueprint.md              ← this file
└── README.md
```

---

## Build Order Summary

```
1. Run: python generate_data.py            → creates AdPulse_Analytics.xlsx
2. Power BI Desktop → Get Data → Excel     → load 7 sheets
3. Model View → build relationships        → 6 relationships
4. Mark dim_date as Date Table             → Modeling tab
5. Create _Measures table                  → Enter Data
6. Write all DAX measures                  → organized in folders
7. Create hierarchies (Product, Date, Seller)
8. Build Page 1: Executive Summary         → test slicers
9. Build Page 2: P&L + Waterfall           → verify waterfall flow
10. Build Page 3: Pipeline + Funnel        → verify funnel sort
11. Build Page 4: Seller Performance       → set up drill-through
12. Build Drill-through: Seller Detail     → add back button
13. Build Page 5: Client & Industry
14. Build Page 6: Product + Drill-up/down  → assign hierarchy to axis
15. Build Page 7: Monthly Trends           → 3-line chart, MoM colors
16. Apply theme, sync slicers, bookmarks
17. Publish to Power BI Service
18. Screenshots + Loom recording
19. GitHub push
20. LinkedIn post with 3 key insights
```
