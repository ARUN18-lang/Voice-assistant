import os 
from dotenv import load_dotenv, find_dotenv

def load_env():
    _ = load_dotenv(find_dotenv())

def get_serper_api_key():
    load_env()
    serper = os.getenv('SERPAPI_API_KEY')    
    return serper

def get_sarvam_api_key():
    load_env()
    sarvam = os.getenv('SARVAM_API_KEY')
    return sarvam

def get_financial_api_key():
    load_env()
    financial = os.getenv('FINANCIAL_API_KEY')
    return financial

def get_groq_api_key():
    load_env()
    groq_api_key = os.getenv("GROQ_API_KEY")
    return groq_api_key

def get_hf_token():
    load_env()
    hf_token = os.getenv('HF_API_TOKEN')
    return hf_token
