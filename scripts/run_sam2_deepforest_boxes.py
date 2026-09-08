import argparse  # Import argparse so the condition and standardized image stem are specified explicitly at runtime.
import csv  # Import csv so the frozen DeepForest prediction table can be read without adding another dependency.
import hashlib  # Import hashlib so every input artifact can be verified by SHA-256 before B2 inference.
import json  # Import json so the complete B2 prediction record can be preserved in machine-readable form.
import time  # Import time so total B2 inference duration can be measured.
from pathlib import Path  # Import Path so repository-relative paths are constructed consistently.
import numpy as np  # Import NumPy so the untouched RGB image and SAM 2 box prompts use the formats expected by Meta's predictor.
import torch  # Import PyTorch so SAM 2 can run on the RTX 5070 and GPU memory usage can be recorded.
from PIL import Image  # Import Pillow so both the native image and the 7.89 cm DeepForest image can be verified and loaded.
from sam2.build_sam import build_sam2  # Import Meta's official SAM 2 model builder.
from sam2.sam2_image_predictor import SAM2ImagePredictor  # Import Meta's official image predictor for box-prompt segmentation.
from sam2.utils.amg import area_from_rle, mask_to_rle_pytorch  # Import Meta's official utilities for lossless mask encoding and mask-area calculation.
MODEL_CONFIG = "configs/sam2.1/sam2.1_hiera_b+.yaml"  # Freeze the official SAM 2.1 Hiera Base+ configuration used throughout Phase B.
CHECKPOINT_PATH = Path("models/sam2/checkpoints/sam2.1_hiera_base_plus.pt")  # Freeze the local path to Meta's official SAM 2.1 Base+ weights.
CHECKPOINT_SHA256 = "a2345aede8715ab1d5d31b4a509fb160c5a4af1970f199d9054ccfb746c004c5"  # Record the immutable SHA-256 identity of the SAM 2.1 Base+ checkpoint.
SAM2_SOURCE_COMMIT = "2b90b9f5ceec907a1c18123530e92e794ad901a4"  # Record the exact official Meta SAM 2 source revision used for B2.
NATIVE_WIDTH = 8192  # Freeze the verified width of every untouched standardized RGB image used for SAM 2 inference.
NATIVE_HEIGHT = 6144  # Freeze the verified height of every untouched standardized RGB image used for SAM 2 inference.
DEEPFOREST_WIDTH = 1734  # Freeze the verified width of the 7.89 cm images on which the DeepForest boxes were generated.
DEEPFOREST_HEIGHT = 1300  # Freeze the verified height of the 7.89 cm images on which the DeepForest boxes were generated.
EXPECTED_COUNTS = {("before", "PT_R1"): 293, ("after", "PT_R1"): 302, ("before", "PT_02"): 386, ("after", "PT_02"): 412}  # Freeze the verified number of DeepForest box prompts for each image.
EXPECTED_NATIVE_SHA256 = {("before", "PT_R1"): "6714da4af1cf0c099a3addfef1e7fa1bdc30f43668fd010f3e2c3bdb5d8e3a4f", ("after", "PT_R1"): "52055a866e17486a663df1fd746d300c2525a7f5227fa9f8bbafad9f0378bb79", ("before", "PT_02"): "3cfd7506f79fbab319912bbaab23c88a2e7637fbe959b309724023f58f742e34", ("after", "PT_02"): "99f051490499a722782facab412b9d3eac73a28641c93bfc23e7913ec6a3171f"}  # Freeze the previously verified SHA-256 identities of the four untouched native JPEGs.
EXPECTED_DEEPFOREST_IMAGE_SHA256 = {("before", "PT_R1"): "4feccc73936ccebc75c424b053d0e2902e7f26f664a5c4c24ea20a7fffa2e565", ("after", "PT_R1"): "8e360c5985e234fc95f61ab519b9a0e99a28d039b46affe3d4bd0b1ede7f9176", ("before", "PT_02"): "3cc55adf73b65578e30b752985e6f14858415c14ccb730d66f4fde095c522f21", ("after", "PT_02"): "b7decb3721a09e8ff80f91a8238ca7f53a6d0037bef9fbd3efbd816d037acb73"}  # Freeze the SHA-256 identities of the four exact 7.89 cm DeepForest input images.
EXPECTED_DEEPFOREST_CSV_SHA256 = {("before", "PT_R1"): "278d9b064acadd47a60d015ce6b6e98d3df06b2372ec1ba89f37ebb138c4f7a3", ("after", "PT_R1"): "0eaf1dd912d369a45b53d4276836f64f76d4892c7198c04772b9a7c8e0dd6e4c", ("before", "PT_02"): "c8a7505c2d28c49d3b3d9691a00344c1ba431c7cdf8c221646a91e58e4867784", ("after", "PT_02"): "4c78f491546a0241942296123e46c362f2e82e17d0faec26e933cd8a86e7cd4e"}  # Freeze the SHA-256 identities of the four exact DeepForest prediction tables used as B2 prompts.
def sha256_file(path):  # Define a small helper that calculates the SHA-256 identity of one input artifact.
    digest = hashlib.sha256()  # Create a fresh SHA-256 calculator for this file.
    with path.open("rb") as input_file:  # Open the file in binary mode without modifying it.
        for chunk in iter(lambda: input_file.read(1024 * 1024), b""):  # Read the file in one-megabyte chunks so large images do not need to be loaded solely for hashing.
            digest.update(chunk)  # Add each binary chunk to the running SHA-256 calculation.
    return digest.hexdigest()  # Return the completed immutable file identifier.
