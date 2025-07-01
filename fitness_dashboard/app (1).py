import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Fitness Metrics Dashboard", layout="wide")
st.title("📊 Fitness Metrics Dashboard")

uploaded_file = st.file_uploader("Upload your Fitness CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    numeric_columns = ["Step Count", "Distance", "Energy Burned", 
                       "Flights Climbed", "Walking Double Support Percentage", 
                       "Walking Speed"]

    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    data["Date"] = pd.to_datetime(data["Date"])

    daily_avg_metrics = data.groupby("Date")[numeric_columns].mean().reset_index()

    daily_avg_metrics_melted = daily_avg_metrics.melt(
        id_vars=["Date"], 
        value_vars=numeric_columns,
        var_name="variable",
        value_name="value"
    )

    st.subheader("🌳 Treemap of Daily Averages")
    fig_treemap = px.treemap(daily_avg_metrics_melted,
                              path=["variable"],
                              values="value",
                              color="variable",
                              hover_data=["value"],
                              title="Daily Averages for Different Metrics")
    st.plotly_chart(fig_treemap, use_container_width=True)

    st.subheader("📈 Time Series Trends")
    for col in numeric_columns:
        fig_line = px.line(daily_avg_metrics, x="Date", y=col, title=f"{col} Over Time")
        st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("📊 Box Plots to Analyze Distribution")
    fig_box = px.box(data, y=numeric_columns, title="Distribution of Fitness Metrics")
    st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("📉 Correlation Heatmap")
    corr = data[numeric_columns].corr()
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="Viridis"
    ))
    fig_heatmap.update_layout(title="Correlation Heatmap of Metrics")
    st.plotly_chart(fig_heatmap, use_container_width=True)

else:
    st.info("Please upload a CSV file to proceed.")
