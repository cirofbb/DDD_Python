"""
Tentei de todas as formas integrar minha chave API key da OpenAI numa aplicação LangChain, mas não consegui.
Sempre retornava o mesmo erro:

{
    "detail": "Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}"
}

Explorei todas as formas imagináveis de contornar o problema, porque tinha créditos disponíveis e chaves válidas.

Por este motivo, a questão abaixo foi desenvolvida com o modelo t5-small, sem utilização de LangChain e OpenAI.

"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import os

app = FastAPI()

class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    translated_text: str

translator = pipeline("translation_en_to_fr", model="t5-small")

@app.post("/translate/", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    try:
        result = translator(request.text, max_length=512)
        translated_text = result[0]['translation_text']
        
        return TranslationResponse(translated_text=translated_text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Translation API is running"}