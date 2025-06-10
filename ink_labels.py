import os
import shutil
from PIL import Image
import numpy as np
import zarr
import argparse

# Disable decompression bomb protection for large images
Image.MAX_IMAGE_PIXELS = None

def main(input_path, output_path):
    # Create output directory if it doesn't exist
    if os.path.exists(output_path): shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)

    # Read the image and get the shape and dtype
    with Image.open(input_path) as img: data = np.array(img)
    dtype = data.dtype
    height, width = data.shape
    depth = 65
    
    # Read the images into the image stack
    image_stack = np.zeros((depth, height, width), dtype=dtype)

    for i in range(depth):
        image_stack[i] = data
        print(f"Processed {i}")

    # Save as Zarr v2
    print(f"Saving to {output_path}...")
    z = zarr.create(
        store=output_path,
        shape=(depth, height, width),
        dtype=dtype,
        chunks=(128, 128, 128),
        dimension_separator='/',
        compressor=zarr.Blosc(cname='zstd', clevel=5),
        write_empty_chunks=False,
    )

    z[:] = image_stack
    print("Zarr file created successfully!")

# python ink_labels.py /Users/yao/Desktop/full-scrolls/20230702185753/ink_labels.png ./output/ink_labels
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate ink labels Zarr file')
    parser.add_argument('input_path', type=str, help='Ink labels image path')
    parser.add_argument('output_path', type=str, help='Output path')
    args = parser.parse_args()

    main(args.input_path, args.output_path) 