(sam2) gabpe@gps2:~/src/urban-tree-vision-baselines$ sha256sum data/annotations/experiment_001/b3_field_points/before/PT_02/PT_02_before_field_points.csv # Reconfirm that the CSV contents still have the frozen SHA-256 value after changing only its file permissions.
43bc6786e2c558dcd5044f8f140f730817e68b445d1a48ed242f18d2bafb20ed  data/annotations/experiment_001/b3_field_points/before/PT_02/PT_02_before_field_points.csv
(sam2) gabpe@gps2:~/src/urban-tree-vision-baselines$ git add data/annotations/experiment_001/b3_field_points/before/PT_02/PT_02_before_field_points.csv # Stage only the corrected non-executable file mode for the frozen PT_02 BEFORE annotation CSV.
(sam2) gabpe@gps2:~/src/urban-tree-vision-baselines$ git diff --cached --summary # Confirm that the staged change remains only a 100755 to 100644 file-mode correction with no content modification.
 mode change 100755 => 100644 data/annotations/experiment_001/b3_field_points/before/PT_02/PT_02_before_field_points.csv
(sam2) gabpe@gps2:~/src/urban-tree-vision-baselines$ git diff --cached --check # Confirm that the staged housekeeping change contains no whitespace problems.
(sam2) gabpe@gps2:~/src/urban-tree-vision-baselines$ git commit -m "Fix PT_02 annotation file mode" # Preserve the normal data-file permission for the frozen PT_02 BEFORE annotation without changing its research contents.
[main 3d19b5a] Fix PT_02 annotation file mode
 1 file changed, 0 insertions(+), 0 deletions(-)
 mode change 100755 => 100644 data/annotations/experiment_001/b3_field_points/before/PT_02/PT_02_before_field_points.csv
(sam2) gabpe@gps2:~/src/urban-tree-vision-baselines$ git push origin main # Publish the annotation permission cleanup before modifying the SAM2 inference workflow.
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 20 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (8/8), 658 bytes | 658.00 KiB/s, done.
Total 8 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/gabrielpriante/urban-tree-vision-baselines.git
   8879074..3d19b5a  main -> main
(sam2) gabpe@gps2:~/src/urban-tree-vision-baselines$ git status # Confirm that the repository is clean and synchronized before generalizing B3 inference for PT_02.
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
(sam2) gabpe@gps2:~/src/urban-tree-vision-baselines$ sed -n '1,360p' scripts/run_sam2_field_points.py # Display the complete currently frozen PT_R1 B3 inference implementation so the PT_02 generalization can preserve every existing provenance and validation safeguard.
import argparse  # Import argparse so the before or after PT_R1 condition is specified explicitly at runtime.
import csv  # Import csv so the frozen field-point registration table can be read without adding another dependency.
import hashlib  # Import hashlib so every B3 input artifact can be verified by SHA-256 before inference.
import json  # Import json so the complete field-guided SAM2 prediction record can be preserved in machine-readable form.
import time  # Import time so total B3 inference duration can be measured.
from pathlib import Path  # Import Path so repository-relative research paths are constructed consistently.
import numpy as np  # Import NumPy so field point prompts and the untouched RGB image use the formats expected by Meta's predictor.
import torch  # Import PyTorch so SAM2 can run on the RTX 5070 and GPU memory usage can be recorded.
from PIL import Image  # Import Pillow so the untouched native standardized image can be verified and loaded.
from sam2.build_sam import build_sam2  # Import Meta's official SAM2 model builder used successfully in B1 and B2.
from sam2.sam2_image_predictor import SAM2ImagePredictor  # Import Meta's official single-image predictor for positive point prompts.
from sam2.utils.amg import area_from_rle, mask_to_rle_pytorch  # Import Meta's official utilities for lossless mask encoding and mask-area calculation.

