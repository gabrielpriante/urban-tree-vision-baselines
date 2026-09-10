import argparse  # Import argparse so the condition and study scene are selected explicitly at runtime.
import colorsys  # Import colorsys so a deterministic visualization color can be generated for every registered location.
import json  # Import json so frozen B3 SAM2 prediction artifacts can be read without modification.
from pathlib import Path  # Import Path so repository-relative image and output paths are constructed consistently.

import numpy as np  # Import NumPy so decoded SAM2 masks can be combined with the standardized RGB image.
from PIL import Image, ImageDraw, ImageFont  # Import Pillow tools for image resizing, mask overlays, point markers, and registration labels.
from sam2.utils.amg import rle_to_mask  # Import Meta's official SAM2 utility for decoding stored uncompressed RLE masks.

DISPLAY_WIDTH = 2048  # Freeze a meeting-friendly visualization width while leaving all native research imagery and mask geometry unchanged.

EXPECTED_IDS = {  # Freeze the registration sequence expected for each supported B3 study scene.
    "PT_R1": [3, 4, 5, 6, 7, 8, 9, 10, 11],  # Preserve the nine field-confirmed physical tree IDs used for PT_R1.
    "PT_02": [f"A{index:02d}" for index in range(1, 23)],  # Preserve neutral A01 through A22 registration IDs for PT_02.
}  # Finish the scene-specific expected identifier mapping.

parser = argparse.ArgumentParser()  # Create the command-line parser for the generalized B3 visualization utility.
parser.add_argument("condition", choices=["before", "after"])  # Require the caller to select either the BEFORE or AFTER condition.
parser.add_argument("image_stem", choices=["PT_R1", "PT_02"], nargs="?", default="PT_R1")  # Allow either study scene while preserving the original PT_R1 command form.
args = parser.parse_args()  # Parse the requested condition and study scene before opening any artifact.

image_path = Path("data/raw/experiment_001") / args.condition / f"{args.image_stem}.JPG"  # Locate the untouched standardized native image corresponding to the selected scene and condition.
json_path = Path("outputs/sam2/experiment_001/b3_field_points") / args.condition / args.image_stem / f"{args.image_stem}_sam2_field_point_masks.json"  # Locate the frozen scene-specific B3 SAM2 prediction artifact.
output_dir = json_path.parent  # Reuse the existing ignored B3 result directory for visualization artifacts.
overlay_path = output_dir / f"{args.image_stem}_sam2_field_point_overlay.png"  # Define the combined SAM2 mask and registered-point visualization path.
points_path = output_dir / f"{args.image_stem}_field_points_only.png"  # Define the independent registered-point-only visualization path.

assert image_path.exists(), f"Native image not found: {image_path}"  # Stop if the standardized native image required for visualization is unavailable.
assert json_path.exists(), f"B3 SAM2 output not found: {json_path}"  # Stop if the frozen B3 prediction artifact required for visualization is unavailable.

with Image.open(image_path) as native_image_file:  # Open the untouched standardized aerial image without modifying the source file.
    native_image = native_image_file.convert("RGB")  # Convert the image to RGB so masks and labels render consistently.

with json_path.open("r", encoding="utf-8") as input_file:  # Open the frozen B3 prediction artifact in read-only mode.
    payload = json.load(input_file)  # Load the complete B3 provenance and mask records into memory.

assert payload["condition"] == args.condition, f"Condition mismatch: {payload['condition']}"  # Stop if the prediction artifact belongs to a different experimental condition.
assert payload["image_stem"] == args.image_stem, f"Image stem mismatch: {payload['image_stem']}"  # Stop if the prediction artifact belongs to a different study scene.
assert payload["sam2_mask_count"] == len(EXPECTED_IDS[args.image_stem]), f"Unexpected SAM2 mask count: {payload['sam2_mask_count']}"  # Stop if the prediction artifact does not contain exactly one mask per expected registration.

def record_identifier(record):  # Define a helper that retrieves the correct identifier from either the original or generalized B3 output schema.
    if args.image_stem == "PT_R1":  # Check whether the original field-confirmed PT_R1 scene is being visualized.
        return int(record.get("tree_id", record.get("registration_id")))  # Preserve compatibility with both the original PT_R1 tree_id field and the newer generalized registration_id field.
    return record["registration_id"]  # Return the neutral A-series registration identifier used by PT_02.

observed_ids = [record_identifier(record) for record in payload["masks"]]  # Read every scene-specific registration identifier in stored prediction order.
assert observed_ids == EXPECTED_IDS[args.image_stem], f"Unexpected registration ID sequence: {observed_ids}"  # Stop if masks are missing, duplicated, reordered, or associated with unexpected registrations.

display_height = round(native_image.height * DISPLAY_WIDTH / native_image.width)  # Calculate proportional display height without changing the original image aspect ratio.
display_size = (DISPLAY_WIDTH, display_height)  # Preserve one fixed meeting-friendly display size for both visualizations.
overlay_image = native_image.resize(display_size, Image.Resampling.LANCZOS)  # Create a display-resolution copy used only for the combined SAM2 visualization.
points_image = native_image.resize(display_size, Image.Resampling.LANCZOS)  # Create a separate display-resolution copy used only for the registered-point visualization.

