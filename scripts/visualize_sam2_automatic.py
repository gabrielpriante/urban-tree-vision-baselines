import argparse  # Import argparse so the condition and image stem are supplied explicitly from the terminal.
import colorsys  # Import colorsys so every mask can receive a deterministic display color without changing the prediction data.
import json  # Import json so the preserved B1 prediction file can be loaded exactly as written.
from pathlib import Path  # Import Path so repository-relative image and output paths are handled consistently.
from PIL import Image, ImageDraw  # Import Pillow tools for image resizing, compositing, and drawing.
from sam2.utils.amg import rle_to_mask  # Import Meta's official decoder for the uncompressed RLE masks saved by the B1 pipeline.

DISPLAY_WIDTH = 2048  # Use a 2048-pixel-wide display copy so visualization is manageable while inference remains based on the untouched full-resolution image.
MASK_ALPHA = 90  # Use moderate transparency so the original RGB image remains visible beneath every displayed mask.

parser = argparse.ArgumentParser()  # Create the command-line parser for the B1 visualization workflow.
parser.add_argument("condition", choices=["before", "after"])  # Require the user to specify the experimental condition.
parser.add_argument("image_stem", choices=["PT_R1", "PT_02"])  # Require the user to specify one of the standardized image stems.
args = parser.parse_args()  # Parse the requested visualization target.

input_path = Path("data/raw/experiment_001") / args.condition / f"{args.image_stem}.JPG"  # Locate the untouched standardized RGB image used during B1 inference.
result_path = Path("outputs/sam2/experiment_001/b1_automatic") / args.condition / args.image_stem / f"{args.image_stem}_sam2_automatic_masks.json"  # Locate the preserved machine-readable B1 output.
output_dir = result_path.parent  # Reuse the same ignored directory that contains the raw B1 prediction file.
overlay_path = output_dir / f"{args.image_stem}_sam2_automatic_overlay.png"  # Define the output path for the all-mask segmentation overlay.
boxes_path = output_dir / f"{args.image_stem}_sam2_automatic_boxes_points.png"  # Define the output path for the mask bounding-box and automatic-point visualization.

with result_path.open("r", encoding="utf-8") as result_file:  # Open the preserved B1 JSON prediction file without modifying it.
    results = json.load(result_file)  # Load every preserved automatic mask and its associated metadata.

with Image.open(input_path) as source_image:  # Open the original standardized RGB image used by SAM 2.
    source_rgb = source_image.convert("RGB")  # Convert the source image explicitly to three-channel RGB for consistent display output.

display_height = round(source_rgb.height * DISPLAY_WIDTH / source_rgb.width)  # Calculate the display height while preserving the original image aspect ratio.
display_size = (DISPLAY_WIDTH, display_height)  # Store the final visualization dimensions as a Pillow-compatible width-height tuple.
display_image = source_rgb.resize(display_size, Image.Resampling.LANCZOS)  # Create a high-quality display-sized copy without modifying the original research image.
overlay_image = display_image.copy()  # Create the image that will receive every SAM 2 segmentation mask.
boxes_image = display_image.copy()  # Create a separate image for bounding boxes and automatic point prompts.
boxes_draw = ImageDraw.Draw(boxes_image)  # Create a Pillow drawing context for the box-and-point visualization.
scale_x = DISPLAY_WIDTH / source_rgb.width  # Calculate the horizontal conversion from original-image coordinates to display coordinates.
scale_y = display_height / source_rgb.height  # Calculate the vertical conversion from original-image coordinates to display coordinates.

for annotation in results["masks"]:  # Iterate through every preserved B1 automatic mask without filtering any prediction.
    mask_id = int(annotation["mask_id"])  # Read the deterministic mask identifier preserved by the inference script.
    hue = (mask_id * 0.61803398875) % 1.0  # Assign a repeatable hue using the golden-ratio sequence so neighboring mask IDs receive visually distinct colors.
    red_float, green_float, blue_float = colorsys.hsv_to_rgb(hue, 0.75, 1.0)  # Convert the deterministic display hue into RGB components.
    color = (round(red_float * 255), round(green_float * 255), round(blue_float * 255))  # Convert the display color to standard 8-bit RGB values.
    full_mask = rle_to_mask(annotation["segmentation"])  # Decode the exact preserved SAM 2 mask using Meta's official RLE decoder.
    mask_image = Image.fromarray(full_mask)  # Convert the decoded Boolean segmentation mask into a Pillow image.
    mask_image = mask_image.resize(display_size, Image.Resampling.NEAREST)  # Resize the display copy with nearest-neighbor interpolation so mask membership remains discrete.
    alpha_mask = mask_image.convert("L").point(lambda value: MASK_ALPHA if value else 0)  # Convert mask membership into a fixed semi-transparent visualization alpha channel.
    color_layer = Image.new("RGB", display_size, color)  # Create a solid display-color layer for this individual SAM 2 mask.
    overlay_image = Image.composite(color_layer, overlay_image, alpha_mask)  # Overlay this mask transparently while retaining all previously rendered masks.
    x, y, width, height = annotation["bbox"]  # Read the preserved XYWH bounding box returned by Meta's automatic mask generator.
    x0 = round(x * scale_x)  # Convert the original left box coordinate to display coordinates.
    y0 = round(y * scale_y)  # Convert the original top box coordinate to display coordinates.
    x1 = round((x + width) * scale_x)  # Convert the original right box coordinate to display coordinates.
    y1 = round((y + height) * scale_y)  # Convert the original bottom box coordinate to display coordinates.
    boxes_draw.rectangle((x0, y0, x1, y1), outline=color, width=2)  # Draw the preserved mask bounding box using the same deterministic display color.
    point_x, point_y = annotation["point_coords"][0]  # Read the automatic prompt coordinate that generated this mask.
    display_point_x = round(point_x * scale_x)  # Convert the automatic prompt x coordinate to display coordinates.
    display_point_y = round(point_y * scale_y)  # Convert the automatic prompt y coordinate to display coordinates.
    point_radius = 4  # Use a small fixed display radius for each automatic prompt point.
    boxes_draw.ellipse((display_point_x - point_radius, display_point_y - point_radius, display_point_x + point_radius, display_point_y + point_radius), fill=color)  # Draw the automatic prompt location without altering the preserved prediction data.

overlay_image.save(overlay_path)  # Save the visualization containing every B1 segmentation mask over the RGB image.
boxes_image.save(boxes_path)  # Save the separate visualization containing every preserved bounding box and automatic prompt point.

print(f"Image: {input_path}")  # Report which standardized RGB image was visualized.
print(f"Masks visualized: {len(results['masks'])}")  # Report how many preserved B1 masks were rendered without filtering.
print(f"Display size: {DISPLAY_WIDTH} x {display_height}")  # Report the dimensions of the visualization-only image copy.
print(f"Overlay: {overlay_path}")  # Report where the all-mask overlay was saved.
print(f"Boxes and points: {boxes_path}")  # Report where the box-and-prompt visualization was saved.
