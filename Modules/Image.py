from PIL import Image
from PIL.ExifTags import TAGS
import piexif
import os

def get_exif(image_path):
    image = Image.open(image_path)
    exif_data = None

    # For JPG/JPEG files, use piexif
    if image.format in ['JPEG', 'JPG']:
        exif_data = piexif.load(image.info['exif'])
        if exif_data:
            exif = {
                TAGS.get(tag, tag): value
                for ifd in exif_data
                for tag, value in exif_data[ifd].items()
            }
            return exif

    # For PNG files, use PIL to get basic info
    elif image.format == 'PNG':
        info = image.info
        if info:
            return info

    # For other formats, attempt to extract using PIL
    if image._getexif():
        exif_data = image._getexif()
        exif = {
            TAGS.get(tag, tag): value
            for tag, value in exif_data.items()
            if tag in TAGS
        }
        return exif

    return None

# Example usage
image_paths = ['../../backdoor/indecipherable/cutie.png', '../../Downloads/WindowsXP.jpg']
for image_path in image_paths:
    exif_data = get_exif(image_path)
    print(f"Metadata for {os.path.basename(image_path)}:")
    if exif_data:
        for tag, value in exif_data.items():
            print(f"{tag}: {value}")
    else:
        print("No EXIF data found")
