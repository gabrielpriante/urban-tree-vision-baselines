import argparse  # Import argparse so the condition and standardized image stem are specified explicitly at runtime.
import csv  # Import csv so frozen field-point registration tables can be read without adding another dependency.
import hashlib  # Import hashlib so every B3 input artifact can be verified by SHA-256 before inference.
import json  # Import json so complete field-guided SAM2 prediction records can be preserved in machine-readable form.
import time  # Import time so total B3 inference duration can be measured.
from pathlib import Path  # Import Path so repository-relative research paths are constructed consistently.

import numpy as np  # Import NumPy so point prompts and untouched RGB images use the formats expected by Meta's predictor.
import torch  # Import PyTorch so SAM2 can run on the RTX 5070 and GPU memory usage can be recorded.
from PIL import Image  # Import Pillow so untouched native standardized images can be verified and loaded.
from sam2.build_sam import build_sam2  # Import Meta's official SAM2 model builder already used throughout Phase B.
from sam2.sam2_image_predictor import SAM2ImagePredictor  # Import Meta's official single-image predictor for positive point prompts.
from sam2.utils.amg import area_from_rle, mask_to_rle_pytorch  # Import Meta's official utilities for lossless mask encoding and mask-area calculation.

MODEL_CONFIG = "configs/sam2.1/sam2.1_hiera_b+.yaml"  # Freeze the official SAM2.1 Hiera Base+ configuration already used throughout Phase B.
CHECKPOINT_PATH = Path("models/sam2/checkpoints/sam2.1_hiera_base_plus.pt")  # Freeze the local path to the same official SAM2.1 Base+ checkpoint used in B1, B2, and PT_R1 B3.
CHECKPOINT_SHA256 = "a2345aede8715ab1d5d31b4a509fb160c5a4af1970f199d9054ccfb746c004c5"  # Freeze the verified SHA-256 identity of the SAM2.1 Base+ checkpoint.
SAM2_SOURCE_COMMIT = "2b90b9f5ceec907a1c18123530e92e794ad901a4"  # Freeze the exact official Meta SAM2 source revision already used throughout Phase B.
NATIVE_WIDTH = 8192  # Freeze the verified width of every untouched standardized RGB image used in this experiment.
NATIVE_HEIGHT = 6144  # Freeze the verified height of every untouched standardized RGB image used in this experiment.

EXPECTED_IDS = {  # Freeze the required registration sequence separately for each B3 study scene.
    "PT_R1": [3, 4, 5, 6, 7, 8, 9, 10, 11],  # Preserve the nine field-confirmed physical PT_R1 tree IDs used in the original B3 experiment.
    "PT_02": [f"A{index:02d}" for index in range(1, 23)],  # Preserve neutral registration IDs A01 through A22 for the field-count-constrained PT_02 alleyway experiment.
}  # Finish the scene-specific expected registration identifiers.

ID_COLUMNS = {  # Freeze the annotation column that contains the identifier for each scene.
    "PT_R1": "tree_id",  # Preserve the original PT_R1 CSV schema containing physical field tree IDs.
    "PT_02": "registration_id",  # Use neutral registration IDs for PT_02 because exact physical tree identity is not asserted.
}  # Finish the scene-specific identifier-column mapping.

EXPECTED_REGISTRATION_METHODS = {  # Freeze the permitted registration provenance label for each scene.
    "PT_R1": "manual_field_confirmed_registration",  # Preserve the original PT_R1 field-confirmed image-registration method.
    "PT_02": "manual_field_count_constrained_registration",  # Preserve the lower-spatial-certainty PT_02 field-count-constrained registration method.
}  # Finish the scene-specific registration-method mapping.

