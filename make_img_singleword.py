from sys import argv
from PIL import Image, ImageDraw, ImageFont
import json
import random
import csv
import numpy as np

SAVE_DIR = "/home/peichen/git/CRAFT-Reimplementation/test"
#SAVE_DIR = "/home/peichen/git/CRAFT-Reimplementation/icdar2015"
#SAVE_DIR = "./save"
def get_width(bit):
    if bit == 1:
        return 10
    else:
        return 40

def make_img(pic_num):

    global SAVE_DIR

    W, H = (400, 520)
    big_fnt = ImageFont.truetype('digital-7-mono_[allfont.net].ttf', 90)
    small_fnt = ImageFont.truetype('digital-7-mono_[allfont.net].ttf', 70)
    eng_fnt = ImageFont.truetype("arial.ttf", 30)
    eng_small_fnt = ImageFont.truetype("arial.ttf", 15)
    img_log = {}
    position_dict = {}
    textx_min = [0, 0, 0]
    x_min = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    x_max = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # x_dist = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # width = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for x in range(pic_num):
        digits = [random.randint(100, 999) for i in range(3)] #Generate 3 random num sys, dia, pulse
        # digits = [314, 222, 98]
        y_coord = [110, 190, 270]
        img = Image.new('RGB', (W, H), color = "WhiteSmoke")
        d = ImageDraw.Draw(img)
        d.rectangle((20,20,380,400), fill=(111,112,117)) # grey
        d.rectangle((250,430,340,480), fill=(49,57,128)) # blue
        d.rectangle((120,80,340,340), fill=(188,194,190), outline="black", width=3) # grey+green
        d.text((150,35), "OMRON", font=eng_fnt, fill="Gainsboro")
        d.text((79,130), "SYS", font=eng_small_fnt, fill="Gainsboro")
        d.text((80,210), "DIA", font=eng_small_fnt, fill="Gainsboro")
        d.text((60,290), "PULSE", font=eng_small_fnt, fill="Gainsboro")
        for i, v in enumerate(digits):
            textx_min[i] = 220  if v < 100 else 180          #the number position for PIL
            bit = [v/100, v%100/10, v%10]
            noise = random.randint(0, 50) 
            textx_min[i] = textx_min[i] - noise
            x_max[i][:] = [220 - noise, 260 - noise, 300 - noise]
            for k in range(3):
                x_min[i][k] = x_max[i][k] - get_width(bit[k])
            d.text((textx_min[i], y_coord[i]), str(v), font=big_fnt, fill=(0, 0, 0))

        img.save(f"{SAVE_DIR}/pics/img_{x}.jpg")
        img_log[f"img_{x}.jpg"] = {
           "sys": digits[0],
           "dia": digits[1],
           "pulse": digits[2],
           "num_font": "digital-7-mono_[allfont.net].ttf",
           "word_font": "Arial",
        }
        # noise = [random.randint(0, 5) for i in range(3)]
        with open(f"{SAVE_DIR}/ground_truth/gt_img_{x}.txt", 'w', newline='') as gtfile:
            writer = csv.writer(gtfile)
            #indicators = np.array([[*digits, "OMRON", "SYS", "DIA", "PULSE"]])
            indicators = np.array([[*digits]*3])
            #noise = [[random.randint(0,5)] * 8 for i in range(3)] 
            text_pos = np.array([
                [x_min[0][0], 110, x_max[0][0], 110, x_max[0][0], 180, x_min[0][0], 180],
                [x_min[0][1], 110, x_max[0][1], 110, x_max[0][1], 180, x_min[0][1], 180],
                [x_min[0][2], 110, x_max[0][2], 110, x_max[0][2], 180, x_min[0][2], 180],
                [x_min[1][0], 190, x_max[1][0], 190, x_max[1][0], 260, x_min[1][0], 260],
                [x_min[1][1], 190, x_max[1][1], 190, x_max[1][1], 260, x_min[1][1], 260],
                [x_min[1][2], 190, x_max[1][2], 190, x_max[1][2], 260, x_min[1][2], 260],
                [x_min[2][0], 270, x_max[2][0], 270, x_max[2][0], 335, x_min[2][0], 335],
                [x_min[2][1], 270, x_max[2][1], 270, x_max[2][1], 335, x_min[2][1], 335],
                [x_min[2][2], 270, x_max[2][2], 270, x_max[2][2], 335, x_min[2][2], 335],
                # [150,  35, 275,  35, 275,  65, 150,  65],
                # [ 79, 130, 110, 130, 110, 148,  79, 148],
                # [ 80, 210, 110, 210, 110, 228,  80, 228],
                # [ 60, 290, 110, 290, 110, 308,  60, 308],
            ])
            #text_pos[:3] = text_pos[:3] + noise
            text_pos = np.concatenate((text_pos, indicators.T), axis=1)
            for row in text_pos:
                writer.writerow(row)

    dict_str = json.dumps(img_log)
    with open(f"{SAVE_DIR}/inform.json", mode="w+") as file:
        file.write(dict_str)

if __name__ == '__main__':
    make_img(700)     #$$
