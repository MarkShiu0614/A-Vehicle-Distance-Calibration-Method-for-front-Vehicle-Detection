 
import cv2
import os
import numpy as np

# classes = [
#      "Car",
#      "Van",
#      "Truck",
#      "Tram"]    # KITTI

classes = ["car", "human", "track"]     # nuScence

img_dir = '/home/lab602.11077016/.pipeline/11077016/YOLOXt2/datasets/ppt_image/image/'
label_dir = '/home/lab602.11077016/.pipeline/11077016/YOLOXt2/datasets/ppt_image/label/'
save_dir = '/home/lab602.11077016/.pipeline/11077016/YOLOXt2/datasets/ppt_image/save1/' # 事先新建一个文件夹，用来存放标注好的图片
 
lable_file = os.listdir(label_dir)
img_file = os.listdir(img_dir)

_COLORS = np.array(
    [
        0.929, 0.694, 0.125,    # 1 class
        0.000, 0.447, 0.741,    # 2 class
        0.850, 0.325, 0.098,    # 3 class
        0.500, 0.000, 0.500     # 4 class
    ]
).astype(np.float32).reshape(-1, 3)


for file in lable_file:
 
    file_dir = os.path.join(label_dir, file)
 
    with open(file_dir, 'r') as f:
        print(os.path.join(img_dir, file.split('.')[0]+'.jpg'))
        image_src = cv2.imread(os.path.join(img_dir, file.split('.')[0]+'.jpg'))
        image_row = image_src.shape[0]
        image_col = image_src.shape[1]
 
        for line in f.readlines():
            cls_id = int(line.split(' ')[0])
            x_ = float(line.split(' ')[1])
            y_ = float(line.split(' ')[2])
            w_ = float(line.split(' ')[3])
            h_ = float(line.split(' ')[4])
            az = float(line.split(' ')[5])  
            # print(cls_id)
            # print(az)
            w = image_col
            h = image_row
 
            x1 = w * x_ - 0.5 * w * w_
            x2 = w * x_ + 0.5 * w * w_
            y1 = h * y_ - 0.5 * h * h_
            y2 = h * y_ + 0.5 * h * h_
 
            color = (_COLORS[cls_id] * 255).astype(np.uint8).tolist()
            text = classes[int(cls_id)]+': 100%'
            # text = text + ' {}:{:.1f}m'.format("D",az)
            text_z = '{:.1f}m'.format(az)
        
            txt_color = (0, 0, 0) if np.mean(_COLORS[cls_id]) > 0.5 else (255, 255, 255)
            font = cv2.FONT_HERSHEY_SIMPLEX

            txt_size = cv2.getTextSize(text, font, 0.4, 1)[0]
            txt_z_size = cv2.getTextSize(text_z,font,2,5 )[0]

            draw = cv2.rectangle(image_src,(int(x1),int(y1)),(int(x2),int(y2)),[229,176,36],2)  # [229,176,36]

            txt_bk_color = (_COLORS[cls_id] * 255 * 0.7).astype(np.uint8).tolist()

            blk = np.zeros(image_src.shape, np.uint8)  
            cv2.rectangle(
                blk,
                (int(x1), int(y1 + 1)),
                (int(x1 + txt_size[0] + 1), int(y1 + int(1.5*txt_size[1]))),
                txt_bk_color,
                -1
            )
            # image_src = cv2.addWeighted(image_src, 1.0, blk, 0.5, 1)          
            
            # cv2.putText(image_src, text, (int(x1), int(y1+txt_size[1])), font, 0.4, txt_color, thickness=1)

            cv2.putText(image_src, text_z, (int((x1+x2)/2-(txt_z_size[1]/2)), int((y1+y2)/2+15)), font, 1.8, (0,255,255) , thickness=7)  # 外匡黃
            cv2.putText(image_src, text_z, (int((x1+x2)/2-(txt_z_size[1]/2)), int((y1+y2)/2+15)), font, 1.8, (0,0,255) , thickness=3) # 數字紅

        # cv2.imwrite(os.path.join(save_dir, file.split('.')[0]+'.jpg'), draw)
        cv2.imwrite(os.path.join(save_dir, file.split('.')[0]+'.jpg'), draw)

 