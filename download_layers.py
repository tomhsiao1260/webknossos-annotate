import os
import requests
from tqdm import tqdm
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

USERNAME = os.getenv('VESUVIUS_USERNAME')
PASSWORD = os.getenv('VESUVIUS_PASSWORD')

BASE_URL = os.getenv('BASE_URL')
BASE_DIR = os.getenv('BASE_DIR')

if not USERNAME or not PASSWORD:
    raise ValueError("Please set WEBKNOSSOS_USERNAME and WEBKNOSSOS_PASSWORD in .env file")

os.makedirs("images", exist_ok=True)

def download_file(url, filename):
    """Download a single file with progress bar"""
    response = requests.get(url, auth=(USERNAME, PASSWORD), stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)

# python download_layers.py --start 0 --count 65
def main():
    parser = argparse.ArgumentParser(description="Download a range of TIFF images with authentication.")
    parser.add_argument('--start', type=int, default=0, help='Start index (inclusive), e.g. 10')
    parser.add_argument('--count', type=int, default=65, help='Number of images to download')
    args = parser.parse_args()

    start = args.start
    count = args.count
    end = start + count

    for i in range(start, end):
        filename = f"{i:02d}.tif"
        url = BASE_URL + filename
        output_path = os.path.join(BASE_DIR, filename)
        
        print(f"\nDownloading {filename}...")
        try:
            if os.path.exists(output_path):
                print(f"Skipping {filename} because it already exists")
                continue
            download_file(url, output_path)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {filename}: {e}")
            continue

if __name__ == "__main__":
    main() 