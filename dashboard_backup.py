import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Customer Retention Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium dark theme
st.markdown("""
<style>
.stApp {
    background: #0B1220;
    color: #F8FAFC;
}
[data-testid="stSidebar"] {
    background: #111C2E;
}
.block-container {
    padding-top: 2rem;
    max-width: 1450px;
}
h1, h2, h3 {
    color: #F8FAFC !important;
}
div[data-testid="stMetric"] {
    background: #172235;
    padding: 22px;
    border: 1px solid #26354A;
    border-radius: 14px;
}
div[data-testid="stMetricValue"] {
    color: #F8FAFC;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/telco_churn_clean.csv")

df = load_data()

# Sidebar filters
st.sidebar.title("◈ Intelligence Filters")

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

filtered = df[
    df["Contract"].isin(contracts)
    & df["InternetService"].isin(internet)
].copy()

st.title("Customer Retention Intelligence")
st.caption("CUSTOMER ANALYTICS  /  EXECUTIVE OVERVIEW")
st.info("Portfolio demonstration using the IBM Telco Customer Churn sample dataset.")

if filtered.empty:
    st.warning("No customers match the selected filters.")
    st.stop()

# KPIs
customers = len(filtered)
churned = int(filtered["ChurnFlag"].sum())
retained = customers - churned
churn_rate = churned / customers * 100
monthly_charges_churned = filtered.loc[
    filtered["ChurnFlag"] == 1, "MonthlyCharges"
].sum()

st.markdown("### Executive Performance")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Customers", f"{customers:,}")
c2.metric("Churn Rate", f"{churn_rate:.2f}%")
c3.metric("Retained Customers", f"{retained:,}")
c4.metric("Churned Monthly Charges", f"${monthly_charges_churned:,.0f}")

st.caption(
    "Churned Monthly Charges represents the sum of monthly charges "
    "for churned customers, not a verified revenue-loss forecast."
)

# Charts
def churn_by(column):
    result = (
        filtered.groupby(column, as_index=False)
        .agg(
            Customers=("customerID", "count"),
            ChurnRate=("ChurnFlag", "mean")
        )
    )
    result["ChurnRate"] *= 100
    return result.sort_values("ChurnRate", ascending=False)

def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#172235",
        plot_bgcolor="#172235",
        font_color="#CBD5E1",
        margin=dict(l=20, r=20, t=50, b=20),
        coloraxis_showscale=False
    )
    return fig

left, right = st.columns(2)

with left:
    st.subheader("Churn by Contract")
    contract_data = churn_by("Contract")
    fig = px.bar(
        contract_data,
        x="Contract",
        y="ChurnRate",
        color="ChurnRate",
        color_continuous_scale=["#34D399", "#38BDF8", "#FB7185"],
        labels={"ChurnRate": "Churn Rate (%)"},
        hover_data=["Customers"]
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

with right:
    st.subheader("Churn by Internet Service")
    internet_data = churn_by("InternetService")
    fig = px.bar(
        internet_data,
        x="InternetService",
        y="ChurnRate",
        color="ChurnRate",
        color_continuous_scale=["#34D399", "#38BDF8", "#FB7185"],
        labels={"ChurnRate": "Churn Rate (%)"},
        hover_data=["Customers"]
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("Churn by Payment Method")
    payment_data = churn_by("PaymentMethod")
    fig = px.bar(
        payment_data,
        x="ChurnRate",
        y="PaymentMethod",
        orientation="h",
        color="ChurnRate",
        color_continuous_scale=["#34D399", "#38BDF8", "#FB7185"],
        labels={"ChurnRate": "Churn Rate (%)", "PaymentMethod": ""},
        hover_data=["Customers"]
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

with right:
    st.subheader("Customer Tenure Distribution")
    fig = px.histogram(
        filtered,
        x="tenure",
        color="Churn",
        nbins=24,
        barmode="overlay",
        color_discrete_map={"Yes": "#FB7185", "No": "#34D399"},
        labels={"tenure": "Tenure (Months)"}
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

# Business insights
st.markdown("---")
st.subheader("Business Intelligence Insights")

highest_contract = contract_data.iloc[0]
highest_payment = payment_data.iloc[0]

st.markdown(
    f"""
**Contract Risk:** {highest_contract['Contract']} customers have
a churn rate of **{highest_contract['ChurnRate']:.1f}%**.

**Payment Pattern:** {highest_payment['PaymentMethod']} customers
have a churn rate of **{highest_payment['ChurnRate']:.1f}%**.

**Recommendation:** Investigate retention strategies for
high-churn segments and test interventions before scaling.
These patterns are associations, not evidence of causation.
"""
)

st.markdown("---")
st.caption("Built with Python, Pandas, Plotly & Streamlit | Portfolio Project")
