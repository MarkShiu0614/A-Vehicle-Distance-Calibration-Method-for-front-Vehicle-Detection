
# img_dir = '/home/lab602.11077016/.pipeline/11077016/YOLOXt2/datasets/COCO/val2017/'
# json_file_path = '/home/lab602.11077016/.pipeline/11077016/YOLOXt2/datasets/COCO/annotations/instances_val2017.json'
# save_dir = '/home/lab602.11077016/.pipeline/11077016/YOLOXt2/datasets/COCO/save/' 

import os
import json

# 指定COCO JSON标注文件的路径
coco_json_path = '/home/lab602.11077016/.pipeline/11077016/YOLOXt2/datasets/COCO/annotations/instances_val2017.json'
# 指定存储YOLO标注的目录
yolo_labels_dir = '/home/lab602.11077016/.pipeline/11077016/YOLOXt2/datasets/COCO/save/'
# 指定图像的目录（用于获取图像的大小）
img_dir = '/home/lab602.11077016/.pipeline/11077016/YOLOXt2/datasets/COCO/val2017/'

if not os.path.exists(yolo_labels_dir):
    os.makedirs(yolo_labels_dir)

# 加载COCO标注
with open(coco_json_path, 'r') as f:
    coco_data = json.load(f)

# 创建一个映射，将COCO的图像ID映射到宽度和高度
img_id_to_size = {img['id']: (img['width'], img['height']) for img in coco_data['images']}

# 遍历每个COCO标注
for ann in coco_data['annotations']:
    img_id = ann['image_id']
    img_w, img_h = img_id_to_size[img_id]
    # 获取对象的类别ID
    cat_id = ann['category_id'] - 1  # 在YOLO中，类别ID从0开始

    # 获取对象的边界框并进行归一化处理
    bbox = ann['bbox']  # 格式：[x, y, width, height]
    x_center = (bbox[0] + bbox[2] / 2) / img_w
    y_center = (bbox[1] + bbox[3] / 2) / img_h
    bbox_w = bbox[2] / img_w
    bbox_h = bbox[3] / img_h
    z = ann['z']
    # 创建YOLO标注文件
    yolo_ann_file = os.path.join(yolo_labels_dir, f'{str(img_id).zfill(6)}.txt')
    with open(yolo_ann_file, 'a') as f:
        # 在YOLO中，每一行的格式为：类别id x_center y_center width height
        f.write(f'{cat_id} {x_center} {y_center} {bbox_w} {bbox_h} {z}\n')
