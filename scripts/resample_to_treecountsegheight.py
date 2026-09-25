# Import sys so the script can receive the source image path and optional benchmark run label from the command line.
import sys

# Import Path so repository file paths are handled consistently.
from pathlib import Path

# Import Pillow so the untouched JPEG can be converted and resampled.
from PIL import Image


# Define the nominal native ground sampling distance of the standardized DJI imagery in centimeters per pixel.
NATIVE_GSD_CM = 1.67

# Define the target ground sampling distance expected by the TreeCountSegHeight deployment condition.
TARGET_GSD_CM = 20.00


# Read the source image path supplied as the first command-line argument.
input_path = Path(sys.argv[1])

# Read an optional benchmark run label such as "week3".
run_label = sys.argv[2] if len(sys.argv) > 2 else None

# Stop immediately if the requested source image does not exist.
if not input_path.exists():
    # Raise a clear error instead of silently continuing with a missing image.
    raise FileNotFoundError(f"Input image not found: {input_path}")

# Derive the before or after experimental condition from the source directory name.
condition = input_path.parent.name.lower()

# Define the historical base directory for 20 cm TreeCountSegHeight derived imagery.
output_root = Path("data/derived/experiment_001/treecountsegheight_20cm")

# Add the benchmark run label when one is explicitly supplied.
output_root = output_root / run_label if run_label else output_root

# Define the condition-specific derived-image directory.
output_dir = output_root / condition

# Create the derived output directory and any missing parent directories.
output_dir.mkdir(parents=True, exist_ok=True)

# Calculate the linear scale factor required to move from 1.67 cm per pixel to 20 cm per pixel.
resize_factor = NATIVE_GSD_CM / TARGET_GSD_CM

# Open the untouched standardized JPEG source image.
with Image.open(input_path) as image:
    # Explicitly convert the source to three-channel RGB for the RGB-only pretrained model.
    rgb_image = image.convert("RGB")

    # Calculate the target width while preserving the nominal physical footprint.
    target_width = round(rgb_image.width * resize_factor)

    # Calculate the target height while preserving the nominal physical footprint.
    target_height = round(rgb_image.height * resize_factor)

    # Downsample the RGB image using deterministic Lanczos resampling.
    resized_image = rgb_image.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # Define the TIFF output path while preserving the canonical scene stem.
    output_path = output_dir / f"{input_path.stem}.tif"

    # Save an un-georeferenced three-band RGB TIFF without fabricating spatial metadata.
    resized_image.save(output_path, format="TIFF")

# Report the exact standardized source image used.
print(f"Input image: {input_path}")

# Report the benchmark run label.
print(f"Run label: {run_label}")

# Report whether the source belongs to the before or after condition.
print(f"Condition: {condition}")

# Report the nominal source ground sampling distance used in the calculation.
print(f"Native GSD: {NATIVE_GSD_CM:.2f} cm/pixel")

# Report the fixed TreeCountSegHeight target ground sampling distance.
print(f"Target GSD: {TARGET_GSD_CM:.2f} cm/pixel")

# Report the exact linear resize factor applied to the source image.
print(f"Resize factor: {resize_factor:.6f}")

# Report the resulting raster dimensions.
print(f"Output dimensions: {target_width} x {target_height}")

# Report the path of the derived RGB TIFF.
print(f"Output image: {output_path}")
