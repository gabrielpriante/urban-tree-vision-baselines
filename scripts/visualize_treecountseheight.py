cat > scripts/visualize_treecountsegheight.py <<'PY' # Completely overwrite the old duplicated visualization script with the reusable version.
import sys  # Read command-line arguments.
from pathlib import Path  # Handle repository paths.
import numpy as np  # Work with raster arrays.
import rasterio  # Read TreeCountSegHeight prediction TIFFs.
from PIL import Image  # Read the RGB model input and save PNGs.
import matplotlib.pyplot as plt  # Save the density heatmap.

condition = sys.argv[1]  # Read either before or after from the command line.
image_stem = sys.argv[2]  # Read either PT_R1 or PT_02 from the command line.

input_path = Path("data/derived/experiment_001/treecountsegheight_20cm") / condition / f"{image_stem}.tif"  # Locate the exact 20 cm RGB model input.
segmentation_path = Path("outputs/treecountsegheight/experiment_001") / condition / image_stem / f"{image_stem}_seg.tif"  # Locate the binary segmentation output.
density_path = Path("outputs/treecountsegheight/experiment_001") / condition / image_stem / f"{image_stem}*density.tif"  # Locate the continuous density output.
output_dir = Path("outputs/treecountsegheight/experiment_001") / condition / image_stem  # Locate the corresponding visualization output directory.

with Image.open(input_path) as image:  # Open the exact RGB image supplied to the model.
    rgb = np.array(image.convert("RGB"))  # Convert the model input into an RGB NumPy array.

with rasterio.open(segmentation_path) as src:  # Open the frozen segmentation prediction.
    segmentation = src.read(1)  # Read the segmentation band.

with rasterio.open(density_path) as src:  # Open the frozen density prediction.
    density = src.read(1)  # Read the density band.

tree_mask = segmentation == 1  # Identify pixels classified as tree canopy.
overlay = rgb.astype(np.float32).copy()  # Convert the RGB image to floating point for blending.
highlight = np.zeros_like(overlay)  # Create an empty RGB highlight layer.
highlight[..., 0] = 255.0  # Make the highlight layer red.
overlay[tree_mask] = (0.55 * overlay[tree_mask]) + (0.45 * highlight[tree_mask])  # Blend red into predicted tree pixels.
overlay = np.clip(overlay, 0, 255).astype(np.uint8)  # Convert the overlay back to normal 8-bit RGB.

overlay_path = output_dir / f"{image_stem}_treecountsegheight_overlay.png"  # Define the overlay PNG path.
Image.fromarray(overlay).save(overlay_path)  # Save the RGB prediction overlay.

segmentation_path_png = output_dir / f"{image_stem}_treecountsegheight_segmentation.png"  # Define the segmentation PNG path.
Image.fromarray((segmentation * 255).astype(np.uint8)).save(segmentation_path_png)  # Save the binary segmentation as a visible PNG.

density_path_png = output_dir / f"{image_stem}_treecountsegheight_density.png"  # Define the density heatmap PNG path.
plt.imsave(density_path_png, density, cmap="viridis")  # Save a display-normalized density heatmap.

predicted_count = float(np.sum(density))  # Sum the density prediction using the authors' count interpretation.

print(f"Condition: {condition}")  # Report the actual condition used.
print(f"Image: {image_stem}")  # Report the actual image used.
print(f"Predicted density count: {predicted_count:.6f}")  # Report the corresponding frozen predicted count.
print(f"Overlay: {overlay_path}")  # Report the generated overlay path.
print(f"Segmentation: {segmentation_path_png}")  # Report the generated segmentation path.
print(f"Density: {density_path_png}")  # Report the generated density heatmap path.
PY