import sys  # Import sys so the condition, image name, and optional run label can come from command-line arguments.
from pathlib import Path  # Import Path so repository paths are handled consistently.
import numpy as np  # Import NumPy for raster calculations and image blending.
import rasterio  # Import Rasterio for reading TreeCountSegHeight prediction TIFFs.
from PIL import Image  # Import Pillow for reading RGB TIFFs and saving PNGs.
import matplotlib.pyplot as plt  # Import Matplotlib for saving density heatmaps.
condition = sys.argv[1]  # Read either before or after from the first command-line argument.
image_stem = sys.argv[2]  # Read either PT_R1 or PT_02 from the second command-line argument.
run_label = sys.argv[3] if len(sys.argv) > 3 else None  # Read an optional run label such as week3 while preserving the original Week 1 behavior when omitted.
input_root = Path("data/derived/experiment_001/treecountsegheight_20cm")  # Define the root directory containing TreeCountSegHeight 20 cm model inputs.
output_root = Path("outputs/treecountsegheight/experiment_001")  # Define the root directory containing TreeCountSegHeight model outputs.
if run_label is not None:  # Check whether this visualization belongs to a labeled repeated collection period.
    input_root = input_root / run_label  # Add the run label to the input path when processing Week 3 or another labeled collection.
    output_root = output_root / run_label  # Add the same run label to the output path so visualizations stay with their matching predictions.
input_path = input_root / condition / f"{image_stem}.tif"  # Locate the exact 20 cm RGB TIFF supplied to TreeCountSegHeight.
segmentation_path = output_root / condition / image_stem / f"{image_stem}_seg.tif"  # Locate the frozen segmentation prediction.
density_path = output_root / condition / image_stem / f"{image_stem}*density.tif"  # Locate the frozen density prediction with the authors' literal asterisk filename.
output_dir = output_root / condition / image_stem  # Locate the corresponding prediction directory where visualization PNGs will be written.
with Image.open(input_path) as image:  # Open the exact RGB TIFF supplied to TreeCountSegHeight.
    rgb = np.array(image.convert("RGB"))  # Convert the RGB image into a NumPy array.
with rasterio.open(segmentation_path) as src:  # Open the frozen binary segmentation TIFF.
    segmentation = src.read(1)  # Read the segmentation band.
with rasterio.open(density_path) as src:  # Open the frozen continuous density TIFF.
    density = src.read(1)  # Read the density band.
tree_mask = segmentation == 1  # Identify pixels classified as tree canopy.
overlay = rgb.astype(np.float32).copy()  # Convert RGB values to floating point for blending.
highlight = np.zeros_like(overlay)  # Create an empty highlight layer.
highlight[..., 0] = 255.0  # Make the highlight layer red.
overlay[tree_mask] = (0.55 * overlay[tree_mask]) + (0.45 * highlight[tree_mask])  # Blend red into predicted tree pixels.
overlay = np.clip(overlay, 0, 255).astype(np.uint8)  # Convert the overlay back to normal 8-bit RGB values.
overlay_path = output_dir / f"{image_stem}_treecountsegheight_overlay.png"  # Define the overlay PNG path.
Image.fromarray(overlay).save(overlay_path)  # Save the RGB prediction overlay.
segmentation_png = output_dir / f"{image_stem}_treecountsegheight_segmentation.png"  # Define the standalone segmentation PNG path.
Image.fromarray((segmentation * 255).astype(np.uint8)).save(segmentation_png)  # Save the binary segmentation mask as a visible PNG.
density_png = output_dir / f"{image_stem}_treecountsegheight_density.png"  # Define the density heatmap PNG path.
plt.imsave(density_png, density, cmap="viridis")  # Save the continuous density prediction as a heatmap.
predicted_count = float(np.sum(density, dtype=np.float64))  # Sum the density raster in float64 precision using the model authors' counting interpretation.
print(f"Run label: {run_label if run_label is not None else 'week1'}")  # Print the collection period actually processed.
print(f"Condition: {condition}")  # Print the condition actually processed.
print(f"Image: {image_stem}")  # Print the image actually processed.
print(f"Predicted density count: {predicted_count:.10f}")  # Print the continuous predicted tree count without reducing it to six decimal places.
print(f"Overlay: {overlay_path}")  # Print the generated overlay path.
print(f"Segmentation: {segmentation_png}")  # Print the generated segmentation PNG path.
print(f"Density: {density_png}")  # Print the generated density heatmap path.