parser = argparse.ArgumentParser()  # Create the command-line parser for the frozen B2 experiment.
parser.add_argument("condition", choices=["before", "after"])  # Require the caller to identify the before or after experimental condition.
parser.add_argument("image_stem", choices=["PT_R1", "PT_02"])  # Require the caller to identify one of the two standardized scene images.
args = parser.parse_args()  # Parse the requested B2 image before loading any research artifact.
key = (args.condition, args.image_stem)  # Create the condition-image key used by the frozen provenance dictionaries.
native_path = Path("data/raw/experiment_001") / args.condition / f"{args.image_stem}.JPG"  # Locate the untouched 8192 by 6144 RGB image that SAM 2 will segment.
deepforest_image_path = Path("data/derived/experiment_001/gsd_7.89") / args.condition / f"{args.image_stem}.JPG"  # Locate the exact 1734 by 1300 image used to generate the frozen DeepForest boxes.
deepforest_csv_path = Path("outputs/experiment_001/deepforest/gsd_7.89") / args.condition / f"{args.image_stem}_predictions.csv"  # Locate the exact frozen DeepForest prediction table used as the B2 prompt source.
output_dir = Path("outputs/sam2/experiment_001/b2_deepforest_boxes") / args.condition / args.image_stem  # Define the ignored output directory for this B2 image.
output_dir.mkdir(parents=True, exist_ok=True)  # Create the ignored B2 output directory without modifying any input artifact.
output_path = output_dir / f"{args.image_stem}_sam2_deepforest_box_masks.json"  # Define the machine-readable file that will preserve every DeepForest-guided SAM 2 mask.
native_sha256 = sha256_file(native_path)  # Calculate the SHA-256 identity of the untouched native RGB image supplied to SAM 2.
deepforest_image_sha256 = sha256_file(deepforest_image_path)  # Calculate the SHA-256 identity of the exact 7.89 cm image used by DeepForest.
deepforest_csv_sha256 = sha256_file(deepforest_csv_path)  # Calculate the SHA-256 identity of the exact frozen DeepForest prediction table.
assert native_sha256 == EXPECTED_NATIVE_SHA256[key], f"Native image SHA-256 mismatch: {native_sha256}"  # Stop immediately if the native image differs from the previously frozen research input.
assert deepforest_image_sha256 == EXPECTED_DEEPFOREST_IMAGE_SHA256[key], f"DeepForest image SHA-256 mismatch: {deepforest_image_sha256}"  # Stop immediately if the 7.89 cm DeepForest source image differs from the frozen artifact.
assert deepforest_csv_sha256 == EXPECTED_DEEPFOREST_CSV_SHA256[key], f"DeepForest CSV SHA-256 mismatch: {deepforest_csv_sha256}"  # Stop immediately if the DeepForest prompt table differs from the frozen Phase A output.
with Image.open(deepforest_image_path) as deepforest_source_image:  # Open the 7.89 cm image only to verify the coordinate-space dimensions used by the frozen detector.
    assert deepforest_source_image.size == (DEEPFOREST_WIDTH, DEEPFOREST_HEIGHT), f"Unexpected DeepForest image size: {deepforest_source_image.size}"  # Stop if the actual DeepForest coordinate space differs from the verified 1734 by 1300 dimensions.
