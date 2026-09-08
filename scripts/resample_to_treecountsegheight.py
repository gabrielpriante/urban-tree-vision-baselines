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
