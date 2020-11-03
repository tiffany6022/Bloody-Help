#!/usr/bin/env python3

import numpy as np
import os
import cv2
import time
import base64
from io import BytesIO

from typing import Optional, List
from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# import pytesseract
# load model
from craft_predict.test import Craft_model
from craft_predict.test import test_net
from craft_predict.test import str2bool
# import argparse
from model.img2seq import Img2SeqModel
from model.utils.general import Config, run
from model.utils.text import Vocab
from model.utils.image import greyscale, crop_image, pad_image, \
    downsample_image, TIMEOUT
from scipy.misc import imread
import PIL
from PIL import Image

os.environ["CUDA_VISIBLE_DEVICE"] = "1"

app = FastAPI()

model_path = "./craft_predict/CRAFT_clr_9.pth"
net = Craft_model(model_path, True)
dir_output = "/home/tiffany/git/im2latex/results/full/"
config_vocab = Config(dir_output + "vocab.json")
config_model = Config(dir_output + "model.json")
vocab = Vocab(config_vocab)

model = Img2SeqModel(config_model, dir_output, vocab)
model.build_pred()
model.restore_session(dir_output + "model.weights/")

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

class FastImage(BaseModel):
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
async def img(images: FastImage):
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


    h, w, _ = img.shape
    std = 512
    img = cv2.resize(img, (int(w * std/h), std))
    cv2.imwrite('beforetest.jpg', img)
    print("start to inference")
    #bboxes = test_net(net, img, 0.7, 0.4, 0.4, True, False)
    bboxes = test_net(net, img, 0.7, 0.7, 0.4, True, False)
    print("get bounding box")
    # print(bboxes.shape)
    shift = 5
    outputs = []
    for i, bb in enumerate(bboxes):
        print(bb)
        crop_img = img[int(bb[0][1]) - shift: int(bb[2][1]) + shift, int(bb[0][0]) - shift: int(bb[2][0]) + shift, :]
        print(crop_img.shape)
        h, w, _ = crop_img.shape
        # temp = pytesseract.image_to_string(newimage, lang='lcd_multifonts', config='--psm 7')
        # print("temp=", temp)
        cv2.imwrite('aftertest_1_'+str(i)+'.jpg', crop_img)
        buckets = [
            [240, 100], [320, 80], [400, 80], [400, 100], [480, 80], [480, 100],
            [560, 80], [560, 100], [640, 80], [640, 100], [720, 80], [720, 100],
            [720, 120], [720, 200], [800, 100], [800, 320], [1000, 200],
            [1000, 400], [1200, 200], [1600, 200], [1600, 1600]
        ]
        temp_path = "/tmp/temp.png"
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        ret, crop_img = cv2.threshold(crop_img, 50, 255, cv2.THRESH_BINARY)
        # crop_img = crop_img[:, :, np.newaxis]
        # print(crop_img.dtype)
        crop_img = Image.fromarray(crop_img)
        crop_img.save(temp_path)

        crop_image(temp_path, temp_path)
        crop_img = Image.open(temp_path)
        (W, H) = crop_img.size
        scale = 48 / H
        crop_img = Image.open(temp_path).resize( (int(W*scale), int(H*scale)), Image.BILINEAR )
        crop_img.save(temp_path)

        pad_image(temp_path, temp_path, buckets=buckets)
        downsample_image(temp_path, temp_path, 2)

        crop_img = imread(temp_path)
        crop_img = greyscale(crop_img)
        crop_img = np.asarray(crop_img)
        print("before predict", crop_img.shape)
        cv2.imwrite('aftertest_2_'+str(i)+'.jpg', crop_img)
        hyps = model.predict(crop_img)
        print(hyps)
        model.logger.info(hyps[0])
        outputs.append(int(hyps[0].replace(" ", "")))


    return {
        'SYS': outputs[0],
        'DIA': outputs[1],
        'PUL': outputs[2]
    }
    # return images

#ssl

#img

