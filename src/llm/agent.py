import dotenv

from src.prompt_engineering.schema import StateSchema
from src.prompt_engineering.chainer import data_extractor_chain, anomaly_detection_chain, financial_advisor_chain
from langgraph.graph import StateGraph, END

# Load env
dotenv.load_dotenv()
    
def extract_transactions_node(state: StateSchema):
    output = data_extractor_chain.invoke({"messages": [{"role": "user", "content": state.input}]})
    return {"extracted_data": output.dict()}

def detect_anomalies_node(state: StateSchema):
    output = anomaly_detection_chain.invoke({"messages": [{"role": "user", "content": state.input}]})
    return {"anomaly_report": output}

def financial_advice_node(state: StateSchema):
    output = financial_advisor_chain.invoke({"messages": [{"role": "user", "content": state.input}]})
    return {"financial_advice": output}

# Build LangGraph
builder = StateGraph(state_schema=StateSchema)
builder.add_node("extract_transactions", extract_transactions_node)
builder.add_node("detect_anomalies", detect_anomalies_node)
builder.add_node("financial", financial_advice_node)

builder.set_entry_point("extract_transactions")
builder.add_edge("extract_transactions", "detect_anomalies")
builder.add_edge("detect_anomalies", "financial")
builder.add_edge("financial", END)

graph = builder.compile()