OUTPUT_METHODS = {  # Define human-readable descriptions of the spatial guidance supplied to SAM2.
    "PT_R1": "Field-confirmed manually registered positive points to SAM2 point prompts",  # Describe PT_R1 as field-confirmed identity with manual image registration.
    "PT_02": "Field-count-constrained manually registered positive points to SAM2 point prompts",  # Describe PT_02 as field-count-constrained candidate locations rather than confirmed physical-tree coordinates.
}  # Finish the scene-specific B3 method descriptions.

EXPECTED_NATIVE_SHA256 = {  # Freeze the previously verified SHA-256 identities of all four untouched native standardized JPEGs.
    ("before", "PT_R1"): "6714da4af1cf0c099a3addfef1e7fa1bdc30f43668fd010f3e2c3bdb5d8e3a4f",  # Preserve the verified PT_R1 BEFORE native-image identity.
    ("after", "PT_R1"): "52055a866e17486a663df1fd746d300c2525a7f5227fa9f8bbafad9f0378bb79",  # Preserve the verified PT_R1 AFTER native-image identity.
    ("before", "PT_02"): "3cfd7506f79fbab319912bbaab23c88a2e7637fbe959b309724023f58f742e34",  # Preserve the verified PT_02 BEFORE native-image identity.
    ("after", "PT_02"): "99f051490499a722782facab412b9d3eac73a28641c93bfc23e7913ec6a3171f",  # Preserve the verified PT_02 AFTER native-image identity for later use after its points are frozen.
}  # Finish the native-image SHA-256 mapping.

EXPECTED_FIELD_POINTS_SHA256 = {  # Freeze only field-point annotation artifacts that already exist and were committed before inference.
    ("before", "PT_R1"): "830721c5f19ce9035f68a2f5261e6b338c579edc7df26e1b29ff43e50790017c",  # Preserve the verified PT_R1 BEFORE point-registration identity.
    ("after", "PT_R1"): "e3793dceb6f94a76cf244d5c25d10497c50c3c76525452c92d09f0ece334ad54",  # Preserve the verified PT_R1 AFTER point-registration identity.
    ("before", "PT_02"): "43bc6786e2c558dcd5044f8f140f730817e68b445d1a48ed242f18d2bafb20ed",  # Preserve the verified PT_02 BEFORE 22-point registration identity.
    ("after", "PT_02"): "f77cc5998ca4e0d6a6eff03c3174cb3dd3ca3bddf8ddd9a7166cee2cec6f64b6",  # Preserve the independently frozen PT_02 AFTER 22-point registration identity.
}  # Finish the frozen field-point SHA-256 mapping.

VALID_PT02_CONFIDENCE = {"high", "medium", "low"}  # Freeze the only permitted spatial-registration confidence labels for PT_02.

def sha256_file(path):  # Define a reusable helper that calculates the SHA-256 identity of one research artifact.
    digest = hashlib.sha256()  # Create a fresh SHA-256 calculator for the requested file.
    with path.open("rb") as input_file:  # Open the research artifact in binary mode without modifying it.
        for chunk in iter(lambda: input_file.read(1024 * 1024), b""):  # Read the file in one-megabyte chunks so large imagery does not need to be loaded only for hashing.
            digest.update(chunk)  # Add each binary chunk to the running SHA-256 calculation.
    return digest.hexdigest()  # Return the completed immutable file identifier.

parser = argparse.ArgumentParser()  # Create the command-line parser for the generalized B3 field-guided experiment.
parser.add_argument("condition", choices=["before", "after"])  # Require the caller to explicitly select the BEFORE or AFTER experimental condition.
parser.add_argument("image_stem", choices=["PT_R1", "PT_02"], nargs="?", default="PT_R1")  # Allow PT_R1 or PT_02 while preserving the old PT_R1-only command form as the default.
args = parser.parse_args()  # Parse the requested B3 condition and scene before any research artifact is loaded.

