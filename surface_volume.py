import os
import zarr
import tifffile
import shutil
import numpy as np
import argparse
from dotenv import load_dotenv

def main(start_coord, end_coord, overwrite=True):
    # Load environment variables
    load_dotenv()
    base_dir = os.getenv('BASE_DIR')
    output_path = os.path.join("hello-world-dataset", "surface_volume")

    if base_dir is None:
        raise Exception(f"Base directory {base_dir} does not exist")

    zo, yo, xo = start_coord
    zp, yp, xp = end_coord

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

    if os.path.exists(output_path) and overwrite:
        shutil.rmtree(output_path)

    if not os.path.exists(output_path):
        z = zarr.create(
            store=output_path,
            shape=(65, height, width),
            dtype=dtype,
            chunks=(128, 128, 128),
            dimension_separator='/',
            compressor=zarr.Blosc(cname='zstd', clevel=5),
            write_empty_chunks=False,
        )
    else:
        z = zarr.open(output_path)

    z[zo:zp, yo:yp, xo:xp] = image_stack
    print("Zarr file created successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate surface volume Zarr file')
    parser.add_argument('--x', type=int, help='Starting x-axis')
    parser.add_argument('--y', type=int, help='Starting y-axis')
    parser.add_argument('--z', type=int, help='Starting z-axis')
    parser.add_argument('--w', type=int, help='Width of the volume')
    parser.add_argument('--h', type=int, help='Height of the volume')
    parser.add_argument('--d', type=int, help='Depth of the volume')
    parser.add_argument('--overwrite', action="store_true", help="Overwrite the output directory, if it already exists")

    args = parser.parse_args()
    start_coord = (args.z, args.y, args.x)
    end_coord = (args.z + args.d, args.y + args.h, args.x + args.w)

    main(start_coord, end_coord, args.overwrite)
