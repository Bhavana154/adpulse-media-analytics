# AdPulse Power BI — Exact Click-by-Click Guide
# Minimum clicks. Maximum output. Follow in order.

---

## PRE-CHECK
- [ ] Power BI Desktop installed (Windows)
- [ ] Excel file ready: adpulse-bi-project/excel_data/AdPulse_Analytics.xlsx
- [ ] This file open on second monitor or printed

---

## BLOCK 1: Load Data (5 min)

1. Open Power BI Desktop
2. Click "Get Data" (Home ribbon) → "Excel workbook"
3. Navigate to: `adpulse-bi-project/excel_data/AdPulse_Analytics.xlsx`
4. Click Open
5. Navigator window opens → tick SELECT ALL (check top checkbox)
   - fact_sales ✅
   - fact_pipeline ✅
   - fact_pl ✅
   - dim_seller ✅
   - dim_client ✅
   - dim_product ✅
   - dim_date ✅
6. Click "Load" (bottom right) — wait ~30 seconds
7. All 7 tables appear in Fields pane (right side) ✅

---

## BLOCK 2: Apply Theme (2 min)

1. View ribbon → Themes dropdown arrow (small ↓ beside themes gallery)
2. Click "Browse for themes"
3. Navigate to: `adpulse-bi-project/theme.json`
4. Click Open
5. Confirmation popup → click OK
6. Report background turns light gray ✅

---

## BLOCK 3: Build Relationships (8 min)

1. Click "Model" icon (left sidebar, looks like 3 connected boxes)
2. You see 7 table boxes scattered — drag to arrange:
   - Center: fact_sales (biggest table)
   - Top: dim_date
   - Left: dim_seller
   - Bottom-left: dim_client
   - Bottom: dim_product
   - Right side: fact_pipeline, fact_pl

3. CREATE RELATIONSHIP 1:
   - Drag `fact_sales[date]` → drop onto `dim_date[date]`
   - Popup appears → verify: Many to One (*:1), Cross-filter: Single → OK

4. CREATE RELATIONSHIP 2:
   - Drag `fact_sales[seller_id]` → drop onto `dim_seller[seller_id]`
   - Many to One → OK

5. CREATE RELATIONSHIP 3:
   - Drag `fact_sales[client_id]` → drop onto `dim_client[client_id]`
   - Many to One → OK

6. CREATE RELATIONSHIP 4:
   - Drag `fact_sales[product_id]` → drop onto `dim_product[product_id]`
   - Many to One → OK

7. CREATE RELATIONSHIP 5:
   - Drag `fact_pipeline[seller_id]` → drop onto `dim_seller[seller_id]`
   - Many to One → OK

8. CREATE RELATIONSHIP 6:
   - Drag `fact_pipeline[client_id]` → drop onto `dim_client[client_id]`
   - Many to One → OK

9. Lines now connect tables ✅ (6 lines total)

---

## BLOCK 4: Mark Date Table + Sort Columns (5 min)

1. Still in Model view → click `dim_date` table header
2. Modeling ribbon → "Mark as date table"
3. Dropdown: select `date` column → OK
4. Yellow calendar icon appears on dim_date ✅

SORT month_name by month number:
5. Click `Report` view (top icon left sidebar)
6. In Fields pane → expand `dim_date`
7. Click `month_name` field (highlight it)
8. Column Tools ribbon appears → "Sort by column" → select `month`
9. Repeat: click `month_short` → Sort by column → `month`
10. Click `day_name` → Sort by column → "day" (if exists) OR skip

---

## BLOCK 5: Create _Measures Table (2 min)

1. Home ribbon → "Enter data"
2. Table appears → rename it: type `_Measures` in Name field (bottom)
3. Do NOT add any columns → click Load
4. `_Measures` table appears in Fields pane ✅
5. Click `_Measures` in Fields pane to select it

---

## BLOCK 6: Add All DAX Measures (20 min)

