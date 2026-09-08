# Import csv so a human-readable summary of predicted ADE20K classes can be saved.
import csv

# Import math so image dimensions can be aligned to complete DINOv3 patch boundaries.
import math

# Import sys so the source image path can be supplied from the command line.
import sys

# Import Path so repository, model, image, cache, and output paths can be handled reliably.
from pathlib import Path

# Import Pillow so the source image and segmentation visualizations can be read and written.
from PIL import Image, ImageOps

# Import PyTorch so DINOv3 inference and tensor operations can be executed.
import torch

# Import PyTorch functional operations for normalization, interpolation, and softmax-related calculations.
import torch.nn.functional as F

# Import torchvision functional transforms for image conversion, resizing, and normalization.
import torchvision.transforms.functional as TVF

# Import the interpolation enumeration used for bicubic image preprocessing.
from torchvision.transforms import InterpolationMode

# Import Meta's official DINOv3 ViT-L16 plus dino.txt loader.
from dinov3.hub.dinotxt import dinov3_vitl16_dinotxt_tet1280d20h24l


# Define the short-side image resolution used for this fixed DINOv3 segmentation baseline.
RESIZE_SHORT_SIDE = 512

# Define the sliding-window side length used for this fixed DINOv3 segmentation baseline.
WINDOW_SIZE = 384

# Define the sliding-window stride used for this fixed DINOv3 segmentation baseline.
WINDOW_STRIDE = 192

# Define the ImageNet red-channel mean used during DINOv3 preprocessing.
IMAGENET_MEAN = [0.485, 0.456, 0.406]

# Define the ImageNet channel standard deviations used during DINOv3 preprocessing.
IMAGENET_STD = [0.229, 0.224, 0.225]

# Define CPU as the inference device because CUDA is not available in the current environment.
DEVICE = "cpu"


# Define the fixed 150-class ADE20K semantic vocabulary used for multiclass competition.
ADE20K_CLASS_NAMES = (
    "wall",
    "building",
    "sky",
    "floor",
    "tree",
    "ceiling",
    "road",
    "bed ",
    "windowpane",
    "grass",
    "cabinet",
    "sidewalk",
    "person",
    "earth",
    "door",
    "table",
    "mountain",
    "plant",
    "curtain",
    "chair",
    "car",
    "water",
    "painting",
    "sofa",
    "shelf",
    "house",
    "sea",
    "mirror",
    "rug",
    "field",
    "armchair",
    "seat",
    "fence",
    "desk",
    "rock",
    "wardrobe",
    "lamp",
    "bathtub",
    "railing",
    "cushion",
    "base",
    "box",
    "column",
    "signboard",
    "chest of drawers",
    "counter",
    "sand",
    "sink",
    "skyscraper",
    "fireplace",
    "refrigerator",
    "grandstand",
    "path",
    "stairs",
    "runway",
    "case",
    "pool table",
    "pillow",
    "screen door",
    "stairway",
    "river",
    "bridge",
    "bookcase",
    "blind",
    "coffee table",
    "toilet",
    "flower",
    "book",
    "hill",
    "bench",
    "countertop",
    "stove",
    "palm",
    "kitchen island",
    "computer",
    "swivel chair",
    "boat",
    "bar",
    "arcade machine",
    "hovel",
    "bus",
    "towel",
    "light",
    "truck",
    "tower",
    "chandelier",
    "awning",
    "streetlight",
    "booth",
    "television receiver",
    "airplane",
    "dirt track",
    "apparel",
    "pole",
    "land",
    "bannister",
    "escalator",
    "ottoman",
    "bottle",
    "buffet",
    "poster",
    "stage",
    "van",
    "ship",
    "fountain",
    "conveyer belt",
    "canopy",
    "washer",
    "plaything",
    "swimming pool",
    "stool",
    "barrel",
    "basket",
    "waterfall",
    "tent",
    "bag",
    "minibike",
    "cradle",
    "oven",
    "ball",
    "food",
    "step",
    "tank",
    "trade name",
    "microwave",
    "pot",
    "animal",
    "bicycle",
    "lake",
    "dishwasher",
    "screen",
    "blanket",
    "sculpture",
    "hood",
    "sconce",
    "vase",
    "traffic light",
    "tray",
    "ashcan",
    "fan",
    "pier",
    "crt screen",
    "plate",
    "monitor",
    "bulletin board",
    "shower",
    "radiator",
    "glass",
    "clock",
    "flag",
)


