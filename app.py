"""
AdPulse Media Analytics — Streamlit Dashboard
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AdPulse Media Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "primary":    "#E94560",
    "dark":       "#1A1A2E",
    "green":      "#2ECC71",
    "orange":     "#F39C12",
    "red":        "#E74C3C",
    "blue":       "#3498DB",
    "bg":         "#F5F6FA",
    "text":       "#2C3E50",
}

PALETTE = [
    "#E94560","#1A1A2E","#3498DB","#2ECC71",
    "#F39C12","#9B59B6","#1ABC9C","#E74C3C",
]

# ════════════════════════════════════════════════════════════
# DATA LOAD
# ════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    path = "excel_data/AdPulse_Analytics.xlsx"
    sales    = pd.read_excel(path, sheet_name="fact_sales",    parse_dates=["date"])
    pipeline = pd.read_excel(path, sheet_name="fact_pipeline", parse_dates=["expected_close_date","created_date"])
    pl       = pd.read_excel(path, sheet_name="fact_pl")
    sellers  = pd.read_excel(path, sheet_name="dim_seller")
    clients  = pd.read_excel(path, sheet_name="dim_client")
    products = pd.read_excel(path, sheet_name="dim_product")

    # sort month_year correctly
    sales["month_dt"]    = pd.to_datetime(sales[["year","month"]].assign(day=1))
    pl["month_dt"]       = pd.to_datetime(pl[["year","month"]].assign(day=1))
    pl                   = pl.sort_values("month_dt")

    # MoM
    pl["revenue_pm"]     = pl["revenue_lakhs"].shift(1)
    pl["mom_abs"]        = pl["revenue_lakhs"] - pl["revenue_pm"]
    pl["mom_pct"]        = pl["mom_abs"] / pl["revenue_pm"]

    # YoY
    pl["revenue_py"]     = pl.groupby("month")["revenue_lakhs"].shift(1)
    pl["yoy_pct"]        = (pl["revenue_lakhs"] - pl["revenue_py"]) / pl["revenue_py"]

    return sales, pipeline, pl, sellers, clients, products

sales, pipeline, pl, sellers, clients, products = load_data()

# ════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ════════════════════════════════════════════════════════════
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=60)
st.sidebar.title("AdPulse Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "📊 Executive Summary",
    "💰 P&L Dashboard",
    "🔀 Sales Pipeline & OKR",
    "🏆 Seller Performance",
    "🏢 Client & Industry",
    "📦 Product Analysis",
    "📅 Monthly Trends",
])

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

years      = sorted(sales["year"].unique())
sel_years  = st.sidebar.multiselect("Year", years, default=years)

teams      = sorted(sales["team"].unique())
sel_teams  = st.sidebar.multiselect("Team", teams, default=teams)

regions    = sorted(sales["region"].unique())
sel_region = st.sidebar.multiselect("Region", regions, default=regions)

cats       = sorted(sales["category"].unique())
sel_cats   = st.sidebar.multiselect("Ad Category", cats, default=cats)

# Apply filters
fs = sales[
    sales["year"].isin(sel_years) &
    sales["team"].isin(sel_teams) &
    sales["region"].isin(sel_region) &
    sales["category"].isin(sel_cats)
].copy()

fpl = pl[pl["year"].isin(sel_years)].copy()

st.sidebar.markdown("---")
st.sidebar.caption("Built by Bhavana Badhepalli")
st.sidebar.caption("Stack: Python · Pandas · Plotly · Streamlit")

# ════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════
def kpi_card(col, label, value, delta=None, delta_suffix="", fmt="₹{:.1f}L"):
    if fmt:
        disp = fmt.format(value) if value is not None else "—"
    else:
        disp = value
    col.metric(label=label, value=disp, delta=f"{delta:.1%} {delta_suffix}" if delta is not None else None)

def fmt_cr(val):
    return f"₹{val:.1f}L"

def arrow(pct):
    if pct is None or np.isnan(pct): return "—"
    sym = "▲" if pct >= 0 else "▼"
    color = "green" if pct >= 0 else "red"
    return f'<span style="color:{color}">{sym} {abs(pct):.1%}</span>'


# ════════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE SUMMARY
# ════════════════════════════════════════════════════════════
if page == "📊 Executive Summary":
    st.title("📊 Executive Summary")
    st.markdown("High-level KPIs, revenue trends, and top performers.")
    st.markdown("---")

    total_rev    = fs["revenue_lakhs"].sum()
    total_gp     = fs["gross_profit_lakhs"].sum()
    gm_pct       = total_gp / total_rev if total_rev else 0
    total_target = fs["target_lakhs"].sum()
    achiev       = total_rev / total_target if total_target else 0
    total_deals  = fs["sale_id"].nunique()
    total_clients= fs["client_id"].nunique()
    ebitda       = fpl["ebitda_lakhs"].sum()
    ebitda_mg    = ebitda / fpl["revenue_lakhs"].sum() if fpl["revenue_lakhs"].sum() else 0

    # KPI row
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Revenue",    f"₹{total_rev:.1f}L")
    c2.metric("Gross Margin %",   f"{gm_pct:.1%}")
    c3.metric("EBITDA Margin %",  f"{ebitda_mg:.1%}")
    c4.metric("Achievement %",    f"{achiev:.1%}")
    c5.metric("Total Deals",      f"{total_deals:,}")

    st.markdown("---")

    # Revenue vs Target monthly
    monthly = fs.groupby(["month_dt","month_year"]).agg(
        revenue=("revenue_lakhs","sum"),
        target=("target_lakhs","sum")
    ).reset_index().sort_values("month_dt")

    fig1 = go.Figure()
    fig1.add_bar(x=monthly["month_year"], y=monthly["revenue"], name="Actual Revenue",
                 marker_color=COLORS["primary"])
    fig1.add_scatter(x=monthly["month_year"], y=monthly["target"], name="Target",
                     mode="lines+markers", line=dict(color=COLORS["dark"], dash="dash", width=2))
    fig1.update_layout(title="Monthly Revenue vs Target", xaxis_title="Month",
                       yaxis_title="Lakhs (₹)", plot_bgcolor="white",
                       legend=dict(orientation="h", y=-0.2), height=350)

    # Revenue by Team donut
    team_rev = fs.groupby("team")["revenue_lakhs"].sum().reset_index()
    fig2 = px.pie(team_rev, values="revenue_lakhs", names="team",
                  title="Revenue by Team", hole=0.5,
                  color_discrete_sequence=PALETTE)
    fig2.update_layout(height=350)

    col1, col2 = st.columns([2, 1])
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Top 10 sellers + Revenue by Industry
    top_sellers = fs.groupby("seller_name")["revenue_lakhs"].sum().nlargest(10).reset_index()
    fig3 = px.bar(top_sellers.sort_values("revenue_lakhs"), x="revenue_lakhs", y="seller_name",
                  orientation="h", title="Top 10 Sellers by Revenue",
                  color="revenue_lakhs", color_continuous_scale=["#1A1A2E","#E94560"],
                  labels={"revenue_lakhs":"Revenue (₹L)", "seller_name":"Seller"})
    fig3.update_layout(showlegend=False, plot_bgcolor="white", height=350)

    ind_rev = fs.groupby("industry")["revenue_lakhs"].sum().sort_values(ascending=True).reset_index()
    fig4 = px.bar(ind_rev, x="revenue_lakhs", y="industry", orientation="h",
                  title="Revenue by Industry",
                  color_discrete_sequence=[COLORS["blue"]],
                  labels={"revenue_lakhs":"Revenue (₹L)","industry":"Industry"})
    fig4.update_layout(plot_bgcolor="white", height=350)

    col3, col4 = st.columns(2)
    col3.plotly_chart(fig3, use_container_width=True)
    col4.plotly_chart(fig4, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 2: P&L DASHBOARD
# ════════════════════════════════════════════════════════════
elif page == "💰 P&L Dashboard":
    st.title("💰 Profit & Loss Dashboard")
    st.markdown("Revenue breakdown, cost structure, margin trends, EBITDA waterfall.")
    st.markdown("---")

    pl_rev  = fpl["revenue_lakhs"].sum()
    pl_pub  = fpl["publisher_payout_lakhs"].sum()
    pl_gp   = fpl["gross_profit_lakhs"].sum()
    pl_ebit = fpl["ebitda_lakhs"].sum()
    pl_opex = fpl["total_opex_lakhs"].sum()
    gm      = pl_gp / pl_rev if pl_rev else 0
    em      = pl_ebit / pl_rev if pl_rev else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Revenue",         f"₹{pl_rev:.1f}L")
    c2.metric("Publisher Payout",f"₹{pl_pub:.1f}L", delta=f"{pl_pub/pl_rev:.1%} of rev" if pl_rev else None)
    c3.metric("Gross Profit",    f"₹{pl_gp:.1f}L",  delta=f"GM {gm:.1%}")
    c4.metric("EBITDA",          f"₹{pl_ebit:.1f}L",delta=f"Margin {em:.1%}")

    st.markdown("---")

    # Waterfall
    wf_items  = ["Revenue","Publisher\nPayout","Gross\nProfit","Platform\nCost","Sales\nExpense","G&A\nExpense","EBITDA"]
    wf_vals   = [pl_rev, -pl_pub, None, -fpl["platform_cost_lakhs"].sum(),
                 -fpl["sales_expense_lakhs"].sum(), -fpl["ga_expense_lakhs"].sum(), None]
    wf_measure= ["absolute","relative","total","relative","relative","relative","total"]
    wf_colors = [COLORS["blue"], COLORS["red"], COLORS["green"],
                 COLORS["orange"], COLORS["orange"], COLORS["orange"], COLORS["primary"]]

    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=wf_measure,
        x=wf_items,
        y=wf_vals,
        texttemplate="₹%{y:.1f}L",
        textposition="outside",
        connector={"line": {"color": "#CCCCCC", "width": 1}},
        increasing={"marker": {"color": COLORS["green"]}},
        decreasing={"marker": {"color": COLORS["red"]}},
        totals={"marker": {"color": COLORS["primary"]}},
    ))
    fig_wf.update_layout(
        title="P&L Waterfall: Revenue → EBITDA",
        plot_bgcolor="white",
        height=420,
        showlegend=False,
    )
    st.plotly_chart(fig_wf, use_container_width=True)

    st.markdown("---")

    # Gross Margin trend + Cost breakdown
    fig_gm = go.Figure()
    fig_gm.add_scatter(x=fpl["month_year"], y=fpl["gross_margin_pct"],
                       mode="lines+markers", name="Gross Margin %",
                       line=dict(color=COLORS["primary"], width=3))
    fig_gm.add_hline(y=0.35, line_dash="dash", line_color=COLORS["dark"],
                     annotation_text="35% target", annotation_position="right")
    fig_gm.update_layout(title="Gross Margin % Trend", yaxis_tickformat=".0%",
                         plot_bgcolor="white", height=300)

    # Stacked cost breakdown
    cost_df = fpl.melt(
        id_vars=["month_year"],
        value_vars=["publisher_payout_lakhs","platform_cost_lakhs","sales_expense_lakhs","ga_expense_lakhs"],
        var_name="cost_type", value_name="amount"
    )
    cost_labels = {
        "publisher_payout_lakhs": "Publisher Payout",
        "platform_cost_lakhs":    "Platform Cost",
        "sales_expense_lakhs":    "Sales Expense",
        "ga_expense_lakhs":       "G&A"
    }
    cost_df["cost_type"] = cost_df["cost_type"].map(cost_labels)
    fig_cost = px.bar(cost_df, x="month_year", y="amount", color="cost_type",
                      title="Cost Breakdown by Month",
                      color_discrete_sequence=PALETTE,
                      labels={"amount":"₹Lakhs","month_year":"Month","cost_type":"Cost Type"})
    fig_cost.update_layout(plot_bgcolor="white", height=300, barmode="stack")

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_gm,   use_container_width=True)
    col2.plotly_chart(fig_cost, use_container_width=True)

    st.markdown("---")

    # Monthly P&L table
    st.subheader("Monthly P&L Summary")
    tbl = fpl[["month_year","revenue_lakhs","publisher_payout_lakhs",
               "gross_profit_lakhs","gross_margin_pct","total_opex_lakhs",
               "ebitda_lakhs","ebitda_margin_pct"]].copy()
    tbl.columns = ["Month","Revenue","Pub Payout","Gross Profit","GM%","OPEX","EBITDA","EBITDA%"]
    tbl["GM%"]     = tbl["GM%"].apply(lambda x: f"{x:.1f}%")
    tbl["EBITDA%"] = tbl["EBITDA%"].apply(lambda x: f"{x:.1f}%")
    for col in ["Revenue","Pub Payout","Gross Profit","OPEX","EBITDA"]:
        tbl[col] = tbl[col].apply(lambda x: f"₹{x:.1f}L")
    st.dataframe(tbl, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
# PAGE 3: SALES PIPELINE & OKR
# ════════════════════════════════════════════════════════════
elif page == "🔀 Sales Pipeline & OKR":
    st.title("🔀 Sales Pipeline & OKR Tracking")
    st.markdown("Pipeline funnel, win rate, deal stages, OKR quarter tracking.")
    st.markdown("---")

    okr_quarters = ["All"] + sorted(pipeline["okr_quarter"].unique())
    sel_okr = st.selectbox("OKR Quarter", okr_quarters)
    fp = pipeline if sel_okr == "All" else pipeline[pipeline["okr_quarter"] == sel_okr]

    total_pipe   = fp["deal_value_lakhs"].sum()
    weighted     = fp["weighted_value_lakhs"].sum()
    total_deals  = len(fp)
    won          = fp[fp["stage"] == "Closed Won"]
    lost         = fp[fp["stage"] == "Closed Lost"]
    win_rate     = len(won) / (len(won) + len(lost)) if (len(won) + len(lost)) > 0 else 0
    coverage     = total_pipe / fs["target_lakhs"].sum() if fs["target_lakhs"].sum() else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Pipeline",   f"₹{total_pipe:.1f}L")
    c2.metric("Weighted Pipeline",f"₹{weighted:.1f}L")
    c3.metric("Win Rate",         f"{win_rate:.1%}")
    c4.metric("Pipeline Coverage",f"{coverage:.1f}x")

    st.markdown("---")

    # Funnel
    stage_order = ["Prospecting","Qualification","Proposal","Negotiation","Closed Won"]
    funnel_df = (fp[fp["stage"].isin(stage_order)]
                 .groupby("stage")["deal_value_lakhs"].sum()
                 .reindex(stage_order).reset_index())
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_df["stage"],
        x=funnel_df["deal_value_lakhs"],
        textinfo="value+percent initial",
        marker={"color": [COLORS["blue"],COLORS["primary"],"#9B59B6",COLORS["orange"],COLORS["green"]]},
    ))
    fig_funnel.update_layout(title="Pipeline Funnel by Stage", height=380)

    # Pipeline by OKR Quarter
    okr_df = (pipeline.groupby(["okr_quarter","stage"])["deal_value_lakhs"]
              .sum().reset_index())
    fig_okr = px.bar(okr_df, x="okr_quarter", y="deal_value_lakhs", color="stage",
                     title="Pipeline by OKR Quarter",
                     color_discrete_sequence=PALETTE,
                     labels={"deal_value_lakhs":"₹Lakhs","okr_quarter":"OKR Quarter"})
    fig_okr.update_layout(plot_bgcolor="white", height=380)

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_funnel, use_container_width=True)
    col2.plotly_chart(fig_okr,   use_container_width=True)

    st.markdown("---")

    # Win/Loss by Industry
    wl_df = (fp[fp["stage"].isin(["Closed Won","Closed Lost"])]
             .groupby(["industry","stage"])["deal_value_lakhs"].sum().reset_index())
    fig_wl = px.bar(wl_df, x="industry", y="deal_value_lakhs", color="stage",
                    barmode="group", title="Won vs Lost by Industry",
                    color_discrete_map={"Closed Won": COLORS["green"], "Closed Lost": COLORS["red"]},
                    labels={"deal_value_lakhs":"₹Lakhs"})
    fig_wl.update_layout(plot_bgcolor="white", height=320)
    st.plotly_chart(fig_wl, use_container_width=True)

    st.markdown("---")

    # Pipeline Table
    st.subheader("Pipeline Detail")
    pipe_tbl = fp[["deal_name","seller_name","client_name","industry",
                   "stage","deal_value_lakhs","probability_pct",
                   "weighted_value_lakhs","okr_quarter","expected_close_date"]].copy()
    pipe_tbl.columns = ["Deal","Seller","Client","Industry","Stage",
                        "Value (₹L)","Probability%","Weighted (₹L)","OKR Quarter","Close Date"]
    st.dataframe(pipe_tbl, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
# PAGE 4: SELLER PERFORMANCE
# ════════════════════════════════════════════════════════════
elif page == "🏆 Seller Performance":
    st.title("🏆 Seller Performance")
    st.markdown("Seller leaderboard, team comparison, achievement tracking.")
    st.markdown("---")

    sel_df = (fs.groupby(["seller_id","seller_name","team","tier","region"])
              .agg(revenue=("revenue_lakhs","sum"),
                   target=("target_lakhs","sum"),
                   deals=("sale_id","nunique"))
              .reset_index())
    sel_df["achievement_pct"] = sel_df["revenue"] / sel_df["target"]
    sel_df["rank"] = sel_df["revenue"].rank(ascending=False).astype(int)
    sel_df = sel_df.sort_values("rank")

    hitting = (sel_df["achievement_pct"] >= 1).sum()
    avg_rev = sel_df["revenue"].mean()

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Sellers",        len(sel_df))
    c2.metric("Hitting Target",        f"{hitting} / {len(sel_df)}")
    c3.metric("Avg Revenue / Seller",  f"₹{avg_rev:.1f}L")
    c4.metric("Top Team", fs.groupby("team")["revenue_lakhs"].sum().idxmax())

    st.markdown("---")

    # Leaderboard
    st.subheader("Seller Leaderboard")

    def color_achievement(val):
        if val >= 1.05: return "background-color: #d5f5e3"
        elif val >= 0.9: return "background-color: #fef9e7"
        return "background-color: #fadbd8"

    lb = sel_df[["rank","seller_name","team","tier","revenue","target","achievement_pct","deals"]].copy()
    lb.columns = ["Rank","Seller","Team","Tier","Revenue (₹L)","Target (₹L)","Achievement %","Deals"]
    lb["Revenue (₹L)"]  = lb["Revenue (₹L)"].round(1)
    lb["Target (₹L)"]   = lb["Target (₹L)"].round(1)
    lb["Achievement %"] = lb["Achievement %"].apply(lambda x: f"{x:.1%}")
    st.dataframe(lb, use_container_width=True, hide_index=True, height=400)

    st.markdown("---")

    # Team comparison + Region comparison
    team_df = (fs.groupby("team")
               .agg(revenue=("revenue_lakhs","sum"),
                    target=("target_lakhs","sum"))
               .reset_index())
    fig_team = go.Figure()
    fig_team.add_bar(x=team_df["team"], y=team_df["revenue"], name="Actual",
                     marker_color=COLORS["primary"])
    fig_team.add_bar(x=team_df["team"], y=team_df["target"], name="Target",
                     marker_color=COLORS["dark"])
    fig_team.update_layout(title="Team: Revenue vs Target", barmode="group",
                           plot_bgcolor="white", height=320)

    region_df = (fs.groupby("region")["revenue_lakhs"].sum()
                 .sort_values(ascending=True).reset_index())
    fig_reg = px.bar(region_df, x="revenue_lakhs", y="region", orientation="h",
                     title="Revenue by Region",
                     color_discrete_sequence=[COLORS["blue"]],
                     labels={"revenue_lakhs":"₹Lakhs","region":"Region"})
    fig_reg.update_layout(plot_bgcolor="white", height=320)

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_team, use_container_width=True)
    col2.plotly_chart(fig_reg,  use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 5: CLIENT & INDUSTRY
# ════════════════════════════════════════════════════════════
elif page == "🏢 Client & Industry":
    st.title("🏢 Client & Industry Analysis")
    st.markdown("Top clients, industry breakdown, tier analysis.")
    st.markdown("---")

    client_df = (fs.groupby(["client_id","client_name","industry","tier"])
                 .agg(revenue=("revenue_lakhs","sum"),
                      deals=("sale_id","nunique"))
                 .reset_index().sort_values("revenue", ascending=False))
    total_clients = client_df["client_id"].nunique()
    avg_rev_client = client_df["revenue"].mean()
    top_industry   = client_df.groupby("industry")["revenue"].sum().idxmax()

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Active Clients",     total_clients)
    c2.metric("Avg Rev / Client",   f"₹{avg_rev_client:.1f}L")
    c3.metric("Top Industry",       top_industry)
    c4.metric("Total Revenue",      f"₹{fs['revenue_lakhs'].sum():.1f}L")

    st.markdown("---")

    # Treemap
    fig_tree = px.treemap(
        client_df.head(30),
        path=["industry","client_name"],
        values="revenue",
        title="Top 30 Clients — Revenue Treemap (Category → Client)",
        color="revenue",
        color_continuous_scale=["#1A1A2E","#E94560"],
    )
    fig_tree.update_layout(height=420)
    st.plotly_chart(fig_tree, use_container_width=True)

    st.markdown("---")

    # Industry donut + Tier bar
    ind_df = fs.groupby("industry")["revenue_lakhs"].sum().reset_index()
    fig_ind = px.pie(ind_df, values="revenue_lakhs", names="industry",
                     title="Revenue by Industry", hole=0.45,
                     color_discrete_sequence=PALETTE)
    fig_ind.update_layout(height=350)

    tier_df = fs.groupby("tier")["revenue_lakhs"].sum().reset_index()
    fig_tier = px.bar(tier_df, x="tier", y="revenue_lakhs",
                      title="Revenue by Seller Tier",
                      color="tier", color_discrete_sequence=PALETTE,
                      labels={"revenue_lakhs":"₹Lakhs","tier":"Tier"})
    fig_tier.update_layout(plot_bgcolor="white", height=350, showlegend=False)

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_ind,  use_container_width=True)
    col2.plotly_chart(fig_tier, use_container_width=True)

    st.markdown("---")

    # Client table
    st.subheader("Client Detail")
    ct = client_df.copy()
    ct["revenue"] = ct["revenue"].round(1)
    ct.columns = ["Client ID","Client","Industry","Tier","Revenue (₹L)","Deals"]
    st.dataframe(ct.drop("Client ID", axis=1), use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
# PAGE 6: PRODUCT ANALYSIS (Drill-Down)
# ════════════════════════════════════════════════════════════
elif page == "📦 Product Analysis":
    st.title("📦 Product Analysis")
    st.markdown("Ad format performance, category drill-down, format mix.")
    st.markdown("---")

    prod_df = (fs.groupby(["product_id","product_name","category","sub_category"])
               .agg(revenue=("revenue_lakhs","sum"),
                    deals=("sale_id","nunique"),
                    gp=("gross_profit_lakhs","sum"))
               .reset_index())
    prod_df["margin_pct"] = prod_df["gp"] / prod_df["revenue"]
    prod_df["rank"] = prod_df["revenue"].rank(ascending=False).astype(int)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Products",    prod_df["product_id"].nunique())
    c2.metric("Top Category",      prod_df.groupby("category")["revenue"].sum().idxmax())
    c3.metric("Top Product",       prod_df.loc[prod_df["revenue"].idxmax(), "product_name"])
    c4.metric("Best Margin",       f"{prod_df['margin_pct'].max():.1%}")

    st.markdown("---")

    # Drill-down: Category → Sub-Category → Product
    drill_level = st.radio("Drill Level", ["Category","Sub-Category","Product Name"], horizontal=True)

    if drill_level == "Category":
        grp = fs.groupby("category")["revenue_lakhs"].sum().reset_index()
        grp.columns = ["Label","Revenue"]
    elif drill_level == "Sub-Category":
        grp = fs.groupby(["category","sub_category"])["revenue_lakhs"].sum().reset_index()
        grp["Label"] = grp["category"] + " → " + grp["sub_category"]
        grp = grp[["Label","revenue_lakhs"]].rename(columns={"revenue_lakhs":"Revenue"})
    else:
        grp = fs.groupby(["category","product_name"])["revenue_lakhs"].sum().reset_index()
        grp["Label"] = grp["category"] + " → " + grp["product_name"]
        grp = grp[["Label","revenue_lakhs"]].rename(columns={"revenue_lakhs":"Revenue"})

    grp = grp.sort_values("Revenue", ascending=True)
    fig_drill = px.bar(grp, x="Revenue", y="Label", orientation="h",
                       title=f"Revenue by {drill_level}",
                       color="Revenue",
                       color_continuous_scale=["#1A1A2E","#E94560"],
                       labels={"Revenue":"₹Lakhs","Label":drill_level})
    fig_drill.update_layout(plot_bgcolor="white", height=380, showlegend=False)
    st.plotly_chart(fig_drill, use_container_width=True)

    st.markdown("---")

    # Trend by category + Mix by quarter
    trend_df = (fs.groupby(["month_dt","month_year","category"])["revenue_lakhs"]
                .sum().reset_index().sort_values("month_dt"))
    fig_trend = px.line(trend_df, x="month_year", y="revenue_lakhs", color="category",
                        title="Revenue Trend by Category",
                        color_discrete_sequence=PALETTE,
                        labels={"revenue_lakhs":"₹Lakhs","month_year":"Month"})
    fig_trend.update_layout(plot_bgcolor="white", height=320)

    mix_df = (fs.groupby(["quarter","category"])["revenue_lakhs"]
              .sum().reset_index())
    fig_mix = px.bar(mix_df, x="quarter", y="revenue_lakhs", color="category",
                     barmode="relative",
                     title="Product Mix by Quarter (100% Stacked)",
                     color_discrete_sequence=PALETTE,
                     labels={"revenue_lakhs":"₹Lakhs"})
    fig_mix.update_layout(plot_bgcolor="white", height=320, yaxis_tickformat=".0f")

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_trend, use_container_width=True)
    col2.plotly_chart(fig_mix,   use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 7: MONTHLY TRENDS
# ════════════════════════════════════════════════════════════
elif page == "📅 Monthly Trends":
    st.title("📅 Monthly Trends")
    st.markdown("MoM growth, YoY comparison, 3M rolling avg, seasonality heatmap.")
    st.markdown("---")

    rev_ytd = fpl[fpl["year"] == fpl["year"].max()]["revenue_lakhs"].sum()
    rev_qtd = fpl[(fpl["year"] == fpl["year"].max()) &
                  (fpl["quarter"] == fpl[fpl["year"] == fpl["year"].max()]["quarter"].max())]["revenue_lakhs"].sum()
    last_mom = fpl["mom_pct"].dropna().iloc[-1] if len(fpl["mom_pct"].dropna()) else None
    last_yoy = fpl["yoy_pct"].dropna().iloc[-1] if len(fpl["yoy_pct"].dropna()) else None

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Revenue YTD",   f"₹{rev_ytd:.1f}L")
    c2.metric("Revenue QTD",   f"₹{rev_qtd:.1f}L")
    c3.metric("Latest MoM",    f"{last_mom:.1%}" if last_mom else "—",
              delta=f"{last_mom:.1%}" if last_mom else None)
    c4.metric("Latest YoY",    f"{last_yoy:.1%}" if last_yoy else "—",
              delta=f"{last_yoy:.1%}" if last_yoy else None)

    st.markdown("---")

    # 3-line chart: Actual vs PY vs 3M Rolling
    fpl["rolling_3m"] = fpl["revenue_lakhs"].rolling(3, min_periods=1).mean()
    fig_3line = go.Figure()
    fig_3line.add_scatter(x=fpl["month_year"], y=fpl["revenue_lakhs"],
                          name="Current", mode="lines+markers",
                          line=dict(color=COLORS["primary"], width=3))
    fig_3line.add_scatter(x=fpl["month_year"], y=fpl["revenue_py"],
                          name="Prior Year", mode="lines",
                          line=dict(color=COLORS["dark"], dash="dash", width=2))
    fig_3line.add_scatter(x=fpl["month_year"], y=fpl["rolling_3m"],
                          name="3M Rolling Avg", mode="lines",
                          line=dict(color=COLORS["blue"], dash="dot", width=2))
    fig_3line.update_layout(
        title="Revenue: Actual vs Prior Year vs 3M Rolling Average",
        plot_bgcolor="white", height=360,
        legend=dict(orientation="h", y=-0.2),
        xaxis_title="Month", yaxis_title="₹ Lakhs"
    )
    st.plotly_chart(fig_3line, use_container_width=True)

    st.markdown("---")

    # MoM bar (green/red) + Heatmap
    fpl_mom = fpl.dropna(subset=["mom_pct"]).copy()
    fpl_mom["color"] = fpl_mom["mom_pct"].apply(lambda x: COLORS["green"] if x >= 0 else COLORS["red"])

    fig_mom = go.Figure()
    fig_mom.add_bar(
        x=fpl_mom["month_year"],
        y=fpl_mom["mom_pct"],
        marker_color=fpl_mom["color"],
        text=fpl_mom["mom_pct"].apply(lambda x: f"{x:.1%}"),
        textposition="outside",
    )
    fig_mom.add_hline(y=0, line_color="black", line_width=1)
    fig_mom.update_layout(
        title="Month-over-Month Growth %",
        yaxis_tickformat=".0%",
        plot_bgcolor="white",
        height=320,
        xaxis_title="Month"
    )

    # Heatmap: Month × Year
    heat_df = fpl.pivot_table(index="month_name", columns="year",
                               values="revenue_lakhs", aggfunc="sum")
    month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    heat_df = heat_df.reindex([m for m in month_order if m in heat_df.index])
    fig_heat = px.imshow(
        heat_df,
        title="Revenue Heatmap: Month × Year",
        color_continuous_scale=["white","#E94560"],
        labels=dict(color="₹Lakhs"),
        text_auto=".1f",
    )
    fig_heat.update_layout(height=320)

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_mom,  use_container_width=True)
    col2.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")

    # Monthly summary table
    st.subheader("Monthly Summary Table")
    tbl = fpl[["month_year","revenue_lakhs","revenue_py","yoy_pct","mom_pct",
               "revenue_target_lakhs","gross_margin_pct","ebitda_margin_pct"]].copy()
    tbl.columns = ["Month","Revenue","Prior Year","YoY %","MoM %","Target","GM %","EBITDA %"]
    for c in ["Revenue","Prior Year","Target"]:
        tbl[c] = tbl[c].apply(lambda x: f"₹{x:.1f}L" if pd.notna(x) else "—")
    for c in ["YoY %","MoM %","GM %","EBITDA %"]:
        tbl[c] = tbl[c].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "—")
    st.dataframe(tbl, use_container_width=True, hide_index=True)
