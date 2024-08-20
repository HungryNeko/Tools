import os
import xml.etree.ElementTree as ET
import shutil
from PIL import Image

# YOLO dir
label_folder = 'obb/obb-d/labels'
# image folder
image_folder = "obb/obb-d/images"
# output xml folder
output_folder = 'obb/obb-d/labels_xml'
# classmapping
class_mapping = {
    0:'Dredger',1:'Cell-Container',2:'Container',3:'LawEnforce',4:'Fishing',5:'ore-oil'
}

# 清空输出目录
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder, exist_ok=True)

def create_xml(label_file, img_file, size, objects):
    annotation = ET.Element("annotation")
    
    folder = ET.SubElement(annotation, "folder").text = os.path.basename(output_folder)
    filename = ET.SubElement(annotation, "filename").text = os.path.basename(img_file)
    
    size_elem = ET.SubElement(annotation, "size")
    width = ET.SubElement(size_elem, "width").text = str(size[0])
    height = ET.SubElement(size_elem, "height").text = str(size[1])
    depth = ET.SubElement(size_elem, "depth").text = str(size[2])
    
    segmented = ET.SubElement(annotation, "segmented").text = "0"
    
    for obj in objects:
        obj_elem = ET.SubElement(annotation, "object")
        name = ET.SubElement(obj_elem, "name").text = obj['name']
        pose = ET.SubElement(obj_elem, "pose").text = "Unspecified"
        truncated = ET.SubElement(obj_elem, "truncated").text = "0"
        occluded = ET.SubElement(obj_elem, "occluded").text = "0"
        difficult = ET.SubElement(obj_elem, "difficult").text = str(obj['difficult'])
        
        bndbox = ET.SubElement(obj_elem, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(int(obj['bndbox'][0]))
        ET.SubElement(bndbox, "ymin").text = str(int(obj['bndbox'][1]))
        ET.SubElement(bndbox, "xmax").text = str(int(obj['bndbox'][2]))
        ET.SubElement(bndbox, "ymax").text = str(int(obj['bndbox'][3]))
    
    tree = ET.ElementTree(annotation)
    tree.write(label_file, encoding='utf-8', xml_declaration=True)

def yolo_to_xml(label_folder, image_folder, output_folder, class_mapping):
    for filename in os.listdir(label_folder):
        if filename.endswith('.txt'):
            yolo_path = os.path.join(label_folder, filename)
            base_name = os.path.splitext(filename)[0]
            img_path = None

            # 查找与base_name匹配的图像文件
            for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff']:
                potential_img_path = os.path.join(image_folder, base_name + ext)
                if os.path.exists(potential_img_path):
                    img_path = potential_img_path
                    break

            if img_path is None:
                print(f"Image file not found for: {base_name}")
                continue
            
            # 获取图片尺寸
            with Image.open(img_path) as img:
                width, height = img.size
                depth = len(img.getbands())  # 通道数
            
            with open(yolo_path, 'r') as file:
                lines = file.readlines()
                
            objects = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) != 5:
                    print(f"Skipping invalid line in {filename}: {line}")
                    continue
                
                class_id = int(parts[0])
                x_center, y_center = float(parts[1]) * width, float(parts[2]) * height
                obj_width, obj_height = float(parts[3]) * width, float(parts[4]) * height
                
                xmin = x_center - (obj_width / 2)
                ymin = y_center - (obj_height / 2)
                xmax = x_center + (obj_width / 2)
                ymax = y_center + (obj_height / 2)
                
                objects.append({
                    'name': class_mapping[class_id],
                    'difficult': 0,
                    'bndbox': [xmin, ymin, xmax, ymax]
                })
            
            create_xml(os.path.join(output_folder, base_name + '.xml'), img_path, (width, height, depth), objects)

# 调用函数，设置实际的文件夹路径
yolo_to_xml(label_folder, image_folder, output_folder, class_mapping)