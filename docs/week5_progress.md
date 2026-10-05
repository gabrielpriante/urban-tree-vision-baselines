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

## M03 TreeCountSegHeight

- Status: complete.
- Native GSD assumption: 1.67 cm/pixel.
- Target GSD: 20.00 cm/pixel.
- Resize factor: 0.083500.
- Derived dimensions: 684 x 513 pixels.
- Derived format: three-band RGB TIFF.
- Resampling: Lanczos.
- Docker image: `sizhuoli/tree_expert@sha256:fab4a8e16d7bc085440724c9fa522c957dc04299c625fcab7617b87c1c154e13`.
- Model checkpoint: `trees_20210620-0202_Adam_e4_redgreenblue_256_84_frames_weightmapTversky_MSE100_5weight_attUNet.h5`.
- Checkpoint SHA-256: `abce53345b8159aeda49dce7db32a0806ee90970593e7d2a1fe88d1f133ac843`.
- Segmentation threshold: 0.5.
- Count interpretation: continuous sum of the predicted density raster.
- Counts remain fractional and are not rounded.
- These values are density-estimated counts, not independently localized tree instances.
- All four Docker runs completed with `Predicted 1 images.` and `Failed to predict 0 images.`.
- No field truth or post-hoc tuning was used.

### Derived Input Hashes

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `5016d9409ea864e44b38f162d82d12ebb923cc1859b8a816602253bda1f16b2d` |
| PT_R1 AFTER | `6a4d0313fb20d38be6436ed54f8638967937a6df8d43bb124653932aa654f378` |
| PT_02 BEFORE | `f25f39582ae9433c4244a39cc76f2207073074d84ce5ff5fecd2feab3bd3cfd5` |
| PT_02 AFTER | `45e7d841ace0b528b39168829e94dba6bdee7e7817484b3730112fc94aa89a90` |

### Continuous Predicted Counts

| Image | Density-Sum Count |
| --- | ---: |
| PT_R1 BEFORE | `12.3053006977` |
| PT_R1 AFTER | `11.2363078445` |
| PT_02 BEFORE | `17.5792767350` |
| PT_02 AFTER | `15.2420119513` |

### Raw Prediction TIFF Hashes

| Image | Artifact | SHA-256 |
| --- | --- | --- |
| PT_R1 BEFORE | density | `bc76c7b51d3ec4ac99a36f189c5c99cbc2591698c9543df17c10aaae5e5a5072` |
| PT_R1 BEFORE | segmentation | `16e934bb838427a4ddc30d26d5f3083d77ffb8fd5e22f7d6c37f4f13a719b448` |
| PT_R1 AFTER | density | `5000a8405222f04cac73c79bdf1bf12c0529cf4351019de08ba0b3a92a28a582` |
| PT_R1 AFTER | segmentation | `cf58fa407eef6f9605be77b5b6fe3aa201c6ed169e11c94ef5491a24ea87add1` |
| PT_02 BEFORE | density | `936dfb47dcd37ecdb7e529c6889cbf5fe07671aecc4da448d9376ed68076b4e1` |
| PT_02 BEFORE | segmentation | `a4912b2210d31e9094bb8ee836338e265ba26fef6a0c4a1a080f00da95047cbb` |
| PT_02 AFTER | density | `59152825148fc240405fa05772d8a78b2374fa68a059d1353b6b169da7e87f38` |
| PT_02 AFTER | segmentation | `86cede050c954e71056a27b5a9ce890a7d5fe7df3473f3133b2a0e72d93d9f49` |

### Visualization PNG Hashes

