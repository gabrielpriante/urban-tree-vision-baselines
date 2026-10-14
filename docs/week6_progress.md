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

## M02 DeepForest GSD-Corrected

- Status: complete.
- Native assumed GSD: 1.67 cm/pixel.
- Target GSD: 7.89 cm/pixel.
- Resize factor: 0.211660.
- Resampling method: Lanczos.
- Derived image dimensions: 1734 x 1300 pixels.
- Derived image color mode: RGB.
- DeepForest inference settings remained frozen from M01.
- No field truth or post-hoc tuning was used.
- Detection quantities are independent DeepForest object detections.
- These detections will later provide the frozen box prompts for M05.

### Derived Input SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `c94bf04a63eacc971c6d56bb24c06f0aa484ed18e7facfa1d9d9d49f228aad28` |
| PT_R1 AFTER | `5c8a3fc50bbe6158c82d26c947b1c18e14e72125187bc9f0bda2976b0cce1019` |
| PT_02 BEFORE | `bd0adee95d7b166787ece5d143c222cf17a8ff5fd538d3efcd3ffbc496b8b4d5` |
| PT_02 AFTER | `9369591579c96f210a864b6ac439bbdea74047324354378a5608e268635e00ae` |

### Detection Quantities

| Image | Detections |
| --- | ---: |
| PT_R1 BEFORE | 291 |
| PT_R1 AFTER | 274 |
| PT_02 BEFORE | 349 |
| PT_02 AFTER | 352 |

### Prediction CSV SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `147f2803b5e428ad203811a982ca470659af40432d64e7ef510b9c402e34d7e6` |
| PT_R1 AFTER | `82ca01a6540e6350ffb2ae03ac39eb9ca989c6add122935ed2c87f0ebbeddf9e` |
| PT_02 BEFORE | `50a8de0c78d775f777b469ec6176462ec334be31b3a6833a3e507f6219213822` |
| PT_02 AFTER | `1c532dbacaefcb06dd869b8e5bd633e975835c752a2e8a309ed12e220156bf7c` |

### Prediction Visualization SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `11f251cab9e95f74ae3df2649573e629ee0a539ce059eb6278e2b726a48a566b` |
| PT_R1 AFTER | `5159dd1d0b8844fd2e98af9e0592be154609ade1404708a03f8fdb7133aed1df` |
| PT_02 BEFORE | `8643d1c0c37a9538f9998aa82653fd4a567d3c0ec88d02adedb045d35a04c020` |
| PT_02 AFTER | `b8d04f0fe9aae4863028bdb860996f54e15ed7b54a12e9db332f9456a1d3cf9e` |

The generic DeepForest runner initially wrote the Week 6 M02 artifacts into the Week 6 `single_image` namespace. Those exact M02 artifacts were preserved under the dedicated `gsd_7.89` namespace, and the previously mirrored M01 artifacts were restored to `single_image`. No inference was rerun or altered during this bookkeeping correction.

Useful Week 6 M02 derived inputs, prediction tables, and visualization artifacts were mirrored to the Windows repository after generation.

## M03 TreeCountSegHeight

- Status: complete.
- Native assumed GSD: 1.67 cm/pixel.
- Target GSD: 20.00 cm/pixel.
- Resize factor: 0.083500.
- Resampling method: Lanczos.
- Derived input dimensions: 684 x 513 pixels.
- Derived input color mode: RGB.
- Docker image: `sizhuoli/tree_expert@sha256:fab4a8e16d7bc085440724c9fa522c957dc04299c625fcab7617b87c1c154e13`.
- RGB checkpoint SHA-256: `abce53345b8159aeda49dce7db32a0806ee90970593e7d2a1fe88d1f133ac843`.
- Each image completed successfully with one predicted image and zero failed images.
- No field truth or post-hoc tuning was used.
- M03 quantity is the continuous sum of the model density raster and is not a localized or integer tree count.

