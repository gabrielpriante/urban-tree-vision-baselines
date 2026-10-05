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
WEEK3_EXPECTED_COUNTS = {("before", "PT_R1"): 273, ("after", "PT_R1"): 319, ("before", "PT_02"): 373, ("after", "PT_02"): 427}  # Freeze the verified Week 3 DeepForest box-prompt counts inherited directly from M02.
WEEK3_EXPECTED_NATIVE_SHA256 = {("before", "PT_R1"): "6f9b0c5d0f65bc9201153eb7ff4460cf620cbc7842a51df090e633d249bde9c9", ("after", "PT_R1"): "18e0835a58da6a97601bec1db088f8f611f1b26d5e7fdc4b711ba56999e4f393", ("before", "PT_02"): "fbb8a74a05c2e8730fb9bed565b9935ff6256e276fb791ed66660f3f9ee98a98", ("after", "PT_02"): "d93ac2b2d5f76169790fe78563ee08436de237e04b1fb9b1027a3dd19f047aef"}  # Freeze the verified Week 3 native standardized JPEG identities.
WEEK3_EXPECTED_DEEPFOREST_IMAGE_SHA256 = {("before", "PT_R1"): "143546831abdca0b8d6a1acd4b65665732dc37a16644a6b42e8660f9cabb4f98", ("after", "PT_R1"): "18ad779cdf7ef36e3125b28e3fd356b4ef235ffcef8f907007b5f699ef1c6c64", ("before", "PT_02"): "4c42688acb21cb724a8b661db94e636fea7b4d5414ee807bb594cefc71ae3b17", ("after", "PT_02"): "3765303bcec2ae9b4f9840d1faf5c1b08cdd58f649d061eae328cf1af816f9bb"}  # Freeze the verified Week 3 7.89 cm DeepForest input-image identities.
WEEK3_EXPECTED_DEEPFOREST_CSV_SHA256 = {("before", "PT_R1"): "68a26e6ed4ff71c00272fc56d25673aa0d414876310c180ff9a820380564a37d", ("after", "PT_R1"): "c37a5befc46708877a2e9e3992bfaa8da2923ba9e490c391db5735fec746937b", ("before", "PT_02"): "7489266b9fc62ba55ae0bcc66664c1d16eab3f64309e95d5d918ba09865a5aeb", ("after", "PT_02"): "0d5ad474d3779bd52a1dcdaf0132ed85f48c414f1265ed6c000000aad2591d58"}  # Freeze the verified Week 3 M02 prediction-table identities used as M05 prompts.
WEEK4_EXPECTED_COUNTS = {("before", "PT_R1"): 350, ("after", "PT_R1"): 365, ("before", "PT_02"): 450, ("after", "PT_02"): 478}  # Freeze the verified Week 4 DeepForest box-prompt counts inherited directly from M02.
WEEK4_EXPECTED_NATIVE_SHA256 = {("before", "PT_R1"): "5765eb41ab89c9427141ab27e0e6cfd4feb53e4798ea7af68bf4824a8c7be273", ("after", "PT_R1"): "4fc3d22c3cd837e22828edf13b7556f6fe0def37403b7e950354eab8b0702fdf", ("before", "PT_02"): "75358d8e3144029cee679b2996575d785cb1acb1aa5ab148b9ad5eaf62848429", ("after", "PT_02"): "0cebef67412b933da8c13e66aa75b7a020c957e7403306859f804cf927c12549"}  # Freeze the verified Week 4 native standardized JPEG identities.
WEEK4_EXPECTED_DEEPFOREST_IMAGE_SHA256 = {("before", "PT_R1"): "d774206227add179b1a18f12a4ad5ddb7a1fbbc1b7d7d4db86bfeec7d0e821ee", ("after", "PT_R1"): "0ad4f6b3c4dad1e1280229c9d83936fb6be68338f2f445043be1602bc83fc277", ("before", "PT_02"): "f97bfe06c820d692dd0f2df5651c9f7fcad08b7997263c062cd4b0ba6005f9db", ("after", "PT_02"): "c7e98c8a49871aab7de61fda5ab17d9d4fa9b667c94b89f2b753f23921113c04"}  # Freeze the verified Week 4 7.89 cm DeepForest input-image identities.
WEEK4_EXPECTED_DEEPFOREST_CSV_SHA256 = {("before", "PT_R1"): "b79514ce8b493472ce6715edd632bf8bf94bf59f533feb6dfae55641410b0400", ("after", "PT_R1"): "1f2d33ccd21088ea7cf48c7bc312a1ebc9f33649037ef43102e3cc69e2bd6096", ("before", "PT_02"): "65ff4c615f16ec62832197d4bddfcacadb558f9060c36856d03f8844f26ea897", ("after", "PT_02"): "ba4144199e0d46f4079c64a0ed1930f825d1d4cc768cd1dc09d46b86e5ff0c8a"}  # Freeze the verified Week 4 M02 prediction-table identities used as M05 prompts.
WEEK5_EXPECTED_COUNTS = {("before", "PT_R1"): 447, ("after", "PT_R1"): 376, ("before", "PT_02"): 503, ("after", "PT_02"): 452}  # Freeze the verified Week 5 DeepForest M02 box-prompt counts.
WEEK5_EXPECTED_NATIVE_SHA256 = {("before", "PT_R1"): "470aea6de65e91ea87b69a444c649f80566bc6cd4d8ca72c52c224bbdab827ec", ("after", "PT_R1"): "ad6160e8599e79ab9cda58b7798c91e95399ba4f6f0a4a1585dd54c80016fd45", ("before", "PT_02"): "d5ca1a50522c5c94a1444370c6ab0f3f7c2f5868680a8c334fc0a2dec3c7a16e", ("after", "PT_02"): "73beab517719ab3f88fd80b326ff077adf32aad7c5bdaae4ac208a0c7060e218"}  # Freeze the verified Week 5 native standardized JPEG identities.
WEEK5_EXPECTED_DEEPFOREST_IMAGE_SHA256 = {("before", "PT_R1"): "e1d43d5466c9439ba5ad35b98915ced077254b96194fdbec8151369863a687e3", ("after", "PT_R1"): "0dd5273afb164dd11db04ff0fdff5699f883efb0c1d2bbc9bae63db193908d65", ("before", "PT_02"): "1ce7e179c7ba5089b3342ea6a30895f5cb0692331db1cb0ec6a35f875164131f", ("after", "PT_02"): "2052eb89f43de725c66f2dfd7d5f5161707ff28db125862716279a1e948bbc31"}  # Freeze the verified Week 5 7.89 cm DeepForest input-image identities.
WEEK5_EXPECTED_DEEPFOREST_CSV_SHA256 = {("before", "PT_R1"): "4356c06a649f3200165f8e0d615f79dabad847de21887ef436e7e5e00a446821", ("after", "PT_R1"): "a10d2390b6a70443af66fdadad500c4fb452c567c63b509866c9bd0c7bec8ec3", ("before", "PT_02"): "c6537358e312076fc04bc1a5bb844b0eb26b627277705d40d31c310675764fea", ("after", "PT_02"): "bc201e4316dcec0c016151f41b294bba733936efdf38d0ff2e990bbe75967a4e"}  # Freeze the verified Week 5 M02 prediction-table identities used as M05 prompts.
def sha256_file(path):  # Define a small helper that calculates the SHA-256 identity of one input artifact.
    digest = hashlib.sha256()  # Create a fresh SHA-256 calculator for this file.
    with path.open("rb") as input_file:  # Open the file in binary mode without modifying it.
        for chunk in iter(lambda: input_file.read(1024 * 1024), b""):  # Read the file in one-megabyte chunks so large images do not need to be loaded solely for hashing.
            digest.update(chunk)  # Add each binary chunk to the running SHA-256 calculation.
    return digest.hexdigest()  # Return the completed immutable file identifier.
