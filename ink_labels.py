import os
import tifffile
import shutil
from PIL import Image
import numpy as np
import zarr

# Disable decompression bomb protection for large images
Image.MAX_IMAGE_PIXELS = None

def main():
    # Define input and output paths
    base_dir = "/Users/yao/Desktop/full-scrolls/20230702185753/ink_labels.png"
    output_path = os.path.join("output", "ink_labels")

     # Define the volume to extract
    start_coord = (0, 0, 0)  # (z, y, x) starting coordinates
    end_coord = (65, 13513, 17381) 
    
    z0, y0, x0 = start_coord
    z1, y1, x1 = end_coord

    # Create output directory if it doesn't exist
    if os.path.exists(output_path): shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)

    # Read the image and get the shape and dtype
    with Image.open(base_dir) as img: data = np.array(img)
    dtype = data.dtype
    height, width = data.shape
    
    # Read the images into the image stack
    image_stack = np.zeros((z1-z0, y1-y0, x1-x0), dtype=dtype)

    for i in range(z0, z1):
        image_stack[i-z0] = data[y0:y1, x0:x1]
        print(f"Processed {i}")

    # Save as Zarr v2
    print(f"Saving to {output_path}...")
    z = zarr.create(
        store=output_path,
        shape=(65, height, width),
        dtype=dtype,
        chunks=(128, 128, 128),  # Chunk by slice for efficient access
        dimension_separator='/',
        order='C',
        zarr_format=2,  # Specify Zarr v2 format
    )

    z[z0:z1, y0:y1, x0:x1] = image_stack

    print("Zarr file created successfully!")

if __name__ == "__main__":
    # # Resize the base image to a specified size
    # with Image.open("/Users/yao/Desktop/full-scrolls/20230702185753/20230702185753_inference_polytrope-inklabels-2024-08-16.png") as img:
    #         print(f"Original image size: {img.size}")
    #         resized_img = img.resize((17381, 13513))
    #         resized_img.save(os.path.join(os.path.dirname(base_dir), "ink_labels.png"))
    #         print(f"Resized image size: {resized_img.size}")

    main() 