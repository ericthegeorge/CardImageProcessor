from PIL import Image, ImageFilter
import os
import subprocess
# import torch
# from realesrgan import RealESRGANer
# import numpy as np
# import cv2


# Parameters
bleed_mm = 1.5  # Desired physical bleed in mm
blur_radius = 20
base_dir = "D:\\VanguardImages"
# input_dir = "D:\\VanguardImages\\Booster1-3"  # Replace with your actual folder
# output_dir = "D:\\VanguardImages\\Booster1-3Mirrored"
# upscaled_output_dir = "D:\VanguardImages\Booster1-3Upscaled"
fallback_dpi = 300  # If image has no DPI info

executable_path = "realesrgan-ncnn-vulkan.exe"  # Full path if not in same dir
# command = [
#     executable_path,
#     "-i", input_image,
#     "-o", output_image
# ]


# Make sure output folder exists
# os.makedirs(output_dir, exist_ok=True)

def add_bleed_blur(input_path, output_path, upscaled_output_path, fallback_dpi=300):
    img = Image.open(input_path)
    w, h = img.size


    # trim_amount = 1
    # h_trim_amount = 0
    # left = 0
    # right = w-trim_amount

    # trimmed = img.crop((left, h_trim_amount, right, h))
    # #                              + 1
    # stretched = trimmed.resize((w, h), resample=Image.LANCZOS)
    # # stretched.save(output_path, dpi=(dpi, dpi))
    # w, h = stretched.size
    # print(f"stretched for maelstrom only: {output_path}, w: {w}, h: {h}")
    # img = stretched

    # Extract DPI or fall back
    dpi = img.info.get('dpi', (fallback_dpi, fallback_dpi))[0]
    if dpi == 0 or dpi == fallback_dpi:
        hz = w/2.48
        vt = h/3.46
        dpi = int((hz + vt)/2)



    # bleed_px = int((bleed_mm / 25.4) * dpi)
    bleed_px = 27
    h_px_offset = 0
    bleed_px_h = bleed_px + h_px_offset
    bleed_px_v = bleed_px
    # bleed_px = 38
    print(f"DPI: {dpi}")
    # print(f"Bleed mm / 25.4 * DPI: {(bleed_mm / 25.4) * dpi}")
    print(f"Bleed px: {bleed_px}")
    new_w, new_h = w + 2 * bleed_px_h, h + 2 * bleed_px_v
    blurred_base = Image.new("RGBA", (new_w, new_h))


    # Paste original image in center
    blurred_base.paste(img, (bleed_px_h, bleed_px_v))

    # blur_radius_coefficient = 10


    top = img.crop((0, 0, w, bleed_px_v)).transpose(Image.FLIP_TOP_BOTTOM)
    bottom = img.crop((0, h - bleed_px_v, w, h)).transpose(Image.FLIP_TOP_BOTTOM)
    blurred_base.paste(top, (bleed_px_h, 0))
    blurred_base.paste(bottom, (bleed_px_h, h + bleed_px_v))

    left = img.crop((0, 0, bleed_px_h, h)).transpose(Image.FLIP_LEFT_RIGHT)
    right = img.crop((w - bleed_px_h, 0, w, h)).transpose(Image.FLIP_LEFT_RIGHT)
    blurred_base.paste(left, (0, bleed_px_v))
    blurred_base.paste(right, (w + bleed_px_h, bleed_px_v))


    tl = img.crop((0, 0, bleed_px_h, bleed_px_v)).transpose(Image.ROTATE_180)
    tr = img.crop((w - bleed_px_h, 0, w, bleed_px_v)).transpose(Image.ROTATE_180)
    bl = img.crop((0, h - bleed_px_v, bleed_px_h, h)).transpose(Image.ROTATE_180)
    br = img.crop((w - bleed_px_h, h - bleed_px_v, w, h)).transpose(Image.ROTATE_180)

    blurred_base.paste(tl, (0, 0))
    blurred_base.paste(tr, (w + bleed_px_h, 0))
    blurred_base.paste(bl, (0, h + bleed_px_v))
    blurred_base.paste(br, (w + bleed_px_h, h + bleed_px_v))





    # # Mirror strips from edges
    # top = img.crop((0, 0, w, bleed_px)).transpose(Image.FLIP_TOP_BOTTOM)
    # bottom = img.crop((0, h - bleed_px, w, h)).transpose(Image.FLIP_TOP_BOTTOM)
    # left = img.crop((0, 0, bleed_px, h)).transpose(Image.FLIP_LEFT_RIGHT)
    # right = img.crop((w - bleed_px, 0, w, h)).transpose(Image.FLIP_LEFT_RIGHT)

    # # Corners (mirror diagonally)
    # tl = img.crop((0, 0, bleed_px, bleed_px)).transpose(Image.ROTATE_180)
    # tr = img.crop((w - bleed_px, 0, w, bleed_px)).transpose(Image.ROTATE_180)
    # bl = img.crop((0, h - bleed_px, bleed_px, h)).transpose(Image.ROTATE_180)
    # br = img.crop((w - bleed_px, h - bleed_px, w, h)).transpose(Image.ROTATE_180)

    # # Apply blur
    # # top = top.filter(ImageFilter.GaussianBlur(radius=bleed_px//blur_radius_coefficient))
    # # bottom = bottom.filter(ImageFilter.GaussianBlur(radius=bleed_px//blur_radius_coefficient))
    # # left = left.filter(ImageFilter.GaussianBlur(radius=bleed_px//blur_radius_coefficient))
    # # right = right.filter(ImageFilter.GaussianBlur(radius=bleed_px//blur_radius_coefficient))
    # # tl = tl.filter(ImageFilter.GaussianBlur(radius=bleed_px//blur_radius_coefficient))
    # # tr = tr.filter(ImageFilter.GaussianBlur(radius=bleed_px//blur_radius_coefficient))
    # # bl = bl.filter(ImageFilter.GaussianBlur(radius=bleed_px//blur_radius_coefficient))
    # # br = br.filter(ImageFilter.GaussianBlur(radius=bleed_px//blur_radius_coefficient))

    # # Paste all around
    # blurred_base.paste(top, (bleed_px, 0))
    # blurred_base.paste(bottom, (bleed_px, h + bleed_px))
    # blurred_base.paste(left, (0, bleed_px))
    # blurred_base.paste(right, (w + bleed_px, bleed_px))

    # blurred_base.paste(tl, (0, 0))
    # blurred_base.paste(tr, (w + bleed_px, 0))
    # blurred_base.paste(bl, (0, h + bleed_px))
    # blurred_base.paste(br, (w + bleed_px, h + bleed_px))

    # Save with original DPI

    trim_amount = 8
    h_trim_amount = 1
    # 1 for non-maelstrom
    left = trim_amount
    right = new_w-trim_amount

    trimmed = blurred_base.crop((left, h_trim_amount, right, new_h))
    stretched = trimmed.resize((new_w, new_h), resample=Image.LANCZOS)
    stretched.save(output_path, dpi=(dpi, dpi))
    print(f"Saved mirrored bleed image: {output_path}")


    command = [
    executable_path,
    "-i", output_path,
    "-o", upscaled_output_path
    ]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Upscaling complete.")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error occurred while running Real-ESRGAN:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)

    # output_img.save(upscaled_output_path, dpi = (dpi, dpi))
    # print(f"Saved upscaled bleed image: {upscaled_output_path}")




