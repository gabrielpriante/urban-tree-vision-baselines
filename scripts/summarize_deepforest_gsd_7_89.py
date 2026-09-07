# Import Path so the saved prediction file locations can be represented cleanly.
from pathlib import Path

# Import pandas so the saved DeepForest prediction tables can be analyzed.
import pandas as pd


# Define the saved BEFORE prediction table from the 7.89 cm/pixel experiment.
BEFORE_PATH = Path("outputs/experiment_001/deepforest/gsd_7.89/before/PT_R1_predictions.csv")

# Define the saved AFTER prediction table from the 7.89 cm/pixel experiment.
AFTER_PATH = Path("outputs/experiment_001/deepforest/gsd_7.89/after/PT_R1_predictions.csv")


# Define a function that summarizes one saved DeepForest prediction table.
def summarize_predictions(path: Path, condition: str) -> None:

    # Read the saved prediction CSV into a pandas DataFrame.
    predictions = pd.read_csv(path)

    # Stop immediately if the expected DeepForest confidence column is missing.
    if "score" not in predictions.columns:
        raise ValueError(f"Expected a 'score' column in {path}")

    # Print a separator so the experimental conditions are easy to distinguish.
    print("=" * 50)

    # Print the experimental condition being summarized.
    print(f"Condition: {condition}")

    # Print the total number of retained DeepForest predictions.
    print(f"Total detections: {len(predictions)}")

    # Print the minimum retained confidence score.
    print(f"Minimum score: {predictions['score'].min():.4f}")

    # Print the median retained confidence score.
    print(f"Median score: {predictions['score'].median():.4f}")

    # Print the arithmetic mean confidence score.
    print(f"Mean score: {predictions['score'].mean():.4f}")

    # Print the maximum retained confidence score.
    print(f"Maximum score: {predictions['score'].max():.4f}")

    # Count predictions with confidence greater than or equal to 0.25.
    count_025 = (predictions["score"] >= 0.25).sum()

    # Count predictions with confidence greater than or equal to 0.50.
    count_050 = (predictions["score"] >= 0.50).sum()

    # Count predictions with confidence greater than or equal to 0.75.
    count_075 = (predictions["score"] >= 0.75).sum()

    # Count predictions with confidence greater than or equal to 0.90.
    count_090 = (predictions["score"] >= 0.90).sum()

    # Print the number of predictions surviving a 0.25 diagnostic threshold.
    print(f"Score >= 0.25: {count_025}")

    # Print the number of predictions surviving a 0.50 diagnostic threshold.
    print(f"Score >= 0.50: {count_050}")

    # Print the number of predictions surviving a 0.75 diagnostic threshold.
    print(f"Score >= 0.75: {count_075}")

    # Print the number of predictions surviving a 0.90 diagnostic threshold.
    print(f"Score >= 0.90: {count_090}")


# Summarize the frozen 7.89 cm/pixel BEFORE predictions.
summarize_predictions(BEFORE_PATH, "before")

# Summarize the frozen 7.89 cm/pixel AFTER predictions.
summarize_predictions(AFTER_PATH, "after")