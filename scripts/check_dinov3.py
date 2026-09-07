# Import Python package metadata so the installed DINOv3 package version can be reported.
from importlib.metadata import version

# Import Path so repository and model-weight paths can be constructed reliably.
from pathlib import Path

# Import PyTorch so the runtime version and compute device can be reported.
import torch

# Import Meta's official pretrained DINOv3 ViT-L16 plus dino.txt loader.
from dinov3.hub.dinotxt import dinov3_vitl16_dinotxt_tet1280d20h24l


# Determine the repository root from the physical location of this script.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

# Define the local path to the authorized DINOv3 ViT-L16 LVD-1689M backbone weights.
BACKBONE_WEIGHTS = REPOSITORY_ROOT / "models" / "dinov3" / "dinov3_vitl16_pretrain_lvd1689m-8aa4cbdd.pth"

# Define the local path to the authorized dino.txt vision-head and text-encoder weights.
DINOTXT_WEIGHTS = REPOSITORY_ROOT / "models" / "dinov3" / "dinov3_vitl16_dinotxt_vision_head_and_text_encoder-a442d8f5.pth"


# Stop immediately if the expected DINOv3 backbone file does not exist.
if not BACKBONE_WEIGHTS.exists():
    raise FileNotFoundError(f"DINOv3 backbone weights not found: {BACKBONE_WEIGHTS}")

# Stop immediately if the expected dino.txt weight file does not exist.
if not DINOTXT_WEIGHTS.exists():
    raise FileNotFoundError(f"dino.txt weights not found: {DINOTXT_WEIGHTS}")


# Print the installed DINOv3 package version.
print(f"DINOv3 package version: {version('dinov3')}")

# Print the installed PyTorch version used by the isolated DINOv3 environment.
print(f"PyTorch version: {torch.__version__}")

# Print whether CUDA acceleration is available.
print(f"CUDA available: {torch.cuda.is_available()}")

# Print the exact architecture being loaded.
print("Model: dinov3_vitl16_dinotxt_tet1280d20h24l")

# Print the explicitly selected backbone checkpoint.
print(f"Backbone weights: {BACKBONE_WEIGHTS}")

# Print the explicitly selected dino.txt checkpoint.
print(f"dino.txt weights: {DINOTXT_WEIGHTS}")

# Print a status message before the large model begins loading.
print("Loading pretrained DINOv3 plus dino.txt model...")

# Load the official DINOv3 backbone and dino.txt weights from the explicitly documented local files.
model, tokenizer = dinov3_vitl16_dinotxt_tet1280d20h24l(
    weights=str(DINOTXT_WEIGHTS),
    backbone_weights=str(BACKBONE_WEIGHTS),
)

# Put the model into evaluation mode so training behavior is disabled.
model.eval()

# Place the model explicitly on the CPU because this environment currently has no CUDA support.
model.to("cpu")

# Count every parameter in the complete loaded model for a reproducibility sanity check.
parameter_count = sum(parameter.numel() for parameter in model.parameters())

# Print the loaded model class.
print(f"Model class: {type(model).__name__}")

# Print the tokenizer class returned by the official loader.
print(f"Tokenizer class: {type(tokenizer).__name__}")

# Print the model parameter count.
print(f"Total parameters: {parameter_count:,}")

# Print success only after the complete model stack has loaded.
print("DINOv3 plus dino.txt loaded successfully.")