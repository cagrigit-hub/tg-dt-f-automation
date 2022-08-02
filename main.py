from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from worker.tele_flex_worker import TeleFlexWorker
import asyncio
from dotenv import load_dotenv

load_dotenv()


class Telegram(BaseModel):
    telegram_address: List[str]


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000" "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


  
TF = TeleFlexWorker(
        os.getenv("CUR_USER"), os.getenv("CUR_ID"), os.getenv("CUR_HASH")
    )

@app.post("/telegram", response_model=Telegram)
def add_quote(telegram_address: Telegram):
    
    asyncio.run(TF.write_group_admins(telegram_address.telegram_address))
    return telegram_address


@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.get("/telegram", summary="Get a list of telegrams")
def get_quote():
    
    os.system("python go_spider.py")
    return {"process": "OK"}
