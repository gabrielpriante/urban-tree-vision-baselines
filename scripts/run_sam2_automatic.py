import argparse  # Import argparse so the image and experimental condition are supplied explicitly on the command line.
import hashlib  # Import hashlib so the exact input image can be identified with SHA-256.
import json  # Import json so every automatic-mask result and inference setting can be preserved.
import time  # Import time so wall-clock inference duration can be recorded.
from pathlib import Path  # Import Path so repository file paths are handled consistently.
import numpy as np  # Import NumPy so the RGB image can be supplied to SAM 2 as an HWC uint8 array.
import torch  # Import PyTorch so GPU inference, autocasting, and hardware metadata can be controlled.
from PIL import Image  # Import Pillow so the untouched standardized JPEG can be loaded as RGB.
from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator  # Import Meta's official automatic mask generator.
from sam2.build_sam import build_sam2  # Import Meta's official SAM 2 model builder.

MODEL_CONFIG = "configs/sam2.1/sam2.1_hiera_b+.yaml"  # Freeze the official SAM 2.1 Hiera Base+ configuration used for Phase B.
CHECKPOINT_PATH = Path("models/sam2/checkpoints/sam2.1_hiera_base_plus.pt")  # Freeze the local path to Meta's official Base+ checkpoint.
CHECKPOINT_SHA256 = "a2345aede8715ab1d5d31b4a509fb160c5a4af1970f199d9054ccfb746c004c5"  # Record the exact downloaded checkpoint identity.
SAM2_SOURCE_COMMIT = "2b90b9f5ceec907a1c18123530e92e794ad901a4"  # Record the exact official Meta SAM 2 source revision used for Phase B.

parser = argparse.ArgumentParser()  # Create a command-line parser for the frozen B1 experiment.
parser.add_argument("condition", choices=["before", "after"])  # Require the caller to identify the before or after experimental condition.
parser.add_argument("image_stem", choices=["PT_R1", "PT_02"])  # Require the caller to identify one of the two standardized image stems.
args = parser.parse_args()  # Parse the command-line arguments before loading any research image.

input_path = Path("data/raw/experiment_001") / args.condition / f"{args.image_stem}.JPG"  # Locate the untouched standardized RGB JPEG.
output_dir = Path("outputs/sam2/experiment_001/b1_automatic") / args.condition / args.image_stem  # Define the ignored B1 output directory for this exact image.
output_dir.mkdir(parents=True, exist_ok=True)  # Create the ignored output directory without changing any research inputs.
output_path = output_dir / f"{args.image_stem}_sam2_automatic_masks.json"  # Define the machine-readable file that will preserve every generated mask.

sha256 = hashlib.sha256()  # Create a SHA-256 calculator for the exact research-image input.
with input_path.open("rb") as input_file:  # Open the standardized JPEG in binary mode without modifying it.
    for chunk in iter(lambda: input_file.read(1024 * 1024), b""):  # Read the image in one-megabyte chunks so hashing does not require loading the file twice into memory.
        sha256.update(chunk)  # Add each binary chunk to the running SHA-256 calculation.
input_sha256 = sha256.hexdigest()  # Store the final immutable identifier for the exact JPEG supplied to SAM 2.

with Image.open(input_path) as source_image:  # Open the untouched standardized JPEG with Pillow.
    image = np.array(source_image.convert("RGB"))  # Convert the image to the HWC uint8 RGB array expected by Meta's automatic mask generator.

model = build_sam2(MODEL_CONFIG, CHECKPOINT_PATH, device="cuda", apply_postprocessing=False)  # Build the pinned SAM 2.1 Base+ model using the automatic-mask example's no-postprocessing model configuration.

