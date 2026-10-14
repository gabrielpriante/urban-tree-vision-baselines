# Week 6 Benchmark Progress

## Week 6 Input Ingestion

- Status: complete.
- Sites: PT_R1 and PT_02.
- Conditions: BEFORE and AFTER.
- Standardized RGB images: 4.
- Native dimensions: 8192 x 6144 pixels.
- Color mode: RGB.
- Authoritative execution repository: `/home/gabpe/src/urban-tree-vision-baselines`.
- Native Week 6 inputs were copied from the standardized field-imagery directory into `data/raw/experiment_001/week6`.
- Source and authoritative Linux-copy SHA-256 identities matched exactly.
- The four authoritative Week 6 native inputs were mirrored to the Windows repository.

### Native Input SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `7295f689d76a0bc0a5a49d57e93438e4bb593e896b32bb87e92c027555ed3573` |
| PT_R1 AFTER | `97d5df8d418ea759dc83ef0daa399de08d54bbbbb0ce7bdde75ecd51074c0901` |
| PT_02 BEFORE | `e793437a056d29295dddb275abad3671f17be8986de8c642402c4468abef36e4` |
| PT_02 AFTER | `8ffc3051863fcace2d4d49a91983e98a9b246782f2e162fc11bd2d19c55578e9` |

## M01 DeepForest Native

- Status: complete.
- DeepForest version: 2.1.0.
- PyTorch version: 2.14.0+cu130.
- CUDA available: true.
- GPU: NVIDIA GeForce RTX 5070 Laptop GPU.
- Model: `weecology/deepforest-tree`.
- Input: untouched native standardized Week 6 RGB imagery.
- Patch size: 400 pixels.
- Patch overlap: 0.05.
- IoU threshold: 0.15.
- Score threshold: 0.10.
- NMS threshold: 0.05.
- No field truth or post-hoc tuning was used.
- Detection quantities are independent DeepForest object detections.

### Detection Quantities

| Image | Detections |
| --- | ---: |
| PT_R1 BEFORE | 2603 |
| PT_R1 AFTER | 2491 |
| PT_02 BEFORE | 3535 |
| PT_02 AFTER | 2393 |

### Prediction CSV SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `9151ba0ce0bf63a5c62f8fdbb02c5e0aa59cac63524504978a04438795190e87` |
| PT_R1 AFTER | `be58c74ab79bea0f48cc8aae0a46daa7538b45d42007114a36da1668ba8ddb99` |
| PT_02 BEFORE | `ebf73589b9e2fddea56bb7f8774a2a2306672e4a835a98f339e368de7794b64d` |
| PT_02 AFTER | `07c317d1ba2dcb5447c1a5988944a7267775ca58bd138314fddb1b74f3055390` |

### Prediction Visualization SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `066fb939a8d08c4bcda7dc6ac4030ce6f66036c69c58a50e5792104cbce11953` |
| PT_R1 AFTER | `677947d6b10fc6e55aad0e0380355f7aa7e807ca8968302f05a492b29ba5c43f` |
| PT_02 BEFORE | `3774334d7abba515e98ffeba86dcce125b3d39e91a0cf9a65c0e3fe17b2180b8` |
| PT_02 AFTER | `acb9aa7eca7217f85a693c9eee1d5049fd9e1921d615df5b0809edb7c1e28453` |

Useful Week 6 M01 prediction tables and visualization artifacts were mirrored to the Windows repository after generation.

## Exact Resume Point

Week 6 M01 is complete.

Next task:

1. Complete Week 6 M02 DeepForest GSD-Corrected.
2. Preserve the frozen 7.89 cm/pixel preprocessing protocol.
3. Preserve the frozen DeepForest inference settings used in previous weeks.
4. Do not tune parameters using Week 6 outputs or field truth.