MODEL_CONFIG = "configs/sam2.1/sam2.1_hiera_b+.yaml"  # Freeze the official SAM2.1 Hiera Base+ configuration already used throughout Phase B.
CHECKPOINT_PATH = Path("models/sam2/checkpoints/sam2.1_hiera_base_plus.pt")  # Freeze the local path to the same official SAM2.1 Base+ checkpoint used in B1 and B2.
CHECKPOINT_SHA256 = "a2345aede8715ab1d5d31b4a509fb160c5a4af1970f199d9054ccfb746c004c5"  # Freeze the verified SHA-256 identity of the SAM2.1 Base+ checkpoint.
SAM2_SOURCE_COMMIT = "2b90b9f5ceec907a1c18123530e92e794ad901a4"  # Freeze the exact official Meta SAM2 source revision already used for the earlier Phase B baselines.
NATIVE_WIDTH = 8192  # Freeze the verified width of the untouched PT_R1 standardized RGB images.
NATIVE_HEIGHT = 6144  # Freeze the verified height of the untouched PT_R1 standardized RGB images.
EXPECTED_TREE_IDS = [3, 4, 5, 6, 7, 8, 9, 10, 11]  # Freeze the nine field-confirmed PT_R1 tree IDs in the registration order used during annotation.
EXPECTED_REGISTRATION_METHOD = "manual_field_confirmed_registration"  # Freeze the provenance label used by the committed manual field-to-image registration workflow.
EXPECTED_NATIVE_SHA256 = {"before": "6714da4af1cf0c099a3addfef1e7fa1bdc30f43668fd010f3e2c3bdb5d8e3a4f", "after": "52055a866e17486a663df1fd746d300c2525a7f5227fa9f8bbafad9f0378bb79"}  # Freeze the previously verified SHA-256 identities of the two untouched PT_R1 standardized JPEGs.
EXPECTED_FIELD_POINTS_SHA256 = {"before": "830721c5f19ce9035f68a2f5261e6b338c579edc7df26e1b29ff43e50790017c", "after": "e3793dceb6f94a76cf244d5c25d10497c50c3c76525452c92d09f0ece334ad54"}  # Freeze the verified SHA-256 identities of the committed BEFORE and AFTER field-point registration CSVs.

def sha256_file(path):  # Define a reusable helper that calculates the SHA-256 identity of one research artifact.
    digest = hashlib.sha256()  # Create a fresh SHA-256 calculator for the requested file.
    with path.open("rb") as input_file:  # Open the file in binary mode without modifying it.
        for chunk in iter(lambda: input_file.read(1024 * 1024), b""):  # Read the file in one-megabyte chunks so large imagery does not need to be loaded only for hashing.
            digest.update(chunk)  # Add each binary chunk to the running SHA-256 calculation.
    return digest.hexdigest()  # Return the completed immutable file identifier.

parser = argparse.ArgumentParser()  # Create the command-line parser for the frozen B3 field-guided experiment.
parser.add_argument("condition", choices=["before", "after"])  # Require the caller to explicitly select the BEFORE or AFTER PT_R1 registration and image.
args = parser.parse_args()  # Parse the requested B3 condition before any research artifact is loaded.

native_path = Path("data/raw/experiment_001") / args.condition / "PT_R1.JPG"  # Locate the untouched native PT_R1 RGB image that SAM2 will segment.
field_points_path = Path("data/annotations/experiment_001/b3_field_points") / args.condition / "PT_R1" / f"PT_R1_{args.condition}_field_points.csv"  # Locate the exact committed field-confirmed point registration used as the B3 prompt source.
output_dir = Path("outputs/sam2/experiment_001/b3_field_points") / args.condition / "PT_R1"  # Define the ignored output directory for the selected B3 condition.
output_dir.mkdir(parents=True, exist_ok=True)  # Create the ignored B3 output directory without modifying any tracked research input.
output_path = output_dir / "PT_R1_sam2_field_point_masks.json"  # Define the machine-readable output file that will preserve all nine field-guided SAM2 masks.

checkpoint_sha256 = sha256_file(CHECKPOINT_PATH)  # Calculate the SHA-256 identity of the local SAM2 checkpoint before model loading.
native_sha256 = sha256_file(native_path)  # Calculate the SHA-256 identity of the untouched PT_R1 native RGB image.
field_points_sha256 = sha256_file(field_points_path)  # Calculate the SHA-256 identity of the exact committed field-point registration CSV.

assert checkpoint_sha256 == CHECKPOINT_SHA256, f"SAM2 checkpoint SHA-256 mismatch: {checkpoint_sha256}"  # Stop immediately if the SAM2 checkpoint differs from the frozen Phase B model artifact.
assert native_sha256 == EXPECTED_NATIVE_SHA256[args.condition], f"Native image SHA-256 mismatch: {native_sha256}"  # Stop immediately if the PT_R1 image differs from the previously frozen standardized research input.
assert field_points_sha256 == EXPECTED_FIELD_POINTS_SHA256[args.condition], f"Field-point CSV SHA-256 mismatch: {field_points_sha256}"  # Stop immediately if the field-guided prompt table differs from the frozen committed registration artifact.