# Define a compact fixed set of neutral prompt templates that is frozen before inspecting segmentation results.
PROMPT_TEMPLATES = (
    "{0}",
    "a photo of {0}",
    "an image of {0}",
    "a photograph of {0}",
    "{0} in a scene",
    "the {0}",
    "a visible {0}",
    "a region containing {0}",
)


# Determine the zero-based ADE20K class index corresponding to tree.
TREE_CLASS_INDEX = ADE20K_CLASS_NAMES.index("tree")


# Require exactly one source image path after the script name.
if len(sys.argv) != 2:
    raise ValueError("Usage: run_dinotxt_ade20k.py <image_path>")

# Read the source image path supplied on the command line.
image_path = Path(sys.argv[1])

# Stop immediately if the requested source image does not exist.
if not image_path.exists():
    raise FileNotFoundError(f"Image not found: {image_path}")


# Determine the repository root from the physical location of this script.
repository_root = Path(__file__).resolve().parents[1]

# Define the authorized local DINOv3 ViT-L16 backbone checkpoint.
backbone_weights = repository_root / "models" / "dinov3" / "dinov3_vitl16_pretrain_lvd1689m-8aa4cbdd.pth"

# Define the authorized local dino.txt vision-head and text-encoder checkpoint.
dinotxt_weights = repository_root / "models" / "dinov3" / "dinov3_vitl16_dinotxt_vision_head_and_text_encoder-a442d8f5.pth"

# Define a local ignored cache containing the fixed ADE20K text embeddings after their first calculation.
text_feature_cache = repository_root / "models" / "dinov3" / "ade20k_compact_prompt_text_features.pt"

# Stop immediately if the required DINOv3 visual backbone checkpoint is unavailable.
if not backbone_weights.exists():
    raise FileNotFoundError(f"Backbone weights not found: {backbone_weights}")

# Stop immediately if the required dino.txt checkpoint is unavailable.
if not dinotxt_weights.exists():
    raise FileNotFoundError(f"dino.txt weights not found: {dinotxt_weights}")


# Read the experimental BEFORE or AFTER condition from the source image's parent directory.
condition = image_path.parent.name

# Define the output directory for the native-source ADE20K DINOv3 segmentation experiment.
output_dir = repository_root / "outputs" / "experiment_001" / "dinov3" / "dinotxt" / "ade20k" / "native" / condition

# Create the output directory and any missing parents.
output_dir.mkdir(parents=True, exist_ok=True)


# Print the experiment name before loading the large model.
print("Experiment: DINOv3 dino.txt ADE20K zero-shot segmentation")

# Print the source image being evaluated.
print(f"Image: {image_path}")

# Print the number of fixed semantic classes competing for every image location.
print(f"ADE20K classes: {len(ADE20K_CLASS_NAMES)}")

# Print the number of fixed text prompts used to represent every class.
print(f"Prompt templates per class: {len(PROMPT_TEMPLATES)}")

# Print the zero-based tree-class index for reproducibility.
print(f"Tree class index: {TREE_CLASS_INDEX}")

# Print a status message before loading the large pretrained model.
print("Loading DINOv3 plus dino.txt...")


# Load the authorized local DINOv3 visual backbone and dino.txt text-alignment checkpoints.
model, tokenizer = dinov3_vitl16_dinotxt_tet1280d20h24l(
    weights=str(dinotxt_weights),
    backbone_weights=str(backbone_weights),
)

# Put the complete pretrained model into evaluation mode.
model.eval()

# Move the complete pretrained model explicitly to the CPU.
model.to(DEVICE)

# Select the text-tokenization function returned by Meta's loader.
tokenize = tokenizer.tokenize

# Print confirmation that model loading has completed.
print("Model loaded.")


