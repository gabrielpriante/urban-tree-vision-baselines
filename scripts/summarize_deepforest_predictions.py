# Import Path so prediction file locations can be represented as filesystem paths.
from pathlib import Path

# Import pandas so the saved DeepForest prediction tables can be analyzed directly.
import pandas as pd


# Define the saved BEFORE prediction table produced by the native-resolution baseline.
BEFORE_PATH = Path("outputs/experiment_001/deepforest/single_image/before/PT_R1_predictions.csv")

# Define the saved AFTER prediction table produced by the identical baseline configuration.
AFTER_PATH = Path("outputs/experiment_001/deepforest/single_image/after/PT_R1_predictions.csv")


# Define a function that summarizes one saved DeepForest prediction table.
def summarize_predictions(path: Path, condition: str) -> None:

    # Read the saved prediction CSV into a pandas DataFrame.
    predictions = pd.read_csv(path)

    # Stop with a clear error if the expected DeepForest confidence column is missing.
    if "score" not in predictions.columns:
        raise ValueError(f"Expected a 'score' column in {path}, but found: {list(predictions.columns)}")

    # Print a visual separator so the two experimental conditions are easy to distinguish.
    print("=" * 50)

    # Print the experimental condition currently being summarized.
    print(f"Condition: {condition}")

    # Print the number of retained model detections in the saved prediction table.
    print(f"Total detections: {len(predictions)}")

    # Print the lowest retained DeepForest confidence score.
    print(f"Minimum score: {predictions['score'].min():.4f}")

    # Print the median DeepForest confidence score.
    print(f"Median score: {predictions['score'].median():.4f}")

    # Print the arithmetic mean DeepForest confidence score.
    print(f"Mean score: {predictions['score'].mean():.4f}")

    # Print the highest retained DeepForest confidence score.
    print(f"Maximum score: {predictions['score'].max():.4f}")

    # Count predictions with confidence greater than or equal to 0.25.
    count_025 = (predictions["score"] >= 0.25).sum()

    # Count predictions with confidence greater than or equal to 0.50.
    count_050 = (predictions["score"] >= 0.50).sum()

    # Count predictions with confidence greater than or equal to 0.75.
    count_075 = (predictions["score"] >= 0.75).sum()

    # Count predictions with confidence greater than or equal to 0.90.
    count_090 = (predictions["score"] >= 0.90).sum()

    # Print the number of detections surviving a hypothetical 0.25 confidence cutoff.
    print(f"Score >= 0.25: {count_025}")

    # Print the number of detections surviving a hypothetical 0.50 confidence cutoff.
    print(f"Score >= 0.50: {count_050}")

    # Print the number of detections surviving a hypothetical 0.75 confidence cutoff.
    print(f"Score >= 0.75: {count_075}")

    # Print the number of detections surviving a hypothetical 0.90 confidence cutoff.
    print(f"Score >= 0.90: {count_090}")


# Summarize the frozen BEFORE baseline predictions without rerunning DeepForest.
summarize_predictions(BEFORE_PATH, "before")

# Summarize the frozen AFTER baseline predictions without rerunning DeepForest.
summarize_predictions(AFTER_PATH, "after")