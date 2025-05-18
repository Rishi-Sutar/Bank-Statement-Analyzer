from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Data Extractor Template
data_extractor_template = ChatPromptTemplate.from_messages(
    [
        ("system", """
        You are an intelligent assistant capable of analyzing text data and extracting structured information. 
        Your task is to extract transactions from the provided text and return them in JSON format with the following fields:
        - Transaction Date
        - Posted Date
        - Transaction ID
        - Description / Particulars
        - Withdrawal
        - Deposit
        - Balance
        - Category (classify into one of: ["Fuel", "Dining", "Subscription", "ATM", "Insurance", "Utilities", "Travel", "Parking", "Shopping", "Income", "Transfer", "Other"])

        Ensure the output is valid JSON with double quotes and null (not None) for missing values.
        """),
        ("user", """
        Example Input:
        01/01/2025 | 01/02/2025 | TXN12345 | Fuel Station | 50.00 | null | 950.00
        01/03/2025 | 01/04/2025 | TXN12346 | Grocery Store | null | 100.00 | 1050.00

        Example Output:
        [
            {{
                "Transaction_Date": "01/01/2025",
                "Posted_Date": "01/02/2025",
                "Transaction_ID": "TXN12345",
                "Description": "Fuel Station",
                "Withdrawal": 50.00,
                "Deposit": null,
                "Balance": 950.00,
                "Category": "Fuel"
            }},
            {{
                "Transaction_Date": "01/03/2025",
                "Posted_Date": "01/04/2025",
                "Transaction_ID": "TXN12346",
                "Description": "Grocery Store",
                "Withdrawal": null,
                "Deposit": 100.00,
                "Balance": 1050.00,
                "Category": "Shopping"
            }}
        ]
        """),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Anomaly Detection Template
anomaly_detection_template = ChatPromptTemplate.from_messages(
    [
        ("system", """
        You are an expert in anomaly detection. Your task is to analyze the provided dataset text and identify any anomalies. 
        Provide a detailed explanation of your approach, including assumptions and challenges.
        """),
        ("user", """
        Example Input:
        Transaction_ID: TXN12345, Amount: 5000, Category: "Fuel"
        Transaction_ID: TXN12346, Amount: 100000, Category: "Shopping"

        Example Output:
        Anomaly Detected:
        - Transaction_ID: TXN12346 has an unusually high amount for the "Shopping" category.
        Approach:
        - Compare transaction amounts against category-specific thresholds.
        - Use statistical methods like z-scores or interquartile ranges to identify outliers.
        """),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Financial Advisor Template
financial_advisior_template = ChatPromptTemplate.from_messages(
    [
        ("system", """
        You are a financial advisor. Based on the provided transaction data, summarize the user's financial activity and suggest ways to save money or improve financial health.
        """),
        ("user", """
        Example Input:
        [
            {{
                "Transaction_Date": "01/01/2025",
                "Description": "Fuel Station",
                "Withdrawal": 50.00,
                "Deposit": null,
                "Category": "Fuel"
            }},
            {{
                "Transaction_Date": "01/03/2025",
                "Description": "Grocery Store",
                "Withdrawal": null,
                "Deposit": 100.00,
                "Category": "Shopping"
            }}
        ]

        Example Output:
        Summary:
        - Total Withdrawals: $50.00
        - Total Deposits: $100.00
        - Top Spending Category: "Fuel"

        Suggestions:
        - Reduce spending on fuel by carpooling or using public transport.
        - Allocate a portion of deposits to a savings account for emergencies.
        """),
        MessagesPlaceholder(variable_name="messages"),
    ]
)