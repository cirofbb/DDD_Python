from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

app = FastAPI(title="English to French Translation API")

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
translator = pipeline("translation_en_to_fr", model=model, tokenizer=tokenizer)

class TranslationRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Translation API en-fr is running"}

@app.post("/translate")
def translate_text(request: TranslationRequest):
    """
    Recebe texto em inglês, traduz para o francês e retorna a tradução.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="O texto de entrada não pode estar vazio.")
    
    try:
        translated = translator(request.text, max_length=400)[0]["translation_text"]
        return {"text_in_english": request.text, "text_in_french": translated}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a tradução: {e}")