with Image.open(native_path) as native_source_image:  # Open the untouched PT_R1 standardized JPEG that SAM2 will segment.
    assert native_source_image.size == (NATIVE_WIDTH, NATIVE_HEIGHT), f"Unexpected native image size: {native_source_image.size}"  # Stop if the image coordinate space differs from the verified 8192 by 6144 dimensions.
    image = np.array(native_source_image.convert("RGB"))  # Convert the untouched native image into the HWC uint8 RGB array expected by Meta's SAM2 predictor.

with field_points_path.open("r", encoding="utf-8", newline="") as csv_file:  # Open the frozen field-point registration table without modifying it.
    field_rows = list(csv.DictReader(csv_file))  # Read all nine field-confirmed tree registrations in their committed CSV order.

assert len(field_rows) == len(EXPECTED_TREE_IDS), f"Unexpected field-point count: {len(field_rows)}"  # Stop if the B3 prompt source does not contain exactly nine field-confirmed tree registrations.
observed_tree_ids = [int(row["tree_id"]) for row in field_rows]  # Read the tree IDs from the committed registration table in their existing order.
assert observed_tree_ids == EXPECTED_TREE_IDS, f"Unexpected tree ID sequence: {observed_tree_ids}"  # Stop if any tree is missing, duplicated, reordered, or replaced relative to the frozen registration protocol.

for row in field_rows:  # Validate every committed field-point record before loading the SAM2 model.
    assert row["condition"] == args.condition, f"Condition mismatch for Tree {row['tree_id']}: {row['condition']}"  # Stop if a row belongs to the wrong BEFORE or AFTER condition.
    assert row["image_stem"] == "PT_R1", f"Image stem mismatch for Tree {row['tree_id']}: {row['image_stem']}"  # Stop if a field registration references a scene other than PT_R1.
    assert row["image_filename"] == "PT_R1.JPG", f"Image filename mismatch for Tree {row['tree_id']}: {row['image_filename']}"  # Stop if the registration references a different standardized filename.
    assert int(row["native_width"]) == NATIVE_WIDTH, f"Native width mismatch for Tree {row['tree_id']}: {row['native_width']}"  # Stop if the registered horizontal coordinate space differs from the actual native image.
    assert int(row["native_height"]) == NATIVE_HEIGHT, f"Native height mismatch for Tree {row['tree_id']}: {row['native_height']}"  # Stop if the registered vertical coordinate space differs from the actual native image.
    assert row["registration_method"] == EXPECTED_REGISTRATION_METHOD, f"Registration method mismatch for Tree {row['tree_id']}: {row['registration_method']}"  # Stop if a row was not produced under the frozen manual field-confirmed registration protocol.
    assert 0 <= int(row["x"]) < NATIVE_WIDTH, f"Invalid x coordinate for Tree {row['tree_id']}: {row['x']}"  # Stop if a registered positive point falls outside the native image horizontally.
    assert 0 <= int(row["y"]) < NATIVE_HEIGHT, f"Invalid y coordinate for Tree {row['tree_id']}: {row['y']}"  # Stop if a registered positive point falls outside the native image vertically.

model = build_sam2(MODEL_CONFIG, CHECKPOINT_PATH, device="cuda", apply_postprocessing=False)  # Build the same pinned SAM2.1 Base+ model without additional postprocessing.
predictor = SAM2ImagePredictor(model)  # Create Meta's official single-image prompt predictor for repeated frozen field-point prompts.

torch.cuda.reset_peak_memory_stats()  # Reset peak GPU-memory accounting immediately before B3 image embedding and field-guided inference.
start_time = time.perf_counter()  # Record the wall-clock start time immediately before SAM2 processes the research image.
results = []  # Create the list that will preserve one B3 SAM2 result for every field-confirmed tree.

