from sys import argv
from PIL import Image, ImageDraw, ImageFont

sys = argv[1]
dia = argv[2]
pulse = argv[3]

W, H = (400, 520)

img = Image.new('RGB', (W, H), color = "WhiteSmoke")
big_fnt = ImageFont.truetype('digital-7-mono_[allfont.net].ttf', 90)
small_fnt = ImageFont.truetype('digital-7-mono_[allfont.net].ttf', 70)
eng_fnt = ImageFont.truetype("arial.ttf", 30)
eng_small_fnt = ImageFont.truetype("arial.ttf", 15)

d = ImageDraw.Draw(img)
d.rectangle((20,20,380,400), fill=(111,112,117)) # grey
d.rectangle((250,430,340,480), fill=(49,57,128)) # blue
d.rectangle((120,80,340,340), fill=(188,194,190), outline="black", width=3) # grey+green
d.text((150,35), "OMRON", font=eng_fnt, fill="Gainsboro")
d.text((79,130), "SYS", font=eng_small_fnt, fill="Gainsboro")
d.text((80,210), "DIA", font=eng_small_fnt, fill="Gainsboro")
d.text((60,290), "PULSE", font=eng_small_fnt, fill="Gainsboro")
d.text((180,110), sys, font=big_fnt, fill=(0, 0, 0))
d.text((220,190), dia, font=big_fnt, fill=(0, 0, 0))
d.text((235,270), pulse, font=small_fnt, fill=(0, 0, 0))
img.save('../public_html/img.png')

