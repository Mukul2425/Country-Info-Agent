from fastapi import FastAPI
from pydantic import BaseModel
from app.agent.graph import graph


app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(request: QuestionRequest):

    result = graph.invoke({
        "question": request.question
    })

    return {"answer": result.get("answer")}