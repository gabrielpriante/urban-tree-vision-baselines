import argparse  # Import argparse so the condition and image stem are supplied explicitly from the terminal.
import colorsys  # Import colorsys so every detection receives a deterministic visualization color.
import json  # Import json so the preserved B2 prediction file can be read exactly as written.
from pathlib import Path  # Import Path so repository-relative paths are handled consistently.
from PIL import Image, ImageDraw  # Import Pillow tools for resizing, compositing, and drawing DeepForest boxes.
from sam2.utils.amg import rle_to_mask  # Import Meta's official decoder for the uncompressed RLE masks preserved by B2.
DISPLAY_WIDTH = 2048  # Use a meeting-friendly 2048-pixel-wide visualization while preserving full-resolution predictions in JSON.
MASK_ALPHA = 85  # Use moderate mask transparency so the underlying aerial imagery remains visible.
parser = argparse.ArgumentParser()  # Create the command-line parser for the B2 visualization workflow.
parser.add_argument("condition", choices=["before", "after"])  # Require the before or after experimental condition.
parser.add_argument("image_stem", choices=["PT_R1", "PT_02"])  # Require one of the two standardized image identifiers.
args = parser.parse_args()  # Parse the requested B2 visualization target.
input_path = Path("data/raw/experiment_001") / args.condition / f"{args.image_stem}.JPG"  # Locate the untouched native RGB image used by SAM 2.
result_path = Path("outputs/sam2/experiment_001/b2_deepforest_boxes") / args.condition / args.image_stem / f"{args.image_stem}_sam2_deepforest_box_masks.json"  # Locate the preserved B2 prediction record.
output_dir = result_path.parent  # Use the same ignored output directory that already stores the raw B2 JSON.
overlay_path = output_dir / f"{args.image_stem}_sam2_deepforest_overlay.png"  # Define the visualization containing SAM 2 masks plus their DeepForest prompt boxes.
boxes_path = output_dir / f"{args.image_stem}_deepforest_boxes_native.png"  # Define a separate visualization containing only the mapped DeepForest boxes.
with result_path.open("r", encoding="utf-8") as result_file:  # Open the preserved B2 JSON file without modifying it.
    results = json.load(result_file)  # Load every frozen DeepForest prompt and corresponding SAM 2 mask.
with Image.open(input_path) as source_image:  # Open the untouched standardized RGB image used during B2 inference.
    source_rgb = source_image.convert("RGB")  # Convert the source image explicitly to three-channel RGB for consistent rendering.
display_height = round(source_rgb.height * DISPLAY_WIDTH / source_rgb.width)  # Calculate display height while preserving the original aspect ratio.
display_size = (DISPLAY_WIDTH, display_height)  # Store the meeting-friendly visualization dimensions.
display_image = source_rgb.resize(display_size, Image.Resampling.LANCZOS)  # Create a high-quality display copy without modifying the research image.
overlay_image = display_image.copy()  # Create the image that will receive all preserved SAM 2 masks and DeepForest prompt boxes.
boxes_image = display_image.copy()  # Create a separate image that will show only the DeepForest prompt boxes.
overlay_draw = ImageDraw.Draw(overlay_image)  # Create a drawing context for box outlines on the mask overlay.
boxes_draw = ImageDraw.Draw(boxes_image)  # Create a drawing context for the DeepForest-only visualization.
scale_x = DISPLAY_WIDTH / source_rgb.width  # Calculate the horizontal conversion from native-image coordinates to display coordinates.
scale_y = display_height / source_rgb.height  # Calculate the vertical conversion from native-image coordinates to display coordinates.
for annotation in results["masks"]:  # Iterate through every preserved B2 result without filtering any DeepForest detection or SAM 2 mask.
    detection_id = int(annotation["detection_id"])  # Read the deterministic DeepForest detection identifier preserved during B2 inference.
    hue = (detection_id * 0.61803398875) % 1.0  # Assign a repeatable hue using the golden-ratio sequence for visually distinct neighboring detections.
    red_float, green_float, blue_float = colorsys.hsv_to_rgb(hue, 0.75, 1.0)  # Convert the deterministic hue to floating-point RGB components.
    color = (round(red_float * 255), round(green_float * 255), round(blue_float * 255))  # Convert the display color to standard 8-bit RGB values.
    full_mask = rle_to_mask(annotation["segmentation"])  # Decode the exact full-resolution SAM 2 mask using Meta's official RLE decoder.
    mask_image = Image.fromarray(full_mask)  # Convert the decoded binary mask into a Pillow image for display rendering.
    mask_image = mask_image.resize(display_size, Image.Resampling.NEAREST)  # Resize only the visualization copy using nearest-neighbor interpolation.
    alpha_mask = mask_image.convert("L").point(lambda value: MASK_ALPHA if value else 0)  # Convert mask membership into a fixed semi-transparent alpha layer.
    color_layer = Image.new("RGB", display_size, color)  # Create a solid deterministic-color layer for this SAM 2 mask.
    overlay_image = Image.composite(color_layer, overlay_image, alpha_mask)  # Overlay this SAM 2 mask without altering the preserved prediction data.
    overlay_draw = ImageDraw.Draw(overlay_image)  # Refresh the drawing context after compositing the current mask layer.
    xmin, ymin, xmax, ymax = annotation["native_box_xyxy"]  # Read the mapped native-image DeepForest box that served as this mask's prompt.
    x0 = round(xmin * scale_x)  # Convert the native left box coordinate to display coordinates.
    y0 = round(ymin * scale_y)  # Convert the native top box coordinate to display coordinates.
    x1 = round(xmax * scale_x)  # Convert the native right box coordinate to display coordinates.
    y1 = round(ymax * scale_y)  # Convert the native bottom box coordinate to display coordinates.
    overlay_draw.rectangle((x0, y0, x1, y1), outline=color, width=2)  # Draw the exact DeepForest prompt box on top of its corresponding SAM 2 mask.
    boxes_draw.rectangle((x0, y0, x1, y1), outline=color, width=2)  # Draw the same mapped DeepForest prompt box on the separate detector-only visualization.
overlay_image.save(overlay_path)  # Save the meeting-friendly visualization containing every B2 mask and its corresponding DeepForest prompt box.
boxes_image.save(boxes_path)  # Save the meeting-friendly visualization containing only the mapped DeepForest boxes.
print(f"Image: {input_path}")  # Report which standardized image was visualized.
print(f"DeepForest boxes visualized: {len(results['masks'])}")  # Report how many frozen DeepForest prompts were rendered.
print(f"SAM2 masks visualized: {len(results['masks'])}")  # Report how many corresponding SAM 2 masks were rendered without filtering.
print(f"Display size: {DISPLAY_WIDTH} x {display_height}")  # Report the dimensions of the visualization-only copy.
print(f"Mask and box overlay: {overlay_path}")  # Report where the combined B2 visualization was saved.
print(f"DeepForest boxes only: {boxes_path}")  # Report where the detector-only visualization was saved.