experiment_key = (args.condition, args.image_stem)  # Combine condition and scene into the stable lookup key used by frozen provenance tables.
expected_ids = EXPECTED_IDS[args.image_stem]  # Read the exact identifier sequence required for the selected B3 scene.
id_column = ID_COLUMNS[args.image_stem]  # Read the identifier column expected in the selected scene's committed CSV.
expected_registration_method = EXPECTED_REGISTRATION_METHODS[args.image_stem]  # Read the only permitted registration provenance label for the selected scene.

assert experiment_key in EXPECTED_FIELD_POINTS_SHA256, f"No frozen field-point SHA-256 is configured for {args.image_stem} {args.condition}. Create, commit, hash, and freeze that annotation before inference."  # Block any scene-condition combination whose point-registration artifact has not been explicitly frozen before inference.

native_path = Path("data/raw/experiment_001") / args.condition / f"{args.image_stem}.JPG"  # Locate the untouched native standardized RGB image that SAM2 will segment.
field_points_path = Path("data/annotations/experiment_001/b3_field_points") / args.condition / args.image_stem / f"{args.image_stem}_{args.condition}_field_points.csv"  # Locate the exact committed scene-specific point-registration CSV used as the B3 prompt source.
output_dir = Path("outputs/sam2/experiment_001/b3_field_points") / args.condition / args.image_stem  # Define the ignored B3 output directory for the selected scene and condition.
output_dir.mkdir(parents=True, exist_ok=True)  # Create the ignored B3 output directory without modifying any tracked research input.
output_path = output_dir / f"{args.image_stem}_sam2_field_point_masks.json"  # Define the machine-readable output file that will preserve one SAM2 mask per frozen registration point.

assert CHECKPOINT_PATH.exists(), f"SAM2 checkpoint not found: {CHECKPOINT_PATH}"  # Stop immediately if the frozen model checkpoint is unavailable.
assert native_path.exists(), f"Native image not found: {native_path}"  # Stop immediately if the standardized native image is unavailable.
assert field_points_path.exists(), f"Field-point CSV not found: {field_points_path}"  # Stop immediately if the committed point-registration artifact is unavailable.
assert not output_path.exists(), f"B3 output already exists and will not be overwritten: {output_path}"  # Protect any completed B3 prediction artifact from accidental reruns or replacement.

checkpoint_sha256 = sha256_file(CHECKPOINT_PATH)  # Calculate the SHA-256 identity of the local SAM2 checkpoint before model loading.
native_sha256 = sha256_file(native_path)  # Calculate the SHA-256 identity of the untouched standardized native RGB image.
field_points_sha256 = sha256_file(field_points_path)  # Calculate the SHA-256 identity of the exact committed point-registration CSV.

assert checkpoint_sha256 == CHECKPOINT_SHA256, f"SAM2 checkpoint SHA-256 mismatch: {checkpoint_sha256}"  # Stop immediately if the SAM2 checkpoint differs from the frozen Phase B model artifact.
assert native_sha256 == EXPECTED_NATIVE_SHA256[experiment_key], f"Native image SHA-256 mismatch: {native_sha256}"  # Stop immediately if the selected image differs from the previously frozen standardized research input.
assert field_points_sha256 == EXPECTED_FIELD_POINTS_SHA256[experiment_key], f"Field-point CSV SHA-256 mismatch: {field_points_sha256}"  # Stop immediately if the selected point table differs from the committed pre-inference registration artifact.

with Image.open(native_path) as native_source_image:  # Open the untouched standardized JPEG that SAM2 will segment.
    assert native_source_image.size == (NATIVE_WIDTH, NATIVE_HEIGHT), f"Unexpected native image size: {native_source_image.size}"  # Stop if the image coordinate space differs from the verified 8192 by 6144 dimensions.
    image = np.array(native_source_image.convert("RGB"))  # Convert the untouched native image into the HWC uint8 RGB array expected by Meta's SAM2 predictor.

