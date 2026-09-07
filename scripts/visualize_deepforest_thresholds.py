# Import Path so prediction files, image files, and output directories are handled cleanly.
from pathlib import Path

# Import pandas so the frozen DeepForest prediction tables can be filtered without rerunning the model.
import pandas as pd

# Import Shapely's WKT parser so geometry saved as text in CSV files can be restored to geometry objects.
from shapely import wkt

# Import DeepForest's visualization helper so filtered predictions can be drawn on the original images.
from deepforest.visualize import plot_results


# Define the confidence thresholds used for this diagnostic comparison.
THRESHOLDS = [0.25, 0.50]

# Define the experimental conditions that will be processed.
CONDITIONS = ["before", "after"]

# Define the standardized image filename shared by the paired BEFORE and AFTER observations.
IMAGE_NAME = "PT_R1.JPG"

# Define the root directory containing the frozen DeepForest prediction tables.
PREDICTION_ROOT = Path("outputs/experiment_001/deepforest/single_image")

# Define the root directory containing the original standardized imagery.
IMAGE_ROOT = Path("data/raw/experiment_001")

# Define the directory where threshold diagnostic visualizations will be written.
OUTPUT_ROOT = Path("outputs/experiment_001/deepforest/threshold_diagnostics")


# Loop through the BEFORE and AFTER conditions.
for condition in CONDITIONS:

    # Build the path to the frozen prediction CSV for the current condition.
    prediction_path = PREDICTION_ROOT / condition / "PT_R1_predictions.csv"

    # Build the path to the untouched original image for the current condition.
    image_path = IMAGE_ROOT / condition / IMAGE_NAME

    # Read the frozen DeepForest predictions into a pandas DataFrame.
    predictions = pd.read_csv(prediction_path)
    # Convert the geometry column from WKT text back into Shapely geometry objects required by DeepForest visualization.
    predictions["geometry"] = predictions["geometry"].apply(wkt.loads)

    # Loop through each predefined confidence threshold.
    for threshold in THRESHOLDS:

        # Retain only predictions whose confidence score meets or exceeds the current threshold.
        filtered_predictions = predictions[predictions["score"] >= threshold].copy()

        # Build a condition-specific output directory for the current threshold.
        output_dir = OUTPUT_ROOT / condition / f"score_{threshold:.2f}"

        # Create the output directory and any missing parent directories.
        output_dir.mkdir(parents=True, exist_ok=True)

        # Build a filename stem that records the condition and confidence threshold.
        output_name = f"PT_R1_{condition}_score_{threshold:.2f}"

        # Save the filtered prediction table so the diagnostic result remains inspectable.
        filtered_predictions.to_csv(output_dir / f"{output_name}.csv", index=False)

        # Draw the filtered predictions on the original standardized image.
        plot_results(
            results=filtered_predictions,
            savedir=str(output_dir),
            basename=output_name,
            image=str(image_path),
            show=False,
        )

        # Print the experimental condition currently being processed.
        print(f"Condition: {condition}")

        # Print the confidence threshold applied to the frozen predictions.
        print(f"Threshold: {threshold:.2f}")

        # Print the number of detections remaining after threshold filtering.
        print(f"Detections retained: {len(filtered_predictions)}")

        # Print a separator so each diagnostic result is easy to distinguish in the terminal.
        print("=" * 50)