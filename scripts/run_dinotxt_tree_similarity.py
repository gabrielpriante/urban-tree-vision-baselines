# Import math so image-window dimensions can be rounded to complete DINOv3 patch boundaries when necessary.
import math

# Import sys so the source image path can be supplied from the command line.
import sys

# Import Path so repository, image, model, and output paths are handled reliably.
from pathlib import Path

# Import Pillow so the standardized drone image and diagnostic outputs can be read and written.
from PIL import Image, ImageOps

# Import PyTorch so DINOv3 inference and similarity calculations can be executed.
import torch

# Import PyTorch functional operations for normalization and interpolation.
import torch.nn.functional as F

# Import torchvision functional transforms for image conversion, resizing, and normalization.
import torchvision.transforms.functional as TVF

# Import the interpolation enumeration used for bicubic image resizing.
from torchvision.transforms import InterpolationMode

# Import Meta's official DINOv3 ViT-L16 plus dino.txt loader.
from dinov3.hub.dinotxt import dinov3_vitl16_dinotxt_tet1280d20h24l


# Define the literal zero-shot concept being evaluated.
PROMPT = "tree"

# Define the short-side resolution used by Meta's official dino.txt segmentation example.
RESIZE_SHORT_SIDE = 512

# Define the sliding-window side length used by Meta's official dino.txt segmentation example.
WINDOW_SIZE = 384

# Define the sliding-window stride used by Meta's official dino.txt segmentation example.
WINDOW_STRIDE = 192

# Define the ImageNet channel means used during DINOv3 image preprocessing.
IMAGENET_MEAN = [0.485, 0.456, 0.406]

# Define the ImageNet channel standard deviations used during DINOv3 image preprocessing.
IMAGENET_STD = [0.229, 0.224, 0.225]

# Define CPU as the inference device because CUDA is unavailable in the current environment.
DEVICE = "cpu"


# Require exactly one image path argument after the script name.
if len(sys.argv) != 2:
    raise ValueError("Usage: run_dinotxt_tree_similarity.py <image_path>")

# Read the image path supplied on the command line.
image_path = Path(sys.argv[1])

# Stop immediately if the requested image does not exist.
if not image_path.exists():
    raise FileNotFoundError(f"Image not found: {image_path}")


# Determine the repository root from the physical location of this script.
repository_root = Path(__file__).resolve().parents[1]

# Define the authorized local DINOv3 ViT-L16 backbone checkpoint.
backbone_weights = repository_root / "models" / "dinov3" / "dinov3_vitl16_pretrain_lvd1689m-8aa4cbdd.pth"

# Define the authorized local dino.txt vision-head and text-encoder checkpoint.
dinotxt_weights = repository_root / "models" / "dinov3" / "dinov3_vitl16_dinotxt_vision_head_and_text_encoder-a442d8f5.pth"

# Stop immediately if the expected backbone checkpoint is missing.
if not backbone_weights.exists():
    raise FileNotFoundError(f"Backbone weights not found: {backbone_weights}")

# Stop immediately if the expected dino.txt checkpoint is missing.
if not dinotxt_weights.exists():
    raise FileNotFoundError(f"dino.txt weights not found: {dinotxt_weights}")


# Read the experimental condition from the directory containing the source image.
condition = image_path.parent.name

# Define the output directory for the native-resolution-source DINOv3 tree-similarity experiment.
output_dir = repository_root / "outputs" / "experiment_001" / "dinov3" / "dinotxt" / "tree_similarity" / "native" / condition

# Create the output directory and any missing parent directories.
output_dir.mkdir(parents=True, exist_ok=True)


# Print the exact zero-shot concept being evaluated.
print(f"Prompt: {PROMPT}")

# Print the source image being evaluated.
print(f"Image: {image_path}")

# Print a status message before loading the large pretrained model.
print("Loading DINOv3 plus dino.txt...")


# Load the authorized local DINOv3 visual backbone and dino.txt text-alignment checkpoints.
model, tokenizer = dinov3_vitl16_dinotxt_tet1280d20h24l(
    weights=str(dinotxt_weights),
    backbone_weights=str(backbone_weights),
)

# Put the complete pretrained model into evaluation mode.
model.eval()

# Move the complete model explicitly to the CPU.
model.to(DEVICE)

# Select the tokenizer function returned by Meta's official loader.
tokenize = tokenizer.tokenize

# Print confirmation that the large model has finished loading.
print("Model loaded.")


# Convert the literal tree concept into text tokens.
text_tokens = tokenize([PROMPT]).to(DEVICE)