with field_points_path.open("r", encoding="utf-8", newline="") as csv_file:  # Open the frozen scene-specific point-registration table without modifying it.
    reader = csv.DictReader(csv_file)  # Create a dictionary-based CSV reader so annotation fields can be validated by name.
    field_names = reader.fieldnames or []  # Preserve the CSV header names while safely handling a malformed file with no header.
    field_rows = list(reader)  # Read every committed registration record in its frozen CSV order.

required_columns = {"condition", "image_stem", "image_filename", "native_width", "native_height", "x", "y", "registration_method", id_column}  # Define the fields required for every scene-specific B3 registration table.
if args.image_stem == "PT_02":  # Check whether the lower-spatial-certainty PT_02 scene is being processed.
    required_columns.add("registration_confidence")  # Require explicit high, medium, or low registration confidence for every PT_02 point.
missing_columns = required_columns.difference(field_names)  # Determine whether any required annotation fields are absent from the committed CSV.
assert not missing_columns, f"Missing required field-point columns: {sorted(missing_columns)}"  # Stop if the committed prompt table does not contain the complete required schema.

assert len(field_rows) == len(expected_ids), f"Unexpected field-point count for {args.image_stem}: {len(field_rows)}"  # Stop if the prompt table does not contain exactly the expected number of registrations.

if args.image_stem == "PT_R1":  # Check whether the original field-confirmed PT_R1 scene is being processed.
    observed_ids = [int(row[id_column]) for row in field_rows]  # Read PT_R1 physical tree IDs as integers in their committed registration order.
else:  # Handle the neutral identifier schema used by PT_02.
    observed_ids = [row[id_column] for row in field_rows]  # Read PT_02 neutral registration IDs as strings in their committed registration order.

assert observed_ids == expected_ids, f"Unexpected registration ID sequence for {args.image_stem}: {observed_ids}"  # Stop if any expected point is missing, duplicated, reordered, or replaced.

for row in field_rows:  # Validate every committed point-registration record before loading the SAM2 model.
    identifier = int(row[id_column]) if args.image_stem == "PT_R1" else row[id_column]  # Read the physical PT_R1 tree ID or neutral PT_02 registration ID using the correct data type.
    assert row["condition"] == args.condition, f"Condition mismatch for {identifier}: {row['condition']}"  # Stop if a row belongs to the wrong BEFORE or AFTER condition.
    assert row["image_stem"] == args.image_stem, f"Image stem mismatch for {identifier}: {row['image_stem']}"  # Stop if a registration references a different study scene.
    assert row["image_filename"] == f"{args.image_stem}.JPG", f"Image filename mismatch for {identifier}: {row['image_filename']}"  # Stop if the registration references a different standardized image filename.
    assert int(row["native_width"]) == NATIVE_WIDTH, f"Native width mismatch for {identifier}: {row['native_width']}"  # Stop if the registered horizontal coordinate space differs from the native image.
    assert int(row["native_height"]) == NATIVE_HEIGHT, f"Native height mismatch for {identifier}: {row['native_height']}"  # Stop if the registered vertical coordinate space differs from the native image.
    assert row["registration_method"] == expected_registration_method, f"Registration method mismatch for {identifier}: {row['registration_method']}"  # Stop if the row does not use the frozen scene-specific registration protocol.
    assert 0 <= int(row["x"]) < NATIVE_WIDTH, f"Invalid x coordinate for {identifier}: {row['x']}"  # Stop if a positive point falls outside the native image horizontally.
    assert 0 <= int(row["y"]) < NATIVE_HEIGHT, f"Invalid y coordinate for {identifier}: {row['y']}"  # Stop if a positive point falls outside the native image vertically.
    if args.image_stem == "PT_02":  # Apply additional uncertainty-provenance validation only to PT_02.
        assert row["registration_confidence"] in VALID_PT02_CONFIDENCE, f"Invalid registration confidence for {identifier}: {row['registration_confidence']}"  # Stop unless PT_02 confidence is explicitly high, medium, or low.

