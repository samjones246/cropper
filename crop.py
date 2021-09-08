from PIL import Image
from glob import glob
import os

# Constants
dest = "cropped"
ext = "jpg"
prefix = "pg"
dims = {
    (1080, 2400): (91, 2269),
    (1200, 2000): (36, 1927)
}

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
    for i, path in enumerate(paths):
        img = Image.open(path)
        if img.size not in dims:
            print(f"Unsupported resolution {img.size[0]}x{img.size[1]} for file '{path}', skipping")
            fail += 1
            continue
        top, bottom = dims[img.size]
        img = img.crop((0, top, img.width, bottom))
        fname = f"{prefix}{i+1}.{ext}"
        img.save(f"{dest}/{fname}")
        success += 1
    print(f"Done: {success} files processed, {fail} skipped")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        input("Press any key to finish...")