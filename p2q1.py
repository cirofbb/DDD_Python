from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.llms import FakeListLLM

app = FastAPI()

class UserInput(BaseModel):
    question: str

responses = [
    "Eu sou um chatbot simples.",
    "Eu respondo perguntas básicas para testes.",
    "A capital do Brasil é Brasília.",
    "Desculpe, eu não sei responder a isso."
]

fake_llm = FakeListLLM(responses=responses)

@app.post("/chat/")
async def chat(input: UserInput):
    try:
        answer = fake_llm(input.question)
        return {"question": input.question, "response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