confidence_counts = {"not_applicable": len(field_rows)}  # Initialize PT_R1 confidence metadata without retroactively assigning confidence to the original PT_R1 registrations.
if args.image_stem == "PT_02":  # Check whether explicit PT_02 spatial-confidence metadata is available.
    confidence_counts = {level: sum(row["registration_confidence"] == level for row in field_rows) for level in ["high", "medium", "low"]}  # Count the frozen PT_02 high, medium, and low registration-confidence labels.

model = build_sam2(MODEL_CONFIG, CHECKPOINT_PATH, device="cuda", apply_postprocessing=False)  # Build the same pinned SAM2.1 Base+ model without additional postprocessing.
predictor = SAM2ImagePredictor(model)  # Create Meta's official single-image prompt predictor for repeated frozen positive point prompts.

torch.cuda.reset_peak_memory_stats()  # Reset peak GPU-memory accounting immediately before B3 image embedding and point-guided inference.
start_time = time.perf_counter()  # Record wall-clock start time immediately before SAM2 processes the selected research image.
results = []  # Create the list that will preserve one SAM2 result for every frozen scene-specific registration point.

with torch.inference_mode():  # Disable gradient calculation because B3 is frozen pretrained inference only.
    with torch.autocast("cuda", dtype=torch.bfloat16):  # Use the same GPU bfloat16 inference precision used in the earlier frozen SAM2 baselines.
        predictor.set_image(image)  # Compute the SAM2 image embedding once so all frozen point prompts reuse the same native-image representation.
        for row in field_rows:  # Process every registered location exactly once and in the committed CSV order.
            identifier = int(row[id_column]) if args.image_stem == "PT_R1" else row[id_column]  # Read the scene-appropriate physical tree ID or neutral registration ID.
            point_x = float(row["x"])  # Read the frozen native-image x coordinate for this registration.
            point_y = float(row["y"])  # Read the frozen native-image y coordinate for this registration.
            registration_confidence = row["registration_confidence"] if args.image_stem == "PT_02" else "not_applicable"  # Preserve explicit PT_02 spatial confidence without retroactively modifying PT_R1 provenance.
            point_coords = np.array([[point_x, point_y]], dtype=np.float32)  # Create the single positive native-image point prompt expected by Meta's SAM2 predictor.
            point_labels = np.array([1], dtype=np.int32)  # Label the single frozen registration point as a positive foreground prompt.
            masks, iou_scores, _ = predictor.predict(point_coords=point_coords, point_labels=point_labels, multimask_output=False, return_logits=False, normalize_coords=True)  # Generate exactly one binary SAM2 mask from one frozen positive point without boxes, negative points, or candidate-mask selection.
            mask = masks[0]  # Select the single returned mask because the B3 protocol freezes multimask output to false.
            mask_tensor = torch.from_numpy(mask).to(torch.bool).unsqueeze(0)  # Convert the binary mask into the batch-shaped Boolean tensor required by Meta's official RLE encoder.
            segmentation_rle = mask_to_rle_pytorch(mask_tensor)[0]  # Encode the complete native-resolution SAM2 mask losslessly using Meta's official uncompressed RLE representation.
            result_record = {"registration_id": identifier, "native_point_xy": [point_x, point_y], "point_label": 1, "registration_method": row["registration_method"], "registration_confidence": registration_confidence, "sam2_predicted_iou": float(iou_scores[0]), "segmentation": segmentation_rle, "area": int(area_from_rle(segmentation_rle))}  # Preserve the frozen point provenance, SAM2 internal quality estimate, complete mask geometry, and mask area without manual alteration.
            if args.image_stem == "PT_R1":  # Preserve the original PT_R1 physical-tree field for backward interpretability.
                result_record["tree_id"] = identifier  # Store the PT_R1 physical field tree ID alongside the generalized registration identifier.
            results.append(result_record)  # Add this untouched one-point-to-one-mask result to the complete B3 prediction record.

