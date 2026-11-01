
from PIL import Image, ExifTags
from pathlib import Path
from datetime import datetime
import os

def analyze_image(image_path):
    path = Path(image_path)

    if not path.exists():
        print("Error: Image file not found!")
        return

    try:
        with Image.open(path) as image:
            print("\n========== IMAGE METADATA ==========")

            # Basic file information
            print("File Name:", path.name)
            print("File Format:", image.format)
            print("Image Mode:", image.mode)
            print("Width:", image.width, "pixels")
            print("Height:", image.height, "pixels")
            print("Resolution:", f"{image.width} x {image.height}")
            print("File Size:", round(os.path.getsize(path) / 1024, 2), "KB")

            # EXIF metadata
            exif_data = image.getexif()

            print("\n========== EXIF DETAILS ==========")

            if not exif_data:
                print("No EXIF metadata found.")
            else:
                for tag_id, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag_id, tag_id)

                    # Avoid printing large binary or nested values
                    if isinstance(value, bytes):
                        value = f"<binary data: {len(value)} bytes>"

                    print(f"{tag_name}: {value}")

            # Camera details
            print("\n========== CAMERA INFORMATION ==========")

            camera_fields = {
                "Make": "Camera Manufacturer",
                "Model": "Camera Model",
                "DateTimeOriginal": "Date Taken",
                "Software": "Software",
                "FNumber": "Aperture",
                "ExposureTime": "Exposure Time",
                "ISOSpeedRatings": "ISO",
                "FocalLength": "Focal Length"
            }

            found_camera_info = False

            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)

                if tag_name in camera_fields:
                    print(f"{camera_fields[tag_name]}: {value}")
                    found_camera_info = True

            if not found_camera_info:
                print("No camera details available.")

            print("\n========== END OF REPORT ==========")

    except Exception as error:
        print("Unable to analyze image:", error)


if __name__ == "__main__":
    image_path = input(
        "Enter the full path of your image: "
    ).strip().strip('"')

    analyze_image(image_path)
