# Import sys so the input image path can be supplied from the command line.
import sys

# Import Path so input and output filesystem paths are handled consistently.
from pathlib import Path

# Import Pillow's Image class so the original JPEG can be resized.
from PIL import Image


# Define the estimated native ground sampling distance of the standardized 95 m imagery in centimeters per pixel.
NATIVE_GSD_CM = 1.67

# Define the target ground sampling distance used for the scale-adjusted DeepForest experiment.
TARGET_GSD_CM = 7.89


# Read the input image path supplied as the first command-line argument.
input_path = Path(sys.argv[1])

# Stop immediately with a clear error if the requested input image does not exist.
if not input_path.exists():
    raise FileNotFoundError(f"Input image not found: {input_path}")

# Read the experimental condition from the image's parent directory.
condition = input_path.parent.name

# Define the directory where scale-adjusted derived imagery will be stored locally.
output_dir = Path("data/derived/experiment_001/gsd_7.89") / condition

# Create the derived-image output directory and any missing parent directories.
output_dir.mkdir(parents=True, exist_ok=True)

# Calculate the linear resize factor needed to move from the native GSD to the target GSD.
resize_factor = NATIVE_GSD_CM / TARGET_GSD_CM

# Open the untouched original JPEG.
with Image.open(input_path) as image:

    # Calculate the target image width while preserving the original physical image extent.
    target_width = round(image.width * resize_factor)

    # Calculate the target image height while preserving the original physical image extent.
    target_height = round(image.height * resize_factor)

    # Resize the image using Lanczos resampling for high-quality downsampling.
    resized_image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # Define the derived output path while preserving the original image filename.
    output_path = output_dir / input_path.name

    # Save the derived JPEG at high quality without modifying the original source image.
    resized_image.save(output_path, quality=95)


# Print the source image path.
print(f"Input image: {input_path}")

# Print the native ground sampling distance used in the calculation.
print(f"Native GSD: {NATIVE_GSD_CM:.2f} cm/pixel")

# Print the target ground sampling distance.
print(f"Target GSD: {TARGET_GSD_CM:.2f} cm/pixel")

# Print the linear resize factor applied to the image.
print(f"Resize factor: {resize_factor:.6f}")

# Print the resulting image dimensions.
print(f"Output dimensions: {target_width} x {target_height}")

# Print the path of the derived scale-adjusted image.
print(f"Output image: {output_path}")