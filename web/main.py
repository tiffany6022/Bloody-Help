#!/usr/bin/env python3

import numpy as np
import cv2
import time
import base64
from io import BytesIO

from typing import Optional, List
from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import pytesseract

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
    index = str(images.base64).find('base64,') + 7 # data:[<media type>][;base64],<data>
    img64 = images.base64[index:]
    imgdata = base64.b64decode(img64)
    # imgdata = '\xff\xa0\x53\x98\xasd'

    img = np.fromstring(imgdata, np.uint8)
    # img = [255, 200, 123, 123, 23 ...]
    im = cv2.imdecode(img, cv2.COLOR_RGB2BGR)
    '''
    im = [[[r, g, b], [r, g, b]],
              [...], ...]
    '''

    print(pytesseract.image_to_string(im, lang='eng', config='--psm 6'))

    # return images

#ssl

#img