with native_path.open("rb"):  # Confirm that the untouched native image path is readable before loading the model.
    pass  # Perform no modification while completing the path-readability check.
with Image.open(native_path) as native_source_image:  # Open the untouched standardized JPEG that SAM 2 will segment.
    assert native_source_image.size == (NATIVE_WIDTH, NATIVE_HEIGHT), f"Unexpected native image size: {native_source_image.size}"  # Stop if the SAM 2 coordinate space differs from the verified 8192 by 6144 dimensions.
    image = np.array(native_source_image.convert("RGB"))  # Convert the untouched image into the HWC uint8 RGB array expected by Meta's SAM 2 predictor.
with deepforest_csv_path.open("r", encoding="utf-8", newline="") as csv_file:  # Open the frozen DeepForest prediction table without modifying it.
    deepforest_rows = list(csv.DictReader(csv_file))  # Read every frozen DeepForest detection in its original table order.
assert len(deepforest_rows) == EXPECTED_COUNTS[key], f"Unexpected DeepForest detection count: {len(deepforest_rows)}"  # Stop if the number of box prompts differs from the count verified before B2 was written.
scale_x = NATIVE_WIDTH / DEEPFOREST_WIDTH  # Calculate the exact horizontal mapping from the 1734-pixel DeepForest coordinate space to the 8192-pixel native image.
scale_y = NATIVE_HEIGHT / DEEPFOREST_HEIGHT  # Calculate the exact vertical mapping from the 1300-pixel DeepForest coordinate space to the 6144-pixel native image.
model = build_sam2(MODEL_CONFIG, CHECKPOINT_PATH, device="cuda", apply_postprocessing=False)  # Build the same pinned SAM 2.1 Base+ model without extra postprocessing.
predictor = SAM2ImagePredictor(model)  # Create Meta's official single-image prompt predictor for repeated DeepForest box prompts.
torch.cuda.reset_peak_memory_stats()  # Reset peak GPU-memory accounting immediately before B2 image embedding and mask inference.
start_time = time.perf_counter()  # Record the wall-clock start time immediately before SAM 2 processes the research image.
results = []  # Create the list that will preserve one B2 SAM 2 result for every frozen DeepForest detection.
with torch.inference_mode():  # Disable gradient calculation because B2 is pretrained inference only.
    with torch.autocast("cuda", dtype=torch.bfloat16):  # Use the same GPU bfloat16 inference precision employed for the frozen B1 baseline.
        predictor.set_image(image)  # Compute the SAM 2 image embedding once so all frozen DeepForest boxes can reuse the same native-image representation.
        for detection_id, row in enumerate(deepforest_rows):  # Process every frozen DeepForest detection exactly once and in its existing table order.
            xmin = float(row["xmin"])  # Read the frozen DeepForest left box coordinate in the 1734-pixel coordinate space.
            ymin = float(row["ymin"])  # Read the frozen DeepForest top box coordinate in the 1300-pixel coordinate space.
            xmax = float(row["xmax"])  # Read the frozen DeepForest right box coordinate in the 1734-pixel coordinate space.
            ymax = float(row["ymax"])  # Read the frozen DeepForest bottom box coordinate in the 1300-pixel coordinate space.
            assert 0.0 <= xmin < xmax <= DEEPFOREST_WIDTH, f"Invalid DeepForest x coordinates at row {detection_id}: {(xmin, xmax)}"  # Stop rather than silently modifying any frozen horizontal prompt coordinate.
            assert 0.0 <= ymin < ymax <= DEEPFOREST_HEIGHT, f"Invalid DeepForest y coordinates at row {detection_id}: {(ymin, ymax)}"  # Stop rather than silently modifying any frozen vertical prompt coordinate.
            native_box = np.array([xmin * scale_x, ymin * scale_y, xmax * scale_x, ymax * scale_y], dtype=np.float32)  # Map the complete frozen DeepForest XYXY box into the untouched native-image coordinate space using verified dimensions.
            masks, iou_scores, _ = predictor.predict(box=native_box, multimask_output=False, return_logits=False, normalize_coords=True)  # Generate exactly one binary SAM 2 mask from this mapped DeepForest box prompt without manual point prompts or candidate-mask selection.
            mask = masks[0]  # Select the single mask returned because the B2 protocol freezes multimask output to false for each box prompt.
            mask_tensor = torch.from_numpy(mask).unsqueeze(0)  # Convert the single binary mask into the batch-shaped tensor expected by Meta's official RLE encoder.
            segmentation_rle = mask_to_rle_pytorch(mask_tensor)[0]  # Encode the full-resolution SAM 2 mask losslessly using Meta's official uncompressed RLE representation.
            results.append({"detection_id": detection_id, "deepforest_box_7_89_xyxy": [xmin, ymin, xmax, ymax], "native_box_xyxy": [float(value) for value in native_box], "deepforest_label": row["label"], "deepforest_score": float(row["score"]), "sam2_predicted_iou": float(iou_scores[0]), "segmentation": segmentation_rle, "area": int(area_from_rle(segmentation_rle))})  # Preserve the exact detector prompt, coordinate mapping, detector score, SAM 2 quality estimate, full mask geometry, and mask area for this detection.
