from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class Transaction(BaseModel):
    Transaction_Date: str
    Posted_Date: str
    Transaction_ID: str
    Description: str
    Withdrawal: Optional[float] = None
    Deposit: Optional[float] = None
    Balance: float
    Category: str

class DataExtractor(BaseModel):
    transactions: List[Transaction]

class AnomalyDetection(BaseModel):
    anomalies: List[Dict[str, Any]] = Field(default_factory=list)
    summary: Optional[str] = None
    advice: Optional[str] = None
    
class FinancialAdvisor(BaseModel):
    advice: str
    summary: Optional[str] = None
    recommendations: Optional[List[str]] = Field(default_factory=list)

class StateSchema(BaseModel):
    input: str
    extracted_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    anomaly_report: Optional[AnomalyDetection] = None
    financial_advice: Optional[FinancialAdvisor] = None