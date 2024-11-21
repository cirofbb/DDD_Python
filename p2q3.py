from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

app = FastAPI()

class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    translated_text: str

model_name = "Helsinki-NLP/opus-mt-en-de"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=512,
    device='cuda' if torch.cuda.is_available() else 'cpu'
)

llm = HuggingFacePipeline(pipeline=pipe)

@app.post("/translate/", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    try:
        translation = llm(request.text)
        
        return TranslationResponse(translated_text=translation.strip())
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "English to German Translation API is running"}
