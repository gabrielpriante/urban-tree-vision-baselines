# Import hashlib so we can calculate a SHA-256 checksum for the original image.
import hashlib

# Import re so DJI-specific metadata embedded as XMP text can be searched safely.
import re

# Import sys so the image path can be supplied from the command line.
import sys

# Import Path so filesystem paths are handled consistently.
from pathlib import Path

# Import Pillow's EXIF tag dictionary so numeric EXIF fields can be converted into readable names.
from PIL import ExifTags

# Import Pillow's Image class so the JPEG and its standard EXIF metadata can be inspected.
from PIL import Image


# Read the image path supplied as the first command-line argument.
image_path = Path(sys.argv[1])

# Stop immediately with a clear error if the requested image does not exist.
if not image_path.exists():
    raise FileNotFoundError(f"Image not found: {image_path}")


# Create a SHA-256 hashing object for the original image file.
sha256 = hashlib.sha256()

# Open the original image file in binary mode so its bytes can be hashed without modifying them.
with image_path.open("rb") as image_file:

    # Read the file in one-megabyte chunks so hashing does not require loading the entire JPEG into memory at once.
    for chunk in iter(lambda: image_file.read(1024 * 1024), b""):

        # Add the current file chunk to the running SHA-256 calculation.
        sha256.update(chunk)


# Open the JPEG with Pillow so image dimensions and standard EXIF metadata can be inspected.
with Image.open(image_path) as image:

    # Read the native image width in pixels.
    width = image.width

    # Read the native image height in pixels.
    height = image.height

    # Calculate the total native image size in megapixels.
    megapixels = (width * height) / 1_000_000

    # Read the standard EXIF metadata attached to the JPEG.
    raw_exif = image.getexif()

    # Convert numeric EXIF tag identifiers into human-readable EXIF tag names.
    exif = {ExifTags.TAGS.get(tag_id, tag_id): value for tag_id, value in raw_exif.items()}


# Read the JPEG bytes so DJI-specific XMP metadata can also be inspected.
raw_bytes = image_path.read_bytes()

# Decode embedded metadata text while safely ignoring binary content that is not valid text.
metadata_text = raw_bytes.decode("utf-8", errors="ignore")


# Define a helper function for locating a DJI XMP metadata value by field name.
def find_dji_value(field_name: str) -> str | None:

    # Build a pattern that searches for the requested DJI metadata field inside an XML-style attribute.
    pattern = rf'drone-dji:{re.escape(field_name)}="([^"]+)"'

    # Search the decoded JPEG metadata for the requested DJI field.
    match = re.search(pattern, metadata_text)

    # Return the discovered metadata value when the field exists.
    if match:
        return match.group(1)

    # Return None when the requested DJI field is not present in the image.
    return None


# Read the camera manufacturer from standard EXIF metadata when available.
camera_make = exif.get("Make")

# Read the camera model from standard EXIF metadata when available.
camera_model = exif.get("Model")

# Read the physical focal length recorded by the camera when available.
focal_length = exif.get("FocalLength")

# Read the 35 mm equivalent focal length when the camera records it.
focal_length_35mm = exif.get("FocalLengthIn35mmFilm")

# Read the original capture timestamp when available.
capture_time = exif.get("DateTimeOriginal")

# Read DJI relative altitude from embedded XMP metadata when available.
relative_altitude = find_dji_value("RelativeAltitude")

# Read DJI absolute altitude from embedded XMP metadata when available.
absolute_altitude = find_dji_value("AbsoluteAltitude")

# Read the camera gimbal pitch from embedded DJI metadata when available.
gimbal_pitch = find_dji_value("GimbalPitchDegree")

# Read the camera gimbal yaw from embedded DJI metadata when available.
gimbal_yaw = find_dji_value("GimbalYawDegree")

# Read the aircraft yaw from embedded DJI metadata when available.
flight_yaw = find_dji_value("FlightYawDegree")


# Print a separator so metadata from multiple images is visually distinct.
print("=" * 60)

# Print the path of the image being inspected.
print(f"Image: {image_path}")

# Print the SHA-256 checksum that uniquely identifies the original image bytes.
print(f"SHA-256: {sha256.hexdigest()}")

# Print the native image width.
print(f"Width: {width} px")

# Print the native image height.
print(f"Height: {height} px")

# Print the native image size in megapixels.
print(f"Megapixels: {megapixels:.2f}")

# Print the recorded camera manufacturer.
print(f"Camera make: {camera_make}")

# Print the recorded camera model.
print(f"Camera model: {camera_model}")

# Print the physical focal length recorded by the image.
print(f"Focal length: {focal_length}")

# Print the 35 mm equivalent focal length when available.
print(f"35 mm equivalent focal length: {focal_length_35mm}")

# Print the recorded capture timestamp.
print(f"Capture time: {capture_time}")

# Print DJI relative altitude when available.
print(f"DJI relative altitude: {relative_altitude}")

# Print DJI absolute altitude when available.
print(f"DJI absolute altitude: {absolute_altitude}")

# Print DJI gimbal pitch when available.
print(f"DJI gimbal pitch: {gimbal_pitch}")

# Print DJI gimbal yaw when available.
print(f"DJI gimbal yaw: {gimbal_yaw}")

# Print DJI aircraft yaw when available.
print(f"DJI flight yaw: {flight_yaw}")