overlay_array = np.array(overlay_image).astype(np.float32)  # Convert the display image to floating point so transparent mask blending can be calculated safely.
scale_x = DISPLAY_WIDTH / native_image.width  # Calculate the horizontal mapping from native pixel coordinates into display coordinates.
scale_y = display_height / native_image.height  # Calculate the vertical mapping from native pixel coordinates into display coordinates.

def visualization_color(index, total):  # Define a deterministic color generator that works for both nine and twenty-two registered objects.
    hue = index / total  # Distribute registration colors evenly around the hue wheel according to frozen registration order.
    red, green, blue = colorsys.hsv_to_rgb(hue, 0.75, 0.95)  # Convert the deterministic hue into a bright visualization-only RGB color.
    return np.array([red * 255, green * 255, blue * 255], dtype=np.float32)  # Return the generated color in standard 0 through 255 RGB space.

for index, record in enumerate(payload["masks"]):  # Process every frozen B3 SAM2 mask exactly once in stored registration order.
    native_mask = rle_to_mask(record["segmentation"])  # Decode the complete native-resolution SAM2 mask using Meta's official RLE utility.
    mask_image = Image.fromarray(np.asarray(native_mask, dtype=np.uint8) * 255)  # Convert the decoded binary mask into a Pillow image suitable for display resizing.
    display_mask = mask_image.resize(display_size, Image.Resampling.NEAREST)  # Resize only the visualization mask while preserving categorical boundaries.
    mask_array = np.asarray(display_mask) > 0  # Convert the resized mask back into a Boolean array used for transparent blending.
    color = visualization_color(index, len(payload["masks"]))  # Generate the deterministic display color associated with this registration.
    overlay_array[mask_array] = overlay_array[mask_array] * 0.55 + color * 0.45  # Blend the frozen SAM2 mask over the aerial image without filtering or changing mask geometry.

overlay_image = Image.fromarray(np.clip(overlay_array, 0, 255).astype(np.uint8))  # Convert the completed mask blend back into a standard RGB Pillow image.
overlay_draw = ImageDraw.Draw(overlay_image)  # Create a drawing surface for point markers and labels on the combined SAM2 visualization.
points_draw = ImageDraw.Draw(points_image)  # Create a separate drawing surface for the point-only reference visualization.
font = ImageFont.load_default(size=26)  # Use Pillow's bundled font so the visualization has no external font dependency.

for record in payload["masks"]:  # Draw the exact frozen positive point and identifier for every B3 registration.
    identifier = record_identifier(record)  # Read the scene-appropriate physical tree ID or neutral registration ID.
    native_x, native_y = record["native_point_xy"]  # Read the exact native-image positive point originally supplied to SAM2.
    display_x = round(native_x * scale_x)  # Convert the frozen native x coordinate into display space.
    display_y = round(native_y * scale_y)  # Convert the frozen native y coordinate into display space.
    radius = 8  # Freeze a small point-marker radius that remains visible without obscuring substantial crown imagery.
    point_box = (display_x - radius, display_y - radius, display_x + radius, display_y + radius)  # Define the circular display marker around the exact positive point.
    label = f"T{identifier}" if args.image_stem == "PT_R1" else str(identifier)  # Preserve T-prefix labels for PT_R1 while displaying the neutral A-series IDs directly for PT_02.
    overlay_draw.ellipse(point_box, fill="red", outline="white", width=3)  # Draw the frozen positive point on the combined SAM2 mask visualization.
    overlay_draw.text((display_x + 12, display_y - 16), label, fill="red", stroke_width=3, stroke_fill="white", font=font)  # Draw the registration identifier beside its frozen point on the combined visualization.
    points_draw.ellipse(point_box, fill="red", outline="white", width=3)  # Draw the same frozen positive point on the independent point-only visualization.
    points_draw.text((display_x + 12, display_y - 16), label, fill="red", stroke_width=3, stroke_fill="white", font=font)  # Draw the registration identifier beside its point on the independent point-only visualization.

overlay_image.save(overlay_path)  # Save the complete field-guided SAM2 visualization without altering any underlying research prediction.
points_image.save(points_path)  # Save the point-only visualization so manual spatial guidance can be inspected separately from SAM2 geometry.

print(f"Image: {image_path}")  # Report the exact standardized aerial image used as the visualization background.
print(f"Scene: {args.image_stem}")  # Report the study scene represented by the visualization.
print(f"Condition: {args.condition}")  # Report whether the visualization represents BEFORE or AFTER imagery.
print(f"SAM2 masks visualized: {len(payload['masks'])}")  # Report the number of frozen B3 masks included in the combined visualization.
print(f"Registered points visualized: {len(payload['masks'])}")  # Report the number of frozen positive prompts included in both visualizations.
print(f"Registration IDs: {observed_ids}")  # Report the exact registration sequence represented in the visualization.
print(f"Display size: {DISPLAY_WIDTH} x {display_height}")  # Report the meeting-friendly rendering dimensions.
print(f"Mask and point overlay: {overlay_path}")  # Report the combined mask-and-point visualization path.
print(f"Field points only: {points_path}")  # Report the independent point-only visualization path.