# AdPulse Media Analytics — Power BI Portfolio Project

> Domain: Ad-tech / Media Sales Analytics (InMobi-style)
> Stack: Excel → Power BI Desktop (No SQL, No Azure)
> Pages: 7 | DAX Measures: 35+ | Features: Drill-through, Drill-up/down, Waterfall, P&L, MoM, OKR Pipeline

---

## Dashboards Built

| # | Page | Key Feature |
|---|------|------------|
| 1 | Executive Summary | KPI tiles, MoM arrows, Revenue vs Target |
| 2 | P&L Dashboard | Waterfall chart, Cost breakdown, Margin trends |
| 3 | Sales Pipeline & OKR | Funnel chart, Win rate, Weighted pipeline |
| 4 | Seller Performance | Leaderboard, Drill-through → Seller Detail |
| 5 | Client & Industry | Treemap, Tier analysis, Industry split |
| 6 | Product Analysis | Drill-up/down hierarchy, Format mix |
| 7 | Monthly Trends | MoM, YoY, 3M Rolling Avg, Heatmap |

---

## How to Run

### Step 1: Generate Data
```bash
pip install faker pandas openpyxl numpy
python generate_data.py
```
Output: `excel_data/AdPulse_Analytics.xlsx` (7 sheets, ~1,900 rows)

### Step 2: Open Power BI
- File → Get Data → Excel → `AdPulse_Analytics.xlsx`
- Follow: `powerbi_blueprint.md`

---

## Data Model

```
fact_sales ──── dim_date
           ──── dim_seller
           ──── dim_client
           ──── dim_product
fact_pipeline── dim_seller
           ──── dim_client
fact_pl     (standalone monthly P&L)
```

---

## Key DAX Measures

- `MoM Growth %`, `YoY Growth %`, `Revenue YTD/QTD/MTD`
- `Win Rate`, `Weighted Pipeline`, `Pipeline Coverage`
- `EBITDA`, `EBITDA Margin %`, `Gross Margin %`
- `Sellers Hitting Target`, `Seller Rank`
- `Revenue 3M Rolling Avg`, `Simulated Gross Profit (What-If)`

---

## Business Insights

1. Q4 drives 28% of annual revenue — seasonal index peaks Dec (1.20x)
2. Enterprise team 3x more productive per rep than SMB
3. Win rate 34% — Negotiation → Closed Won biggest drop-off
4. Video Ads highest margin product (42% GP vs Display 28%)
5. Gaming + BFSI = 52% revenue from 15% of clients
6. MoM growth stalls Jun–Aug both years (summer slump)
7. Publisher payout averaging 65% — 1pp improvement = significant upside

---

## Tools

- Python 3.10+ (data generation)
- Power BI Desktop (free)
- Excel / openpyxl (data format)
- Power BI Service via M365 Developer Program (publish)

---

## Links

- GitHub: https://github.com/Bhavana154/adpulse-media-analytics
- Live Demo: *(deploy to Streamlit Cloud — instructions below)*

## Deploy Live (Free)

1. Go to **share.streamlit.io**
2. Sign in with GitHub (`Bhavana154`)
3. Click **"New app"**
4. Repo: `Bhavana154/adpulse-media-analytics`
5. Branch: `main` | Main file: `app.py`
6. Click **Deploy** → live URL in ~3 min

---

Built by: Bhavana Badhepalli
GitHub: https://github.com/Bhavana154
