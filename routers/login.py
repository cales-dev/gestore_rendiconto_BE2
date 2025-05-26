from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def login():
    return "{'message':'ok'}"