**Open this file:** `adpulse-bi-project/docs/dax_measures.md`
**Method:** For each measure block:

1. Modeling ribbon → "New Measure"
2. Formula bar appears at top
3. DELETE default text (`Measure = `)
4. PASTE the measure from dax_measures.md
5. Press Enter (or click ✓ checkmark)
6. Measure appears in `_Measures` table

**Add measures in this order (copy-paste each):**

### From FOLDER 01 Sales (8 measures):
```
Total Revenue, Total Cost, Gross Profit, Gross Margin %,
Total Target, Revenue Achievement %, Total Deals, Avg Deal Size
```

### From FOLDER 02 MoM (5 measures):
```
Revenue PM, MoM Growth Abs, MoM Growth %, MoM Arrow, MoM Color
```

### From FOLDER 03 YoY (4 measures):
```
Revenue PY, YoY Growth %, YoY Growth Abs, YoY Arrow
```

### From FOLDER 04 Time Intelligence (5 measures):
```
Revenue YTD, Revenue QTD, Revenue MTD, Revenue 3M Rolling Avg,
Revenue Last 30 Days
```

### From FOLDER 05 P&L (13 measures):
```
PL Revenue, PL Target, Publisher Payout, PL Gross Profit,
PL Gross Margin %, Platform Cost, Sales Expense, GA Expense,
Total OPEX, EBITDA, EBITDA Margin %, Revenue vs Budget %,
Revenue vs Budget Abs
```

### From FOLDER 06 Pipeline (9 measures):
```
Total Pipeline Value, Weighted Pipeline, Total Pipeline Deals,
Closed Won Value, Closed Lost Value, Win Rate, Pipeline Coverage,
Avg Deal Size Pipeline, Open Pipeline
```

### From FOLDER 07 Seller (5 measures):
```
Sellers Hitting Target, Sellers Below Target, Seller Rank,
Avg Revenue per Seller, Top Seller Revenue
```

### From FOLDER 08 Conditional Formatting (3 measures):
```
KPI Color YoY, Achievement Color, EBITDA Color
```

**Total: 52 measures ✅**

**SET DISPLAY FOLDERS (optional but clean):**
- Click each measure → Properties pane (right of Fields pane)
- "Display folder" text box → type folder name (01 Sales, 02 MoM, etc.)

---

## BLOCK 7: Create Hierarchies (5 min)

### Product Hierarchy:
1. Fields pane → expand `dim_product`
2. Right-click `category` → "Create hierarchy" → named "Product Hierarchy"
3. Right-click `sub_category` → "Add to hierarchy" → Product Hierarchy
4. Right-click `product_name` → "Add to hierarchy" → Product Hierarchy
5. Result: Category → Sub-Category → Product Name ✅

### Date Hierarchy:
1. Fields pane → expand `dim_date`
2. Right-click `year` → "Create hierarchy" → named "Date Hierarchy"
3. Add in order: `quarter`, `month_name`, `day` → Add to hierarchy
4. Result: Year → Quarter → Month → Day ✅

### Seller Hierarchy:
1. Fields pane → expand `dim_seller`
2. Right-click `team` → "Create hierarchy" → named "Seller Hierarchy"
3. Add: `tier`, `seller_name` → Add to hierarchy
4. Result: Team → Tier → Seller Name ✅

---

## BLOCK 8: Build Pages

### RENAME Page 1:
Right-click "Page 1" tab (bottom) → Rename → type `Executive Summary`

---

### PAGE 1: Executive Summary

**Add 5 KPI Cards (top row):**

Card 1 — Total Revenue:
1. Click blank canvas area
2. Visualizations pane → click Card icon (📋)
3. Fields pane → drag `[Total Revenue]` → drop into "Fields" well
4. Format pane → Title → type "Total Revenue"
5. Resize: drag corners → make small rectangle (top left area)

Card 2 — Gross Margin %:
1. Click blank area → Card → drag `[Gross Margin %]`
2. Format → Data label → Format: Percentage, 1 decimal

