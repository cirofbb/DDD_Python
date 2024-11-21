from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Annotated, Dict
from datetime import date, datetime, timedelta

router = APIRouter()

items_id: Dict[int, str] = {1: "Item A", 2: "Item B", 3: "Item C"}

class InvalidItemIDException(HTTPException):
    def __init__(self, item_id: int):
        detalhe = f"O item_id '{item_id}' não é válido. Tente novamente com um nº inteiro positivo"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detalhe)

class UserResponse(BaseModel):
    username: str
    message: str

class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Nome de usuário deve ser uma string não vazia")
    age: Annotated[int, Field(ge=1, description="Idade deve ser um número inteiro positivo")]

class Item(BaseModel):
    name: str
    description: str

class BirthdayRequest(BaseModel):
    name: str
    birthday: date = Field(..., description="Data de aniversário no formato YYYY-MM-DD")

@router.get("/item/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id <= 0:
        raise InvalidItemIDException(item_id)
    item = items_id.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"item_id": item_id, "item": item}

@router.delete("/item/{item_id}")
async def delete_item(item_id: int):
    if item_id <= 0:
        raise InvalidItemIDException(item_id)
    if item_id not in items_id:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    del items_id[item_id]
    return {"message": f"O ID {item_id} foi deletado com sucesso"}

@router.get("/")
async def read_root():
    return {"mensagem": "Hello, FastAPI!"}

@router.get("/status")
async def get_status():
    return {"status": "Servidor funcionando"}

@router.get("/user/{username}", response_model=UserResponse)
async def saudacao(username: str):
    valid_users = ['Fernando', 'Ciro', 'AK']
    if username not in valid_users:
       raise HTTPException(status_code=404, detail=f"Erro 404: Usuário '{username}' não encontrado") 
    return UserResponse(username=username, message=f"Saudações vascaínas, {username}!")

@router.post("/create-user", response_model=UserResponse)
async def create_user(user: CreateUserRequest):
    return UserResponse(username=user.username, message=f"{user.username} criado com sucesso")

@router.post("/birthday")
async def calculo(birthday_request: BirthdayRequest):
    today = date.today()
    birthday_this_year = birthday_request.birthday.replace(year=today.year)
    
    if birthday_this_year < today:
        birthday_this_year = birthday_this_year.replace(year=today.year + 1)
    
    days_until_birthday = (birthday_this_year - today).days
    return {
        "message": f"Olá, {birthday_request.name}! Faltam {days_until_birthday} dias para o seu próximo aniversário."
    }