parser = argparse.ArgumentParser()  # Create the command-line parser for the frozen B2 experiment.
parser.add_argument("condition", choices=["before", "after"])  # Require the caller to identify the before or after experimental condition.
parser.add_argument("image_stem", choices=["PT_R1", "PT_02"])  # Require the caller to identify one of the two standardized scene images.
parser.add_argument("run_label", nargs="?", default=None)  # Accept an optional repeated-collection label such as week3 while preserving original Week 1 behavior when omitted.
args = parser.parse_args()  # Parse the requested B2 image before loading any research artifact.
key = (args.condition, args.image_stem)  # Create the condition-image key used by the frozen provenance dictionaries.
if args.run_label not in (None, "week3", "week4", "week5"):  # Restrict M05 to collection periods whose provenance has been explicitly frozen.
    raise SystemExit(f"Unsupported run label: {args.run_label}")  # Stop rather than silently using provenance from the wrong collection period.
if args.run_label == "week3":  # Select the already-frozen Week 3 provenance when Week 3 is explicitly requested.
    expected_counts = WEEK3_EXPECTED_COUNTS  # Use the frozen Week 3 DeepForest prompt counts.
    expected_native_sha256 = WEEK3_EXPECTED_NATIVE_SHA256  # Use the frozen Week 3 native-image identities.
    expected_deepforest_image_sha256 = WEEK3_EXPECTED_DEEPFOREST_IMAGE_SHA256  # Use the frozen Week 3 corrected-GSD image identities.
    expected_deepforest_csv_sha256 = WEEK3_EXPECTED_DEEPFOREST_CSV_SHA256  # Use the frozen Week 3 M02 prediction-table identities.
