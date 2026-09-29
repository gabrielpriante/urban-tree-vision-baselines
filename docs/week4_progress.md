# Week 4 Benchmark Progress

## Benchmark Scope

- Balanced Week 4 set contains PT_R1 and PT_02, BEFORE and AFTER.
- Extra Week 4 PT_R1 orthomosaic is excluded from the repeated-imagery benchmark.
- Native standardized imagery is 8192 x 6144 RGB.
- No truth-informed tuning or post-hoc parameter adjustment is permitted.

## Frozen Native Week 4 Inputs

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `5765eb41ab89c9427141ab27e0e6cfd4feb53e4798ea7af68bf4824a8c7be273` |
| PT_R1 AFTER | `4fc3d22c3cd837e22828edf13b7556f6fe0def37403b7e950354eab8b0702fdf` |
| PT_02 BEFORE | `75358d8e3144029cee679b2996575d785cb1acb1aa5ab148b9ad5eaf62848429` |
| PT_02 AFTER | `0cebef67412b933da8c13e66aa75b7a020c957e7403306859f804cf927c12549` |

## M01 DeepForest Native

- Status: complete.
- Frozen model: `weecology/deepforest-tree` with DeepForest 2.1.0.
- Parameters: patch_size=400, overlap=0.05, IoU=0.15, score=0.10, NMS=0.05.

| Image | Detections |
| --- | ---: |
| PT_R1 BEFORE | 4289 |
| PT_R1 AFTER | 4851 |
| PT_02 BEFORE | 5436 |
| PT_02 AFTER | 6857 |

## M02 DeepForest GSD-Corrected

- Status: complete.
- Native GSD assumption: 1.67 cm/pixel.
- Target GSD: 7.89 cm/pixel.
- Derived dimensions: 1734 x 1300 RGB.

| Image | Detections |
| --- | ---: |
| PT_R1 BEFORE | 350 |
| PT_R1 AFTER | 365 |
| PT_02 BEFORE | 450 |
| PT_02 AFTER | 478 |

## M03 TreeCountSegHeight

- Status: complete.
- Native GSD assumption: 1.67 cm/pixel.
- Target GSD: 20.00 cm/pixel.
- Resize factor: 0.083500.
- Derived dimensions: 684 x 513 RGB TIFF.
- Resampling: Lanczos.
- Docker image: `sizhuoli/tree_expert@sha256:fab4a8e16d7bc085440724c9fa522c957dc04299c625fcab7617b87c1c154e13`.
- Model checkpoint: `trees_20210620-0202_Adam_e4_redgreenblue_256_84_frames_weightmapTversky_MSE100_5weight_attUNet.h5`.
- Checkpoint SHA-256: `abce53345b8159aeda49dce7db32a0806ee90970593e7d2a1fe88d1f133ac843`.
- Count interpretation: continuous sum of the predicted density raster.
- Counts remain fractional and are not rounded.
- These values are density-estimated counts, not independently localized tree instances.
- All four Docker runs completed with `Predicted 1 images.` and `Failed to predict 0 images.`.

### Derived Input Hashes

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `1b414cf9b2a3fe05d6442d9181b4f020a05886572f940ad50aa410743581eb1c` |
| PT_R1 AFTER | `06a0a396fa03e45cd32f07ce14c2da92147212534a58e8994243a68ece87e92e` |
| PT_02 BEFORE | `60567c4ae4b5ae4a11585841e3122911078d0a6e78424050b955d1874deae816` |
| PT_02 AFTER | `81e2b3a2e4da290638035d2981254b933c0577de20b72ed2c1d18ba1c1033670` |

### Continuous Predicted Counts

| Image | Density-Sum Count |
| --- | ---: |
| PT_R1 BEFORE | `6.9141701255` |
| PT_R1 AFTER | `10.2336220462` |
| PT_02 BEFORE | `12.5232079662` |
| PT_02 AFTER | `8.3929474838` |

### Raw Prediction TIFF Hashes

| Image | Artifact | SHA-256 |
| --- | --- | --- |
| PT_R1 BEFORE | density | `95e1ee98478e8dfbed3f27c5887738c43c36bd725fab2328fd51b0f1873c0ab6` |
| PT_R1 BEFORE | segmentation | `86a3b50329fca8d880e871d83d274e40576b25ffb362ab5e478ef53da5fe2dde` |
| PT_R1 AFTER | density | `aae9194023a9b839ca1e1e6d43cf6da0ac95912c87bda909fb458c12f61ac947` |
| PT_R1 AFTER | segmentation | `63f4d985c034d91d8e2f160d8c08ddc5897936fb6f00b4c21855a41a8fc85ceb` |
| PT_02 BEFORE | density | `11b5c329a131969c44be7545df416965bc0598113d5850b439d8cdded3f6fd51` |
| PT_02 BEFORE | segmentation | `d80208706392b8a16866746182ee3a09ae155698edb3ce15a0828f4c20f99a35` |
| PT_02 AFTER | density | `e588f7f530970e2424911a6bd33d58f72917ff438bacf936353ec1bfce982c03` |
| PT_02 AFTER | segmentation | `d730502861a2dc40fa993b9dd4897508c19141f5443dcf868be7f27a7f9920c3` |

### Visualization PNG Hashes

