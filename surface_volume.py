import os
import zarr
import tifffile
import shutil
import numpy as np
import argparse
from dotenv import load_dotenv

def main(start_coord, end_coord):
    # Load environment variables
    load_dotenv()
    base_dir = os.getenv('BASE_DIR')
    output_path = os.path.join("hello-world-dataset", "surface_volume")

    if base_dir is None:
        raise Exception(f"Base directory {base_dir} does not exist")
    
    zo, yo, xo = start_coord
    zp, yp, xp = end_coord
    
    # Create output directory if it doesn't exist
    if os.path.exists(output_path): shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)

    # Pre-allocate a numpy array for all images
    tiff_files = sorted([f for f in os.listdir(base_dir) if f.endswith('.tif')])[zo:zp]
    first_image = tifffile.imread(os.path.join(base_dir, tiff_files[0]))
    height, width = first_image.shape
    dtype = first_image.dtype

    image_stack = np.zeros((len(tiff_files), yp-yo, xp-xo), dtype=dtype)
    
    # Read the images into the image stack
    for i in range(zo, zp):
        data = tifffile.imread(os.path.join(base_dir, tiff_files[i]))
        image_stack[i-zo] = data[yo:yp, xo:xp]
        print(f"Processed {i} of {len(tiff_files)}")

    print("Image stack shape:", image_stack.shape)

    # Save as Zarr v2
    print(f"Saving to {output_path}...")
    z = zarr.create(
        store=output_path,
        shape=(65, height, width),
        dtype=dtype,
        chunks=(128, 128, 128),
        dimension_separator='/',
        compressor=zarr.Blosc(cname='zstd', clevel=5),
        write_empty_chunks=False,
    )

    z[zo:zp, yo:yp, xo:xp] = image_stack
    print("Zarr file created successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate surface volume Zarr file')
    parser.add_argument('--zo', type=int, help='Starting z-axis')
    parser.add_argument('--yo', type=int, help='Starting y-axis')
    parser.add_argument('--xo', type=int, help='Starting x-axis')
    parser.add_argument('--zp', type=int, help='Ending z-axis')
    parser.add_argument('--yp', type=int, help='Ending y-axis')
    parser.add_argument('--xp', type=int, help='Ending x-axis')

    args = parser.parse_args()
    start_coord = (args.zo, args.yo, args.xo)
    end_coord = (args.zp, args.yp, args.xp)

    main(start_coord, end_coord) 