with torch.inference_mode():  # Disable gradient calculation because B3 is frozen pretrained inference only.
    with torch.autocast("cuda", dtype=torch.bfloat16):  # Use the same GPU bfloat16 inference precision used in the earlier frozen SAM2 baselines.
        predictor.set_image(image)  # Compute the SAM2 image embedding once so all nine frozen field points reuse the same native-image representation.
        for row in field_rows:  # Process each field-confirmed tree exactly once and in the committed registration order.
            tree_id = int(row["tree_id"])  # Read the frozen physical tree identifier from the committed field registration.
            point_x = float(row["x"])  # Read the frozen native-image x coordinate for this field-confirmed tree.
            point_y = float(row["y"])  # Read the frozen native-image y coordinate for this field-confirmed tree.
            point_coords = np.array([[point_x, point_y]], dtype=np.float32)  # Create the single positive native-image point prompt expected by Meta's SAM2 predictor.
            point_labels = np.array([1], dtype=np.int32)  # Label the single frozen field point as a positive foreground prompt.
            masks, iou_scores, _ = predictor.predict(point_coords=point_coords, point_labels=point_labels, multimask_output=False, return_logits=False, normalize_coords=True)  # Generate exactly one binary SAM2 mask from the single frozen positive field point without boxes, negative points, or candidate-mask selection.
            mask = masks[0]  # Select the single returned mask because the B3 protocol freezes multimask output to false.
            mask_tensor = torch.from_numpy(mask).to(torch.bool).unsqueeze(0)  # Convert the binary mask into the batch-shaped Boolean tensor required by Meta's official RLE encoder.
            segmentation_rle = mask_to_rle_pytorch(mask_tensor)[0]  # Encode the complete native-resolution SAM2 mask losslessly using Meta's official uncompressed RLE representation.
            results.append({"tree_id": tree_id, "native_point_xy": [point_x, point_y], "point_label": 1, "registration_method": row["registration_method"], "sam2_predicted_iou": float(iou_scores[0]), "segmentation": segmentation_rle, "area": int(area_from_rle(segmentation_rle))})  # Preserve the physical tree ID, frozen point prompt, SAM2 quality estimate, complete mask geometry, and mask area without manual alteration.

elapsed_seconds = time.perf_counter() - start_time  # Calculate total B3 image-embedding plus nine-point-prompt inference duration.
peak_gpu_memory_mb = torch.cuda.max_memory_allocated() / (1024 ** 2)  # Record the maximum PyTorch GPU allocation observed during the complete B3 run.

payload = {"phase": "B3", "method": "Field-confirmed manually registered positive points to SAM2 point prompts", "condition": args.condition, "image_stem": "PT_R1", "native_image_path": str(native_path), "native_image_sha256": native_sha256, "native_image_width": NATIVE_WIDTH, "native_image_height": NATIVE_HEIGHT, "field_points_path": str(field_points_path), "field_points_sha256": field_points_sha256, "field_tree_ids": EXPECTED_TREE_IDS, "field_point_count": len(field_rows), "sam2_mask_count": len(results), "model_config": MODEL_CONFIG, "checkpoint_path": str(CHECKPOINT_PATH), "checkpoint_sha256": checkpoint_sha256, "sam2_source_commit": SAM2_SOURCE_COMMIT, "torch_version": torch.__version__, "torch_cuda_version": torch.version.cuda, "gpu": torch.cuda.get_device_name(0), "prompt_type": "single_positive_point", "positive_points_per_tree": 1, "negative_points_per_tree": 0, "box_prompts_used": False, "multimask_output": False, "manual_mask_selection": False, "post_inference_prompt_adjustment": False, "apply_postprocessing": False, "elapsed_seconds": elapsed_seconds, "peak_gpu_memory_mb": peak_gpu_memory_mb, "masks": results}  # Assemble complete B3 provenance, frozen prompt rules, runtime metadata, and one-to-one field-tree-to-SAM2 mask records.

with output_path.open("w", encoding="utf-8") as output_file:  # Open the ignored B3 machine-readable output path for writing.
    json.dump(payload, output_file, indent=2)  # Save every field-guided SAM2 prediction without manual filtering, selection, or truth-informed alteration.

print(f"Native input: {native_path}")  # Report the exact untouched PT_R1 RGB image supplied to SAM2.
print(f"Native SHA-256: {native_sha256}")  # Report the immutable identity of the native standardized research image.
print(f"Field points: {field_points_path}")  # Report the exact committed field-point registration table used for B3 prompts.
print(f"Field points SHA-256: {field_points_sha256}")  # Report the immutable identity of the frozen field-point prompt table.
print(f"Field tree IDs: {observed_tree_ids}")  # Report the complete frozen physical tree-ID sequence consumed by B3.
print(f"Positive point prompts: {len(field_rows)}")  # Report the exact number of positive field prompts supplied to SAM2.
print(f"SAM2 masks: {len(results)}")  # Report the resulting mask count so the expected one-to-one field-tree mapping is immediately visible.
print(f"Elapsed seconds: {elapsed_seconds:.2f}")  # Report total wall-clock B3 inference duration.
print(f"Peak GPU memory MB: {peak_gpu_memory_mb:.2f}")  # Report peak allocated GPU memory during the complete B3 run.
print(f"Output: {output_path}")  # Report the machine-readable B3 prediction location.(sam2) gabpe@gps2:~/src/urban-tree-vision-baselines$