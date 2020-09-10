#!/usr/local/bin/python3
import sys
from test import test_net
from test import Craft_model
import imgproc
import argparse
from test import str2bool

model_path = './CRAFT_clr_9.pth'

parser = argparse.ArgumentParser(description='CRAFT Text Detection')
parser.add_argument('--text_threshold', default=0.7, type=float, help='text confidence threshold')
parser.add_argument('--low_text', default=0.4, type=float, help='text low-bound score')
parser.add_argument('--link_threshold', default=0.4, type=float, help='link confidence threshold')
parser.add_argument('--cuda', default=True, type=str2bool, help='Use cuda to train model')
parser.add_argument('--poly', default=False, action='store_true', help='enable polygon type')
args = parser.parse_args()

#test('./real_weights/CRAFT_clr_' + repr(epoch) + '.pth')
#bboxes = test_net('./CRAFT_clr_9.pth','./img_8.jpg')         #! modified saving directory
net = Craft_model(model_path)
image_path = './img_8.jpg'
image = imgproc.loadImage(image_path)
bboxes = test_net(net, image, args.text_threshold, args.link_threshold, args.low_text, args.cuda, args.poly)
print('bboooooooxes = ', bboxes)
print(bboxes.shape)
