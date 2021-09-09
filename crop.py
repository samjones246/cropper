from PIL import Image
from glob import glob
import os
from math import floor

# Constants
dest = "cropped"
ext = "jpg"
prefix = "pg"
dims = {
    (1080, 2400): (91, 2269),
    (1200, 2000): (36, 1927)
}
target_bytes_total = 100000000 # Desired total size for output files
temp_file_name = "__temp__"
variance = 0.05

def main():
    # Create output folder if it is not present
    if not os.path.exists(dest):
        os.mkdir(dest)

    # Get input files
    paths = glob(f"./*.{ext}")
    print(f"Found {len(paths)} input files, starting...")

    # Iterate over input files, crop and save
    success = 0
    fail = 0
    quality = -1
    target_bytes_file = (target_bytes_total / len(paths)) * (1-variance)
    print(f"Target file size: {int(target_bytes_file / 1000)}kb")
    for i, path in enumerate(paths):
        img = Image.open(path)
        if img.size not in dims:
            print(f"Unsupported resolution {img.size[0]}x{img.size[1]} for file '{path}', skipping")
            fail += 1
            continue
                
        top, bottom = dims[img.size]
        img = img.crop((0, top, img.width, bottom))
        fname = f"{prefix}{i+1}.{ext}"
        
        if quality == -1: # Quality not yet determined, use this image to compute:
            quality = 100
            step = quality
            direction = -1
            while step > 0:    
                img.save(f"{temp_file_name}.{ext}", optimise=True, quality=quality)
                result = os.path.getsize(f"{temp_file_name}.{ext}")
                if result < target_bytes_file:
                    direction = 1
                else:
                    direction = -1
                if quality == 100 and direction == 1:
                    break
                step = floor(step / 2)
                quality += step * direction
                quality = max(min(quality, 100), 0) # Clamp to [0,100] just in case
            os.remove(f"{temp_file_name}.{ext}")
                
        img.save(f"{dest}/{fname}", optimise=True, quality=quality)
        success += 1
    print(f"Done: {success} files processed, {fail} skipped")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        input("Press enter to finish...")