# Check whether the deterministic fixed text-feature cache already exists.
if text_feature_cache.exists():

    # Print that existing frozen ADE20K text features will be reused.
    print(f"Loading cached ADE20K text features: {text_feature_cache}")

    # Load the cached fixed text embeddings directly onto the CPU.
    text_features = torch.load(text_feature_cache, map_location=DEVICE)

    # Stop if the cached file does not contain exactly one embedding per ADE20K class.
    if text_features.shape[0] != len(ADE20K_CLASS_NAMES):
        raise ValueError("Cached ADE20K text-feature count does not match the fixed class vocabulary.")

# Handle the first run when fixed ADE20K text embeddings have not yet been generated.
else:

    # Print that the fixed text embeddings will be generated once and cached for future images.
    print("Encoding fixed ADE20K text features for the first time...")

    # Create an empty list that will collect one final averaged text embedding for every class.
    class_text_features = []

    # Disable gradient tracking while encoding the fixed semantic vocabulary.
    with torch.inference_mode():

        # Iterate through every fixed ADE20K semantic class.
        for class_index, class_name in enumerate(ADE20K_CLASS_NAMES):

            # Build the fixed text-prompt ensemble for the current semantic class.
            prompt_texts = [template.format(class_name.strip()) for template in PROMPT_TEMPLATES]

            # Convert all fixed prompts for the current class into model tokens.
            prompt_tokens = tokenize(prompt_texts).to(DEVICE)

            # Encode all fixed prompts for the current class using dino.txt.
            prompt_features = model.encode_text(prompt_tokens)

            # Remove the first half corresponding to the text CLS representation used outside dense segmentation.
            prompt_features = prompt_features[:, prompt_features.shape[1] // 2 :]

            # Normalize every individual prompt embedding before averaging.
            prompt_features = F.normalize(prompt_features, p=2, dim=-1)

            # Average the fixed prompt representations into one embedding for the current ADE20K class.
            class_feature = prompt_features.mean(dim=0)

            # Normalize the averaged class embedding again after prompt ensembling.
            class_feature = F.normalize(class_feature, p=2, dim=-1)

            # Add the final fixed class representation to the complete ADE20K vocabulary.
            class_text_features.append(class_feature)

            # Print progress because initial CPU text encoding may take some time.
            print(f"Encoded class {class_index + 1}/{len(ADE20K_CLASS_NAMES)}: {class_name.strip()}")

    # Stack all fixed class embeddings into one class-by-feature tensor.
    text_features = torch.stack(class_text_features)

    # Save the deterministic fixed class embeddings so the AFTER image does not need to encode them again.
    torch.save(text_features.cpu(), text_feature_cache)

    # Print the location of the ignored local text-feature cache.
    print(f"Saved ADE20K text-feature cache: {text_feature_cache}")


# Move the complete fixed ADE20K text-feature tensor onto the CPU inference device.
text_features = text_features.to(DEVICE)


# Open the original standardized drone JPEG.
with Image.open(image_path) as opened_image:

    # Apply any standard JPEG EXIF display-orientation instruction.
    oriented_image = ImageOps.exif_transpose(opened_image)

    # Convert the image explicitly to RGB.
    source_image = oriented_image.convert("RGB")


# Record the untouched source-image dimensions before DINO preprocessing.
source_width, source_height = source_image.size

# Convert the RGB image into a floating-point PyTorch tensor.
image_tensor = TVF.to_tensor(source_image)

# Read the tensor's original channel, height, and width dimensions.
_, source_tensor_height, source_tensor_width = image_tensor.shape


# Check whether image width is the shorter dimension.
if source_tensor_width < source_tensor_height:

    # Set the resized width to the predefined DINO short-side resolution.
    resized_width = RESIZE_SHORT_SIDE

    # Calculate the corresponding resized height while preserving aspect ratio.
    resized_height = int(RESIZE_SHORT_SIDE * source_tensor_height / source_tensor_width)

# Handle landscape imagery where image height is the shorter dimension.
else:

    # Set the resized height to the predefined DINO short-side resolution.
    resized_height = RESIZE_SHORT_SIDE

    # Calculate the corresponding resized width while preserving aspect ratio.
    resized_width = int(RESIZE_SHORT_SIDE * source_tensor_width / source_tensor_height)


# Resize the image using bicubic interpolation while preserving its aspect ratio.
image_tensor = TVF.resize(
    image_tensor,
    [resized_height, resized_width],
    interpolation=InterpolationMode.BICUBIC,
    antialias=True,
)

# Normalize the resized image using the fixed ImageNet channel statistics.
image_tensor = TVF.normalize(
    image_tensor,
    mean=IMAGENET_MEAN,
    std=IMAGENET_STD,
)

# Move the normalized transformed image to the CPU inference device.
image_tensor = image_tensor.to(DEVICE)


# Read the transformed image dimensions used by the sliding-window procedure.
_, transformed_height, transformed_width = image_tensor.shape

# Print the untouched source dimensions.
print(f"Original dimensions: {source_width} x {source_height}")

# Print the dimensions used by DINOv3 after fixed short-side resizing.
print(f"Model preprocessing dimensions: {transformed_width} x {transformed_height}")


# Read the total number of fixed ADE20K classes.
number_of_classes = len(ADE20K_CLASS_NAMES)

# Create a tensor that will accumulate classwise softmax scores across overlapping windows.
class_score_sum = torch.zeros(
    (number_of_classes, transformed_height, transformed_width),
    dtype=torch.float32,
    device=DEVICE,
)

# Create a tensor counting how many sliding windows contribute to every transformed image location.
window_count = torch.zeros(
    (transformed_height, transformed_width),
    dtype=torch.float32,
    device=DEVICE,
)


# Calculate the number of vertical sliding-window locations required for complete coverage.
vertical_windows = max(
    transformed_height - WINDOW_SIZE + WINDOW_STRIDE - 1,
    0,
) // WINDOW_STRIDE + 1

# Calculate the number of horizontal sliding-window locations required for complete coverage.
horizontal_windows = max(
    transformed_width - WINDOW_SIZE + WINDOW_STRIDE - 1,
    0,
) // WINDOW_STRIDE + 1

# Calculate the total number of DINOv3 image windows that will be evaluated.
total_windows = vertical_windows * horizontal_windows

# Initialize a human-readable inference progress counter.
window_number = 0

# Print the number of fixed overlapping image windows.
print(f"Sliding windows: {total_windows}")


# Disable gradient tracking for the complete segmentation inference procedure.
with torch.inference_mode():

    # Iterate through every vertical sliding-window position.
    for vertical_index in range(vertical_windows):

        # Iterate through every horizontal sliding-window position.
        for horizontal_index in range(horizontal_windows):

            # Advance the human-readable inference progress counter.
            window_number += 1

            # Calculate the initial upper image coordinate of the current window.
            y1 = vertical_index * WINDOW_STRIDE

            # Calculate the initial left image coordinate of the current window.
            x1 = horizontal_index * WINDOW_STRIDE

            # Calculate the lower coordinate while remaining inside the transformed image.
            y2 = min(y1 + WINDOW_SIZE, transformed_height)

            # Calculate the right coordinate while remaining inside the transformed image.
            x2 = min(x1 + WINDOW_SIZE, transformed_width)

            # Shift the final vertical window backward when needed so it remains full-sized.
            y1 = max(y2 - WINDOW_SIZE, 0)

            # Shift the final horizontal window backward when needed so it remains full-sized.
            x1 = max(x2 - WINDOW_SIZE, 0)

            # Extract the current normalized image window.
            image_window = image_tensor[:, y1:y2, x1:x2]

            # Read the current image-window dimensions.
            _, window_height, window_width = image_window.shape

            # Read the patch size directly from the loaded DINOv3 ViT backbone.
            patch_size = model.visual_model.backbone.patch_size

            # Round the image-window height upward to a complete DINOv3 patch boundary.
            patch_height = math.ceil(window_height / patch_size) * patch_size

            # Round the image-window width upward to a complete DINOv3 patch boundary.
            patch_width = math.ceil(window_width / patch_size) * patch_size


            # Check whether the current image window already aligns with complete DINOv3 patches.
            if (window_height, window_width) == (patch_height, patch_width):

                # Add the one-image batch dimension required by the DINO visual model.
                model_window = image_window.unsqueeze(0)

            # Handle any future image window whose dimensions do not align with the patch grid.
            else:

                # Resize the image window to dimensions divisible by the DINOv3 patch size.
                model_window = F.interpolate(
                    image_window.unsqueeze(0),
                    size=(patch_height, patch_width),
                    mode="bicubic",
                    align_corners=False,
                )


            # Extract the dense DINOv3 visual patch tokens through the dino.txt visual model.
            _, _, patch_tokens = model.visual_model.get_class_and_patch_tokens(model_window)

            # Reshape the sequential dense patch tokens back into their two-dimensional spatial grid.
            patch_features = patch_tokens.reshape(
                1,
                patch_height // patch_size,
                patch_width // patch_size,
                -1,
            )

            # Remove the single-image batch dimension.
            patch_features = patch_features.squeeze(0)

            # Normalize every dense visual patch feature before cosine-similarity calculation.
            patch_features = F.normalize(
                patch_features,
                p=2,
                dim=-1,
            )

            # Calculate cosine similarity between all 150 fixed class embeddings and every image patch.
            cosine_scores = torch.einsum(
                "cd,hwd->chw",
                text_features,
                patch_features,
            )

            # Upsample low-resolution patch similarities back to the current image-window dimensions.
            cosine_scores = F.interpolate(
                cosine_scores.unsqueeze(0),
                size=(window_height, window_width),
                mode="bilinear",
                align_corners=False,
            ).squeeze(0)

            # Convert cosine similarities into relative class-competition scores within the current image window.
            window_class_scores = cosine_scores.softmax(dim=0)

            # Accumulate relative class scores into their matching transformed-image coordinates.
            class_score_sum[:, y1:y2, x1:x2] += window_class_scores

            # Record one additional observation for every image location covered by the current window.
            window_count[y1:y2, x1:x2] += 1

            # Print progress because the 866-million-parameter model is running entirely on CPU.
            print(f"Window {window_number}/{total_windows} complete.")


# Stop immediately if any transformed image location received no segmentation prediction.
if torch.any(window_count == 0):
    raise RuntimeError("At least one transformed image pixel received no sliding-window prediction.")

# Average class-competition scores wherever multiple overlapping windows predicted the same location.
class_scores = class_score_sum / window_count.unsqueeze(0)

# Select the winning ADE20K semantic class at every transformed image location without using any threshold.
class_map = class_scores.argmax(dim=0)

# Extract the fixed tree-class competition score before discarding the complete score tensor.
tree_class_score = class_scores[TREE_CLASS_INDEX]

# Create a binary tree mask where pixels are selected only when tree wins the 150-class competition.
tree_mask = class_map == TREE_CLASS_INDEX


# Move the complete winning-class map into ordinary CPU memory.
class_map = class_map.cpu()

# Move the raw tree-class competition score map into ordinary CPU memory.
tree_class_score = tree_class_score.cpu()

# Move the binary tree-winning mask into ordinary CPU memory.
tree_mask = tree_mask.cpu()


# Define the path for the raw winning ADE20K class-index tensor.
class_map_path = output_dir / f"{image_path.stem}_ade20k_class_map.pt"

# Save the complete winning-class tensor without visualization modification.
torch.save(class_map, class_map_path)

# Define the path for the raw tree-class competition score tensor.
tree_score_path = output_dir / f"{image_path.stem}_tree_class_score.pt"

# Save the untouched tree-class competition score map.
torch.save(tree_class_score, tree_score_path)


# Convert the binary tree mask into unsigned 8-bit image values where white means tree won.
tree_mask_image_tensor = tree_mask.to(torch.uint8) * 255

# Convert the tree mask tensor into a Pillow-compatible NumPy array.
tree_mask_array = tree_mask_image_tensor.numpy()

# Create a grayscale Pillow image from the binary tree-winning mask.
tree_mask_image = Image.fromarray(tree_mask_array, mode="L")

# Define the path for the human-readable binary tree mask.
tree_mask_path = output_dir / f"{image_path.stem}_tree_mask.png"

# Save the fixed no-threshold binary tree mask.
tree_mask_image.save(tree_mask_path)


# Resize the source RGB image to exactly match the DINOv3 transformed segmentation dimensions.
preview_image = source_image.resize(
    (transformed_width, transformed_height),
    Image.Resampling.BICUBIC,
)

# Define the path for the transformed source preview.
preview_path = output_dir / f"{image_path.stem}_input_preview.png"

# Save the transformed source preview for direct side-by-side comparison.
preview_image.save(preview_path)


# Convert the transformed source preview to RGBA so a transparent tree overlay can be composited.
overlay_base = preview_image.convert("RGBA")

# Create an initially transparent overlay matching the transformed image dimensions.
tree_overlay = Image.new(
    "RGBA",
    overlay_base.size,
    (255, 0, 0, 0),
)

# Convert the binary tree mask into a semi-transparent alpha mask for visualization only.
tree_overlay_alpha = tree_mask_image.point(
    lambda pixel: 120 if pixel > 0 else 0,
)

# Apply the visualization-only alpha mask to the tree overlay.
tree_overlay.putalpha(tree_overlay_alpha)

# Composite the red tree-winning regions over the transformed source preview.
overlay_image = Image.alpha_composite(
    overlay_base,
    tree_overlay,
)

# Define the path for the human-readable tree-overlay image.
overlay_path = output_dir / f"{image_path.stem}_tree_overlay.png"

# Save the visualization-only overlay.
overlay_image.convert("RGB").save(overlay_path)


# Count how many transformed image locations were assigned to every ADE20K class.
class_counts = torch.bincount(
    class_map.reshape(-1),
    minlength=number_of_classes,
)

# Calculate the total number of transformed segmentation locations.
total_pixels = class_map.numel()

# Define the path for the human-readable predicted-class summary.
class_summary_path = output_dir / f"{image_path.stem}_class_counts.csv"


# Open the class-summary CSV for writing with consistent newline behavior.
with class_summary_path.open("w", newline="", encoding="utf-8") as summary_file:

    # Create a CSV writer for the predicted-class summary table.
    writer = csv.writer(summary_file)

    # Write the summary-table column names.
    writer.writerow(
        [
            "class_index",
            "class_name",
            "pixel_count",
            "pixel_fraction",
        ]
    )

    # Iterate through every fixed ADE20K class in its original order.
    for class_index, class_name in enumerate(ADE20K_CLASS_NAMES):

        # Read the number of transformed locations assigned to the current semantic class.
        pixel_count = int(class_counts[class_index].item())

        # Calculate the fraction of transformed image locations assigned to the current class.
        pixel_fraction = pixel_count / total_pixels

        # Write the current fixed class result to the summary table.
        writer.writerow(
            [
                class_index,
                class_name.strip(),
                pixel_count,
                pixel_fraction,
            ]
        )


# Calculate the number of transformed image locations where tree won the full 150-class competition.
tree_pixel_count = int(tree_mask.sum().item())

# Calculate the fraction of transformed image locations where tree won the full 150-class competition.
tree_pixel_fraction = tree_pixel_count / total_pixels


# Print the number of transformed image locations classified as tree.
print(f"Tree-winning pixels: {tree_pixel_count}")

# Print the fraction of transformed image locations classified as tree.
print(f"Tree-winning pixel fraction: {tree_pixel_fraction:.6f}")

# Print the path containing the raw complete ADE20K class map.
print(f"Raw ADE20K class map: {class_map_path}")

# Print the path containing the raw tree-class competition scores.
print(f"Raw tree-class score: {tree_score_path}")

# Print the path containing the fixed binary tree mask.
print(f"Tree mask: {tree_mask_path}")

# Print the path containing the source image with tree-winning regions highlighted.
print(f"Tree overlay: {overlay_path}")

# Print the path containing the matching transformed source preview.
print(f"Input preview: {preview_path}")

# Print the path containing counts for all 150 fixed ADE20K classes.
print(f"Class-count summary: {class_summary_path}")

# Print a completion message without interpreting semantic tree pixels as individual tree crowns.
print("DINOv3 ADE20K zero-shot segmentation complete.")