elif args.run_label == "week4":  # Select the newly frozen Week 4 provenance when Week 4 is explicitly requested.
    expected_counts = WEEK4_EXPECTED_COUNTS  # Use the frozen Week 4 DeepForest prompt counts.
    expected_native_sha256 = WEEK4_EXPECTED_NATIVE_SHA256  # Use the frozen Week 4 native-image identities.
    expected_deepforest_image_sha256 = WEEK4_EXPECTED_DEEPFOREST_IMAGE_SHA256  # Use the frozen Week 4 corrected-GSD image identities.
    expected_deepforest_csv_sha256 = WEEK4_EXPECTED_DEEPFOREST_CSV_SHA256  # Use the frozen Week 4 M02 prediction-table identities.
elif args.run_label == "week5":  # Select the frozen Week 5 provenance when Week 5 is explicitly requested.
    expected_counts = WEEK5_EXPECTED_COUNTS  # Use the frozen Week 5 DeepForest prompt counts.
    expected_native_sha256 = WEEK5_EXPECTED_NATIVE_SHA256  # Use the frozen Week 5 native-image identities.
    expected_deepforest_image_sha256 = WEEK5_EXPECTED_DEEPFOREST_IMAGE_SHA256  # Use the frozen Week 5 corrected-GSD image identities.
    expected_deepforest_csv_sha256 = WEEK5_EXPECTED_DEEPFOREST_CSV_SHA256  # Use the frozen Week 5 M02 prediction-table identities.
else:  # Preserve the original unlabeled Week 1 benchmark behavior.
    expected_counts = EXPECTED_COUNTS  # Use the original Week 1 DeepForest prompt counts.
    expected_native_sha256 = EXPECTED_NATIVE_SHA256  # Use the original Week 1 native-image identities.
    expected_deepforest_image_sha256 = EXPECTED_DEEPFOREST_IMAGE_SHA256  # Use the original Week 1 corrected-GSD image identities.
    expected_deepforest_csv_sha256 = EXPECTED_DEEPFOREST_CSV_SHA256  # Use the original Week 1 M02 prediction-table identities.
native_root = Path("data/raw/experiment_001")  # Define the root containing untouched standardized RGB benchmark images.
deepforest_image_root = Path("data/derived/experiment_001/gsd_7.89")  # Define the root containing frozen 7.89 cm DeepForest input images.
deepforest_csv_root = Path("outputs/experiment_001/deepforest/gsd_7.89")  # Define the root containing frozen M02 DeepForest prediction tables.
output_root = Path("outputs/sam2/experiment_001")  # Define the root containing SAM2 benchmark outputs.
if args.run_label is not None:  # Route repeated collections into their matching run-label directories while preserving unlabeled Week 1 behavior.
    native_root = native_root / args.run_label  # Route the untouched SAM2 RGB input to the requested collection period.
    deepforest_image_root = deepforest_image_root / args.run_label  # Route the corrected-GSD DeepForest image to the requested collection period.
    deepforest_csv_root = deepforest_csv_root / args.run_label  # Route the frozen M02 prompt table to the requested collection period.
    output_root = output_root / args.run_label  # Isolate M05 outputs inside the requested collection-period namespace.
