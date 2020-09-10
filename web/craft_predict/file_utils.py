# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2
import imgproc

# borrowed from https://github.com/lengstrom/fast-style-transfer/blob/master/src/utils.py
def get_files(img_dir):
    imgs, masks, xmls = list_files(img_dir)
    return imgs, masks, xmls

def list_files(in_path):
    img_files = []
    mask_files = []
    gt_files = []
    for (dirpath, dirnames, filenames) in os.walk(in_path):
        for file in filenames:
            filename, ext = os.path.splitext(file)
            ext = str.lower(ext)
            if ext == '.jpg' or ext == '.jpeg' or ext == '.gif' or ext == '.png' or ext == '.pgm':
                img_files.append(os.path.join(dirpath, file))
            elif ext == '.bmp':
                mask_files.append(os.path.join(dirpath, file))
            elif ext == '.xml' or ext == '.gt' or ext == '.txt':
                gt_files.append(os.path.join(dirpath, file))
            elif ext == '.zip':
                continue
    # img_files.sort()
    # mask_files.sort()
    # gt_files.sort()
    return img_files, mask_files, gt_files

def saveResult(img_file, img, boxes, dirname='./result2/', verticals=None, texts=None):
        """ save text detection result one by one
        Args:
            img_file (str): image file name
            img (array): raw image context
            boxes (array): array of result file
                Shape: [num_detections, 4] for BB output / [num_detections, 4] for QUAD output
        Return:
            None
        """
        img = np.array(img)

        # make result file list
        filename, file_ext = os.path.splitext(os.path.basename(img_file))

        # result directory
        res_file = dirname + "/res_" + filename + '.txt'
        res_img_file = dirname + "/res_" + filename + '.jpg'
        gt_file = "./test/real_gt/gt_" + filename + '.txt'

        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        with open(res_file, 'w') as f:
            for i, box in enumerate(boxes):
                poly = np.array(box).astype(np.int32).reshape((-1))
                strResult = ','.join([str(p) for p in poly]) + '\r\n'
                poly = np.array(box).astype(np.int32)          #! unlock the comment by pei
                min_x = np.min(poly[:,0])                      #! ..
                max_x = np.max(poly[:,0])                      #! ..
                min_y = np.min(poly[:,1])                      #! ..
                max_y = np.max(poly[:,1])                      #! ..
                ####################  added by pei/2020/08/31
                start_point = (min_x, min_y)
                end_point = (max_x, max_y)
                color = (255, 233, 50)
                thickness = 2
                img = cv2.rectangle(img, start_point, end_point, color, thickness)
                ####################
                #strResult = ','.join([str(min_x), str(min_y), str(max_x), str(max_y)]) + '\r\n'  #! ..
                strResult = ','.join([str(min_x), str(min_y), str(max_x), str(min_y), str(max_x), str(max_y), str(min_x), str(max_y)]) + '\r\n'  #! added by pei/2020/08/31
                f.write(strResult)

        #         poly = poly.reshape(-1, 2)
        #         cv2.polylines(img, [poly.reshape((-1, 1, 2))], True, color=(0, 0, 255), thickness=2)
        #         ptColor = (0, 255, 255)
        #         if verticals is not None:
        #             if verticals[i]:
        #                 ptColor = (255, 0, 0)
        #
        #         if texts is not None:
        #             font = cv2.FONT_HERSHEY_SIMPLEX
        #             font_scale = 0.5
        #             cv2.putText(img, "{}".format(texts[i]), (poly[0][0]+1, poly[0][1]+1), font, font_scale, (0, 0, 0), thickness=1)
        #             cv2.putText(img, "{}".format(texts[i]), tuple(poly[0]), font, font_scale, (0, 255, 255), thickness=1)
        #
        # with open(gt_file, 'r') as f: 
        #     for line in f:
        #         currentline = line.split(",")
        #         start_point = (int(currentline[0]), int(currentline[1]))
        #         end_point = (int(currentline[4]), int(currentline[5]))
        #         color = (255, 128, 128)
        #         thickness = 2
        #         img = cv2.rectangle(img, start_point, end_point, color, thickness)
         #Save result image
        cv2.imwrite(res_img_file, img)