Card 3 — EBITDA Margin %:
1. Card → `[EBITDA Margin %]` → format as %

Card 4 — Revenue Achievement %:
1. Card → `[Revenue Achievement %]` → format as %

Card 5 — Win Rate:
1. Card → `[Win Rate]` → format as %

**Add Combo Chart (Revenue vs Target):**
1. Visualizations → Clustered column and line chart
2. X-axis: drag `dim_date[month_year]`
3. Column Y-axis: drag `[Total Revenue]`
4. Line Y-axis: drag `[Total Target]`
5. Format → Title → "Monthly Revenue vs Target"
6. Resize: make wide, center-left

**Add Donut Chart (Revenue by Team):**
1. Visualizations → Donut chart
2. Legend: drag `dim_seller[team]`
3. Values: drag `[Total Revenue]`
4. Format → Title → "Revenue by Team"

**Add Bar Chart (Top Sellers):**
1. Visualizations → Clustered bar chart
2. Y-axis: drag `dim_seller[seller_name]`
3. X-axis: drag `[Total Revenue]`
4. Filters pane → Top N → 10 → by `[Total Revenue]`
5. Format → Title → "Top 10 Sellers"

**Add Bar Chart (Revenue by Industry):**
1. Bar chart → Y: `dim_client[industry]` → X: `[Total Revenue]`
2. Sort: right-click visual → Sort by → Total Revenue (descending)

**Add Slicers:**
1. Visualizations → Slicer
2. Field: `dim_date[year]` → style: Dropdown
3. Repeat for: `dim_date[quarter]`, `dim_seller[team]`, `dim_seller[region]`
4. Arrange slicers top-right corner

---

### PAGE 2: P&L Dashboard

Right-click tab → Add page → Rename "P&L Dashboard"

**Add 4 KPI Cards:**
- PL Revenue, Publisher Payout, PL Gross Profit, EBITDA

**Add Waterfall Chart:**
1. Visualizations → Waterfall chart
2. Category: type these manually in a new "What-If" or use text box as labels
   - EASIER METHOD: Unpivot fact_pl in Power Query:
   
**Power Query for Waterfall (do this FIRST):**
1. Home → Transform data (opens Power Query Editor)
2. Left pane → click `fact_pl`
3. Select columns: `revenue_lakhs`, `publisher_payout_lakhs`,
   `platform_cost_lakhs`, `sales_expense_lakhs`,
   `ga_expense_lakhs`, `ebitda_lakhs`
4. Also keep: `year`, `month`, `month_year`
5. Home → Close & Apply
6. In report: Waterfall → Category: create a new table

**SIMPLER WATERFALL APPROACH:**
1. Visualizations → Waterfall chart
2. Category field: Create a calculated table in DAX:
   
   ```
   Modeling → New Table
   ```
   
   ```dax
   PL_Waterfall_Labels = 
   DATATABLE(
       "Item", STRING, "Sort_Order", INTEGER, "Type", STRING,
       {
           {"Revenue",          1, "Increase"},
           {"Publisher Payout", 2, "Decrease"},
           {"Gross Profit",     3, "Total"},
           {"Platform Cost",    4, "Decrease"},
           {"Sales Expense",    5, "Decrease"},
           {"G&A Expense",      6, "Decrease"},
           {"EBITDA",           7, "Total"}
       }
   )
   ```
   
   ```dax
   WF Value = 
   SWITCH(
       SELECTEDVALUE(PL_Waterfall_Labels[Item]),
       "Revenue",          [PL Revenue],
       "Publisher Payout", [Publisher Payout],
       "Gross Profit",     [PL Gross Profit],
       "Platform Cost",    [Platform Cost],
       "Sales Expense",    [Sales Expense],
       "G&A Expense",      [GA Expense],
       "EBITDA",           [EBITDA]
   )
   ```
   
