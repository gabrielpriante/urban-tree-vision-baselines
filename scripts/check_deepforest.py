# Import Python's package metadata utility so we can report installed software versions.
from importlib.metadata import version

# Import PyTorch so we can report the available computation device.
import torch

# Import DeepForest's main model interface.
from deepforest import main


# Define the exact Hugging Face repository containing the pretrained DeepForest tree model.
MODEL_NAME = "weecology/deepforest-tree"

# Define the exact model revision requested from the Hugging Face repository.
MODEL_REVISION = "main"


# Print the installed DeepForest software version.
print(f"DeepForest version: {version('deepforest')}")

# Print the installed PyTorch software version.
print(f"PyTorch version: {torch.__version__}")

# Print whether this environment currently has access to CUDA.
print(f"CUDA available: {torch.cuda.is_available()}")

# Print the exact pretrained model repository that this test will load.
print(f"Model repository: {MODEL_NAME}")

# Print the exact model revision that this test will request.
print(f"Model revision: {MODEL_REVISION}")

# Create the DeepForest model wrapper without yet loading pretrained model weights.
model = main.deepforest()

# Download and load the specified pretrained tree detection model.
model.load_model(model_name=MODEL_NAME, revision=MODEL_REVISION)

# Print the label dictionary loaded with the pretrained model.
print(f"Model labels: {model.label_dict}")

# Print a success message only after the pretrained model has loaded successfully.
print("DeepForest pretrained tree model loaded successfully.")