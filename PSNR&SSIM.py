import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from tqdm import tqdm  # 导入tqdm库

def calculate_psnr(img1, img2):
    """Calculate the PSNR between two images."""
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))

def calculate_ssim(img1, img2):
    """Calculate SSIM with dynamic window size based on image dimensions."""
    min_dim = min(img1.shape[0], img1.shape[1], img2.shape[0], img2.shape[1])
    # 确保win_size是奇数并且小于最小尺寸，同时不小于3（以避免极小图像的问题）
    win_size = min(7, min_dim - 1 if min_dim % 2 == 0 else min_dim)
    if win_size < 3:  # 对非常小的图像，无法计算SSIM
        print("Warning: Image too small for SSIM calculation with win_size.")
        return None
    return ssim(img1, img2, win_size=win_size, channel_axis=2)

def calculate_folder_metrics(folder1, folder2):
    """Calculate average PSNR and SSIM for matching images in two folders."""
    psnr_values = []
    ssim_values = []
    common_images = set(os.listdir(folder1)) & set(os.listdir(folder2))

    for img_name in tqdm(common_images, desc=f"Comparing {folder1} with {folder2}"):  # 添加进度条
        img1_path = os.path.join(folder1, img_name)
        img2_path = os.path.join(folder2, img_name)
        img1 = cv2.imread(img1_path, cv2.IMREAD_COLOR)
        img2 = cv2.imread(img2_path, cv2.IMREAD_COLOR)

        if img1 is None or img2 is None:
            print(f"Error loading image: {img_name}")
            continue

        img1 = cv2.resize(img1, (img2.shape[1], img2.shape[0]))  # 保证两张图片尺寸一致
        psnr_value = calculate_psnr(img1, img2)
        ssim_value = calculate_ssim(img1, img2)

        psnr_values.append(psnr_value)
        if ssim_value is not None:
            ssim_values.append(ssim_value)

    overall_psnr = np.mean(psnr_values) if psnr_values else 0
    overall_ssim = np.mean(ssim_values) if ssim_values else 0

    return overall_psnr, overall_ssim

def compare_image_folders(folders):
    """Run PSNR and SSIM comparison for each folder pair and output results."""
    for folder1, folder2, name in folders:
        print(f"Starting comparison: {name}")
        overall_psnr, overall_ssim = calculate_folder_metrics(folder1, folder2)
        print(name)
        print(f"Overall PSNR for {folder1} vs {folder2}: {overall_psnr}")
        print(f"Overall SSIM for {folder1} vs {folder2}: {overall_ssim}")
        print("________________________________________________________")

if __name__ == "__main__":
    folders_to_compare = [
        ("data/lib/images", "data/lib/input", "lib color"),
        ("data/lib/input", "data/lib/inputp", "lib su"),
        ("data/lib/images", "data/lib/inputp", "lib full"),
        ("data/line2/images", "data/line2/input", "line2 color"),
        ("data/line2/input", "data/line2/inputp", "line2 su"),
        ("data/line2/images", "data/line2/inputp", "line2 full"),
        ("data/train/images", "data/train/input", "train color"),
        ("data/train/input", "data/train/inputp", "train su"),
        ("data/train/images", "data/train/inputp", "train full"),
        ("data/lib/images", "data/lib/input", "me color"),
        ("data/lib/input", "data/lib/inputp", "me su"),
        ("data/lib/images", "data/lib/inputp", "me full")
    ]

    compare_image_folders(folders_to_compare)