3. Waterfall → Category: `PL_Waterfall_Labels[Item]`
4. Y-axis: `[WF Value]`
5. Sort by Sort_Order

**Add Line Chart (Gross Margin Trend):**
1. Line chart → X: `dim_date[month_year]` → Y: `[PL Gross Margin %]`
2. Add constant line: Analytics pane → Constant line → value 0.35 (35% target)

**Add Stacked Bar (Cost Breakdown):**
1. 100% Stacked bar chart
2. X-axis: `dim_date[month_year]`
3. Legend: manually select Publisher Payout, Platform Cost, Sales Expense, GA Expense
4. Use individual P&L measures per legend item

**Add Matrix Table (Monthly P&L):**
1. Matrix visual
2. Rows: `fact_pl[month_year]`
3. Values: PL Revenue, Publisher Payout, PL Gross Profit, PL Gross Margin %, EBITDA, EBITDA Margin %
4. Format → Conditional formatting on PL Gross Margin % and EBITDA Margin % → Color scale (red → green)

---

### PAGE 3: Sales Pipeline & OKR

Add page → Rename "Sales Pipeline & OKR"

**Add 4 Cards:** Total Pipeline Value, Weighted Pipeline, Win Rate, Pipeline Coverage

**Add Funnel Chart:**
1. Visualizations → Funnel
2. Group: `fact_pipeline[stage]`
3. Values: `[Total Pipeline Value]`
4. Sort: manually sort stages via visual Sort options
   Order: Prospecting → Qualification → Proposal → Negotiation → Closed Won

**Add Stacked Bar (Pipeline by OKR Quarter):**
1. Stacked bar → Y: `fact_pipeline[okr_quarter]`
2. X: `[Total Pipeline Value]`
3. Legend: `fact_pipeline[stage]`

**Add Clustered Bar (Pipeline by Team):**
1. Clustered bar → Y: `dim_seller[team]`
2. X: `[Total Pipeline Value]` + `[Weighted Pipeline]`

**Add Bar (Win/Loss by Industry):**
1. Clustered bar → Y: `dim_client[industry]`
2. X: `[Closed Won Value]`, `[Closed Lost Value]`

**Add Table (Pipeline Detail):**
1. Table visual
2. Columns: `fact_pipeline[deal_name]`, `dim_seller[seller_name]`,
   `dim_client[client_name]`, `dim_client[industry]`,
   `fact_pipeline[stage]`, `[Total Pipeline Value]`,
   `fact_pipeline[expected_close_date]`

**Slicer:** `fact_pipeline[okr_quarter]`, `dim_seller[team]`

---

### PAGE 4: Seller Performance

Add page → Rename "Seller Performance"

**Add 4 Cards:** Total Sellers, Sellers Hitting Target, Avg Revenue per Seller, [Total Revenue]

**Add Matrix/Table (Leaderboard):**
1. Matrix visual
2. Rows: `dim_seller[seller_name]`
3. Values: `[Total Revenue]`, `[Total Target]`, `[Revenue Achievement %]`, `[Total Deals]`, `[Seller Rank]`
4. Conditional formatting on Achievement %:
   - Format → Conditional formatting → Background color
   - Rules: ≥ 1.05 = green, ≥ 0.90 = orange, else red

**ENABLE DRILL-THROUGH:**
1. Right side → Drill through section (in Visualizations pane, scroll down)
2. Drag `dim_seller[seller_name]` → drop in "Add drill-through fields here"
3. "Keep all filters" toggle → ON

**Add Clustered Bar (Team Actual vs Target):**
1. Clustered column chart
2. X: `dim_seller[team]`
3. Values: `[Total Revenue]`, `[Total Target]`

**Add Donut (Achievement Distribution):**
1. Donut → Legend: create bins OR use team
2. Values: `[Total Revenue]`

---

### PAGE 4b: Seller Detail (Drill-Through Destination)

Add page → Rename "Seller Detail"

