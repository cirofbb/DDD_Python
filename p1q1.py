from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2')
set_seed(42)

app = FastAPI()

class TextInput(BaseModel):
    prompt: str
    max_length: int = 100

@app.post("/generate-text/")
async def generate_text(input: TextInput):
    try:
        results = generator(
            input.prompt, 
            max_length=input.max_length, 
            num_return_sequences=1,
            top_k=50,
            top_p=0.95,
            truncation=True
            )
        generated_text = results[0]["generated_text"]
        return {"prompt": input.prompt, "generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