# Disable gradient tracking while creating the fixed zero-shot text representation.
with torch.inference_mode():

    # Encode the tree text prompt into the dino.txt joint embedding space.
    text_features = model.encode_text(text_tokens)

    # Discard the first half corresponding to the CLS representation as done in Meta's segmentation example.
    text_features = text_features[:, text_features.shape[1] // 2 :]

    # Normalize the text embedding so later dot products represent cosine similarity.
    text_features = F.normalize(text_features, p=2, dim=-1)


# Open the original standardized drone JPEG.
with Image.open(image_path) as opened_image:

    # Apply any standard EXIF display-orientation instruction stored in the JPEG.
    oriented_image = ImageOps.exif_transpose(opened_image)

    # Convert the source explicitly to three-channel RGB.
    source_image = oriented_image.convert("RGB")


# Record the untouched source-image dimensions.
source_width, source_height = source_image.size

# Convert the RGB Pillow image into a floating-point PyTorch tensor.
image_tensor = TVF.to_tensor(source_image)

# Read the tensor dimensions before model-specific resizing.
_, image_height, image_width = image_tensor.shape


# Handle portrait images whose width is the shorter dimension.
if image_width < image_height:

    # Set the shorter image width to 512 pixels.
    resized_width = RESIZE_SHORT_SIDE

    # Calculate the corresponding height while preserving the original aspect ratio.
    resized_height = int(RESIZE_SHORT_SIDE * image_height / image_width)

# Handle landscape images whose height is the shorter dimension.
else:

    # Set the shorter image height to 512 pixels.
    resized_height = RESIZE_SHORT_SIDE

    # Calculate the corresponding width while preserving the original aspect ratio.
    resized_width = int(RESIZE_SHORT_SIDE * image_width / image_height)


# Resize the image using bicubic interpolation while preserving its aspect ratio.
image_tensor = TVF.resize(
    image_tensor,
    [resized_height, resized_width],
    interpolation=InterpolationMode.BICUBIC,
    antialias=True,
)

# Normalize the resized image with the ImageNet statistics used in Meta's example.
image_tensor = TVF.normalize(
    image_tensor,
    mean=IMAGENET_MEAN,
    std=IMAGENET_STD,
)

# Move the normalized image tensor onto the CPU inference device.
image_tensor = image_tensor.to(DEVICE)


# Read the actual transformed dimensions after resizing.
_, transformed_height, transformed_width = image_tensor.shape

# Print the untouched original image dimensions.
print(f"Original dimensions: {source_width} x {source_height}")

# Print the dimensions entering the sliding-window DINOv3 procedure.
print(f"Model preprocessing dimensions: {transformed_width} x {transformed_height}")


# Create a tensor that will accumulate raw tree cosine-similarity values across overlapping windows.
similarity_sum = torch.zeros(
    (transformed_height, transformed_width),
    dtype=torch.float32,
    device=DEVICE,
)

# Create a tensor that will count how many windows contribute to every image pixel.
similarity_count = torch.zeros(
    (transformed_height, transformed_width),
    dtype=torch.float32,
    device=DEVICE,
)


# Calculate the number of vertical sliding-window positions required to cover the image.
vertical_windows = max(
    transformed_height - WINDOW_SIZE + WINDOW_STRIDE - 1,
    0,
) // WINDOW_STRIDE + 1

# Calculate the number of horizontal sliding-window positions required to cover the image.
horizontal_windows = max(
    transformed_width - WINDOW_SIZE + WINDOW_STRIDE - 1,
    0,
) // WINDOW_STRIDE + 1

# Calculate the total number of image windows that will pass through DINOv3.
total_windows = vertical_windows * horizontal_windows

# Initialize a human-readable progress counter.
window_number = 0

# Print the expected number of DINOv3 inference windows before processing begins.
print(f"Sliding windows: {total_windows}")


# Disable gradient tracking for the complete image inference procedure.
with torch.inference_mode():

    # Iterate through every vertical sliding-window location.
    for vertical_index in range(vertical_windows):

        # Iterate through every horizontal sliding-window location.
        for horizontal_index in range(horizontal_windows):

            # Advance the human-readable inference progress counter.
            window_number += 1

            # Calculate the initial upper coordinate of the current image window.
            y1 = vertical_index * WINDOW_STRIDE

            # Calculate the initial left coordinate of the current image window.
            x1 = horizontal_index * WINDOW_STRIDE

            # Calculate the lower coordinate without passing the image boundary.
            y2 = min(y1 + WINDOW_SIZE, transformed_height)

            # Calculate the right coordinate without passing the image boundary.
            x2 = min(x1 + WINDOW_SIZE, transformed_width)

            # Shift the final vertical window backward when necessary so it remains full-sized.
            y1 = max(y2 - WINDOW_SIZE, 0)

            # Shift the final horizontal window backward when necessary so it remains full-sized.
            x1 = max(x2 - WINDOW_SIZE, 0)

            # Extract the current normalized image window.
            image_window = image_tensor[:, y1:y2, x1:x2]

            # Read the actual dimensions of the current window.
            _, window_height, window_width = image_window.shape

            # Read the spatial patch size directly from the loaded DINOv3 backbone.
            patch_size = model.visual_model.backbone.patch_size

            # Calculate a window height divisible by the DINOv3 patch size.
            patch_height = math.ceil(window_height / patch_size) * patch_size

            # Calculate a window width divisible by the DINOv3 patch size.
            patch_width = math.ceil(window_width / patch_size) * patch_size


            # Check whether the current window already aligns exactly with the DINOv3 patch grid.
            if (window_height, window_width) == (patch_height, patch_width):

                # Add the batch dimension required by the visual model without changing image scale.
                model_window = image_window.unsqueeze(0)

            # Handle any future input whose final window does not align exactly with the patch grid.
            else:

                # Add a batch dimension and resize the window to complete DINOv3 patch boundaries.
                model_window = F.interpolate(
                    image_window.unsqueeze(0),
                    size=(patch_height, patch_width),
                    mode="bicubic",
                    align_corners=False,
                )


            # Extract the dense patch tokens through Meta's dino.txt visual model.
            _, _, patch_tokens = model.visual_model.get_class_and_patch_tokens(model_window)

            # Reshape the sequential patch tokens back into their two-dimensional spatial arrangement.
            patch_features = patch_tokens.reshape(
                1,
                patch_height // patch_size,
                patch_width // patch_size,
                -1,
            )

            # Remove the one-image batch dimension.
            patch_features = patch_features.squeeze(0)

            # Normalize every visual patch feature so dot products represent cosine similarity.
            patch_features = F.normalize(
                patch_features,
                p=2,
                dim=-1,
            )

            # Calculate cosine similarity between the tree text embedding and every visual image patch.
            window_similarity = torch.einsum(
                "cd,hwd->chw",
                text_features,
                patch_features,
            ).squeeze(0)

            # Upsample the patch-level similarity values back to the current image-window dimensions.
            window_similarity = F.interpolate(
                window_similarity.unsqueeze(0).unsqueeze(0),
                size=(window_height, window_width),
                mode="bilinear",
                align_corners=False,
            ).squeeze(0).squeeze(0)

            # Add the raw similarity values into their matching image coordinates.
            similarity_sum[y1:y2, x1:x2] += window_similarity

            # Record one additional observation for every pixel covered by the current window.
            similarity_count[y1:y2, x1:x2] += 1

            # Print progress because CPU inference through this model can take substantial time.
            print(f"Window {window_number}/{total_windows} complete.")


# Verify that the sliding-window procedure covered every transformed image pixel.
if torch.any(similarity_count == 0):
    raise RuntimeError("At least one image pixel received no sliding-window prediction.")

# Average raw cosine similarities wherever overlapping windows produced multiple observations.
similarity_map = similarity_sum / similarity_count

# Move the completed raw tree-similarity map explicitly into ordinary CPU memory.
similarity_map = similarity_map.cpu()


# Define the output location for the untouched floating-point cosine-similarity tensor.
raw_output_path = output_dir / f"{image_path.stem}_tree_similarity.pt"

# Save the raw similarity tensor without thresholding or visualization normalization.
torch.save(similarity_map, raw_output_path)


# Measure the minimum raw tree cosine similarity observed anywhere in the transformed image.
similarity_min = similarity_map.min()

# Measure the maximum raw tree cosine similarity observed anywhere in the transformed image.
similarity_max = similarity_map.max()

# Calculate the range of raw similarity values for visualization only.
similarity_range = similarity_max - similarity_min


# Check that the similarity map contains more than one unique value.
if similarity_range.item() > 0:

    # Min-max normalize the map only so it can be inspected visually as an 8-bit image.
    visual_similarity = (similarity_map - similarity_min) / similarity_range

# Handle the unlikely case where every image location has exactly the same similarity value.
else:

    # Create an all-zero visualization while leaving the saved raw tensor unchanged.
    visual_similarity = torch.zeros_like(similarity_map)


# Convert the visualization-only normalized values into unsigned 8-bit grayscale intensities.
visual_similarity = (visual_similarity * 255).clamp(0, 255).to(torch.uint8)

# Convert the grayscale tensor into a NumPy array that Pillow can save.
visual_similarity_array = visual_similarity.numpy()

# Create a grayscale Pillow image from the normalized diagnostic array.
similarity_image = Image.fromarray(visual_similarity_array)

# Define the output path for the human-readable grayscale similarity visualization.
visual_output_path = output_dir / f"{image_path.stem}_tree_similarity.png"

# Save the visualization-only similarity map.
similarity_image.save(visual_output_path)


# Resize the original RGB image to exactly match the DINOv3 similarity-map dimensions.
preview_image = source_image.resize(
    (transformed_width, transformed_height),
    Image.Resampling.BICUBIC,
)

# Define the output path for the matching resized source-image preview.
preview_output_path = output_dir / f"{image_path.stem}_input_preview.png"

# Save the matching source-image preview for side-by-side inspection.
preview_image.save(preview_output_path)


# Print the minimum untouched cosine-similarity value.
print(f"Minimum tree similarity: {similarity_min.item():.6f}")

# Print the maximum untouched cosine-similarity value.
print(f"Maximum tree similarity: {similarity_max.item():.6f}")

# Print the path containing the raw floating-point similarity tensor.
print(f"Raw similarity map: {raw_output_path}")

# Print the path containing the visualization-only grayscale similarity map.
print(f"Similarity visualization: {visual_output_path}")

# Print the path containing the matching transformed source-image preview.
print(f"Input preview: {preview_output_path}")

# Print a completion message without describing the similarity map as a discrete tree segmentation.
print("DINOv3 tree-similarity inference complete.")