**SET AS DRILL-THROUGH PAGE:**
1. In Drill through section → drag `dim_seller[seller_name]` field
2. Back button auto-creates → position top-left

**Add 4 Cards:** Revenue MTD, Total Target, Revenue Achievement %, Total Deals

**Add Line Chart (Monthly Revenue):**
1. Line → X: `dim_date[month_year]` → Y: `[Total Revenue]`, `[Total Target]`

**Add Bar (Revenue by Product):**
1. Bar → Y: `dim_product[product_name]` → X: `[Total Revenue]`

**Add Bar (Top Clients for this Seller):**
1. Bar → Y: `dim_client[client_name]` → X: `[Total Revenue]`
2. Top N filter: 10

**Add Funnel (Seller Pipeline):**
1. Funnel → Group: `fact_pipeline[stage]` → Values: `[Total Pipeline Value]`

---

### PAGE 5: Client & Industry

Add page → Rename "Client & Industry"

**Add 4 Cards:** Total Clients, Avg Revenue per Client (= `[Total Revenue]` / `[Total Clients]`), [Total Revenue], [Total Deals]

**Add Treemap:**
1. Treemap visual
2. Group: `dim_client[client_name]`
3. Values: `[Total Revenue]`
4. Tooltip: `[Total Deals]`, `[Gross Margin %]`

**Add Donut (Industry Split):**
1. Donut → Legend: `dim_client[industry]` → Values: `[Total Revenue]`

**Add Bar (Client Tier Revenue):**
1. Bar → Y: `dim_client[tier]` → X: `[Total Revenue]`

**Add Stacked Bar (New vs Existing):**
1. Stacked bar → X: `dim_date[month_year]`
2. Values: `[Total Revenue]`
3. Legend: `dim_client[tier]` (proxy for client segment)

**Add Table:**
Client, Industry, Tier, Region, Revenue, Deals, YoY%

**Slicers:** `dim_client[industry]`, `dim_client[tier]`, `dim_seller[region]`

---

### PAGE 6: Product Analysis (Drill-Up/Down)

Add page → Rename "Product Analysis"

**Add 4 Cards:** Active Products (DISTINCTCOUNT), Top Category, [Total Revenue], [Gross Margin %]

**Add Bar Chart WITH HIERARCHY (Drill-up/down):**
1. Clustered bar chart
2. X-axis: drag "Product Hierarchy" (the hierarchy you created, not individual fields)
3. Y-axis: `[Total Revenue]`
4. Visual header icons appear: ↓ (Drill down), ↑ (Drill up), ⊕ (Expand all)
5. Default shows Category level
6. Click ↓ to enable drill → click a bar → goes to Sub-Category
7. Click ↓ again → Product Name level
8. Click ↑ to go back up

**Add Line Chart (Product Revenue Trend):**
1. Line → X: `dim_date[month_year]`
2. Y: `[Total Revenue]`
3. Legend: `dim_product[category]`

**Add 100% Stacked Bar (Mix by Quarter):**
1. 100% Stacked bar
2. X: `dim_date[quarter]`
3. Values: `[Total Revenue]`
4. Legend: `dim_product[category]`

**Add Table:** Product, Category, Revenue, Deals, Margin%, Rank

**Slicer:** `dim_product[category]`

---

### PAGE 7: Monthly Trends

Add page → Rename "Monthly Trends"

**Add 4 Cards:** Revenue YTD, Revenue QTD, MoM Growth %, YoY Growth %

**Add Multi-Line Chart (3 lines):**
1. Line chart
2. X: `dim_date[month_year]`
3. Values: `[Total Revenue]`, `[Revenue PY]`, `[Revenue 3M Rolling Avg]`
4. Format → Lines:
   - Total Revenue: solid, thick
   - Revenue PY: dashed
   - 3M Rolling Avg: dotted, different color

**Add Bar Chart (MoM Growth %):**
1. Clustered bar
2. X: `dim_date[month_year]`
3. Y: `[MoM Growth %]`
4. Format → Data colors → Conditional formatting → Field value → `[MoM Color]`
   (Green for positive, red for negative)

