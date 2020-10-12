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
from craft_predict.test import Craft_model
from craft_predict.test import test_net
from craft_predict.test import str2bool
# import argparse

app = FastAPI()

model_path = "./craft_predict/CRAFT_clr_9.pth"
net = Craft_model(model_path)

# TEXT_THRESHOLD = 0.4
# parser = argparse.ArgumentParser(description='CRAFT Text Detection')
# parser.add_argument('--text_threshold', default=0.7, type=float, help='text confidence threshold')
# parser.add_argument('--low_text', default=0.4, type=float, help='text low-bound score')
# parser.add_argument('--link_threshold', default=0.4, type=float, help='link confidence threshold')
# parser.add_argument('--cuda', default=True, type=str2bool, help='Use cuda to train model')
# parser.add_argument('--poly', default=False, action='store_true', help='enable polygon type')
# args = parser.parse_args()

# def rotate(image, angle, center=None, scale=1.0):
#     (h, w) = image.shape[:2]
#     if center is None:
#         center = (w / 2, h / 2)
#     M = cv2.getRotationMatrix2D(center, angle, scale)
#     rotated = cv2.warpAffine(image, M, (w, h))
#     return rotated

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
    # (600,480,3)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # bboxes = test_net(net, img, args.text_threshold, args.link_threshold, args.low_text, args.cuda, args.poly)


    cv2.imwrite('beforetest.jpg', img)

    # bboxes = test_net(net, img, 0.7, 0.4, 0.4, True, False)
    # print(bboxes.shape)
    # shift = 0
    # for i, bb in enumerate(bboxes):
    #     cropimg = img[int(bb[0][1]) - shift: int(bb[2][1]) + shift, int(bb[0][0]) - shift: int(bb[2][0]) + shift]
    #     # gray_img = cv2.cvtColor(cropimg, cv2.COLOR_BGR2GRAY)
    #     # th3_img = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #     #                            cv2.THRESH_BINARY,11,2)
    #     # cropimg = cv2.cvtColor(th3_img, cv2.COLOR_GRAY2BGR)
    #     # cropimg = rotate(cropimg, 4)
    #     cv2.imwrite('aftertest'+str(i)+'.jpg', cropimg)
    #     required_str = pytesseract.image_to_string(cropimg, lang='lcd_digit2', config='--psm 6')
    #     print("tesseract: "+required_str)

    return {
        'SYS': 104,
        'DIA': 58,
        'PUL': 82
    }
    # return images

#ssl

#img

