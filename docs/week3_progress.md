# Week 3 Benchmark Progress

## Input Images

- PT_R1 BEFORE SHA-256: `6f9b0c5d0f65bc9201153eb7ff4460cf620cbc7842a51df090e633d249bde9c9`
- PT_R1 AFTER SHA-256: `18e0835a58da6a97601bec1db088f8f611f1b26d5e7fdc4b711ba56999e4f393`
- PT_02 BEFORE SHA-256: `fbb8a74a05c2e8730fb9bed565b9935ff6256e276fb791ed66660f3f9ee98a98`
- PT_02 AFTER SHA-256: `d93ac2b2d5f76169790fe78563ee08436de237e04b1fb9b1027a3dd19f047aef`

## M01 DeepForest Native

| Image | Detections | Prediction CSV SHA-256 |
| --- | ---: | --- |
| PT_R1 BEFORE | 3013 | `54ed2c5d7c08669bcc358a53f2bb0d4bcd112598dffaa454db16c57e3ce4c413` |
| PT_R1 AFTER | 3949 | `df38cad3f1138a1ece57ebeec54cc87eb6c3f349882483595ca13695c4f6159d` |
| PT_02 BEFORE | 4002 | `58f9c736dc417e806f378b20836223b274e541147603d86652b229b01e1dc547` |
| PT_02 AFTER | 5545 | `fa9f8568707f6b27a9cfd0147be6e866ed7d6b7b91323589be025b92b221b3f8` |

## M02 DeepForest GSD-Corrected

Target deployment GSD: `7.89 cm/pixel`.

| Image | Detections | Prediction CSV SHA-256 |
| --- | ---: | --- |
| PT_R1 BEFORE | 273 | `68a26e6ed4ff71c00272fc56d25673aa0d414876310c180ff9a820380564a37d` |
| PT_R1 AFTER | 319 | `c37a5befc46708877a2e9e3992bfaa8da2923ba9e490c391db5735fec746937b` |
| PT_02 BEFORE | 373 | `7489266b9fc62ba55ae0bcc66664c1d16eab3f64309e95d5d918ba09865a5aeb` |
| PT_02 AFTER | 427 | `0d5ad474d3779bd52a1dcdaf0132ed85f48c414f1265ed6c000000aad2591d58` |

## M03 TreeCountSegHeight

Preprocessing and inference are complete for all four Week 3 images.

- Native GSD assumption: `1.67 cm/pixel`
- Target GSD: `20.00 cm/pixel`
- Output dimensions: `684 x 513`
- Resampling: Lanczos
- Format: three-band RGB TIFF
- Docker image: `sizhuoli/tree_expert@sha256:fab4a8e16d7bc085440724c9fa522c957dc04299c625fcab7617b87c1c154e13`
- Model checkpoint: `trees_20210620-0202_Adam_e4_redgreenblue_256_84_frames_weightmapTversky_MSE100_5weight_attUNet.h5`
- Checkpoint SHA-256: `abce53345b8159aeda49dce7db32a0806ee90970593e7d2a1fe88d1f133ac843`
- Count interpretation: continuous sum of the model density raster
- Counts remain fractional and are not rounded
- These are density-estimated counts, not independently localized tree instances

### Derived Inputs

| Image | Derived TIFF SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `63e0cf4a8ae848b09905e36357e81c7b4e27baa30f6d044c286a87f985d2affb` |
| PT_R1 AFTER | `cbf3844bb67ee5cf083f61cdaa4d576924529bd342d1e2be8b21d41c64373f46` |
| PT_02 BEFORE | `fade86a8e5f95e1f6f6712faf0ae2a96fa68f23dd92a9c586e896141558764e7` |
| PT_02 AFTER | `4edc99267737a0a1a95b19aa85723398a6b67e97824ad856769c1962ad2a975e` |

### Continuous Predicted Counts

| Image | Density-Sum Count |
| --- | ---: |
| PT_R1 BEFORE | `2.7866833359` |
| PT_R1 AFTER | `4.6561581232` |
| PT_02 BEFORE | `0.3150038328` |
| PT_02 AFTER | `3.4307784382` |

### Raw Prediction TIFF Hashes

| Image | Artifact | SHA-256 |
| --- | --- | --- |
| PT_R1 BEFORE | density | `bafe61eb22b91af8944771c8310e9937ff17bfaa0d71945ea0d99f3a377d6195` |
| PT_R1 BEFORE | segmentation | `3be9dc553c87ee4324142ba6eea31ed27a1cb974554d55f52515d78ad66a5cfd` |
| PT_R1 AFTER | density | `09082df97f4a87f75c854230a1c2a228cd4ee1d6838b409ad2d6de9732c02a51` |
| PT_R1 AFTER | segmentation | `f765c4f2cf4136c25fb3bc4586406d71de1391d243ed918b3cdc7c9a0af2ddbf` |
| PT_02 BEFORE | density | `0518c9aabffc61d8937f742476c342e12e243c0769acba596cd0b6c494bcbf41` |
| PT_02 BEFORE | segmentation | `95f2ef9259d1b8d8dba61c6937ea4b940fc4a142c573001876100014dd9b40fe` |
| PT_02 AFTER | density | `b2c01577ffd883597718022fe973b03020726ab8c2683eae780634b175d3ab75` |
| PT_02 AFTER | segmentation | `58aa52a30f19d5233db92826ffca7fb8c1c8ce5a9771bde6d7c1c9e5b8e1d49a` |

### Visualization PNG Hashes