elapsed_seconds = time.perf_counter() - start_time  # Calculate total B2 image-embedding plus box-prompt inference duration.
peak_gpu_memory_mb = torch.cuda.max_memory_allocated() / (1024 ** 2)  # Record the maximum PyTorch GPU allocation observed during the complete B2 run.
payload = {"phase": "B2", "method": "Frozen DeepForest 7.89 cm boxes to SAM2 box prompts", "condition": args.condition, "image_stem": args.image_stem, "native_image_path": str(native_path), "native_image_sha256": native_sha256, "native_image_width": NATIVE_WIDTH, "native_image_height": NATIVE_HEIGHT, "deepforest_image_path": str(deepforest_image_path), "deepforest_image_sha256": deepforest_image_sha256, "deepforest_image_width": DEEPFOREST_WIDTH, "deepforest_image_height": DEEPFOREST_HEIGHT, "deepforest_csv_path": str(deepforest_csv_path), "deepforest_csv_sha256": deepforest_csv_sha256, "coordinate_scale_x": scale_x, "coordinate_scale_y": scale_y, "deepforest_detection_count": len(deepforest_rows), "sam2_mask_count": len(results), "model_config": MODEL_CONFIG, "checkpoint_path": str(CHECKPOINT_PATH), "checkpoint_sha256": CHECKPOINT_SHA256, "sam2_source_commit": SAM2_SOURCE_COMMIT, "torch_version": torch.__version__, "torch_cuda_version": torch.version.cuda, "gpu": torch.cuda.get_device_name(0), "multimask_output": False, "manual_box_editing": False, "field_truth_used_for_prompt_selection": False, "elapsed_seconds": elapsed_seconds, "peak_gpu_memory_mb": peak_gpu_memory_mb, "masks": results}  # Assemble the complete provenance, frozen protocol, runtime metadata, and one-to-one DeepForest-to-SAM2 prediction record.
with output_path.open("w", encoding="utf-8") as output_file:  # Open the ignored B2 machine-readable output path for writing.
    json.dump(payload, output_file, indent=2)  # Save every B2 prompt and mask without manual filtering or truth-informed alteration.
print(f"Native input: {native_path}")  # Report the exact untouched RGB image supplied to SAM 2.
print(f"Native SHA-256: {native_sha256}")  # Report the immutable identity of the native research image.
print(f"DeepForest image: {deepforest_image_path}")  # Report the exact 7.89 cm image defining the original box coordinate space.
print(f"DeepForest image SHA-256: {deepforest_image_sha256}")  # Report the immutable identity of the 7.89 cm DeepForest source image.
print(f"DeepForest CSV: {deepforest_csv_path}")  # Report the exact frozen detector prediction table used for B2 prompts.
print(f"DeepForest CSV SHA-256: {deepforest_csv_sha256}")  # Report the immutable identity of the frozen DeepForest prediction table.
print(f"Coordinate scale X: {scale_x:.12f}")  # Report the exact horizontal coordinate-space conversion factor.
print(f"Coordinate scale Y: {scale_y:.12f}")  # Report the exact vertical coordinate-space conversion factor.
print(f"DeepForest boxes: {len(deepforest_rows)}")  # Report the number of frozen DeepForest detections consumed by B2.
print(f"SAM2 masks: {len(results)}")  # Report the number of resulting SAM 2 masks so the expected one-to-one mapping is immediately visible.
print(f"Elapsed seconds: {elapsed_seconds:.2f}")  # Report total wall-clock B2 inference duration.
print(f"Peak GPU memory MB: {peak_gpu_memory_mb:.2f}")  # Report peak allocated GPU memory during B2.
print(f"Output: {output_path}")  # Report the machine-readable B2 prediction location.
