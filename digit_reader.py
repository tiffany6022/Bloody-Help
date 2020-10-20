"""
digit_reader.py
Module to extract and read seven-segment display digits from an
ROI in an image.
@author: Suyash Kumar <suyashkumar2003@gmail.com>
"""
import cv2
import os
import time
import warnings
warnings.filterwarnings("ignore") # Filter matplotlib warnings
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import argparse

"""
Parses environment variables to int, sets
to default if they don't exist yet
"""
def environ_read(eVar):
    if(eVar):
        eVar = int(eVar)
    else:
        eVar = 0 # Set to default

# Read Environment Vars safely
dev = environ_read(os.environ.get('DEV'))
demo = environ_read(os.environ.get('DEMO'))

# Number Mapping:
mapping = {
    "0101000": 1,
    "0110111": 2,
    "0101111": 3,
    "1101010": 4,
    "1001111": 5,
    "1011111": 6,
    "1011011": 6,
    "0101100": 7,
    "1101100": 7,
    "1111111": 8,
    "1101110": 9,
    "1101111": 9,
    "1111101": 0
}

# def cropImage(image, roi):
#     #print roi
#     clone = image.copy()
#     retImg = clone[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]
#     return retImg

def line_profile(image, profType, loc):
    height, width = image.shape[:2]
    if (profType == "h"):
        cv2.imwrite(f'./output/h_{loc}.png', image[int(round(height*loc)):int(round(height*loc))+1, 0:width])
        return image[int(round(height*loc)):int(round(height*loc))+1, 0:width]
    elif(profType == "v"):
        cv2.imwrite('./output/v.png', image[0:height, int(round(0.5*width)):int(round(0.5*width)+1)])
        return image[0:height, int(round(0.5*width)):int(round(0.5*width)+1)]

def getProcessStringHoriz(arr):
    firstHalf = check_high(arr[0:int(round(len(arr)/2))])
    # print(firstHalf)
    lastHalf  = check_high(arr[int(round(len(arr)/2)):len(arr)])
    # print(lastHalf)
    return str(firstHalf)+str(lastHalf)

def getProcessStringVert(arr):
    # if check_high(arr) == 2:
    #     return "222"
    firstQuarter = check_high(arr[0:int(round(len(arr)/3))])
    middleHalf   = check_high(arr[int(round(1*len(arr)/3)):int(round(2*len(arr)/3))])
    lastQuarter  = check_high(arr[int(2*round(len(arr)/3)):len(arr)])
    return str(firstQuarter)+str(middleHalf)+str(lastQuarter)


def check_high(arraySlice, N=0.15, threshold=10):
    arraySlice = arraySlice[1:-1]
    # print(arraySlice)
    sliceLength = len(arraySlice)
    numInRow = 0
    maxInRow = 0
    for x in arraySlice:
        if (x<threshold):
            numInRow = numInRow + 1
        else:
            if numInRow > maxInRow:
                maxInRow = numInRow
            numInRow = 0
    # print(arraySlice, numInRow)
    # if (maxInRow/sliceLength > 0.7 or numInRow/sliceLength > 0.7):
    #     return 2
    if (maxInRow/sliceLength > N or numInRow/sliceLength > N):
        return 1
    else:
        return 0


"""
Returns digit given a cropped grayscale image of the 7 segments.
In the image 0 is signal and 255 is background
"""
def resolve_digit(croppedImage):
    height, width = croppedImage.shape[:2]
    if height / width > 3:
        return 1

    #L1Coord = [(round(height*.25),round(height*.25)+1), (0,width)]
    L1 = line_profile(croppedImage, "h", 0.3)
    L2 = line_profile(croppedImage, "h", 0.7)
    L3 = line_profile(croppedImage, "v", 0.5)
    L1Arr = [int(x) for x in L1[0]]
    L2Arr = [int(x) for x in L2[0]]
    L3Arr = [int(x) for x in L3]

    #cv2.imshow("orig",croppedImage)
    print(getProcessStringHoriz(L1Arr), getProcessStringHoriz(L2Arr), getProcessStringVert(L3Arr))
    processString = getProcessStringHoriz(L1Arr)+getProcessStringHoriz(L2Arr)+getProcessStringVert(L3Arr)
    # if getProcessStringVert(L3Arr) == "222":
    #     processString = "0101000"
    digit = mapping.get(processString)
    if (digit is None):
        print("Digit not recognized: " + processString)
        # cv2.imshow("orig", croppedImage)
        # digit = input("What digit is this? Enter here: ")
        # cv2.waitKey(0)
    #cv2.waitKey(0)
    # if (dev):
    #     print(processString)
    #     print(mapping[processString])
    #     # Show images and line profiles:
    #     cv2.imshow("L1", L1)
    #     cv2.imshow("L2", L2)
    #     cv2.imshow("L3",L3)
    #     cv2.imshow("orig",croppedImage)
    #
    #     plt.figure(1)
    #     plt.subplot(311)
    #     plt.plot(L1Arr)
    #     plt.title("L1")
    #     plt.subplot(312)
    #     plt.plot(L2Arr)
    #     plt.title("L2")
    #     plt.subplot(313)
    #     plt.plot(L3Arr)
    #     plt.title("L3")
    #     plt.show()
    #
    #     cv2.waitKey(0)
    return digit

# def read_digits(image, roiPoints):
def read_digits(image):
    digits = []
    # for selection in xrange(0,len(roiPoints)/2):
    currentSel = image
    currentSel = cv2.cvtColor(currentSel, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    ret, newimage = cv2.threshold(currentSel, 50,255,cv2.THRESH_BINARY_INV)
    cv2.imwrite('./output/newimage.png', newimage)
    # currentSel = cropImage(currentSel, [roiPoints[selection*2], roiPoints[2*selection+1]])
    digit=resolve_digit(newimage)
    digits.append(digit)
    # if (demo):
    #     cv2.imshow("demo",currentSel)
    #     print(digit)
    #     cv2.waitKey(0)
    print(digits)
    # return digits


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--photo', help = "Input Photo File")
    args = parser.parse_args()

    img = cv2.imread(args.photo)
    read_digits(img)
