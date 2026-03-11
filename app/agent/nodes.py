import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.agent.state import AgentState

llm = ChatOpenAI(model="gpt-4o-mini")


intent_prompt = ChatPromptTemplate.from_template(
"""
Extract the country and requested information fields from the question.

Supported fields:
capital
population
currency
region
languages

Return JSON ONLY:

{
  "country": "...",
  "fields": ["..."]
}

Question: {question}
"""
)


def extract_intent(state: AgentState):

    question = state["question"]

    try:
        response = llm.invoke(intent_prompt.format(question=question))

        data = json.loads(response.content)

        return {
            "country": data.get("country"),
            "fields": data.get("fields", [])
        }

    except Exception:

        return {
            "error": "Failed to extract intent."
        }
    
from app.tools.country_api import get_country_data


def call_country_api(state: AgentState):

    country = state.get("country")

    if not country:
        return {"error": "No country provided."}

    data = get_country_data(country)

    if not data:
        return {"error": "Country not found."}

    return {"api_data": data}

def synthesize_answer(state: AgentState):

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