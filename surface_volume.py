import os
import zarr
import tifffile
import shutil
import numpy as np

def main():
    # Define input and output paths
    base_dir = "/Users/yao/Desktop/full-scrolls/20230702185753/layers/"
    output_path = os.path.join("output", "surface_volume")

     # Define the volume to extract
    start_coord = (0, 3047, 13152)  # (z, y, x) starting coordinates
    end_coord = (10, 3863, 14128) 
    
    z0, y0, x0 = start_coord
    z1, y1, x1 = end_coord
    
    # Create output directory if it doesn't exist
    if os.path.exists(output_path): shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)

    # Pre-allocate a numpy array for all images
    tiff_files = sorted([f for f in os.listdir(base_dir) if f.endswith('.tif')])
    first_image = tifffile.imread(os.path.join(base_dir, tiff_files[0]))
    height, width = first_image.shape
    dtype = first_image.dtype

    image_stack = np.zeros((len(tiff_files), y1-y0, x1-x0), dtype=dtype)
    
    # Read the images into the image stack
    for i in range(z0, z1):
        data = tifffile.imread(os.path.join(base_dir, tiff_files[i]))
        image_stack[i-z0] = data[y0:y1, x0:x1]
        print(f"Processed {i} of {len(tiff_files)}")

    print("Image stack shape:", image_stack.shape)

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
    main() 