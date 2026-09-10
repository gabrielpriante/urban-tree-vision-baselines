import argparse  # Import argparse so the BEFORE or AFTER condition is selected explicitly at runtime.
import json  # Import json so the frozen B3 SAM2 prediction artifact can be read without modification.
from pathlib import Path  # Import Path so repository-relative image and output paths are constructed consistently.

import numpy as np  # Import NumPy so decoded SAM2 masks can be combined with the native RGB image.
from PIL import Image, ImageDraw, ImageFont  # Import Pillow tools for resizing, mask overlays, point markers, and tree labels.
from sam2.utils.amg import rle_to_mask  # Import Meta's official SAM2 utility for decoding the stored uncompressed RLE masks.

DISPLAY_WIDTH = 2048  # Freeze the meeting-friendly visualization width while leaving the research imagery and mask geometry unchanged.
EXPECTED_TREE_IDS = [3, 4, 5, 6, 7, 8, 9, 10, 11]  # Freeze the expected field-confirmed tree sequence for B3 visualization.

parser = argparse.ArgumentParser()  # Create the command-line parser for the B3 visualization utility.
parser.add_argument("condition", choices=["before", "after"])  # Require the caller to select either the BEFORE or AFTER PT_R1 result.
args = parser.parse_args()  # Parse the requested visualization condition before opening any artifact.

image_path = Path("data/raw/experiment_001") / args.condition / "PT_R1.JPG"  # Locate the untouched native PT_R1 image corresponding to the selected condition.
json_path = Path("outputs/sam2/experiment_001/b3_field_points") / args.condition / "PT_R1" / "PT_R1_sam2_field_point_masks.json"  # Locate the frozen B3 SAM2 mask output for the selected condition.
output_dir = json_path.parent  # Reuse the existing ignored B3 result directory for visualization artifacts.
overlay_path = output_dir / "PT_R1_sam2_field_point_overlay.png"  # Define the meeting-friendly output showing the nine SAM2 masks and frozen field points.
points_path = output_dir / "PT_R1_field_points_only.png"  # Define the meeting-friendly output showing only the nine frozen field points and tree IDs.

with Image.open(image_path) as native_image_file:  # Open the untouched PT_R1 standardized image without modifying the source file.
    native_image = native_image_file.convert("RGB")  # Convert the image to RGB so mask overlays and labels render consistently.

with json_path.open("r", encoding="utf-8") as input_file:  # Open the frozen B3 JSON prediction artifact in read-only mode.
    payload = json.load(input_file)  # Load the complete B3 provenance and mask records into memory.

tree_ids = [record["tree_id"] for record in payload["masks"]]  # Read the physical tree IDs from the frozen SAM2 result in stored order.
assert tree_ids == EXPECTED_TREE_IDS, f"Unexpected tree ID sequence: {tree_ids}"  # Stop if the visualization input does not contain exactly Trees 3 through 11 in the frozen order.
assert payload["sam2_mask_count"] == len(EXPECTED_TREE_IDS), f"Unexpected SAM2 mask count: {payload['sam2_mask_count']}"  # Stop if the frozen B3 result does not contain exactly nine masks.

display_height = round(native_image.height * DISPLAY_WIDTH / native_image.width)  # Calculate the proportional display height without changing the native image aspect ratio.
display_size = (DISPLAY_WIDTH, display_height)  # Preserve the fixed meeting-friendly display dimensions used for both B3 visualizations.
overlay_image = native_image.resize(display_size, Image.Resampling.LANCZOS)  # Create a display-resolution copy used only for the combined SAM2 mask visualization.
points_image = native_image.resize(display_size, Image.Resampling.LANCZOS)  # Create a separate display-resolution copy used only for the frozen field-point visualization.

overlay_array = np.array(overlay_image).astype(np.float32)  # Convert the display-resolution overlay image to floating point so transparent mask blending can be calculated safely.
scale_x = DISPLAY_WIDTH / native_image.width  # Calculate the horizontal mapping from native 8192-pixel coordinates to the display visualization.
scale_y = display_height / native_image.height  # Calculate the vertical mapping from native 6144-pixel coordinates to the display visualization.