### Derived Input SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `1ef40401082aa08d8d48b404e0d330cd41002d8b336e36a504f03deb342cf34c` |
| PT_R1 AFTER | `ab22a7a2439ab18d2f16a243644501b175f96afe187e689e03ab0ae701d3998b` |
| PT_02 BEFORE | `e7b504b96b71ee7554f92b79edc0210dafed740a473e9c15b7a4d2550de0ac38` |
| PT_02 AFTER | `2720da27fd45b6c150a3a6322642235c8d7bc53aa766f9103df3b97fc27b9ad5` |

### Continuous Density Estimates

| Image | Density Sum |
| --- | ---: |
| PT_R1 BEFORE | 2.0023066569 |
| PT_R1 AFTER | 2.6256756801 |
| PT_02 BEFORE | 1.7336878702 |
| PT_02 AFTER | 0.7501857653 |

### Raw Density Raster SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `a1b2bb827dc08f857b62cea97d72a5da82b77a52b8e1aaa3b784b41698fce60b` |
| PT_R1 AFTER | `6cb379702f084b23595bbcd59a2094aef660c254c279ffc3e92e7577f723f473` |
| PT_02 BEFORE | `96f289c1f786c08ca516548693571fecc8628e18efbca79d7f1c1fd581cf574f` |
| PT_02 AFTER | `07e42bff53b24fe51863385663397e708f7d1fc4c50ea675dbc490bb9c116405` |

### Raw Segmentation Raster SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `a9210246d06c7a399bdba6f364ae7dfd986f03a3c084a45c5b68bb3e693d48eb` |
| PT_R1 AFTER | `2fb41971de12298f840634745ab5e2dbc5d247fd4312492e21e203c69ec25261` |
| PT_02 BEFORE | `909383733f9e8ade53dd92dcce5ea94a6c9fb556088213c234f8315b1ece2e65` |
| PT_02 AFTER | `4394d9d52176034d87dbab4f50da598b0ca8930989b15b421c686996fc6f69ef` |

### Visualization SHA-256

| Image | Overlay | Segmentation | Density |
| --- | --- | --- | --- |
| PT_R1 BEFORE | `bcef7ffa02898cb00de71f57c603a5297f984c2d7685a12f4c9bf88c40a1e3d3` | `e8886e902f0e318af6944a09cdf320a2b6daae26b194313f39e8ca27744ebae0` | `0092ef8ff1d2d675ec930aa42b2ac83e0eae7aaae181c2d77898385ff1b58f46` |
| PT_R1 AFTER | `49b861ef1129635a7d92524bc41b1817375b86508dd4c63cbbbc2d22277a99b4` | `d72f096ac9a7dac8a2e4aa1e08d6868038de34f25785dac19796c65db85179d5` | `9004cfb5a152e7084983e28926cf6df58e6e6914f0d78cb6e6beaae3452f82f7` |
| PT_02 BEFORE | `e169f9e2e9108f503b00123c93223f5e559fafde4863080b3e475c1ac1961c60` | `cbddb2401eabcf5879672d91ef4f5c43f021b9c92c21e4f5e1a7e3cbae30dcea` | `7ab461f2290685cad402c5b8136763b61b201ce07894d51cd56b899525c94376` |
| PT_02 AFTER | `413b4e06d0da01bf26f98125bf1055e130fa6be7d5d11aab1ab4433e1d621433` | `2944b578b2b1d006d813857869a3e7d96b2470c9e02ebdb85d28b98c85b16141` | `d9a45692de9edbc7eeaaa2281cbcf80f443fbb5e8f9bb41ca8eb6b1b29f906f4` |

Week 6 M03 derived inputs, raw model outputs, and visualization artifacts were mirrored to the Windows repository.

## M04 SAM2 Automatic

