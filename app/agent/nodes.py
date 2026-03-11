import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.agent.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()
from app.schemas.intent_schema import IntentSchema
from app.utils.logger import logger

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)
intent_llm = llm.with_structured_output(IntentSchema)



def extract_intent(state: AgentState):

    question = state["question"]
    logger.info(f"Extracting intent from question: {question}")
    try:
        result = intent_llm.invoke(
            f"""
Extract the country and requested fields from the question.

Allowed fields:
capital
population
currency
region
languages

Question: {question}
"""
        )

        return {
        "country": result.country,
        "fields": result.fields or []
    }

    except Exception as e:
        logger.error(f"Error occurred while extracting intent: {e}")

        print("Intent extraction error:", e)

        return {
            "error": "Failed to extract intent."
        }
    
from app.tools.country_api import get_country_data


def call_country_api(state: AgentState):

    country = state.get("country")
    logger.info(f"Calling REST Countries API for: {country}")
    if not country:
        return {"error": "No country provided."}

    data = get_country_data(country)

    if not data:
        return {"error": "Country not found."}

    return {"api_data": data}

def synthesize_answer(state: AgentState):
    
    logger.info("Synthesizing final answer")
    if state.get("error"):
        return {"answer": state["error"]}

    data = state.get("api_data")
    fields = state.get("fields", [])

    response_parts = []

    if "capital" in fields:
        capital = data.get("capital", ["Unknown"])[0]
        response_parts.append(f"Capital: {capital}")

    if "population" in fields:
        population = data.get("population", "Unknown")
        response_parts.append(f"Population: {population}")

    if "currency" in fields:
        currencies = data.get("currencies", {})
        if currencies:
            currency = list(currencies.keys())[0]
            response_parts.append(f"Currency: {currency}")

    if "region" in fields:
        response_parts.append(f"Region: {data.get('region')}")

    if "languages" in fields:
        langs = list(data.get("languages", {}).values())
        response_parts.append(f"Languages: {', '.join(langs)}")

    if not response_parts:
        return {"answer": "Requested data not available."}

    return {"answer": ", ".join(response_parts)}