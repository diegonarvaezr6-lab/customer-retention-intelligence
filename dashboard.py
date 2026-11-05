import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from html import escape

st.set_page_config(
    page_title="Customer Retention Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# DESIGN SYSTEM
# -------------------------------

BG = "#080F1D"
CARD = "#121F33"
BORDER = "#25364F"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"
CYAN = "#38BDF8"
GREEN = "#34D399"
RED = "#FB7185"
AMBER = "#FBBF24"

st.markdown("""
<style>
.stApp {
    background: #080F1D;
    color: #F1F5F9;
}
[data-testid="stSidebar"] {
    background: #101B2D;
    border-right: 1px solid #25364F;
}
.block-container {
    max-width: 1550px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #F1F5F9 !important;
    letter-spacing: -0.5px;
}
.hero {
    background: linear-gradient(120deg, #152D49, #0E192B);
    border: 1px solid #284463;
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 26px;
}
.eyebrow {
    color: #38BDF8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}
.hero-title {
    color: #F8FAFC;
    font-size: clamp(28px, 3vw, 42px);
    font-weight: 750;
    margin: 12px 0;
}
.hero-subtitle {
    color: #AFC0D3;
    font-size: 15px;
}
.kpi-card {
    background: #121F33;
    border: 1px solid #25364F;
    border-radius: 16px;
    padding: 22px;
    min-height: 145px;
}
.kpi-label {
    color: #94A3B8;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.kpi-value {
    color: #F8FAFC;
    font-size: clamp(23px, 2.2vw, 36px);
    font-weight: 750;
    margin-top: 14px;
}
.kpi-note {
    color: #94A3B8;
    font-size: 12px;
    margin-top: 8px;
}
.section-label {
    color: #38BDF8;
    font-size: 12px;
    letter-spacing: 1.5px;
    font-weight: 700;
    margin-top: 20px;
}
.insight-card {
    background: #121F33;
    border: 1px solid #25364F;
    border-left: 4px solid #38BDF8;
    border-radius: 12px;
    padding: 20px;
    min-height: 150px;
}
.insight-title {
    color: #F8FAFC;
    font-weight: 700;
    font-size: 16px;
}
.insight-text {
    color: #CBD5E1;
    font-size: 14px;
    margin-top: 10px;
    line-height: 1.6;
}
div[data-testid="stPlotlyChart"] {
    border: 1px solid #25364F;
    border-radius: 15px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# DATA
# -------------------------------

@st.cache_data
def load_data():
    data = pd.read_csv("data/telco_churn_clean.csv")
    required = [
        "customerID", "ChurnFlag", "Contract",
        "InternetService", "PaymentMethod",
        "MonthlyCharges", "tenure", "Churn"
    ]
    missing = [c for c in required if c not in data.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return data

df = load_data()

# -------------------------------
# FILTERS
# -------------------------------

st.sidebar.markdown("## ◈ INTELLIGENCE")
st.sidebar.caption("CUSTOMER RETENTION ANALYTICS")
st.sidebar.divider()

contracts = st.sidebar.multiselect(
    "Contract Type",
    sorted(df["Contract"].unique()),
    default=sorted(df["Contract"].unique())
)

internet = st.sidebar.multiselect(
    "Internet Service",
    sorted(df["InternetService"].unique()),
    default=sorted(df["InternetService"].unique())
)

payments = st.sidebar.multiselect(
    "Payment Method",
    sorted(df["PaymentMethod"].unique()),
    default=sorted(df["PaymentMethod"].unique())
)

filtered = df[
    df["Contract"].isin(contracts)
    & df["InternetService"].isin(internet)
    & df["PaymentMethod"].isin(payments)
].copy()

st.sidebar.divider()
st.sidebar.caption("DATA SOURCE: IBM TELCO SAMPLE DATASET")

# -------------------------------
# HERO
# -------------------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">CUSTOMER INTELLIGENCE / EXECUTIVE ANALYTICS</div>
    <div class="hero-title">Customer Retention Intelligence</div>
    <div class="hero-subtitle">
        Understand customer attrition, identify high-churn segments,
        and support evidence-based retention decisions.
    </div>
</div>
""", unsafe_allow_html=True)

if filtered.empty:
    st.warning("No customers match the selected filters.")
    st.stop()

# -------------------------------
# KPI METRICS
# -------------------------------

customers = len(filtered)
churned = int(filtered["ChurnFlag"].sum())
retained = customers - churned
churn_rate = churned / customers * 100
retention_rate = retained / customers * 100

churned_charges = filtered.loc[
    filtered["ChurnFlag"] == 1, "MonthlyCharges"
].sum()

def kpi(label, value, note, color=CYAN):
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{escape(label)}</div>
        <div class="kpi-value" style="color:{color}">
            {escape(value)}
        </div>
        <div class="kpi-note">{escape(note)}</div>
    </div>
    """

st.markdown('<div class="section-label">01 / EXECUTIVE PERFORMANCE</div>',
            unsafe_allow_html=True)
st.subheader("Portfolio Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(kpi("Total Customers", f"{customers:,}",
                    "Customers in selected segment"), unsafe_allow_html=True)
with c2:
    st.markdown(kpi("Churn Rate", f"{churn_rate:.2f}%",
                    "Share of customers who churned", RED),
                unsafe_allow_html=True)
with c3:
    st.markdown(kpi("Retention Rate", f"{retention_rate:.2f}%",
                    f"{retained:,} retained customers", GREEN),
                unsafe_allow_html=True)
with c4:
    st.markdown(kpi("Churned Monthly Charges",
                    f"${churned_charges:,.0f}",
                    "Historical charges, not forecast loss", AMBER),
                unsafe_allow_html=True)

st.caption(
    "Sample customer dataset. Churned monthly charges are the sum of "
    "monthly charges associated with churned customers, not verified revenue loss."
)

# -------------------------------
# CHART HELPERS
# -------------------------------

def churn_by(column):
    result = (
        filtered.groupby(column, as_index=False)
        .agg(
            Customers=("customerID", "count"),
            Churned=("ChurnFlag", "sum"),
            ChurnRate=("ChurnFlag", "mean")
        )
    )
    result["ChurnRate"] *= 100
    return result.sort_values("ChurnRate", ascending=False)

def chart_style(fig, height=380):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color="#CBD5E1", size=12),
        margin=dict(l=24, r=24, t=35, b=30),
        showlegend=False,
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="#26354A", zeroline=False),
        yaxis=dict(gridcolor="#26354A", zeroline=False)
    )
    return fig

def risk_color(rate):
    if rate >= 35:
        return RED
    if rate >= 20:
        return AMBER
    return GREEN

# -------------------------------
# CHARTS
# -------------------------------

st.markdown('<div class="section-label">02 / CUSTOMER RISK</div>',
            unsafe_allow_html=True)
st.subheader("Churn Drivers & Segments")

contract_data = churn_by("Contract")
internet_data = churn_by("InternetService")
payment_data = churn_by("PaymentMethod")

left, right = st.columns(2)

with left:
    fig = go.Figure(go.Bar(
        x=contract_data["Contract"],
        y=contract_data["ChurnRate"],
        marker_color=[risk_color(x) for x in contract_data["ChurnRate"]],
        text=contract_data["ChurnRate"].map(lambda x: f"{x:.1f}%"),
        textposition="outside",
        customdata=contract_data[["Customers", "Churned"]],
        hovertemplate=(
            "Contract: %{x}<br>Churn: %{y:.2f}%"
            "<br>Customers: %{customdata[0]:,}"
            "<br>Churned: %{customdata[1]:,}<extra></extra>"
        )
    ))
    fig.update_layout(title="Churn Rate by Contract")
    fig.update_yaxes(title="Churn Rate (%)", range=[0, 55])
    st.plotly_chart(chart_style(fig), use_container_width=True)

with right:
    fig = go.Figure(go.Bar(
        x=internet_data["InternetService"],
        y=internet_data["ChurnRate"],
        marker_color=[risk_color(x) for x in internet_data["ChurnRate"]],
        text=internet_data["ChurnRate"].map(lambda x: f"{x:.1f}%"),
        textposition="outside",
        customdata=internet_data[["Customers", "Churned"]],
        hovertemplate=(
            "Service: %{x}<br>Churn: %{y:.2f}%"
            "<br>Customers: %{customdata[0]:,}"
            "<br>Churned: %{customdata[1]:,}<extra></extra>"
        )
    ))
    fig.update_layout(title="Churn Rate by Internet Service")
    fig.update_yaxes(title="Churn Rate (%)", range=[0, 55])
    st.plotly_chart(chart_style(fig), use_container_width=True)

left, right = st.columns(2)

with left:
    fig = go.Figure(go.Bar(
        x=payment_data["ChurnRate"],
        y=payment_data["PaymentMethod"],
        orientation="h",
        marker_color=[risk_color(x) for x in payment_data["ChurnRate"]],
        text=payment_data["ChurnRate"].map(lambda x: f"{x:.1f}%"),
        textposition="outside",
        customdata=payment_data[["Customers", "Churned"]],
        hovertemplate=(
            "Payment: %{y}<br>Churn: %{x:.2f}%"
            "<br>Customers: %{customdata[0]:,}"
            "<br>Churned: %{customdata[1]:,}<extra></extra>"
        )
    ))
    fig.update_layout(title="Churn Rate by Payment Method")
    fig.update_xaxes(title="Churn Rate (%)", range=[0, 60])
    st.plotly_chart(chart_style(fig, 420), use_container_width=True)

with right:
    fig = px.histogram(
        filtered,
        x="tenure",
        color="Churn",
        nbins=24,
        barmode="group",
        color_discrete_map={"Yes": RED, "No": GREEN},
        labels={"tenure": "Customer Tenure (Months)"}
    )
    fig.update_layout(title="Customer Tenure Distribution", showlegend=True)
    fig = chart_style(fig, 420)
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# EXECUTIVE INSIGHTS
# -------------------------------

st.markdown('<div class="section-label">03 / STRATEGIC INSIGHTS</div>',
            unsafe_allow_html=True)
st.subheader("Executive Intelligence")

top_contract = contract_data.iloc[0]
top_payment = payment_data.iloc[0]
top_internet = internet_data.iloc[0]

insights = [
    (
        "Contract Exposure",
        f"{top_contract['Contract']} customers show a "
        f"{top_contract['ChurnRate']:.1f}% churn rate."
    ),
    (
        "Payment Behavior",
        f"{top_payment['PaymentMethod']} has the highest observed "
        f"payment-segment churn rate: {top_payment['ChurnRate']:.1f}%."
    ),
    (
        "Service Segment",
        f"{top_internet['InternetService']} has a "
        f"{top_internet['ChurnRate']:.1f}% churn rate."
    )
]

cols = st.columns(3)
for col, (title, description) in zip(cols, insights):
    with col:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">{escape(title)}</div>
                <div class="insight-text">{escape(description)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("### Recommended Business Actions")
st.markdown("""
1. **Prioritize retention research** for segments with high observed churn.
2. **Investigate onboarding and service quality** among newer customers.
3. **Test targeted retention initiatives** using controlled experiments.
4. **Monitor churn rates over time** when longitudinal data becomes available.

These findings describe associations in sample data and do not establish causation.
""")

st.divider()
st.caption(
    "CUSTOMER RETENTION INTELLIGENCE | "
    "Python • Pandas • Plotly • Streamlit | Portfolio Demonstration"
)
