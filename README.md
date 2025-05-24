# 🏦 Bank Statement Analyzer

An intelligent Bank Statement Analyzer that extracts and analyzes financial data from images or PDFs of bank statements. It generates KPIs, insightful visualizations, anomaly detection, and personalized financial advice. Powered by LangGraph and Gemini 1.5 Flash for advanced LLM-driven financial reasoning.

## 🚀 Features

- 📥 Upload bank statement as PDF or image

- 🔍 OCR-based text extraction using EasyOCR

- 🧠 LLM-based processing with Gemini 1.5 Flash via LangGraph

- 📊 Automatic generation of financial KPIs

- 📈 Interactive visualizations

- ⚠️ Anomaly detection in spending or deposits

- 💡 Tailored financial advice based on your statement

## 🛠️ Tech Stack
Frontend: Streamlit

OCR: EasyOCR

LLM: Gemini 1.5 Flash (via LangGraph)

Data Analysis: Pandas, NumPy

Visualization: Matplotlib / Plotly / Seaborn

LangGraph: For structured LLM output workflows

## ⚙️ Installation

1. Clone the repository from github

```bash
git clone https://github.com/your-username/bank-statement-analyzer.git
cd bank-statement-analyzer
```

2. Create and activate virtual envirornment

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```
4. Run the app using streamlit

```bash
streamlit run app.py
```

## 🧪 Usage

1. Upload a PDF or image of a bank statement.

2. Let the app extract and analyze the data.

3. View:

    - Key Financial Metrics 
        
        - Total Inflow / Outflow

        - Monthly Savings Ratio

        - Highest Spending Categories

        - Average Daily/Monthly Balance

        - Number of Transactions

        - Recurring Payments

    - Visualizations of your transactions

    - Anomalies (e.g. suspicious charges or unusual deposits)

    - LLM-generated Financial Advice

## ✅ Conclusion
The Bank Statement Analyzer provides an end-to-end AI-powered solution to understand personal or business financial statements with minimal effort. By combining OCR, structured LLM workflows via LangGraph, and Gemini 1.5 Flash's powerful reasoning capabilities, the app not only extracts accurate data but also delivers actionable financial insights, visualizations, and anomaly detection.

Whether you're a finance enthusiast, a business owner, or just managing your personal budget, this tool empowers you to make informed decisions with ease.