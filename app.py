import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="India CPI & Inflation Dashboard",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */
    .main {
        padding-top: 1rem;
    }

    /* Dashboard title */
    .dashboard-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .dashboard-subtitle {
        font-size: 1.05rem;
        color: #666666;
        margin-bottom: 1.5rem;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e1e5e8;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e5e5;
    }

    /* Info boxes */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    file_path = "data/cleaned/CPI_cleaned.xlsx"

    df = pd.read_excel(file_path)

    # Convert month to text
    df["month"] = df["month"].astype(str)

    return df


df = load_data()


# ============================================================
# DATA VALIDATION
# ============================================================

required_columns = [
    "month",
    "rural_cpi",
    "urban_cpi",
    "combined_cpi",
    "rural_inflation",
    "urban_inflation",
    "combined_inflation",
    "Rural_Urban_CPI_Gap",
    "Combined_CPI_MoM_Change",
    "Combined_CPI_MoM_Pct"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        "The following required columns are missing from "
        "CPI_cleaned.xlsx:"
    )

    st.write(missing_columns)

    st.stop()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🇮🇳 CPI Dashboard")

st.sidebar.markdown(
    "### Dashboard Navigation"
)

page = st.sidebar.radio(
    "Select Section",
    [
        "Overview",
        "Rural vs Urban",
        "Inflation Analysis",
        "Data Explorer"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    ### Dataset Information

    **Period**

    January 2025 – July 2026

    **Frequency**

    Monthly

    **Observations**

    19

    **Latest Observation**

    July 2026
    """
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "India CPI & Inflation Analysis | "
    "Portfolio Data Analytics Project"
)


# ============================================================
# COMMON VALUES
# ============================================================

latest = df.iloc[-1]

first = df.iloc[0]

latest_cpi = latest["combined_cpi"]

latest_inflation = latest["combined_inflation"]

first_cpi = first["combined_cpi"]

cpi_growth = (
    (latest_cpi - first_cpi)
    / first_cpi
) * 100

cpi_point_change = latest_cpi - first_cpi

latest_rural_cpi = latest["rural_cpi"]

latest_urban_cpi = latest["urban_cpi"]

latest_rural_inflation = latest["rural_inflation"]

latest_urban_inflation = latest["urban_inflation"]

latest_inflation_gap = (
    latest_rural_inflation
    - latest_urban_inflation
)


# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================

if page == "Overview":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="dashboard-title">'
        '🇮🇳 India CPI & Inflation Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Consumer Price Index and inflation trends | '
        'January 2025 – July 2026'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    st.subheader("📌 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            label="Latest Combined CPI",
            value=f"{latest_cpi:.2f}"
        )

    with col2:

        st.metric(
            label="Latest Inflation",
            value=f"{latest_inflation:.2f}%"
        )

    with col3:

        st.metric(
            label="CPI Growth Since Jan-25",
            value=f"{cpi_growth:.2f}%"
        )

    with col4:

        st.metric(
            label="Rural–Urban Inflation Gap",
            value=f"{latest_inflation_gap:.2f} pp"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # COMBINED CPI TREND
    # --------------------------------------------------------

    st.subheader("📈 Combined CPI Trend")

    fig_cpi = go.Figure()

    fig_cpi.add_trace(
        go.Scatter(
            x=df["month"],
            y=df["combined_cpi"],
            mode="lines+markers",
            name="Combined CPI",
            hovertemplate=
                "<b>%{x}</b><br>"
                "Combined CPI: %{y:.2f}"
                "<extra></extra>"
        )
    )

    fig_cpi.update_layout(
        xaxis_title="Month",
        yaxis_title="Combined CPI",
        hovermode="x unified",
        template="plotly_white",
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig_cpi,
        use_container_width=True
    )

    # --------------------------------------------------------
    # CPI COMPARISON
    # --------------------------------------------------------

    st.subheader(
        "🏡 Rural vs Urban vs Combined CPI"
    )

    fig_comparison = go.Figure()

    fig_comparison.add_trace(
        go.Scatter(
            x=df["month"],
            y=df["rural_cpi"],
            mode="lines+markers",
            name="Rural CPI",
            hovertemplate=
                "<b>%{x}</b><br>"
                "Rural CPI: %{y:.2f}"
                "<extra></extra>"
        )
    )

    fig_comparison.add_trace(
        go.Scatter(
            x=df["month"],
            y=df["urban_cpi"],
            mode="lines+markers",
            name="Urban CPI",
            hovertemplate=
                "<b>%{x}</b><br>"
                "Urban CPI: %{y:.2f}"
                "<extra></extra>"
        )
    )

    fig_comparison.add_trace(
        go.Scatter(
            x=df["month"],
            y=df["combined_cpi"],
            mode="lines+markers",
            name="Combined CPI",
            hovertemplate=
                "<b>%{x}</b><br>"
                "Combined CPI: %{y:.2f}"
                "<extra></extra>"
        )
    )

    fig_comparison.update_layout(
        xaxis_title="Month",
        yaxis_title="CPI",
        hovermode="x unified",
        template="plotly_white",
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig_comparison,
        use_container_width=True
    )

    # --------------------------------------------------------
    # MONTHLY CPI MOVEMENT
    # --------------------------------------------------------

    st.subheader(
        "📊 Monthly Combined CPI Movement"
    )

    fig_mom = go.Figure()

    fig_mom.add_trace(
        go.Bar(
            x=df["month"],
            y=df["Combined_CPI_MoM_Pct"],
            name="MoM CPI Change",
            text=[
                f"{value:.2f}%"
                if pd.notna(value)
                else ""
                for value in df["Combined_CPI_MoM_Pct"]
            ],
            textposition="outside",
            hovertemplate=
                "<b>%{x}</b><br>"
                "MoM CPI Change: %{y:.2f}%"
                "<extra></extra>"
        )
    )

    fig_mom.add_hline(
        y=0,
        line_dash="dash"
    )

    fig_mom.update_layout(
        xaxis_title="Month",
        yaxis_title="MoM CPI Change (%)",
        template="plotly_white",
        height=420,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig_mom,
        use_container_width=True
    )

    # --------------------------------------------------------
    # KEY INSIGHT
    # --------------------------------------------------------

    st.subheader("💡 Key Insight")

    st.info(
        f"""
        **Combined CPI increased from {first_cpi:.2f} in
        January 2025 to {latest_cpi:.2f} in July 2026.**

        This represents an increase of **{cpi_point_change:.2f}
        CPI points**, equivalent to approximately
        **{cpi_growth:.2f}% growth** over the study period.
        """
    )

    # --------------------------------------------------------
    # PROJECT SUMMARY
    # --------------------------------------------------------

    st.subheader("📌 Project Summary")

    st.markdown(
        """
        This dashboard analyzes monthly Consumer Price Index
        (CPI) and inflation data to understand:

        - Overall CPI movement
        - Rural versus urban price differences
        - Inflation trends
        - Month-over-month CPI movements
        - Rural–urban inflation differences

        The dataset was prepared in Excel and analyzed using
        Python, Pandas, Plotly, and Streamlit.
        """
    )


# ============================================================
# PAGE 2 — RURAL VS URBAN
# ============================================================

elif page == "Rural vs Urban":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="dashboard-title">'
        '🏡 Rural vs Urban Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Comparing rural and urban CPI and inflation patterns'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    st.subheader("📌 Rural–Urban Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Latest Rural CPI",
            f"{latest_rural_cpi:.2f}"
        )

    with col2:

        st.metric(
            "Latest Urban CPI",
            f"{latest_urban_cpi:.2f}"
        )

    with col3:

        st.metric(
            "Rural Inflation",
            f"{latest_rural_inflation:.2f}%"
        )

    with col4:

        st.metric(
            "Urban Inflation",
            f"{latest_urban_inflation:.2f}%"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # CPI COMPARISON
    # --------------------------------------------------------

    st.subheader("📈 Rural vs Urban CPI")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["month"],
            y=df["rural_cpi"],
            mode="lines+markers",
            name="Rural CPI",
            hovertemplate=
                "<b>%{x}</b><br>"
                "Rural CPI: %{y:.2f}"
                "<extra></extra>"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["month"],
            y=df["urban_cpi"],
            mode="lines+markers",
            name="Urban CPI",
            hovertemplate=
                "<b>%{x}</b><br>"
                "Urban CPI: %{y:.2f}"
                "<extra></extra>"
        )
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="CPI",
        hovermode="x unified",
        template="plotly_white",
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # CPI GAP
    # --------------------------------------------------------

    st.subheader("⚖️ Rural–Urban CPI Gap")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["month"],
            y=df["Rural_Urban_CPI_Gap"],
            name="Rural–Urban CPI Gap",
            hovertemplate=
                "<b>%{x}</b><br>"
                "CPI Gap: %{y:.2f}"
                "<extra></extra>"
        )
    )

    fig.add_hline(
        y=0,
        line_dash="dash"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Rural CPI − Urban CPI",
        template="plotly_white",
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # INFLATION DATA
    # --------------------------------------------------------

    inflation_df = df.dropna(
        subset=[
            "rural_inflation",
            "urban_inflation"
        ]
    ).copy()

    # --------------------------------------------------------
    # RURAL VS URBAN INFLATION
    # --------------------------------------------------------

    st.subheader(
        "💹 Rural vs Urban Inflation"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=inflation_df["month"],
            y=inflation_df["rural_inflation"],
            mode="lines+markers",
            name="Rural Inflation",
            hovertemplate=
                "<b>%{x}</b><br>"
                "Rural Inflation: %{y:.2f}%"
                "<extra></extra>"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=inflation_df["month"],
            y=inflation_df["urban_inflation"],
            mode="lines+markers",
            name="Urban Inflation",
            hovertemplate=
                "<b>%{x}</b><br>"
                "Urban Inflation: %{y:.2f}%"
                "<extra></extra>"
        )
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Inflation (%)",
        hovermode="x unified",
        template="plotly_white",
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # INFLATION GAP
    # --------------------------------------------------------

    inflation_df["Inflation_Gap"] = (
        inflation_df["rural_inflation"]
        - inflation_df["urban_inflation"]
    )

    st.subheader(
        "⚖️ Rural–Urban Inflation Gap"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=inflation_df["month"],
            y=inflation_df["Inflation_Gap"],
            name="Inflation Gap",
            hovertemplate=
                "<b>%{x}</b><br>"
                "Inflation Gap: %{y:.2f} pp"
                "<extra></extra>"
        )
    )

    fig.add_hline(
        y=0,
        line_dash="dash"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Inflation Gap (percentage points)",
        template="plotly_white",
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # KEY INSIGHT
    # --------------------------------------------------------

    st.subheader("💡 Key Insight")

    st.info(
        f"""
        In **July 2026**, rural inflation was
        **{latest_rural_inflation:.2f}%**, while urban inflation
        was **{latest_urban_inflation:.2f}%**.

        Therefore, rural inflation was
        **{latest_inflation_gap:.2f} percentage points higher**
        than urban inflation.
        """
    )


# ============================================================
# PAGE 3 — INFLATION ANALYSIS
# ============================================================

elif page == "Inflation Analysis":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="dashboard-title">'
        '💹 Inflation & Price Movement Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Understanding inflation trends and month-over-month '
        'CPI movements'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # INFLATION DATA
    # --------------------------------------------------------

    inflation_df = df.dropna(
        subset=["combined_inflation"]
    ).copy()

    first_inflation = (
        inflation_df.iloc[0]["combined_inflation"]
    )

    latest_inflation_value = (
        inflation_df.iloc[-1]["combined_inflation"]
    )

    inflation_change = (
        latest_inflation_value
        - first_inflation
    )

    max_mom = df["Combined_CPI_MoM_Pct"].max()

    min_mom = df["Combined_CPI_MoM_Pct"].min()

    # --------------------------------------------------------
    # FIND EXTREME MONTHS
    # --------------------------------------------------------

    max_row = df.loc[
        df["Combined_CPI_MoM_Pct"].idxmax()
    ]

    min_row = df.loc[
        df["Combined_CPI_MoM_Pct"].idxmin()
    ]

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    st.subheader("📌 Inflation Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Latest Inflation",
            f"{latest_inflation_value:.2f}%"
        )

    with col2:

        st.metric(
            "Inflation Change Since Jan-26",
            f"+{inflation_change:.2f} pp"
        )

    with col3:

        st.metric(
            "Highest MoM CPI Change",
            f"{max_mom:.2f}%"
        )

    with col4:

        st.metric(
            "Lowest MoM CPI Change",
            f"{min_mom:.2f}%"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # COMBINED INFLATION TREND
    # --------------------------------------------------------

    st.subheader(
        "📈 Combined Inflation Trend"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=inflation_df["month"],
            y=inflation_df["combined_inflation"],
            mode="lines+markers",
            name="Combined Inflation",
            hovertemplate=
                "<b>%{x}</b><br>"
                "Inflation: %{y:.2f}%"
                "<extra></extra>"
        )
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Inflation (%)",
        hovermode="x unified",
        template="plotly_white",
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # MONTH-OVER-MONTH CPI MOVEMENT
    # --------------------------------------------------------

    st.subheader(
        "📊 Month-over-Month CPI Movement"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["month"],
            y=df["Combined_CPI_MoM_Pct"],
            name="MoM CPI Change",
            text=[
                f"{value:.2f}%"
                if pd.notna(value)
                else ""
                for value in df["Combined_CPI_MoM_Pct"]
            ],
            textposition="outside",
            hovertemplate=
                "<b>%{x}</b><br>"
                "MoM Change: %{y:.2f}%"
                "<extra></extra>"
        )
    )

    fig.add_hline(
        y=0,
        line_dash="dash"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="MoM CPI Change (%)",
        template="plotly_white",
        height=420,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # SIGNIFICANT MOVEMENTS
    # --------------------------------------------------------

    st.subheader("🔎 Significant Movements")

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"""
            **Largest Monthly Increase**

            **{max_row["month"]}**

            Combined CPI increased by

            **{max_row["Combined_CPI_MoM_Pct"]:.2f}%**
            """
        )

    with col2:

        st.warning(
            f"""
            **Largest Monthly Decline**

            **{min_row["month"]}**

            Combined CPI changed by

            **{min_row["Combined_CPI_MoM_Pct"]:.2f}%**
            """
        )

    # --------------------------------------------------------
    # KEY INSIGHT
    # --------------------------------------------------------

    st.subheader("💡 Key Insight")

    st.info(
        f"""
        Combined inflation increased from
        **{first_inflation:.2f}% in January 2026**
        to **{latest_inflation_value:.2f}% in July 2026**.

        This represents an increase of
        **{inflation_change:.2f} percentage points**.
        """
    )


# ============================================================
# PAGE 4 — DATA EXPLORER
# ============================================================

elif page == "Data Explorer":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="dashboard-title">'
        '📋 Data Explorer'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Explore and download the cleaned CPI dataset'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # DATA NOTE
    # --------------------------------------------------------

    st.info(
        """
        **Data note:** Inflation values are blank for the supplied
        January–December 2025 observations.

        These blanks have been retained because unavailable data
        should not be interpreted as 0% inflation.
        """
    )

    # --------------------------------------------------------
    # MONTH FILTER
    # --------------------------------------------------------

    st.subheader("🔎 Filter Data")

    selected_months = st.multiselect(
        "Select months",
        options=df["month"].tolist(),
        default=df["month"].tolist()
    )

    filtered_df = df[
        df["month"].isin(selected_months)
    ].copy()

    # --------------------------------------------------------
    # DATA TABLE
    # --------------------------------------------------------

    st.subheader("📊 Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Selected Data as CSV",
        data=csv,
        file_name="CPI_selected_data.csv",
        mime="text/csv"
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("📌 Dataset Summary")

    if len(filtered_df) > 0:

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Selected Records",
                len(filtered_df)
            )

        with col2:

            st.metric(
                "Average Combined CPI",
                f"{filtered_df['combined_cpi'].mean():.2f}"
            )

        with col3:

            st.metric(
                "Maximum Combined CPI",
                f"{filtered_df['combined_cpi'].max():.2f}"
            )

        with col4:

            st.metric(
                "Minimum Combined CPI",
                f"{filtered_df['combined_cpi'].min():.2f}"
            )

    else:

        st.warning(
            "Please select at least one month."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Source: Government of India CPI / Inflation data • "
    "Period: January 2025 – July 2026 • "
    "Frequency: Monthly • "
    "July 2026 figures are provisional."
)