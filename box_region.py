from PIL import Image, ImageDraw
import re

image_path = "/Users/yao/Desktop/full-scrolls/20230702185753/20230702185753_inference_polytrope-inklabels-2024-08-16.png"
output_path = "/Users/yao/Desktop/full-scrolls/20230702185753/box_region.png"

input_str = """
# Line 01
--x 1128 --y 7416 --z 0 --w 576 --h 624 --d 65
--x 1992 --y 10848 --z 0 --w 552 --h 720 --d 65

# Line 02
--x 1680 --y 6432 --z 0 --w 744 --h 960 --d 65

# Line 03
--x 2328 --y 5784 --z 0 --w 552 --h 456 --d 65
--x 3288 --y 9456 --z 0 --w 552 --h 552 --d 65
--x 3840 --y 11424 --z 0 --w 672 --h 504 --d 65

# Line 04
--x 3384 --y 6528 --z 0 --w 528 --h 600 --d 65
--x 3600 --y 7488 --z 0 --w 600 --h 552 --d 65
--x 4080 --y 9000 --z 0 --w 672 --h 624 --d 65
--x 4728 --y 11184 --z 0 --w 576 --h 600 --d 65

# Line 05
--x 3672 --y 4032 --z 0 --w 672 --h 960 --d 65

# Line 06
--x 5280 --y 6864 --z 0 --w 576 --h 504 --d 65

# Line 07

# Line 08
--x 6840 --y 6144 --z 0 --w 672 --h 960 --d 65
--x 8112 --y 10464 --z 0 --w 936 --h 528 --d 65

# Line 09

# Line 10
--x 8016 --y 3144 --z 0 --w 624 --h 792 --d 65
--x 8304 --y 4032 --z 0 --w 696 --h 912 --d 65

# Line 11
--x 9360 --y 5304 --z 0 --w 744 --h 792 --d 65

# Line 12
--x 9936 --y 3696 --z 0 --w 624 --h 840 --d 65

# Line 13

# Line 14

# Line 15
--x 12480 --y 3432 --z 0 --w 720 --h 912 --d 65

# Line 16
--x 13272 --y 3024 --z 0 --w 720 --h 984 --d 65

# Line 17
--x 15480 --y 7224 --z 0 --w 600 --h 912 --d 65

# Line 18
"""

# Disable decompression bomb protection for large images
Image.MAX_IMAGE_PIXELS = None

def draw_boxes_on_image(image_path, input_str, output_path):
    img = Image.open(image_path)
    
    if img.mode == 'L':
        img = img.convert('RGB')
    
    draw = ImageDraw.Draw(img)
    yellow = (255, 255, 0)
    
    pattern = r"--x (\d+) --y (\d+) --z \d+ --w (\d+) --h (\d+) --d \d+"
    matches = re.findall(pattern, input_str)
    
    for match in matches:
        x, y, w, h = map(int, match)
        x2, y2 = x + w, y + h
        draw.rectangle((x, y, x2, y2), outline=yellow, width=30)
    
    img.save(output_path)

draw_boxes_on_image(image_path, input_str, output_path)