- Status: complete.
- Input imagery: untouched native Week 6 RGB imagery at 8192 x 6144 pixels.
- Python: 3.11.16.
- PyTorch: 2.11.0+cu128.
- CUDA runtime: 12.8.
- GPU: NVIDIA GeForce RTX 5070 Laptop GPU.
- SAM2 checkpoint: `models/sam2/checkpoints/sam2.1_hiera_base_plus.pt`.
- Checkpoint SHA-256: `a2345aede8715ab1d5d31b4a509fb160c5a4af1970f199d9054ccfb746c004c5`.
- SAM2 source commit: `2b90b9f5ceec907a1c18123530e92e794ad901a4`.
- Config: `configs/sam2.1/sam2.1_hiera_b+.yaml`.
- points_per_side: 32.
- points_per_batch: 4.
- pred_iou_thresh: 0.8.
- stability_score_thresh: 0.95.
- stability_score_offset: 1.0.
- mask_threshold: 0.0.
- box_nms_thresh: 0.7.
- crop_n_layers: 0.
- crop_nms_thresh: 0.7.
- crop_overlap_ratio: 512 / 1500.
- crop_n_points_downscale_factor: 1.
- min_mask_region_area: 0.
- output_mode: uncompressed_rle.
- use_m2m: false.
- multimask_output: true.
- No field truth or post-hoc tuning was used.
- M04 quantity is the number of automatic SAM2 masks and is not interpreted as tree count.

### Automatic Mask Quantities

| Image | Automatic Masks |
| --- | ---: |
| PT_R1 BEFORE | 99 |
| PT_R1 AFTER | 84 |
| PT_02 BEFORE | 84 |
| PT_02 AFTER | 98 |

### Raw Mask JSON SHA-256

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `4d3abceee96be91204defc4a90176657da67712dfb1cc5c554c69d0cf13943f7` |
| PT_R1 AFTER | `0166feb5a76b46326f426e4f4cc59ebbae380212fad6e00784cd67465542fc4f` |
| PT_02 BEFORE | `c730a241e8710ddbe69d3f559463d1157d082e0472ba5df6ecc7b122cb9f4820` |
| PT_02 AFTER | `18cf1b4ce5d4575009773bc6d88ac881b3a45f9fef442959ad877feecf819917` |

### Visualization SHA-256

| Image | Overlay | Boxes and Points |
| --- | --- | --- |
| PT_R1 BEFORE | `910addf327bdc9e152dcc21773250c02fb30eda6dfda1bfa6d2bed1ee77a5676` | `9dd096f46ee836591b4f99c63eead94ec87cdc6018bd9f0b7ea8703ddf13c02a` |
| PT_R1 AFTER | `c4e516b9e30d729751ee64aebe9d1a7455fa468baa8b5b2f55ec185f9ec1274e` | `44d0634d1259653cff73a53a6a289501b091633fa7787d38dd5a64bf4576efa6` |
| PT_02 BEFORE | `65c884205b334c4a848a9a2574b4869e07113016b6e6d1dcddee0a0b5696680e` | `6cc7134cc2628c8987b3b6f3f9a375558da152294cc09b4326d7c84f30ec9ed7` |
| PT_02 AFTER | `2a9352f429a6916e22a4730692d332e3215daca7089eea3ab21e8b1baa849464` | `55ecc4220a1d5b78013f2149c6342511643af333ed90e99fd9d8f9e45bbf2bd4` |

Week 6 M04 raw mask outputs and visualization artifacts were mirrored to the Windows repository.

## Exact Resume Point

Week 6 is complete through M04.

1. M01 DeepForest Native: complete.
2. M02 DeepForest GSD-Corrected: complete.
3. M03 TreeCountSegHeight: complete.
4. M04 SAM2 Automatic: complete.
5. Next task: M05 DeepForest GSD-Corrected to SAM2.
6. Docker is not required for M05.
7. M05 must inherit the frozen M02 DeepForest boxes and must not be interpreted as an independent tree count.
8. Do not tune using Week 6 outputs or field truth.
