# Week 5 Benchmark Progress

## Native Image Ingestion

- Status: complete.
- Benchmark images: 4.
- Sites: PT_R1 and PT_02.
- Conditions: BEFORE and AFTER.
- Dimensions: 8192 x 6144 pixels.
- Mode: RGB.
- Linux repository is authoritative.
- Native Week 5 images were mirrored to the Windows repository after ingestion.

### Native Image SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `470aea6de65e91ea87b69a444c649f80566bc6cd4d8ca72c52c224bbdab827ec` |
| PT_R1 AFTER | `ad6160e8599e79ab9cda58b7798c91e95399ba4f6f0a4a1585dd54c80016fd45` |
| PT_02 BEFORE | `d5ca1a50522c5c94a1444370c6ab0f3f7c2f5868680a8c334fc0a2dec3c7a16e` |
| PT_02 AFTER | `73beab517719ab3f88fd80b326ff077adf32aad7c5bdaae4ac208a0c7060e218` |

## M01 DeepForest Native

- Status: complete.
- Model: `weecology/deepforest-tree`.
- Model revision: `main`.
- DeepForest version: 2.1.0.
- Patch size: 400 pixels.
- Patch overlap: 0.05.
- IoU threshold: 0.15.
- Score threshold: 0.10.
- NMS threshold: 0.05.
- No field truth or post-hoc tuning was used.

### Detection Counts

| Image | Detections |
| --- | ---: |
| PT_R1 BEFORE | 5475 |
| PT_R1 AFTER | 5071 |
| PT_02 BEFORE | 6604 |
| PT_02 AFTER | 6733 |

### Prediction CSV Hashes

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `26ebef4ca854143171f2be3c5f06d908e0343150e3911c4e63afdafbc525714a` |
| PT_R1 AFTER | `76d99a0ec9bc009207eb1615af8f46cc2488b42372fc6a3f4efab1820786d3d6` |
| PT_02 BEFORE | `4ce99717fbfc0a2896d1d8ced81b6620a170428c4503e29ef8027ab1a8f2f492` |
| PT_02 AFTER | `4c3c9e9d84efc840d9685ab46dc7c04e93969457276bc22f661ef7e20cc9207e` |

### Visualization PNG Hashes

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `66221b0cc659ebc62fbe658ee41529d52249e7defa282845875fb8646bbbba7a` |
| PT_R1 AFTER | `6b334db27e11e209916bfe003787fcba02903b351fdcffa3e5a159ae26fe6f7e` |
| PT_02 BEFORE | `15d12307d97e35a55f708126b0f0cf8e5b0c032ba131626605ba0f4764a6694b` |
| PT_02 AFTER | `391a051b846d0d889ddb40e3700a28ed20bf4c9ee1d4abd19cf4155963f56515` |

Useful M01 prediction tables and visualization artifacts were mirrored to the Windows repository after generation.

## M02 DeepForest GSD-Corrected

- Status: complete.
- Native GSD assumption: 1.67 cm/pixel.
- Target GSD: 7.89 cm/pixel.
- Resize factor: 0.211660.
- Derived dimensions: 1734 x 1300 pixels.
- Derived mode: RGB.
- Resampling: Lanczos.
- JPEG quality: 95.
- Model: `weecology/deepforest-tree`.
- Model revision: `main`.
- Patch size: 400 pixels.
- Patch overlap: 0.05.
- IoU threshold: 0.15.
- Score threshold: 0.10.
- NMS threshold: 0.05.
- No field truth or post-hoc tuning was used.

### Derived Image SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `e1d43d5466c9439ba5ad35b98915ced077254b96194fdbec8151369863a687e3` |
| PT_R1 AFTER | `0dd5273afb164dd11db04ff0fdff5699f883efb0c1d2bbc9bae63db193908d65` |
| PT_02 BEFORE | `1ce7e179c7ba5089b3342ea6a30895f5cb0692331db1cb0ec6a35f875164131f` |
| PT_02 AFTER | `2052eb89f43de725c66f2dfd7d5f5161707ff28db125862716279a1e948bbc31` |

### Detection Counts

| Image | Detections |
| --- | ---: |
| PT_R1 BEFORE | 447 |
| PT_R1 AFTER | 376 |
| PT_02 BEFORE | 503 |
| PT_02 AFTER | 452 |

### Prediction CSV Hashes

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `4356c06a649f3200165f8e0d615f79dabad847de21887ef436e7e5e00a446821` |
| PT_R1 AFTER | `a10d2390b6a70443af66fdadad500c4fb452c567c63b509866c9bd0c7bec8ec3` |
| PT_02 BEFORE | `c6537358e312076fc04bc1a5bb844b0eb26b627277705d40d31c310675764fea` |
| PT_02 AFTER | `bc201e4316dcec0c016151f41b294bba733936efdf38d0ff2e990bbe75967a4e` |

### Visualization PNG Hashes

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `5d82e2dd56e74dea189b0eae65904939c18a7216e53e5a0284cd29400f806e9d` |
| PT_R1 AFTER | `08834bdfcce3319ddb64efec1d344a4c070e0871d05b5a48925b96abfe078fbd` |
| PT_02 BEFORE | `702b48f96c63b2fd624c5b211cb73dedce660e034b3f712d07dfb2479dec3809` |
| PT_02 AFTER | `ed82dc541d236e39bf1f62f22de2dd7b2391b22bc918bae0ba848a7d4857a87e` |

Useful M02 derived imagery, prediction tables, and visualization artifacts were mirrored to the Windows repository after generation.

## Exact Resume Point

M01 and M02 are complete for Week 5.

Next task:

1. Complete Week 5 M03 TreeCountSegHeight.
2. Resample the four native benchmark images to the frozen 20.00 cm/pixel TreeCountSegHeight input resolution.
3. Preserve the existing model checkpoint and Docker protocol.
4. Preserve continuous density-sum counts as fractional values.
5. Do not tune using field truth.
