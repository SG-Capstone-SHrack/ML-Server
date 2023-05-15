import os
import json
import torch

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from fastapi.responses import HTMLResponse

from config import settings
from router import router


app = FastAPI()

templates = Jinja2Templates(directory='./')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# router
app.include_router(router)


if __name__ == "__main__":    
    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("execution")
