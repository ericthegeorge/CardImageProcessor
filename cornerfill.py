import cv2
import numpy as np
import os

def fill_corners_solid(input_path, output_path, output_mask_path):

    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img.shape[2] != 4:
        raise ValueError("Image does not have an alpha channel")

    # cv2.imshow("initial image", img)
    # cv2.waitKey()

    bgr = img[:, :, :3]  # 3-channel BGR
    alpha = img[:, :, 3]  # 1-channel alpha

    # Create mask where alpha = 0 (fully transparent)
    _, mask = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    mask = cv2.dilate(mask, kernel, iterations=1)


    # cv2.imshow("mask", mask)
    # cv2.waitKey()


    inpaint_radius = 5  # Increased from default 3
    result = bgr.copy()

    # First pass - NS algorithm (better for textures)
    result = cv2.inpaint(result, mask, inpaint_radius, cv2.INPAINT_NS)

    # Second pass - Telea algorithm (better for smooth areas)
    result = cv2.inpaint(result, mask, inpaint_radius, cv2.INPAINT_TELEA)

    # Edge-preserving smoothing
    # result = cv2.edgePreservingFilter(result, flags=1, sigma_s=60, sigma_r=0.4)

    cv2.imwrite(output_path, result)
    print(f"Done: {input_path}")


# Batch processing with alpha removal
base_dir = "D:\\VanguardImages"
output_subdir = "ContentAwareFilled"
output_maskdir = "Masks"

# for vcl in range(22, 43):
    # input_dir = os.path.join(base_dir, str(vcl))
    # output_dir = os.path.join(base_dir, str(vcl), output_subdir)

#     if not os.path.exists(input_dir):
#         print(f"Skipping: {input_dir} (does not exist)")
#         continue

#     os.makedirs(output_dir, exist_ok=True)

#     for filename in os.listdir(input_dir):
filename = "vback.png"
if filename.lower().endswith(".png"):
    input_dir = base_dir
    output_dir = base_dir
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename)

    fill_corners_solid(input_path, output_path, "D:\\VanguardImages\\vbackmasks")  # Lower = more sensitive to dark pixels
    print(f"Fixed corners: {filename}")

    # print(f"Completed volume: {vcl}")

# print("Corner filling complete!")