| Image | Artifact | SHA-256 |
| --- | --- | --- |
| PT_R1 BEFORE | density | `a518ee5b71cedf069df178714deeaf2909576441a51530055a78b098760ec068` |
| PT_R1 BEFORE | overlay | `4b16afdad50afbce0c5bb7a603478b6617ff6d58f91fd269c71f2a940ed02db1` |
| PT_R1 BEFORE | segmentation | `390887671600a74b32af8b963dd1b06841bc1b63bb645c061359ace77019d68a` |
| PT_R1 AFTER | density | `49896ba254c4b0f817ed3c6692d450388519ec53d435a625c5a9d2f182046031` |
| PT_R1 AFTER | overlay | `b4bddb08fd3b0dd4be23f90364fe2688ef90caf43771085c53415c85ad5a6605` |
| PT_R1 AFTER | segmentation | `855ca9e70c2b90529e32d720b37ddc006fa3197befa8e06ed9e7d8fbcaaf47b0` |
| PT_02 BEFORE | density | `32f681625cc7b523ca3ee69da7858386c48645b0af7504df9f1c13a3c2977550` |
| PT_02 BEFORE | overlay | `a32654f1c183681196afb126efd6c67740aeefd029cd327147c1b6a193030bb6` |
| PT_02 BEFORE | segmentation | `37fbe0f9a88df44fd2e66b62e85fe095de6bf3207f87747e174fd7989f2f60ba` |
| PT_02 AFTER | density | `4761b043b52917b9ed2f2912e831da1e2734804ddf34ed5f9d46c72a48bc667a` |
| PT_02 AFTER | overlay | `c052efd687a1bb41f65a9c7bea697cc53cf257010e44d01fe97462e004360f04` |
| PT_02 AFTER | segmentation | `91b38c4b6d80c2f8d037701ab14c5f664be75c8c443a41fff606d2d503ca29e5` |

Useful M03 outputs and visualization artifacts were mirrored to the Windows repository after generation.

## M04 SAM2 Automatic

Inference and visualization are complete for all four Week 3 standardized RGB images.

- Model: SAM 2.1 Hiera Base+
- Model config: `configs/sam2.1/sam2.1_hiera_b+.yaml`
- Checkpoint: `models/sam2/checkpoints/sam2.1_hiera_base_plus.pt`
- Checkpoint SHA-256: `a2345aede8715ab1d5d31b4a509fb160c5a4af1970f199d9054ccfb746c004c5`
- SAM2 source commit: `2b90b9f5ceec907a1c18123530e92e794ad901a4`
- Full-resolution input: `8192 x 6144`
- `points_per_side=32`
- `points_per_batch=4`
- `pred_iou_thresh=0.8`
- `stability_score_thresh=0.95`
- `stability_score_offset=1.0`
- `mask_threshold=0.0`
- `box_nms_thresh=0.7`
- `crop_n_layers=0`
- `crop_nms_thresh=0.7`
- `crop_overlap_ratio=512/1500`
- `crop_n_points_downscale_factor=1`
- `min_mask_region_area=0`
- `output_mode=uncompressed_rle`
- `use_m2m=False`
- `multimask_output=True`
- Automatic mask count is a segmentation-output quantity and is **not interpreted as tree count**.
- No tree-specific filtering or post-hoc tuning was performed.

### Automatic Mask Counts

| Image | Automatic Masks |
| --- | ---: |
| PT_R1 BEFORE | 106 |
| PT_R1 AFTER | 102 |
| PT_02 BEFORE | 86 |
| PT_02 AFTER | 96 |

### Prediction JSON Hashes

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `9cf83ec63694402a1e7cac02d591e22c0660189dc58739eeb2ced2bba3c6ae89` |
| PT_R1 AFTER | `7a4232a2057aa21de405980d0e8dc5624a880facfb9b6d58bc21333daae4de04` |
| PT_02 BEFORE | `8ab30531f0a9acdcdc75b08541dc20df96f52ede38217de1415ff071116e791b` |
| PT_02 AFTER | `dbd4b7c3a881f7270ae779267fdfae65f2e005c49418e5f5528fe6c9cfe964b7` |

### Visualization PNG Hashes

| Image | Artifact | SHA-256 |
| --- | --- | --- |
| PT_R1 BEFORE | boxes and points | `542a20f79eea9a047742c2d42457cecafa236e636b754fecba6945f2e6890caf` |
| PT_R1 BEFORE | overlay | `1de0ea2a851047247fb20ab9854fe8e27075d03a6a1985f0cedbc560d5d7e78c` |
| PT_R1 AFTER | boxes and points | `dafd7b8571530146aea4f88b73614b995ba29eff2282522acb816b053ac27ef0` |
| PT_R1 AFTER | overlay | `8fd650bfca90d965e392cad8d78a518d5f31fab47345b14d64424bc641f58527` |
| PT_02 BEFORE | boxes and points | `7a105f5b88d1c7efae3d67a51ae62a0325c8b4f453d538bf82484865a0474e9f` |
| PT_02 BEFORE | overlay | `59eb3fdcba95b59437ec5b4539cd03d9991f22f1e88b06094f995abd23cb09fc` |
| PT_02 AFTER | boxes and points | `91eb7fb5fa4c16cf9c119edbe147d0cdd63ec217585590d257075175157eb826` |
| PT_02 AFTER | overlay | `927aad8419a0449f1861b2612b01e90cd414f031dd9406030bf918973a246430` |

Useful M04 JSON predictions and visualization artifacts were mirrored to the Windows repository after generation.

## Exact Resume Point

M01, M02, M03, and M04 are complete for Week 3.

Next task:

1. Begin M05 DeepForest GSD-Corrected -> SAM2 on the four Week 3 standardized RGB images.
2. Reuse the frozen Week 3 M02 DeepForest predictions as the SAM2 box prompts.
3. Preserve the frozen Week 1 M05 SAM2 box-guided settings.
4. Treat M05 instance count as inherited from DeepForest, not an independent SAM2 tree count.
5. Retain all outputs without post-hoc tuning.
