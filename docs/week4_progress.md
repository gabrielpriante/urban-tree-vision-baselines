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

- Preprocessing: complete.
- Docker inference: complete for all four images.
- Postprocessing, output hashing, visualization, and density-sum counts: not yet completed.
- Native GSD assumption: 1.67 cm/pixel.
- Target GSD: 20.00 cm/pixel.
- Derived dimensions: 684 x 513 RGB TIFF.
- Docker image: `sizhuoli/tree_expert@sha256:fab4a8e16d7bc085440724c9fa522c957dc04299c625fcab7617b87c1c154e13`.
- RGB checkpoint SHA-256: `abce53345b8159aeda49dce7db32a0806ee90970593e7d2a1fe88d1f133ac843`.
- All four runs ended with `Predicted 1 images.` and `Failed to predict 0 images.`.

### M03 Derived Input Hashes

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `1b414cf9b2a3fe05d6442d9181b4f020a05886572f940ad50aa410743581eb1c` |
| PT_R1 AFTER | `06a0a396fa03e45cd32f07ce14c2da92147212534a58e8994243a68ece87e92e` |
| PT_02 BEFORE | `60567c4ae4b5ae4a11585841e3122911078d0a6e78424050b955d1874deae816` |
| PT_02 AFTER | `81e2b3a2e4da290638035d2981254b933c0577de20b72ed2c1d18ba1c1033670` |

## Exact Resume Point

1. Do not rerun M01, M02, or M03 Docker inference.
2. Inspect the four existing Week 4 M03 output directories and identify the density and segmentation TIFF filenames.
3. Calculate continuous density-sum counts using the same Week 3 method and preserve fractional precision.
4. Hash all eight raw M03 TIFF outputs.
5. Run the existing TreeCountSegHeight visualization script with the Week 4 run label and generate density, overlay, and segmentation PNGs.
6. Hash all twelve visualization PNGs and mirror final M03 artifacts to Windows.
7. Then begin M04 SAM2 Automatic Week 4.
8. M05 will reuse the frozen M02 prompt counts 350, 365, 450, and 478.