mask_generator = SAM2AutomaticMaskGenerator(  # Construct the B1 automatic mask generator with explicitly frozen untuned parameters.
    model=model,  # Supply the pinned SAM 2.1 Base+ model.
    points_per_side=32,  # Use Meta's default 32 by 32 point-prompt grid.
    points_per_batch=64,  # Use Meta's default inference batch of 64 prompt points.
    pred_iou_thresh=0.8,  # Use Meta's default predicted-IoU quality threshold.
    stability_score_thresh=0.95,  # Use Meta's default mask-stability threshold.
    stability_score_offset=1.0,  # Use Meta's default stability-score cutoff offset.
    mask_threshold=0.0,  # Use Meta's default mask-logit binarization threshold.
    box_nms_thresh=0.7,  # Use Meta's default within-image duplicate-mask NMS threshold.
    crop_n_layers=0,  # Use Meta's default of no additional image-crop inference layers.
    crop_nms_thresh=0.7,  # Preserve Meta's default crop-level NMS value even though crop layers are disabled.
    crop_overlap_ratio=512 / 1500,  # Preserve Meta's default crop overlap ratio even though crop layers are disabled.
    crop_n_points_downscale_factor=1,  # Preserve Meta's default crop point-grid downscale factor.
    min_mask_region_area=0,  # Disable small-region postprocessing exactly as frozen for B1.
    output_mode="uncompressed_rle",  # Preserve exact masks as compact uncompressed run-length encodings instead of huge in-memory binary arrays.
    use_m2m=False,  # Preserve Meta's default of no additional mask-to-mask refinement step.
    multimask_output=True,  # Preserve Meta's default generation of multiple candidate masks per prompt before quality filtering.
)  # Finish construction of the frozen B1 automatic mask generator.

torch.cuda.reset_peak_memory_stats()  # Reset GPU peak-memory accounting immediately before research-image inference.
start_time = time.perf_counter()  # Record the wall-clock start time immediately before mask generation.

with torch.inference_mode():  # Disable gradient calculation because B1 is pretrained inference only.
    with torch.autocast("cuda", dtype=torch.bfloat16):  # Use GPU bfloat16 autocasting for SAM 2 inference without changing the stored model weights.
        masks = mask_generator.generate(image)  # Generate all B1 automatic masks from the image without tree labels, detector boxes, or field prompts.

elapsed_seconds = time.perf_counter() - start_time  # Calculate the total automatic-mask inference duration.
peak_gpu_memory_mb = torch.cuda.max_memory_allocated() / (1024 ** 2)  # Record the maximum allocated GPU memory observed during B1 inference.

serialized_masks = []  # Create a JSON-safe list that will preserve every automatic mask returned by SAM 2.
for mask_id, annotation in enumerate(masks):  # Process every returned automatic mask without manually selecting or filtering any result.
    serialized_masks.append({  # Add one complete machine-readable mask record to the preserved output.
        "mask_id": mask_id,  # Assign a deterministic integer identifier based only on the generator's returned order.
        "segmentation": annotation["segmentation"],  # Preserve the exact uncompressed RLE representation of the generated mask.
        "area": int(annotation["area"]),  # Preserve the mask area in original-image pixels.
        "bbox": [float(value) for value in annotation["bbox"]],  # Preserve the XYWH bounding box returned by Meta's generator.
        "predicted_iou": float(annotation["predicted_iou"]),  # Preserve SAM 2's own predicted mask-quality score.
        "point_coords": [[float(value) for value in point] for point in annotation["point_coords"]],  # Preserve the automatic point prompt that generated the mask.
        "stability_score": float(annotation["stability_score"]),  # Preserve the returned mask-stability score.
        "crop_box": [float(value) for value in annotation["crop_box"]],  # Preserve the generator crop box in XYWH coordinates.
    })  # Finish the preserved record for this generated mask.

