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

## Exact Resume Point

M01 is complete for Week 5.

Next task:

1. Complete Week 5 M02 DeepForest GSD-Corrected.
2. Use the frozen 1.67 cm/pixel native GSD assumption.
3. Resample to 7.89 cm/pixel using Lanczos.
4. Use the same frozen DeepForest parameters as M01.
5. Do not tune using field truth.
