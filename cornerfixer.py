from PIL import Image, ImageDraw, ImageCms
import os
def process_card(input_path, output_path, corner_radius=21):
    # Open the image, remove ICC profile, and convert to RGB
    img = Image.open(input_path)

    # img.save("D:\\VanguardImages\\42\\pre.jpg", "JPEG")
    # print(img.mode)

    cmyk_profile = ImageCms.getOpenProfile("D:\\VanguardImages\\42\\testprofile.icc")
    srgb_profile = ImageCms.createProfile("sRGB")

    # transform = ImageCms.buildTransform(cmyk_profile, srgb_profile, "CMYK", "RGB")

    # rgb_img = ImageCms.applyTransform(img, transform)

    # rgb_img.save("D:\\VanguardImages\\42\\transformed.png")

    # img = rgb_img
    img = img

    img = img.convert("RGB")  # Ensure no alpha channel exists yet
    # print(img.format)
    # img.save("D:\\VanguardImages\\42\\midnoalpha.jpg", "JPEG")
    # Create a mask for rounded corners (white = opaque, black = transparent)
    mask = Image.new("L", img.size, 255)
    draw = ImageDraw.Draw(mask)

    width, height = img.size

    # Draw black rectangles in the corners (to be made transparent)
    draw.rectangle((0, 0, corner_radius, corner_radius), fill=0)
    draw.rectangle((width - corner_radius, 0, width, corner_radius), fill=0)
    draw.rectangle((0, height - corner_radius, corner_radius, height), fill=0)
    draw.rectangle((width - corner_radius, height - corner_radius, width, height), fill=0)

    # Draw white circles to round the corners
    draw.ellipse((0, 0, corner_radius * 2, corner_radius * 2), fill=255)
    draw.ellipse((width - corner_radius * 2, 0, width, corner_radius * 2), fill=255)
    draw.ellipse((0, height - corner_radius * 2, corner_radius * 2, height), fill=255)
    draw.ellipse((width - corner_radius * 2, height - corner_radius * 2, width, height), fill=255)

    # Convert the original image to RGBA and apply the mask as alpha
    rgba_img = img.convert("RGBA")
    # img.save("D:\\VanguardImages\\42\\midalpha.png", "PNG")

    rgba_img.putalpha(mask)

    # Save the result (ensure no ICC profile is saved)
    rgba_img.save(output_path, "PNG", icc_profile=None)
    print(f"Cornered: {input_path}")

# Usage
for i in range (22, 43):
    folder = os.path.join("D:\\VanguardImages", str(i))
    if not os.path.isdir(folder):
        print(f"Skipping missing folder: {folder}")
        continue
    for file in os.listdir(folder):
        if file.lower().endswith((".jpg", ".jpeg")):
            input_path = os.path.join(folder, file)
            output_path = os.path.join(folder, f"{file.rsplit('.', 1)[0]}.png")
            process_card(input_path, output_path)