<<<<<<< HEAD
# Import sys so the input image path can be supplied from the command line.
import sys

# Import Path so file paths are handled consistently across the repository.
from pathlib import Path

# Import Pillow's Image class so the source JPEG can be read and resized.
from PIL import Image

# Define the nominal native ground sampling distance of the standardized DJI imagery.
NATIVE_GSD_CM = 1.67

# Define the TreeCountSegHeight target ground sampling distance.
TARGET_GSD_CM = 20.00

# Read the input image path from the first command-line argument.
input_path = Path(sys.argv[1])

# Stop immediately if the input image does not exist.
if not input_path.exists():
    raise FileNotFoundError(f"Input image not found: {input_path}")

# Read the experimental condition from the parent directory name.
condition = input_path.parent.name

# Define the derived output directory for the 20 cm TreeCountSegHeight condition.
output_dir = Path("data/derived/experiment_001/treecountsegheight_20cm") / condition

# Create the output directory and any missing parents.
output_dir.mkdir(parents=True, exist_ok=True)

# Calculate the linear resize factor needed to preserve physical extent.
resize_factor = NATIVE_GSD_CM / TARGET_GSD_CM

# Open the untouched source image.
with Image.open(input_path) as image:
    # Convert the source image to 3-band RGB explicitly.
    rgb_image = image.convert("RGB")

    # Calculate the target width.
    target_width = round(rgb_image.width * resize_factor)

    # Calculate the target height.
    target_height = round(rgb_image.height * resize_factor)

    # Resize using Lanczos for high-quality downsampling.
    resized_image = rgb_image.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # Define the output TIFF path using the same stem as the original image.
    output_path = output_dir / f"{input_path.stem}.tif"

    # Save as a 3-band uint8 TIFF.
    resized_image.save(output_path, format="TIFF")

# Print the key provenance and output details.
print(f"Input image: {input_path}")
print(f"Condition: {condition}")
print(f"Native GSD: {NATIVE_GSD_CM:.2f} cm/pixel")
print(f"Target GSD: {TARGET_GSD_CM:.2f} cm/pixel")
print(f"Resize factor: {resize_factor:.6f}")
print(f"Output dimensions: {target_width} x {target_height}")
print(f"Output image: {output_path}")
=======
import sys  # Import sys so the source image path can be supplied from the command line.
from pathlib import Path  # Import Path so repository file paths are handled consistently.
from PIL import Image  # Import Pillow so the untouched JPEG can be converted and resampled.

NATIVE_GSD_CM = 1.67  # Define the nominal native ground sampling distance of the standardized DJI imagery in centimeters per pixel.
TARGET_GSD_CM = 20.00  # Define the target ground sampling distance expected by the TreeCountSegHeight deployment condition.

input_path = Path(sys.argv[1])  # Read the source image path supplied as the first command-line argument.

if not input_path.exists():  # Check that the requested source image actually exists before doing any processing.
    raise FileNotFoundError(f"Input image not found: {input_path}")  # Stop with a clear error if the source image is missing.

condition = input_path.parent.name  # Derive the before or after experimental condition from the source directory name.
output_dir = Path("data/derived/experiment_001/treecountsegheight_20cm") / condition  # Define the ignored output directory for the 20 cm derived condition.
output_dir.mkdir(parents=True, exist_ok=True)  # Create the derived output directory and any missing parent directories.

resize_factor = NATIVE_GSD_CM / TARGET_GSD_CM  # Calculate the linear scale factor required to move from 1.67 cm per pixel to 20 cm per pixel.

with Image.open(input_path) as image:  # Open the untouched standardized JPEG source image.
    rgb_image = image.convert("RGB")  # Explicitly convert the source to three-channel RGB for the RGB-only pretrained model.
    target_width = round(rgb_image.width * resize_factor)  # Calculate the target width while preserving the nominal physical footprint.
    target_height = round(rgb_image.height * resize_factor)  # Calculate the target height while preserving the nominal physical footprint.
    resized_image = rgb_image.resize((target_width, target_height), Image.Resampling.LANCZOS)  # Downsample the RGB image using deterministic Lanczos resampling.
    output_path = output_dir / f"{input_path.stem}.tif"  # Define the TIFF output path while preserving the original image stem.
    resized_image.save(output_path, format="TIFF")  # Save an un-georeferenced three-band RGB TIFF without fabricating spatial metadata.

print(f"Input image: {input_path}")  # Report the exact standardized source image used.
print(f"Condition: {condition}")  # Report whether the source belongs to the before or after condition.
print(f"Native GSD: {NATIVE_GSD_CM:.2f} cm/pixel")  # Report the nominal source ground sampling distance used in the calculation.
print(f"Target GSD: {TARGET_GSD_CM:.2f} cm/pixel")  # Report the fixed TreeCountSegHeight target ground sampling distance.
print(f"Resize factor: {resize_factor:.6f}")  # Report the exact linear resize factor applied to the source image.
print(f"Output dimensions: {target_width} x {target_height}")  # Report the resulting raster dimensions.
print(f"Output image: {output_path}")  # Report the path of the derived RGB TIFF.
>>>>>>> e29e08d227af2186f235752f330d8695d00f5918