payload = {  # Create one complete reproducibility record for the B1 image inference.
    "phase": "B1",  # Record the experimental phase.
    "method": "SAM2 automatic mask generation",  # Record the inference method.
    "condition": args.condition,  # Record the before or after condition.
    "image_stem": args.image_stem,  # Record the standardized image identifier.
    "input_path": str(input_path),  # Record the repository-relative source-image path.
    "input_sha256": input_sha256,  # Record the exact standardized JPEG identity.
    "image_width": int(image.shape[1]),  # Record the untouched image width supplied to SAM 2.
    "image_height": int(image.shape[0]),  # Record the untouched image height supplied to SAM 2.
    "model_config": MODEL_CONFIG,  # Record the official SAM 2.1 Base+ configuration.
    "checkpoint_path": str(CHECKPOINT_PATH),  # Record the local official checkpoint path.
    "checkpoint_sha256": CHECKPOINT_SHA256,  # Record the immutable checkpoint identifier.
    "sam2_source_commit": SAM2_SOURCE_COMMIT,  # Record the immutable upstream Meta source revision.
    "torch_version": torch.__version__,  # Record the exact PyTorch build used during inference.
    "torch_cuda_version": torch.version.cuda,  # Record the CUDA version bundled with the PyTorch build.
    "gpu": torch.cuda.get_device_name(0),  # Record the exact GPU used for B1 inference.
    "generator_parameters": {  # Record every frozen automatic-mask parameter that can affect the generated prediction set.
        "points_per_side": 32,  # Record the fixed prompt-grid density.
        "points_per_batch": 64,  # Record the fixed prompt-processing batch size.
        "pred_iou_thresh": 0.8,  # Record the fixed predicted-IoU filter.
        "stability_score_thresh": 0.95,  # Record the fixed mask-stability filter.
        "stability_score_offset": 1.0,  # Record the fixed stability-score offset.
        "mask_threshold": 0.0,  # Record the fixed mask-logit threshold.
        "box_nms_thresh": 0.7,  # Record the fixed duplicate-mask NMS threshold.
        "crop_n_layers": 0,  # Record that no crop layers were used.
        "crop_nms_thresh": 0.7,  # Record the preserved crop NMS threshold.
        "crop_overlap_ratio": 512 / 1500,  # Record the preserved crop-overlap ratio.
        "crop_n_points_downscale_factor": 1,  # Record the preserved crop point-grid factor.
        "min_mask_region_area": 0,  # Record that no small-region postprocessing was performed.
        "output_mode": "uncompressed_rle",  # Record the lossless serialization format used for the masks.
        "use_m2m": False,  # Record that mask-to-mask refinement was disabled.
        "multimask_output": True,  # Record that multimask generation was enabled.
    },  # Finish the preserved B1 generator settings.
    "mask_count": len(serialized_masks),  # Record the total number of masks returned after Meta's built-in quality filtering and NMS.
    "elapsed_seconds": elapsed_seconds,  # Record wall-clock B1 inference time.
    "peak_gpu_memory_mb": peak_gpu_memory_mb,  # Record peak GPU memory used by automatic mask generation.
    "masks": serialized_masks,  # Preserve every returned automatic mask without tree-specific filtering.
}  # Finish the complete B1 output payload.

with output_path.open("w", encoding="utf-8") as output_file:  # Open the ignored machine-readable output file for writing.
    json.dump(payload, output_file, indent=2)  # Save the complete frozen B1 prediction record as readable JSON.

print(f"Input: {input_path}")  # Report the exact research image processed.
print(f"Input SHA-256: {input_sha256}")  # Report the exact source-image identity.
print(f"Image size: {image.shape[1]} x {image.shape[0]}")  # Report the untouched research-image dimensions.
print(f"Automatic masks: {len(serialized_masks)}")  # Report the number of masks produced by the frozen B1 pipeline.
print(f"Elapsed seconds: {elapsed_seconds:.2f}")  # Report wall-clock automatic-mask inference duration.
print(f"Peak GPU memory MB: {peak_gpu_memory_mb:.2f}")  # Report maximum allocated GPU memory during inference.
print(f"Output: {output_path}")  # Report the machine-readable B1 prediction location.