native_path = native_root / args.condition / f"{args.image_stem}.JPG"  # Locate the untouched 8192 by 6144 RGB image that SAM2 will segment.
deepforest_image_path = deepforest_image_root / args.condition / f"{args.image_stem}.JPG"  # Locate the exact 1734 by 1300 image defining the DeepForest box coordinate space.
deepforest_csv_path = deepforest_csv_root / args.condition / f"{args.image_stem}_predictions.csv"  # Locate the exact frozen DeepForest M02 prediction table used as the M05 prompt source.
output_dir = output_root / "b2_deepforest_boxes" / args.condition / args.image_stem  # Define the isolated output directory for this exact M05 run.
output_dir.mkdir(parents=True, exist_ok=True)  # Create the ignored B2 output directory without modifying any input artifact.
output_path = output_dir / f"{args.image_stem}_sam2_deepforest_box_masks.json"  # Define the machine-readable file that will preserve every DeepForest-guided SAM 2 mask.
native_sha256 = sha256_file(native_path)  # Calculate the SHA-256 identity of the untouched native RGB image supplied to SAM 2.
deepforest_image_sha256 = sha256_file(deepforest_image_path)  # Calculate the SHA-256 identity of the exact 7.89 cm image used by DeepForest.
deepforest_csv_sha256 = sha256_file(deepforest_csv_path)  # Calculate the SHA-256 identity of the exact frozen DeepForest prediction table.
assert native_sha256 == expected_native_sha256[key], f"Native image SHA-256 mismatch: {native_sha256}"  # Stop immediately if the native image differs from the previously frozen research input.
assert deepforest_image_sha256 == expected_deepforest_image_sha256[key], f"DeepForest image SHA-256 mismatch: {deepforest_image_sha256}"  # Stop immediately if the 7.89 cm DeepForest source image differs from the frozen artifact.
assert deepforest_csv_sha256 == expected_deepforest_csv_sha256[key], f"DeepForest CSV SHA-256 mismatch: {deepforest_csv_sha256}"  # Stop immediately if the DeepForest prompt table differs from the frozen Phase A output.
with Image.open(deepforest_image_path) as deepforest_source_image:  # Open the 7.89 cm image only to verify the coordinate-space dimensions used by the frozen detector.
    assert deepforest_source_image.size == (DEEPFOREST_WIDTH, DEEPFOREST_HEIGHT), f"Unexpected DeepForest image size: {deepforest_source_image.size}"  # Stop if the actual DeepForest coordinate space differs from the verified 1734 by 1300 dimensions.
with native_path.open("rb"):  # Confirm that the untouched native image path is readable before loading the model.
    pass  # Perform no modification while completing the path-readability check.
with Image.open(native_path) as native_source_image:  # Open the untouched standardized JPEG that SAM 2 will segment.
    assert native_source_image.size == (NATIVE_WIDTH, NATIVE_HEIGHT), f"Unexpected native image size: {native_source_image.size}"  # Stop if the SAM 2 coordinate space differs from the verified 8192 by 6144 dimensions.
    image = np.array(native_source_image.convert("RGB"))  # Convert the untouched image into the HWC uint8 RGB array expected by Meta's SAM 2 predictor.
with deepforest_csv_path.open("r", encoding="utf-8", newline="") as csv_file:  # Open the frozen DeepForest prediction table without modifying it.
    deepforest_rows = list(csv.DictReader(csv_file))  # Read every frozen DeepForest detection in its original table order.
assert len(deepforest_rows) == expected_counts[key], f"Unexpected DeepForest detection count: {len(deepforest_rows)}"  # Stop if the number of box prompts differs from the count verified before B2 was written.
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
            mask_tensor = torch.from_numpy(mask).to(torch.bool).unsqueeze(0)  # Convert the single binary mask into the batch-shaped tensor expected by Meta's official RLE encoder.
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