**Add Matrix Heatmap:**
1. Matrix visual
2. Rows: `dim_date[month_name]`
3. Columns: `dim_date[year]`
4. Values: `[Total Revenue]`
5. Format → Conditional formatting → Background color → Color scale (white → dark red)

**Add Summary Table:**
Month Year, Revenue, Revenue PY, YoY%, MoM%, Target, Achievement%

**Slicers:** `dim_date[year]`, `dim_seller[team]`, `dim_product[category]`

---

## BLOCK 9: Sync Slicers Across Pages (5 min)

1. View ribbon → "Sync slicers"
2. Sync slicers panel opens (left side)
3. Click Year slicer on Page 1
4. In sync panel → tick ALL pages for Sync column
5. Repeat for Quarter slicer
6. For Team slicer → sync pages 1, 4, 5, 7

---

## BLOCK 10: Add Bookmarks (5 min)

1. View → Bookmarks panel
2. Clear all slicers (click each slicer → erase)
3. Bookmarks panel → "Add" → rename "Reset Filters"
4. Insert → Buttons → Blank → type "Reset Filters" → assign action: Bookmark → Reset Filters
5. Copy button to each page

---

## BLOCK 11: What-If Parameter (3 min)

1. Modeling → New Parameter
2. Name: `Payout Rate`
3. Min: 55, Max: 75, Increment: 1, Default: 65
4. Click OK — Power BI adds slicer automatically
5. Now create these measures (from dax_measures.md FOLDER 09)
6. Add to P&L page: line showing Simulated Gross Profit vs actual

---

## BLOCK 12: Final Polish (5 min)

**Page titles:**
- Insert → Text box → type page name → bold, 20pt, dark navy color
- Copy text box to each page, update text

**Page navigation buttons:**
- Go to Page 1
- Insert → Buttons → Page navigation
- Configure for each page
- Style: match theme

**Mobile layout:**
- View → Mobile layout
- Drag visuals to mobile canvas
- Prioritize: title, KPI cards, main chart

---

## BLOCK 13: Save + Publish (3 min)

1. File → Save As → name: `AdPulse_Analytics.pbix`
2. Save in: `adpulse-bi-project/powerbi/`
3. File → Publish → "Publish to Power BI"
4. Sign in: `admin@bhavanaanalytics.onmicrosoft.com`
5. Destination: My Workspace
6. Click Publish
7. Link appears → copy link → save in README

---

## BLOCK 14: Screenshots (10 min)

For each page:
1. View ribbon → "Fit to page"
2. Windows: Win+Shift+S → snip each page
3. Save in: `adpulse-bi-project/screenshots/`
   - 01_executive.png
   - 02_pl_dashboard.png
   - 03_pipeline_okr.png
   - 04_seller_performance.png
   - 04b_seller_detail.png
   - 05_client_industry.png
   - 06_product_drilldown.png
   - 07_monthly_trends.png

---

## TIME ESTIMATE

| Block | Task | Time |
|-------|------|------|
| 1 | Load data | 5 min |
| 2 | Apply theme | 2 min |
| 3 | Build relationships | 8 min |
| 4 | Mark date table + sort | 5 min |
| 5 | Create _Measures table | 2 min |
| 6 | Add all DAX measures | 20 min |
| 7 | Create hierarchies | 5 min |
| 8 | Build all 7 pages | 60 min |
| 9 | Sync slicers | 5 min |
| 10 | Bookmarks | 5 min |
| 11 | What-If parameter | 3 min |
| 12 | Final polish | 5 min |
| 13 | Save + Publish | 3 min |
| 14 | Screenshots | 10 min |
| **TOTAL** | | **~2.5 hours** |

---

## WHEN YOU GET STUCK — PING ME WITH:

- Screenshot of error
- Which block/step you are on
- Exact error text

I debug immediately.
