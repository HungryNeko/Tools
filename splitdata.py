import os
import random
from shutil import copyfile, rmtree


# dataset path
dataset_path = './datasets/SRSDD_normal'

# 临时的train和val文件夹路径
train_images_path = os.path.join(dataset_path, 'images/train')
val_images_path = os.path.join(dataset_path, 'images/val')
train_labels_path = os.path.join(dataset_path, 'labels/train')
val_labels_path = os.path.join(dataset_path, 'labels/val')

# 删除旧的文件夹
if os.path.exists(train_images_path):
    rmtree(train_images_path)
if os.path.exists(val_images_path):
    rmtree(val_images_path)
if os.path.exists(train_labels_path):
    rmtree(train_labels_path)
if os.path.exists(val_labels_path):
    rmtree(val_labels_path)

# 创建新的文件夹
os.makedirs(train_images_path)
os.makedirs(val_images_path)
os.makedirs(train_labels_path)
os.makedirs(val_labels_path)

# 获取所有图像文件名
all_images = os.listdir(os.path.join(dataset_path, 'images'))
random.shuffle(all_images)

# 划分训练集和验证集，比例为80:20
split_index = int(len(all_images) * 0.8)
train_images = all_images[:split_index]
val_images = all_images[split_index:]

# 复制图像和标签到对应的文件夹
for image in train_images:
    try:
        copyfile(os.path.join(dataset_path, 'images', image), os.path.join(train_images_path, image))
        label = image.replace('.png', '.txt')
        copyfile(os.path.join(dataset_path, 'labels', label), os.path.join(train_labels_path, label))
    except Exception as e:
        print(e)

for image in val_images:
    try:
        copyfile(os.path.join(dataset_path, 'images', image), os.path.join(val_images_path, image))
        label = image.replace('.png', '.txt')
        copyfile(os.path.join(dataset_path, 'labels', label), os.path.join(val_labels_path, label))
    except Exception as e:
        print(e)