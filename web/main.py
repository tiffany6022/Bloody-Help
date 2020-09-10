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
# load model
from test import Craft_model
from test import test_net
from test import str2bool
import argparse

app = FastAPI()

model_path = "../craft_predict/CRAFT_clr_9.pth"
net = Craft_model(model_path)

TEXT_THRESHOLD = 0.4
parser = argparse.ArgumentParser(description='CRAFT Text Detection')
parser.add_argument('--text_threshold', default=0.7, type=float, help='text confidence threshold')
parser.add_argument('--low_text', default=0.4, type=float, help='text low-bound score')
parser.add_argument('--link_threshold', default=0.4, type=float, help='link confidence threshold')
parser.add_argument('--cuda', default=True, type=str2bool, help='Use cuda to train model')
parser.add_argument('--poly', default=False, action='store_true', help='enable polygon type')
args = parser.parse_args()


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
    img = cv2.imdecode(img, cv2.COLOR_RGB2BGR)
    bboxes = test_net(net, img, args.text_threshold, args.link_threshold, args.low_text, args.cuda, args.poly)

    '''
    im = [[[r, g, b], [r, g, b]],
              [...], ...]
    '''
    for bb in bbox:
        required_str = pytesseract.image_to_string(img[x0: x1, y0: y1], lang='eng', config='--psm 6')

    return {
        'sys': ...,
        'dia': ...,
        'pulse': ...
    }
    # return images

#ssl

#img

