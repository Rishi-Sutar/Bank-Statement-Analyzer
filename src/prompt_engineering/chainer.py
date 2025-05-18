from src.prompt_engineering.templates import data_extractor_template, anomaly_detection_template, financial_advisior_template
from src.prompt_engineering.schema import DataExtractor, AnomalyDetection, FinancialAdvisor

from langchain_google_genai import ChatGoogleGenerativeAI
import dotenv
import os   

dotenv.load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

data_extractor_llm = llm.with_structured_output(DataExtractor)
anomaly_detector_llm = llm.with_structured_output(AnomalyDetection)
financial_advisor_llm = llm.with_structured_output(FinancialAdvisor)

data_extractor_chain = data_extractor_template | data_extractor_llm
anomaly_detection_chain = anomaly_detection_template | anomaly_detector_llm
financial_advisor_chain = financial_advisior_template | financial_advisor_llm