| Image | Artifact | SHA-256 |
| --- | --- | --- |
| PT_R1 BEFORE | density | `89fcdb0f2bb66a5e77fa7d1bcd5f720827cb979a269ed540c12d6e8af43e570d` |
| PT_R1 BEFORE | overlay | `8b71cbec740fb5c87c38a1f0ed036001d47402d76a258690d02701ca4e3b9b0b` |
| PT_R1 BEFORE | segmentation | `9cefea1eb1c23a82151bc37d22485d152fd54a8d0f3a301ef69d1d63054b585b` |
| PT_R1 AFTER | density | `7cfe31865e7e432d243786d2e6e80612b9394377b24d0737223736d918a6fb33` |
| PT_R1 AFTER | overlay | `3c47693b49f872f56091b6bfa61bfd6ad032712f9c460586a9622eb2acbf09e4` |
| PT_R1 AFTER | segmentation | `02622fec5cf71097797763454a056427f345a128911d791048ce05125115394a` |
| PT_02 BEFORE | density | `9f0432fad8fd91c8368a8e641fda3323e51a7ca14c7e614c5bba37ecd3caff96` |
| PT_02 BEFORE | overlay | `e8c45292a156680efbf605d938e69837f66461793412b7058140786abfceac6d` |
| PT_02 BEFORE | segmentation | `1728e906201cc371e8c6e32269d7303bc167216ab0f6087ba298bfad79238e40` |
| PT_02 AFTER | density | `4b9af3465829deffe81d369cb930cdbc6dffe6e76d77a999f6e798eb4fece9a4` |
| PT_02 AFTER | overlay | `054a7bd48e16d1f724f0a555448447997d6e6a6b23b4fbd70160d9d0bc748d1f` |
| PT_02 AFTER | segmentation | `c5104e4821fdd68a81993c61ea07530085f19734738e1bac6f1128b3d070f72b` |

Useful M03 derived inputs, raw predictions, and visualization artifacts were mirrored to the Windows repository after generation.

## M04 SAM2 Automatic

- Status: complete.
- Model: SAM 2.1 Hiera Base+.
- Model config: `configs/sam2.1/sam2.1_hiera_b+.yaml`.
- Checkpoint: `models/sam2/checkpoints/sam2.1_hiera_base_plus.pt`.
- Checkpoint SHA-256: `a2345aede8715ab1d5d31b4a509fb160c5a4af1970f199d9054ccfb746c004c5`.
- SAM2 source commit: `2b90b9f5ceec907a1c18123530e92e794ad901a4`.
- Full-resolution inputs: 8192 x 6144 RGB.
- `points_per_side=32`.
- `points_per_batch=4`.
- `pred_iou_thresh=0.8`.
- `stability_score_thresh=0.95`.
- `stability_score_offset=1.0`.
- `mask_threshold=0.0`.
- `box_nms_thresh=0.7`.
- `crop_n_layers=0`.
- `crop_nms_thresh=0.7`.
- `crop_overlap_ratio=512/1500`.
- `crop_n_points_downscale_factor=1`.
- `min_mask_region_area=0`.
- `output_mode=uncompressed_rle`.
- `use_m2m=False`.
- `multimask_output=True`.
- Automatic mask quantity is not interpreted as tree count.
- No tree-specific filtering or truth-informed tuning was performed.

### Automatic Mask Counts

| Image | Automatic Masks |
| --- | ---: |
| PT_R1 BEFORE | 87 |
| PT_R1 AFTER | 76 |
| PT_02 BEFORE | 74 |
| PT_02 AFTER | 50 |

### Prediction JSON Hashes

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `cd45ea28b37fa6e0c9752526b8cc4f8cc6defd7afe1cec8434ac80aa487f5860` |
| PT_R1 AFTER | `c16d1eb8b8a615667776e3175d17fd6dc1f612f32d435e09bb1f9e14e263e94f` |
| PT_02 BEFORE | `5e1a14e29223aeaee3a485a0f94a7d9cbf0f5f8c750a1a90aa8c8aa28ca316ae` |
| PT_02 AFTER | `66133c54e7c5b909a013773189512ea96877fe8a8c4c48d4f37fdbcc6fb23957` |

### Visualization PNG Hashes

| Image | Artifact | SHA-256 |
| --- | --- | --- |
| PT_R1 BEFORE | boxes and points | `23748982a32f1692089e850c8eba3878378893216ffaa2d5e68a1860319e5813` |
| PT_R1 BEFORE | overlay | `3d985e94b992819bc456ee4c1c9585e485d9b1d5f894a5fffbc5ebae6cc9b1c8` |
| PT_R1 AFTER | boxes and points | `868021811b875cb68a39409ac8300c755a849b85be64b0f8e9d421db2927e5f6` |
| PT_R1 AFTER | overlay | `bf86748817347c9ff2b2436d5fdfc622b2edc31d732bd152d6301c160258f819` |
| PT_02 BEFORE | boxes and points | `213ac0797a681e5895b5f40252ff65a813e099c68545c2b99b02a745ea2c9c39` |
| PT_02 BEFORE | overlay | `f4a1f1457f770e44429210d067966709972dbbf16bad6a8105066226f623a3b4` |
| PT_02 AFTER | boxes and points | `46ccd0cdc057d1182b25ca66e8ab89c5b093640a46f8887618683dd31668e8a5` |
| PT_02 AFTER | overlay | `01b9ff994b23c489b56f8908b6cb551e3c12dd055ddd1584394382a0918ab237` |

Useful M04 JSON predictions and visualization artifacts were mirrored to the Windows repository after generation.

## Exact Resume Point

M01, M02, M03, and M04 are complete for Week 4.

Next task:

1. Complete Week 4 M05 DeepForest GSD-Corrected -> SAM2.
2. Reuse the already-frozen Week 4 M02 DeepForest boxes.
3. Expected prompt counts are PT_R1 BEFORE 350, PT_R1 AFTER 365, PT_02 BEFORE 450, and PT_02 AFTER 478.
4. Do not rerun DeepForest.
5. Add Week 4 provenance checks to the existing M05 script before inference.
6. Do not use field truth or post-hoc filtering.