elapsed_seconds = time.perf_counter() - start_time  # Calculate total B3 image-embedding plus point-prompt inference duration.
peak_gpu_memory_mb = torch.cuda.max_memory_allocated() / (1024 ** 2)  # Record the maximum PyTorch GPU allocation observed during the complete B3 run.

payload = {"phase": "B3", "method": OUTPUT_METHODS[args.image_stem], "condition": args.condition, "image_stem": args.image_stem, "native_image_path": str(native_path), "native_image_sha256": native_sha256, "native_image_width": NATIVE_WIDTH, "native_image_height": NATIVE_HEIGHT, "field_points_path": str(field_points_path), "field_points_sha256": field_points_sha256, "registration_ids": observed_ids, "registration_id_column": id_column, "registration_method": expected_registration_method, "registration_confidence_recorded": args.image_stem == "PT_02", "registration_confidence_counts": confidence_counts, "field_point_count": len(field_rows), "sam2_mask_count": len(results), "model_config": MODEL_CONFIG, "checkpoint_path": str(CHECKPOINT_PATH), "checkpoint_sha256": checkpoint_sha256, "sam2_source_commit": SAM2_SOURCE_COMMIT, "torch_version": torch.__version__, "torch_cuda_version": torch.version.cuda, "gpu": torch.cuda.get_device_name(0), "prompt_type": "single_positive_point", "positive_points_per_registration": 1, "negative_points_per_registration": 0, "box_prompts_used": False, "multimask_output": False, "manual_mask_selection": False, "post_inference_prompt_adjustment": False, "apply_postprocessing": False, "elapsed_seconds": elapsed_seconds, "peak_gpu_memory_mb": peak_gpu_memory_mb, "masks": results}  # Assemble complete scene-specific B3 provenance, uncertainty metadata, frozen prompt rules, runtime metadata, and one-to-one registration-to-SAM2 mask records.

if args.image_stem == "PT_R1":  # Preserve the original PT_R1 field-tree metadata key for compatibility with the completed PT_R1 experiment record.
    payload["field_tree_ids"] = observed_ids  # Record the nine physical PT_R1 tree IDs under the original B3 metadata name.

with output_path.open("w", encoding="utf-8") as output_file:  # Open the ignored scene-specific B3 machine-readable output path for writing.
    json.dump(payload, output_file, indent=2)  # Save every point-guided SAM2 prediction without manual filtering, selection, or truth-informed alteration.

print(f"Native input: {native_path}")  # Report the exact untouched standardized RGB image supplied to SAM2.
print(f"Native SHA-256: {native_sha256}")  # Report the immutable identity of the standardized native research image.
print(f"Field points: {field_points_path}")  # Report the exact committed point-registration table used for B3 prompts.
print(f"Field points SHA-256: {field_points_sha256}")  # Report the immutable identity of the frozen point-registration table.
print(f"Registration IDs: {observed_ids}")  # Report the complete frozen scene-specific identifier sequence consumed by B3.
print(f"Registration method: {expected_registration_method}")  # Report whether the run uses field-confirmed or field-count-constrained manual registration.
print(f"Registration confidence counts: {confidence_counts}")  # Report the explicit PT_02 uncertainty distribution or PT_R1 not-applicable count.
print(f"Positive point prompts: {len(field_rows)}")  # Report the exact number of positive point prompts supplied to SAM2.
print(f"SAM2 masks: {len(results)}")  # Report the resulting mask count so the expected one-to-one mapping is immediately visible.
print(f"Elapsed seconds: {elapsed_seconds:.2f}")  # Report total wall-clock B3 inference duration.
print(f"Peak GPU memory MB: {peak_gpu_memory_mb:.2f}")  # Report peak allocated GPU memory during the complete B3 run.
print(f"Output: {output_path}")  # Report the machine-readable B3 prediction location.