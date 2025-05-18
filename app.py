import streamlit as st
from PIL import Image
import numpy as np
import easyocr
import os
import pandas as pd
import plotly.express as px
from src.llm.agent import graph
import fitz

from src.utils.logger import logging
from src.utils.exception_handler import CustomException

analyze = False

import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"


# Streamlit App
st.set_page_config(page_title="Bank Statement Analyzer", layout="wide")
st.title("🧾 Bank Statement Analyzer")

with st.sidebar:

    uploaded_file = st.file_uploader("Upload your bank statement image", type=["jpg", "jpeg", "png", "pdf"])

    if uploaded_file:
        file_type = uploaded_file.type

        if file_type == "application/pdf":
            st.info("PDF uploaded.")
            analyze = st.button("Analyze PDF")
            if analyze:
                with st.spinner("Extracting text from PDF..."):
                    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                    extracted_text = ""
                    for page in doc:
                        extracted_text += page.get_text()
        else:
            image = Image.open(uploaded_file)
            analyze = st.button("Analyze Image")
            if analyze:
                with st.spinner("Extracting text using OCR..."):
                    reader = easyocr.Reader(['en'], gpu=False)
                    result = reader.readtext(np.array(image), detail=0)
                    extracted_text = "\n".join([line for line in result if len(line.strip()) > 3])
                    

if uploaded_file and analyze:
    try:
        logging.info("File uploaded: %s", uploaded_file.name)
        with st.spinner("Running LangGraph for extraction and analysis..."):
            result = graph.invoke({"input": extracted_text})
        logging.info("Graph analysis completed.")

        extracted_data = result.get("extracted_data")
        df = pd.DataFrame(extracted_data.get("transactions", []))

        expected_cols = ["Withdrawal", "Deposit", "Balance", "Transaction_Date", "Posted_Date", "Category"]
        missing_cols = [col for col in expected_cols if col not in df.columns]
        if missing_cols:
            msg = f"Missing columns in extracted data: {', '.join(missing_cols)}"
            logging.error(msg)
            st.error(msg)
            st.stop()

        # Clean up data
        df["Withdrawal"] = df["Withdrawal"].fillna(0.0)
        df["Deposit"] = df["Deposit"].fillna(0.0)
        df["Balance"] = df["Balance"].astype(float)
        df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"], errors='coerce')
        df["Posted_Date"] = pd.to_datetime(df["Posted_Date"], errors='coerce')

        # KPIs
        total_withdrawals = df["Withdrawal"].sum()
        total_deposits = df["Deposit"].sum()
        current_balance = df["Balance"].iloc[-1]
        num_transactions = len(df)
        top_category = df["Category"].value_counts().idxmax()
        avg_transaction = (df["Withdrawal"] + df["Deposit"]).mean()
        date_range = (df["Transaction_Date"].max() - df["Transaction_Date"].min()).days
        max_withdrawal = df["Withdrawal"].max()
        max_deposit = df["Deposit"].max()

        # Show KPIs
        st.subheader("📈 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💸 Total Withdrawals", f"₹{total_withdrawals:,.2f}")
        col2.metric("💰 Total Deposits", f"₹{total_deposits:,.2f}")
        col3.metric("🏦 Current Balance", f"₹{current_balance:,.2f}")
        col4.metric("🗓️ Date Range", f"{date_range} days")
        col1.metric("🔢 Transactions", num_transactions)
        col2.metric("💵 Avg Transaction", f"₹{avg_transaction:,.2f}")
        col3.metric("📈 Max Withdrawal", f"₹{max_withdrawal:,.2f}")
        col4.metric("📈 Max Deposit", f"₹{max_deposit:,.2f}")
        
        # Display the DataFrame
        st.subheader("📊 Transactions Data")
        st.dataframe(df, use_container_width=True)

        col5, col6 = st.columns(2)
        if df["Category"].nunique() > 2:
            with col5:
            # Visualizations
                st.subheader("📊 Category-wise Spending")
                category_chart = px.pie(df[df["Withdrawal"] > 0], values='Withdrawal', names='Category', title="Spending by Category")
                st.plotly_chart(category_chart, use_container_width=True)

        with col6:
            st.subheader("💵 Withdrawals vs Deposits")
            comparison_df = pd.DataFrame({
                "Type": ["Withdrawal", "Deposit"],
                "Amount": [total_withdrawals, total_deposits]
            })
            
            bar_chart = px.bar(comparison_df, x="Type", y="Amount", title="💵 Withdrawals vs Deposits", text_auto=True)
            st.plotly_chart(bar_chart, use_container_width=True)
            
        st.subheader("📉 Balance Over Time")
        balance_chart = px.line(df.sort_values("Transaction_Date"), x="Transaction_Date", y="Balance", title="Balance Trend")
        st.plotly_chart(balance_chart, use_container_width=True)

        df["Month"] = df["Transaction_Date"].dt.to_period("M").astype(str)
        monthly_summary = df.groupby("Month")[["Withdrawal", "Deposit"]].sum().reset_index()
        st.subheader("📆 Monthly Summary")
        monthly_chart = px.bar(monthly_summary, x="Month", y=["Withdrawal", "Deposit"], barmode="group")
        st.plotly_chart(monthly_chart, use_container_width=True)

        # Display JSON & Insights

        st.subheader("🚨 Anomaly Report")
        anomaly_report = result.get("anomaly_report")
        if anomaly_report:
            anomalies = getattr(anomaly_report, "anomalies", None)
            summary = getattr(anomaly_report, "summary", None)
            advice = getattr(anomaly_report, "advice", None)

            if summary:
                st.markdown("**Summary:**")
                st.info(summary)
            if advice:
                st.markdown("**Advice:**")
                st.write(advice)
            if anomalies:
                valid_anomalies = [a for a in anomalies if a]
                if valid_anomalies:
                    st.markdown("**Anomalies:**")
                    for anomaly in valid_anomalies:
                        st.write(f"- {anomaly}")
                else:
                    st.info("No anomalies detected.")
            if not (advice or summary or anomalies):
                st.info("No anomalies detected.")
        else:
            st.info("No anomalies detected.")

        st.subheader("💡 Financial Advice")
        financial_advice = result.get("financial_advice")
        if financial_advice:
            advice = getattr(financial_advice, "advice", None)
            summary = getattr(financial_advice, "summary", None)
            recommendations = getattr(financial_advice, "recommendations", None)

            if summary:
                st.markdown("**Summary:**")
                st.info(summary)
            if advice:
                st.markdown("**Advice:**")
                st.write(advice)
            if recommendations:
                st.markdown("**Recommendations:**")
                for rec in recommendations:
                    st.write(f"- {rec}")
            if not (advice or summary or recommendations):
                st.info("No financial advice available.")
        else:
            st.info("No financial advice available.")

    except Exception as e:
        logging.error("Exception occurred: %s", str(e))
        raise CustomException(e, sys)
