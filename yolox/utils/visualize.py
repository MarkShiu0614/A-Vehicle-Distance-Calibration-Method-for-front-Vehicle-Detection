#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii Inc. All rights reserved.

import cv2
import numpy as np

__all__ = ["vis","vis_z"]


def vis(img, boxes, scores, z, cls_ids, conf=0.5, class_names=None ):
    # print(cls_ids)
    # print(int(cls_ids[0]))
    # print("------")
    # print(len(boxes))
    # print("------")
    # 開啟所有 result_list 相關
    result_list = []    # 存TXT

    for i in range(len(boxes)):
        box = boxes[i]
        # print(box)
        cls_id = int(cls_ids[i])
        az = float(z[i])
        score = scores[i]
        if score < conf:
            continue
        x0 = int(box[0])
        y0 = int(box[1])
        x1 = int(box[2])
        y1 = int(box[3])
        # 存TXT
        class_name = class_names[cls_id]    # X
        x0_1 = x0 / 1600      # nuScenes
        y0_1 = y0 / 900
        # x0_1 = x0 / 1242        # kitti
        # y0_1 = y0 / 375
        # x1_1 = x0 / 1600
        # y1_1 = y0 / 900
        '''
        計算曲面的公式：
        Z1 = -18.46 * X^2 + 311.91 * Y^2 + -22.68 * X * Y + 27.83 * X + -277.13 * Y + 62.96
        Z2 = -20.98 * X^2 + 691.35 * Y^2 + -79.38 * X * Y + 60.15 * X + -642.13 * Y + 148.30
        '''
        # 中位數
        # Qfunc = -18.46 * x0_1**2 + 311.91 * y0_1**2 + -22.68 * x0_1 * y0_1 + 27.83 * x0_1 + -277.13 * y0_1 + 62.96
        # 平均數
        Qfunc = -20.98 * x0_1**2 + 691.35 * y0_1**2 + -79.38 * x0_1 * y0_1 + 60.15 * x0_1 + -642.13 * y0_1 + 148.30
        print(float(Qfunc))
        az_z = az
        
        one_line = (str(cls_id), str(x0_1), str(y0_1), str(x1), str(y1), str(az_z), str(Qfunc))    # class, z
        str_one_line = " ".join(one_line)	
        result_list.append(str_one_line)    # 結束

        color = (_COLORS[cls_id] * 255).astype(np.uint8).tolist()
        text = '{}:{:.1f}%'.format(class_names[cls_id], score * 100 )
        # text = text + ' {}:{:.1f}m'.format("D",az)
        text_z = '{:.1f}m'.format(az_z)
        
        txt_color = (0, 0, 0) if np.mean(_COLORS[cls_id]) > 0.5 else (255, 255, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX

        txt_size = cv2.getTextSize(text, font, 0.4, 1)[0]
        txt_z_size = cv2.getTextSize(text_z,font,2,5 )[0]
        # print("txt_size :")
        # print(txt_size)
        txt_size_z = cv2.getTextSize(text_z, font, 0.4, 2)[0]
        
        cv2.rectangle(img, (x0, y0), (x1, y1), color, 2)

        txt_bk_color = (_COLORS[cls_id] * 255 * 0.7).astype(np.uint8).tolist()

        blk = np.zeros(img.shape, np.uint8)  
        cv2.rectangle(
            blk,
            (x0, y0 + 1),
            (x0 + txt_size[0] + 1, y0 + int(1.5*txt_size[1])),
            txt_bk_color,
            -1
        )
        img = cv2.addWeighted(img, 1.0, blk, 0.5, 1)

        cv2.putText(img, text, (x0, y0 + txt_size[1]), font, 0.4, txt_color, thickness=1)

        cv2.putText(img, text_z, (int((x0+x1)/2-(txt_z_size[0]/2)), int((y0+y1)/2+12)), font, 1.8, (0,255,255), thickness=7) # 外匡黃
        cv2.putText(img, text_z, (int((x0+x1)/2-(txt_z_size[0]/2)), int((y0+y1)/2+12)), font, 1.8, (0,0,255), thickness=3) # 數字紅

        # cv2.rectangle(
        #     img,
        #     (x0, y0 + 1),
        #     (x0 + txt_size[0] +txt_size_z[0] + 1, y0 + int(1.5*(txt_size[1]+ txt_size_z[1]))),
        #     txt_bk_color,
        #     -1
        # )
        # cv2.putText(img, text_z, (x0, y0 + txt_size_z[1]), font, 0.4, txt_color, thickness=1)

    return img, result_list
    # return img

def vis_z(img, boxes, z ):

    for i in range(len(boxes)):
        box = boxes[i]
        # print(box)
        az = float(z[i])
        x0 = int(box[0])
        y0 = int(box[1])
        x1 = int(box[2])
        y1 = int(box[3])

        # color = (_COLORS[cls_id] * 255).astype(np.uint8).tolist()
        # text = '{}:{:.1f}%'.format(class_names[cls_id], score * 100 )
        text = ' {}:{:.1f}m'.format("D",az)
        
        # txt_color = (0, 0, 0) if np.mean(_COLORS[cls_id]) > 0.5 else (255, 255, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX

        txt_size = cv2.getTextSize(text, font,0.4, 1)[0]
        # txt_size_z = cv2.getTextSize(text_z, font, 0.4, 1)[0]
        cv2.rectangle(img, (x0, y0), (x1, y1), (0,255,0), 1)

        # txt_bk_color = (_COLORS[cls_id] * 255 * 0.7).astype(np.uint8).tolist()

        blk = np.zeros(img.shape, np.uint8)  
        cv2.rectangle(
            blk,
            (x1-1, y1),
            (x1 - int(txt_size[0]), y1 - txt_size[1] - 1),
            (0,255,0),
            -1
        )
        img = cv2.addWeighted(img, 1.0, blk, 0.5, 1)

        # cv2.putText(img, text, (x0, y0 + txt_size[1]), font, 0.4, txt_color, thickness=1)
        cv2.putText(img, text, (x1 - txt_size[0], y1), font, 0.4, (255,255,255), thickness=1)



    return img

_COLORS = np.array(
    [
        0.929, 0.694, 0.125,
        0.000, 0.447, 0.741,
        0.850, 0.325, 0.098
    ]
).astype(np.float32).reshape(-1, 3)
# _COLORS = np.array(
#     [
#         0.000, 0.447, 0.741,
#         0.850, 0.325, 0.098,
#         0.929, 0.694, 0.125,
#         0.494, 0.184, 0.556,
#         0.466, 0.674, 0.188,
#         0.301, 0.745, 0.933,
#         0.635, 0.078, 0.184,
#         0.300, 0.300, 0.300,
#         0.600, 0.600, 0.600,
#         1.000, 0.000, 0.000,
#         1.000, 0.500, 0.000,
#         0.749, 0.749, 0.000,
#         0.000, 1.000, 0.000,
#         0.000, 0.000, 1.000,
#         0.667, 0.000, 1.000,
#         0.333, 0.333, 0.000,
#         0.333, 0.667, 0.000,
#         0.333, 1.000, 0.000,
#         0.667, 0.333, 0.000,
#         0.667, 0.667, 0.000,
#         0.667, 1.000, 0.000,
#         1.000, 0.333, 0.000,
#         1.000, 0.667, 0.000,
#         1.000, 1.000, 0.000,
#         0.000, 0.333, 0.500,
#         0.000, 0.667, 0.500,
#         0.000, 1.000, 0.500,
#         0.333, 0.000, 0.500,
#         0.333, 0.333, 0.500,
#         0.333, 0.667, 0.500,
#         0.333, 1.000, 0.500,
#         0.667, 0.000, 0.500,
#         0.667, 0.333, 0.500,
#         0.667, 0.667, 0.500,
#         0.667, 1.000, 0.500,
#         1.000, 0.000, 0.500,
#         1.000, 0.333, 0.500,
#         1.000, 0.667, 0.500,
#         1.000, 1.000, 0.500,
#         0.000, 0.333, 1.000,
#         0.000, 0.667, 1.000,
#         0.000, 1.000, 1.000,
#         0.333, 0.000, 1.000,
#         0.333, 0.333, 1.000,
#         0.333, 0.667, 1.000,
#         0.333, 1.000, 1.000,
#         0.667, 0.000, 1.000,
#         0.667, 0.333, 1.000,
#         0.667, 0.667, 1.000,
#         0.667, 1.000, 1.000,
#         1.000, 0.000, 1.000,
#         1.000, 0.333, 1.000,
#         1.000, 0.667, 1.000,
#         0.333, 0.000, 0.000,
#         0.500, 0.000, 0.000,
#         0.667, 0.000, 0.000,
#         0.833, 0.000, 0.000,
#         1.000, 0.000, 0.000,
#         0.000, 0.167, 0.000,
#         0.000, 0.333, 0.000,
#         0.000, 0.500, 0.000,
#         0.000, 0.667, 0.000,
#         0.000, 0.833, 0.000,
#         0.000, 1.000, 0.000,
#         0.000, 0.000, 0.167,
#         0.000, 0.000, 0.333,
#         0.000, 0.000, 0.500,
#         0.000, 0.000, 0.667,
#         0.000, 0.000, 0.833,
#         0.000, 0.000, 1.000,
#         0.000, 0.000, 0.000,
#         0.143, 0.143, 0.143,
#         0.286, 0.286, 0.286,
#         0.429, 0.429, 0.429,
#         0.571, 0.571, 0.571,
#         0.714, 0.714, 0.714,
#         0.857, 0.857, 0.857,
#         0.000, 0.447, 0.741,
#         0.314, 0.717, 0.741,
#         0.50, 0.5, 0
#     ]
# ).astype(np.float32).reshape(-1, 3)