palette = [  # Define a deterministic set of visualization colors so every field tree receives a stable display color.
    (230, 25, 75),  # Assign the first deterministic display color.
    (60, 180, 75),  # Assign the second deterministic display color.
    (0, 130, 200),  # Assign the third deterministic display color.
    (245, 130, 48),  # Assign the fourth deterministic display color.
    (145, 30, 180),  # Assign the fifth deterministic display color.
    (70, 240, 240),  # Assign the sixth deterministic display color.
    (240, 50, 230),  # Assign the seventh deterministic display color.
    (210, 245, 60),  # Assign the eighth deterministic display color.
    (250, 190, 212),  # Assign the ninth deterministic display color.
]  # Finish the deterministic nine-tree visualization palette.

for index, record in enumerate(payload["masks"]):  # Process every frozen B3 tree mask exactly once in stored tree-ID order.
    native_mask = rle_to_mask(record["segmentation"])  # Decode the complete native-resolution SAM2 mask using Meta's official RLE utility.
    mask_image = Image.fromarray((np.asarray(native_mask, dtype=np.uint8) * 255))  # Convert the decoded binary mask into a Pillow image suitable for display resizing.
    display_mask = mask_image.resize(display_size, Image.Resampling.NEAREST)  # Resize only the visualization mask while preserving categorical mask boundaries.
    mask_array = np.asarray(display_mask) > 0  # Convert the resized visualization mask back into a Boolean array for alpha blending.
    color = np.array(palette[index], dtype=np.float32)  # Select the deterministic display color associated with this field-confirmed tree.
    overlay_array[mask_array] = overlay_array[mask_array] * 0.55 + color * 0.45  # Blend the frozen SAM2 mask over the aerial image without filtering or modifying mask geometry.

overlay_image = Image.fromarray(np.clip(overlay_array, 0, 255).astype(np.uint8))  # Convert the completed mask blend back into a standard RGB Pillow image.
overlay_draw = ImageDraw.Draw(overlay_image)  # Create a drawing surface for the frozen point markers and tree labels on the mask overlay.
points_draw = ImageDraw.Draw(points_image)  # Create a drawing surface for the frozen point-only reference image.
font = ImageFont.load_default(size=26)  # Use Pillow's bundled font so the visualization has no external font dependency.

for record in payload["masks"]:  # Draw the frozen positive point and physical tree ID for every B3 result.
    tree_id = record["tree_id"]  # Read the physical tree identifier preserved with this SAM2 mask.
    native_x, native_y = record["native_point_xy"]  # Read the exact native-image positive point supplied to SAM2.
    display_x = round(native_x * scale_x)  # Convert the frozen native x coordinate into the display visualization coordinate space.
    display_y = round(native_y * scale_y)  # Convert the frozen native y coordinate into the display visualization coordinate space.
    radius = 8  # Freeze a small display marker radius that remains visible without obscuring the crown.
    point_box = (display_x - radius, display_y - radius, display_x + radius, display_y + radius)  # Define the circular display marker bounds around the exact field point.
    overlay_draw.ellipse(point_box, fill="red", outline="white", width=3)  # Draw the frozen positive field point on the combined SAM2 mask visualization.
    overlay_draw.text((display_x + 12, display_y - 16), f"T{tree_id}", fill="red", stroke_width=3, stroke_fill="white", font=font)  # Label the physical tree ID beside its field point on the combined visualization.
    points_draw.ellipse(point_box, fill="red", outline="white", width=3)  # Draw the same frozen positive field point on the point-only reference image.
    points_draw.text((display_x + 12, display_y - 16), f"T{tree_id}", fill="red", stroke_width=3, stroke_fill="white", font=font)  # Label the physical tree ID beside its field point on the point-only reference image.

overlay_image.save(overlay_path)  # Save the complete nine-mask field-guided SAM2 visualization without altering any underlying research result.
points_image.save(points_path)  # Save the point-only visualization so the frozen human registration can be compared independently from SAM2 geometry.

print(f"Image: {image_path}")  # Report the exact standardized aerial image used as the visualization background.
print(f"Field-guided SAM2 masks visualized: {len(payload['masks'])}")  # Report the number of frozen B3 masks included in the combined visualization.
print(f"Field points visualized: {len(payload['masks'])}")  # Report the number of frozen positive field prompts included in both visualizations.
print(f"Tree IDs: {tree_ids}")  # Report the exact physical tree-ID sequence represented in the visualization.
print(f"Display size: {DISPLAY_WIDTH} x {display_height}")  # Report the meeting-friendly rendering dimensions.
print(f"Mask and point overlay: {overlay_path}")  # Report the combined B3 mask-and-point visualization path.
print(f"Field points only: {points_path}")  # Report the independent frozen field-point visualization path.