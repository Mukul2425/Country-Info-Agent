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