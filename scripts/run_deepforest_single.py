# Import sys so the script can receive an image path from the command line.
import sys

# Import Path so file and directory paths are handled cleanly across operating systems.
from pathlib import Path

# Import the main DeepForest model interface.
from deepforest import main

# Import DeepForest's visualization helper so prediction boxes can be drawn on the original image.
from deepforest.visualize import plot_results


# Define the exact pretrained tree detection model repository used for this baseline.
MODEL_NAME = "weecology/deepforest-tree"

# Define the model revision requested from the repository.
MODEL_REVISION = "main"

# Define the image patch size in pixels used during tiled inference.
PATCH_SIZE = 400

# Define the fractional overlap between adjacent inference patches.
PATCH_OVERLAP = 0.05

# Define the IoU threshold used to suppress duplicate detections created across overlapping tiles.
IOU_THRESHOLD = 0.15

# Define the minimum model confidence required for a tree detection to be retained.
SCORE_THRESHOLD = 0.10

# Define the model-level non-maximum suppression threshold.
NMS_THRESHOLD = 0.05


# Read the image path supplied as the first command-line argument.
image_path = Path(sys.argv[1])

# Stop immediately with a clear error if the supplied image does not exist.
if not image_path.exists():
    raise FileNotFoundError(f"Image not found: {image_path}")

# Read the experimental condition from the name of the image's parent directory, such as "before" or "after".
condition = image_path.parent.name

# Define a separate output directory for the current experimental condition so identically named before and after images cannot overwrite each other.
output_dir = Path("outputs/experiment_001/deepforest/single_image") / condition

# Create the output directory and any missing parent directories.
output_dir.mkdir(parents=True, exist_ok=True)

# Create the DeepForest model wrapper.
model = main.deepforest()

# Load the pretrained individual-tree detection model.
model.load_model(model_name=MODEL_NAME, revision=MODEL_REVISION)

# Explicitly set the model confidence threshold used for retained predictions.
model.config.score_thresh = SCORE_THRESHOLD

# Explicitly set the model non-maximum suppression threshold.
model.config.nms_thresh = NMS_THRESHOLD

# Run tiled inference on the original image using explicitly defined baseline parameters.
predictions = model.predict_tile(
    path=str(image_path),
    patch_size=PATCH_SIZE,
    patch_overlap=PATCH_OVERLAP,
    iou_threshold=IOU_THRESHOLD,
    dataloader_strategy="single",
)

# Create the output filename for the raw prediction table.
csv_path = output_dir / f"{image_path.stem}_predictions.csv"

# Save every retained DeepForest prediction to a CSV file without adding a pandas index column.
predictions.to_csv(csv_path, index=False)

# Create a filename stem for the annotated prediction image.
plot_name = f"{image_path.stem}_predictions"

# Draw the DeepForest predictions on the original image and save the visualization as a PNG.
plot_results(
    results=predictions,
    savedir=str(output_dir),
    basename=plot_name,
    image=str(image_path),
    show=False,
)

# Print the image path that was analyzed.
print(f"Image: {image_path}")

# Print the number of retained tree detections produced by DeepForest.
print(f"Detections: {len(predictions)}")

# Print the location of the raw prediction CSV file.
print(f"Prediction CSV: {csv_path}")

# Print the location of the annotated PNG visualization.
print(f"Prediction image: {output_dir / f'{plot_name}.png'}")