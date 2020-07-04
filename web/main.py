#!/usr/bin/env python3
import time

from typing import Optional, List
from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

class Image(BaseModel):
    base64: str
    name: str

app.mount("/static", StaticFiles(directory="dist"), name="static")


templates = Jinja2Templates(directory="dist")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )

@app.post("/img/")
async def img(images: Image):
    return [1, 2, 3]

#ssl

#img

