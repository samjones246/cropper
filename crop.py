from PIL import Image
from glob import glob
import os

# Constants
dest = "cropped"
ext = "jpg"
prefix = "pg"
top = 91
bottom = 2269

def main():
    # Create output folder if it is not present
    if not os.path.exists(dest):
        os.mkdir(dest)

    # Get input files
    paths = glob(f"./*.{ext}")

    # Iterate over input files, crop and save
    for i, path in enumerate(paths):
        img = Image.open(path)
        img = img.crop((0, top, img.width, bottom))
        fname = f"{prefix}{i+1}.{ext}"
        img.save(f"{dest}/{fname}")


if __name__ == "__main__":
    main()