# # Process images
# for vcl in range (22, 43):

#     input_dir = os.path.join(base_dir, str(vcl), "ContentAwareFilled")
#     output_dir = os.path.join(base_dir, str(vcl), "BlurredBases")
#     upscaled_output_dir = os.path.join(base_dir, str(vcl), "Upscaled")

#     if not os.path.exists(input_dir):
#         print(f"Skipping: {input_dir} (does not exist)")
#         continue  # Skip this index cleanly


#     os.makedirs(output_dir, exist_ok=True)
#     os.makedirs(upscaled_output_dir, exist_ok=True)

#     for filename in os.listdir(input_dir):
filename = "vback.png"
if filename.lower().endswith((".png")):
    # input_path = os.path.join(input_dir, filename)
    input_path = os.path.join("D:\\VanguardImages", filename)

    img = Image.open(input_path)

    # Get DPI (Pillow stores it as (xdpi, ydpi))
    dpi = img.info.get('dpi', (fallback_dpi, fallback_dpi))[0]  # Use x DPI
    if dpi == 0:
        dpi = fallback_dpi

    # Calculate bleed in pixels
    bleed_px = int((bleed_mm / 25.4) * dpi)

    w, h = img.size
    output_dir = "D:\\VanguardImages"
    upscaled_output_dir = output_dir
    output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.png")
    upscaled_output_path = os.path.join(upscaled_output_dir, f"{os.path.splitext(filename)[0]}.png")


    add_bleed_blur(input_path, output_path, upscaled_output_path)
    # print(f"Done. Processed: {vcl}")