| Image | Artifact | SHA-256 |
| --- | --- | --- |
| PT_R1 BEFORE | density | `566380aeceb9ae42731ae98c4312ebb02dde44c4f6ecd6ab612539ebc3de78ae` |
| PT_R1 BEFORE | overlay | `5798289597ba18ca8e7c91c3f1b69cf24208f9bf230e55d791fb76688194ad63` |
| PT_R1 BEFORE | segmentation | `6857ebeb2531d684f38772fbad1ad6ec17155c01e02ad04806ca9cfec0a99e40` |
| PT_R1 AFTER | density | `500dbbb3ce8365ee3bf145b3bd409f8c51d85cdf645bf699b1d610c7625e8126` |
| PT_R1 AFTER | overlay | `c7673ad4d74998ecb7dbbff37aba6aba06342b1db6214c56e42178bb9042932a` |
| PT_R1 AFTER | segmentation | `81865dcec24601965947ad3f9623d6abc59f54753a27f0dd9b32d26a76274bf7` |
| PT_02 BEFORE | density | `fa08630b77630ef3a36ef57e15fb0284eb4f61fbe34ac48521360e41b98f6736` |
| PT_02 BEFORE | overlay | `100d4858624042fe6872204032591cff090e081c8507ceddfcdc902d25f8ac87` |
| PT_02 BEFORE | segmentation | `b05476f2bcd5bdc479fbe37baf13449744ccfbf71e9cf13841186657d5268fa7` |
| PT_02 AFTER | density | `df824a049b3a07032dc8f665cd78b12d614c435fd9bcf09b312eeb824d928e25` |
| PT_02 AFTER | overlay | `c527460005f8c633b0251bc7a3a4d0e2c1095526dbd0ab5246022c5cd39601e0` |
| PT_02 AFTER | segmentation | `c6bc893097fcc521c1337524493b996d42197511d1646bb017d54bc28d390996` |

Useful M03 derived inputs, raw predictions, and visualization artifacts were mirrored to the Windows repository after generation.

## M04 SAM2 Automatic

- Status: complete.
- Model: SAM 2.1 Hiera Base+.
- Configuration: `configs/sam2.1/sam2.1_hiera_b+.yaml`.
- Checkpoint: `models/sam2/checkpoints/sam2.1_hiera_base_plus.pt`.
- Checkpoint SHA-256: `a2345aede8715ab1d5d31b4a509fb160c5a4af1970f199d9054ccfb746c004c5`.
- SAM2 source commit: `2b90b9f5ceec907a1c18123530e92e794ad901a4`.
- Python: 3.11.16.
- PyTorch: 2.11.0+cu128.
- CUDA runtime: 12.8.
- GPU: NVIDIA GeForce RTX 5070 Laptop GPU.
- Input: untouched native standardized 8192 x 6144 RGB JPEG.
- Points per side: 32.
- Points per batch: 4.
- Predicted-IoU threshold: 0.8.
- Stability-score threshold: 0.95.
- Automatic-mask quantities are segmentation quantities, not tree counts.
- No tree-specific filtering was applied.
- No field truth or post-hoc tuning was used.

### Automatic Mask Quantities

| Image | Masks |
| --- | ---: |
| PT_R1 BEFORE | 76 |
| PT_R1 AFTER | 78 |
| PT_02 BEFORE | 80 |
| PT_02 AFTER | 78 |

### Raw Prediction JSON Hashes

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `7b1ae24c0c5148904eb5a54dd09d1daa965f5143e1482864afcb6a55e4ac2311` |
| PT_R1 AFTER | `3fd3fbe125217ab01d319217fea64beaaeb567b7ba721828ac42cba17a50bb5d` |
| PT_02 BEFORE | `1d233f4baddb0137f83a73977813a008920fefa5cb19d0a073dc13ec35d79161` |
| PT_02 AFTER | `8d96fc823199a2ffee11b16590f68dfc77e95e82df74d0d8a0ac7fadff6c25f0` |

### Visualization PNG Hashes

| Image | Artifact | SHA-256 |
| --- | --- | --- |
| PT_R1 BEFORE | boxes and points | `8698d101f751cd317f9615fdb14955e58b90507ec43d0084e841c0a517544c20` |
| PT_R1 BEFORE | overlay | `fb829c8288831d1c91313fd0e6cea91496b0496eddf02a123ad923cf1b3c77ee` |
| PT_R1 AFTER | boxes and points | `27b6cad6d5b02955f53bcaab95e29bdcc549d7947765f92bf91fac72a164d69f` |
| PT_R1 AFTER | overlay | `8923fc90f60f79add0d6ca24cd9eb2fa4c6803f16aa209b408ce048ec8dc14df` |
| PT_02 BEFORE | boxes and points | `4e99c4eb8ec7cd828119792a17f53c334bccec4ee5b0f30ac0b755d74314a803` |
| PT_02 BEFORE | overlay | `3c0e3b5ebd079a73195ce599b5c40c23dcaec7fb0de4d218d65df7a134f46683` |
| PT_02 AFTER | boxes and points | `59c483691dd8f30865e193cf67d8490e5fa08b597da9c1c4ecd57c532f09db0b` |
| PT_02 AFTER | overlay | `bda24c6edf51db7c527517e9ecbd62e6623c8fc5f8bd029c0176e018025b07c7` |

Useful M04 raw predictions and visualization artifacts were mirrored to the Windows repository after generation.

## M05 DeepForest GSD-Corrected to SAM2

- Status: complete.
- Detector source: frozen Week 5 M02 DeepForest GSD-Corrected predictions.
- DeepForest coordinate-space dimensions: 1734 x 1300 pixels.
- Native SAM2 image dimensions: 8192 x 6144 pixels.
- Coordinate scale X: 4.724336793541.
- Coordinate scale Y: 4.726153846154.
- SAM2 model: SAM 2.1 Hiera Base+.
- Configuration: `configs/sam2.1/sam2.1_hiera_b+.yaml`.
- Checkpoint: `models/sam2/checkpoints/sam2.1_hiera_base_plus.pt`.
- Checkpoint SHA-256: `a2345aede8715ab1d5d31b4a509fb160c5a4af1970f199d9054ccfb746c004c5`.
- SAM2 source commit: `2b90b9f5ceec907a1c18123530e92e794ad901a4`.
- One SAM2 mask was generated for every frozen DeepForest box.
- No DeepForest boxes were manually edited.
- M05 inherits the M02 detection quantity and is not an independent tree-count model.
- No field truth or post-hoc prompt tuning was used.

### One-to-One Box-to-Mask Quantities

| Image | DeepForest Boxes | SAM2 Masks |
| --- | ---: | ---: |
| PT_R1 BEFORE | 447 | 447 |
| PT_R1 AFTER | 376 | 376 |
| PT_02 BEFORE | 503 | 503 |
| PT_02 AFTER | 452 | 452 |

### Raw Prediction JSON Hashes

| Image | SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `61bf8a85d7eaf16f6aed6ce5c5f90853a9b6fb310e0d1a621069c6a40e246a2c` |
| PT_R1 AFTER | `4af43c475613a334355f35c55796c8d2b7b542f5af631b082ede5538d45dad08` |
| PT_02 BEFORE | `bd6634bc43d2288e4406a10a41b87c21cf4585ee0dd91675c6d6bff4a70a14fa` |
| PT_02 AFTER | `edff5065a38242e3373f2026846860f1b4a4f3694e8a123e79367337205d6177` |

### Visualization PNG Hashes

| Image | Artifact | SHA-256 |
| --- | --- | --- |
| PT_R1 BEFORE | DeepForest boxes | `c8b18723f864b9fd3cfc5ea9e944bafbbef54da46ede80c5c31a10f1f0467af2` |
| PT_R1 BEFORE | SAM2 overlay | `185f539827f0af1b6867582111149c9b81ecb5f5aaa05e7fb8e462f3197afbb4` |
| PT_R1 AFTER | DeepForest boxes | `02e378e9acdacd155c3b55ac3ded1d22f4941a8689ee3d1becc564fa4786df9b` |
| PT_R1 AFTER | SAM2 overlay | `2a39a3e426e97c859165b3c3cedcc2febba7d8ee5723df77a2829eff553d8488` |
| PT_02 BEFORE | DeepForest boxes | `72f6f6dc878a4194205424fcba4326b694a8de96b5295650b98d03022dd1d01e` |
| PT_02 BEFORE | SAM2 overlay | `2f0a4a8a8f169512d0b3d4e12f010d2e1e5d35630eda1f7b0042cd0502b1978e` |
| PT_02 AFTER | DeepForest boxes | `15f7c5366b785d25255917b951b3a52513caedd5ebdc94dd781a5066c748409e` |
| PT_02 AFTER | SAM2 overlay | `81c8302434c1663d8e1d9378828fb7b41be783f0cae0b2d3382f14f6a288499d` |

Useful M05 raw predictions and visualization artifacts were mirrored to the Windows repository after generation.

## Exact Resume Point

Week 5 is complete through the frozen M01-M05 benchmark pipeline.

1. M01 DeepForest Native: complete.
2. M02 DeepForest GSD-Corrected: complete.
3. M03 TreeCountSegHeight: complete.
4. M04 SAM2 Automatic: complete.
5. M05 DeepForest GSD-Corrected to SAM2: complete.
6. M06 TreePseCo remains skipped because execution and checkpoint access remain unresolved.
7. Next benchmark expansion is M07 SAM3-family instance segmentation.
8. Do not alter completed M01-M05 parameters based on observed Week 5 outputs or field truth.
