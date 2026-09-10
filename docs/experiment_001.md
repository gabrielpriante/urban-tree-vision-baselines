# Experiment 001: Pretrained Vision Baselines

## Objective

Evaluate pretrained computer vision models on standardized RGB drone imagery collected before and after field work.

The purpose of this experiment is to establish baseline model behavior before local fine-tuning or field-ground-truth-informed adjustment.

## Inputs

The experiment uses standardized RGB imagery collected from consistent observation locations.

Each image will receive a stable identifier in the project data manifest.

Original input images will remain unchanged.

## Conditions

Images will be classified into two experimental conditions:

- Before
- After

The before and after images will be analyzed independently using the same model configuration whenever the model permits identical inference settings.

## Baseline 1: DeepForest

DeepForest will be evaluated using its pretrained individual tree detection model.

The initial run will use no local fine-tuning.

Inference parameters will be recorded explicitly, including parameters related to tiled inference.

Raw bounding-box predictions and confidence values will be retained.

## Baseline 2: DINOv3

A DINOv3-based pretrained approach will be evaluated on the same standardized imagery.

The exact DINOv3 model and downstream inference method will be documented before execution.

No local fine-tuning will be used during the initial baseline experiment.

Raw model outputs will be retained before any conversion into derived tree-level representations.

## Baseline Separation

DeepForest and DINOv3 outputs will not be assumed to represent equivalent prediction tasks.

Each model will first be evaluated according to the output representation produced by its selected pretrained inference method.

Any later conversion between segmentation masks, bounding boxes, or other representations will be documented as a derived analytical step.

## Field Validation

Field observations will not be used to modify baseline predictions during inference.

The sequence will be:

1. Run the model.
2. Save predictions.
3. Save inference metadata.
4. Freeze the baseline output.
5. Compare the frozen output with field observations.

This separation prevents field knowledge from unintentionally influencing the initial pretrained baseline.

## Initial Non-Goals

Experiment 001 does not initially include:

- Local model fine-tuning
- Manual correction of predictions
- Ground-truth-informed threshold optimization
- Photogrammetric reconstruction
- Tree height estimation
- Tree health modeling
- Multi-model ensembling
- Temporal change attribution
- Tiling-origin sensitivity analysis

These may be evaluated in later experiments.

## Reproducibility Requirements

Each inference run should record enough information to reproduce the prediction set, including:

- Input image identifier
- Input filename
- Input image dimensions
- Model name
- Model version
- Model identifier or checkpoint
- Inference configuration
- Software environment
- Hardware device
- Source-code version
- Prediction output location

## Phase A: TreeCountSegHeight RGB baseline

TreeCountSegHeight was evaluated using the project's official pretrained RGB model and official Docker environment.

### Deployment condition

- Source imagery: standardized 8192 x 6144 DJI RGB JPEGs.
- Nominal source GSD: 1.67 cm/pixel.
- Target GSD: 20.00 cm/pixel.
- Resampling: Lanczos.
- Derived input size: 684 x 513 pixels.
- Input type: three-band uint8 RGB TIFF.
- No CRS or geospatial metadata was fabricated.
- Pretrained model: RGB attention U-Net segmentation and density-counting model.
- Segmentation threshold: 0.5.
- Other inference parameters retained from the authors' packaged configuration.
- No model fine-tuning, threshold optimization, or ground-truth-informed parameter adjustment was performed.

### Frozen density-count outputs

| Image | Condition | Density-based count |
| --- | --- | ---: |
| PT_R1 | Before | 3.728563 |
| PT_R1 | After | 3.219690 |
| PT_02 | Before | 0.787543 |
| PT_02 | After | 1.188348 |

### Interpretation

The pretrained RGB TreeCountSegHeight baseline transferred poorly to the study imagery. Segmentation outputs were extremely sparse and omitted substantial visually apparent tree canopy in both scenes. The low density-based count estimates were consistent with the sparse spatial predictions.

Before-and-after differences are retained as model outputs but are not interpreted as tree gain or loss. The paired drone images differ in viewing orientation, and the weak baseline transfer makes causal interpretation inappropriate.

No additional tuning was performed after inspecting these outputs.

### Reproducibility notes

The official Docker image was pinned by digest:

`sha256:fab4a8e16d7bc085440724c9fa522c957dc04299c625fcab7617b87c1c154e13`

The RGB model checkpoint used was:

`trees_20210620-0202_Adam_e4_redgreenblue_256_84_frames_weightmapTversky_MSE100_5weight_attUNet.h5`

Checkpoint SHA-256:

`abce53345b8159aeda49dce7db32a0806ee90970593e7d2a1fe88d1f133ac843`

The four derived 20 cm TIFF inputs were also hashed before inference.

## Phase B3: Field-confirmed point-guided SAM2

Phase B3 evaluates whether field-confirmed tree identity and approximate image location can provide useful spatial guidance to a general segmentation model.

For PT_R1, field observations confirmed nine trees with IDs 3 through 11. Precise field GPS coordinates were unavailable because location metadata was not retained in the submitted field imagery. The field-confirmed trees were therefore manually registered to the standardized aerial images using one positive point placed clearly inside each visible crown.

The BEFORE and AFTER images were registered independently. Registered points were frozen before SAM2 inference and were not moved or adjusted after model outputs were observed.

### Prompt protocol

- Model: SAM2.1 Hiera Base+.
- Native image size: 8192 x 6144 pixels.
- Prompt type: one positive point per field-confirmed tree.
- Trees: IDs 3 through 11.
- Positive points per tree: 1.
- Negative points per tree: 0.
- Box prompts: none.
- Multimask output: false.
- Manual mask selection: none.
- Post-inference prompt adjustment: none.
- Additional model postprocessing: none.
- BEFORE and AFTER images were processed independently using the same inference configuration.

### Frozen field-point inputs

| Condition | Field-point CSV SHA-256 |
| --- | --- |
| Before | `830721c5f19ce9035f68a2f5261e6b338c579edc7df26e1b29ff43e50790017c` |
| After | `e3793dceb6f94a76cf244d5c25d10497c50c3c76525452c92d09f0ece334ad54` |

### Frozen SAM2 outputs

| Condition | Points | Masks | Runtime (s) | Peak GPU memory (MB) | Output SHA-256 |
| --- | ---: | ---: | ---: | ---: | --- |
| Before | 9 | 9 | 2.50 | 709.73 | `0f79272857e97630ea0def49f40a5b2ac674903e88470342a8799c03e6031918` |
| After | 9 | 9 | 2.54 | 709.73 | `54178c901084bc2b2bf1fcd81af1464ec08b7953b4bcf2495b22d83acb76462c` |

### Tree-level outputs

| Tree ID | Before predicted IoU | Before area (pixels) | After predicted IoU | After area (pixels) |
| ---: | ---: | ---: | ---: | ---: |
| 3 | 0.9141 | 150313 | 0.8945 | 109258 |
| 4 | 0.7773 | 26719 | 0.3594 | 263085 |
| 5 | 0.8789 | 18896 | 0.8867 | 16111 |
| 6 | 0.7305 | 5061 | 0.8789 | 52950 |
| 7 | 0.8594 | 16058 | 0.8711 | 16716 |
| 8 | 0.6484 | 12188 | 0.8438 | 21825 |
| 9 | 0.6992 | 207251 | 0.7812 | 165086 |
| 10 | 0.8477 | 232652 | 0.7930 | 182718 |
| 11 | 0.3535 | 561039 | 0.7148 | 35494 |

The reported `sam2_predicted_iou` values are SAM2 internal mask-quality estimates. They are not measured intersection-over-union values against manually delineated ground-truth crowns and must not be interpreted as segmentation accuracy.

### Initial interpretation

Field-confirmed point guidance substantially reduced task-irrelevant segmentation compared with unguided SAM2 and constrained inference to known tree locations. The resulting masks were nevertheless heterogeneous. Some prompts produced compact local masks, while others produced small partial regions or expanded into adjacent connected vegetation.

These results indicate that supplying field-confirmed object identity and approximate location can substantially improve task localization, but a single positive point does not guarantee separation of an individual crown from surrounding vegetation.

No prompts, thresholds, masks, or model settings were modified after inspecting these outputs.

Differences between BEFORE and AFTER mask geometry or area are not interpreted as pruning effects, biological change, canopy gain, or canopy loss. The standardized images differ in viewing orientation, and Phase B3 currently evaluates prompt-guided segmentation behavior rather than temporal change.

### PT_02 alleyway extension

The same single-positive-point B3 protocol was extended to PT_02 as a dense-canopy stress test.

Field work established a count of 22 trees within the alleyway study area, but precise tree-level GPS coordinates were unavailable. The 22 presumed tree locations were therefore manually registered to the standardized aerial imagery using neutral identifiers A01 through A22.

Unlike PT_R1, the PT_02 identifiers do not assert confirmed physical tree identity. They represent field-count-constrained registration slots placed using the best available field-informed interpretation of the aerial imagery.

The BEFORE and AFTER images were registered independently. Registration confidence was recorded separately for every PT_02 point as high, medium, or low. These confidence labels describe uncertainty in the manual field-to-image registration and were not supplied to SAM2 as model inputs.

### PT_02 frozen registration inputs

| Condition | High | Medium | Low | Field-point CSV SHA-256 |
| --- | ---: | ---: | ---: | --- |
| Before | 2 | 4 | 16 | `43bc6786e2c558dcd5044f8f140f730817e68b445d1a48ed242f18d2bafb20ed` |
| After | 5 | 6 | 11 | `f77cc5998ca4e0d6a6eff03c3174cb3dd3ca3bddf8ddd9a7166cee2cec6f64b6` |

### PT_02 frozen SAM2 outputs

| Condition | Point prompts | Masks | Runtime (s) | Peak GPU memory (MB) | Output SHA-256 |
| --- | ---: | ---: | ---: | ---: | --- |
| Before | 22 | 22 | 4.65 | 709.73 | `f1aaec9771179d46ecf6ecc1aaa8db69775680eab2826ec5344801cf390b8fdf` |
| After | 22 | 22 | 4.76 | 709.73 | `c16a21b65bc7d0c2ff1dc257c625be7f8cc97794a54dfea301c69270e32eb45b` |

The one-to-one relationship between point prompts and masks is imposed by the inference protocol and must not be interpreted as successful detection of 22 individual trees.

### PT_02 tree-level output metadata

| Registration | Before predicted IoU | Before area (pixels) | After predicted IoU | After area (pixels) |
| --- | ---: | ---: | ---: | ---: |
| A01 | 0.8984 | 175956 | 0.8945 | 154429 |
| A02 | 0.8125 | 20781 | 0.8359 | 44601 |
| A03 | 0.8789 | 162978 | 0.8945 | 146147 |
| A04 | 0.8320 | 111554 | 0.8438 | 114867 |
| A05 | 0.8164 | 110891 | 0.8359 | 114625 |
| A06 | 0.8359 | 119186 | 0.8359 | 114109 |
| A07 | 0.2432 | 270846 | 0.8398 | 115926 |
| A08 | 0.3887 | 425688 | 0.5625 | 153102 |
| A09 | 0.4121 | 1148681 | 0.8086 | 169133 |
| A10 | 0.3906 | 1372468 | 0.3945 | 192580 |
| A11 | 0.3789 | 961060 | 0.8711 | 135547 |
| A12 | 0.3730 | 921138 | 0.8750 | 133622 |
| A13 | 0.4590 | 949326 | 0.8789 | 136551 |
| A14 | 0.9023 | 488398 | 0.8438 | 143407 |
| A15 | 0.8945 | 472089 | 0.9180 | 389236 |
| A16 | 0.9023 | 441998 | 0.9180 | 390848 |
| A17 | 0.9023 | 451541 | 0.8984 | 380344 |
| A18 | 0.9141 | 466830 | 0.9336 | 386559 |
| A19 | 0.9141 | 438840 | 0.9102 | 386825 |
| A20 | 0.9297 | 442814 | 0.9141 | 371453 |
| A21 | 0.9258 | 442344 | 0.9180 | 373552 |
| A22 | 0.8867 | 452889 | 0.8633 | 32253 |

As with PT_R1, the reported predicted IoU values are SAM2 internal mask-quality estimates rather than measured IoU against manually delineated crown ground truth.

### PT_02 interpretation

The PT_02 results demonstrate a substantially more difficult segmentation setting than PT_R1. Visual inspection showed that single positive points frequently produced large masks spanning connected vegetation rather than cleanly separating presumed individual crowns.

This behavior was particularly apparent within the dense alleyway vegetation corridor. Some spatially isolated registrations produced more locally constrained masks, while many registrations within contiguous canopy produced shared or merged vegetation regions.

The PT_02 results therefore reinforce an important limitation of minimal point guidance: providing approximate object location can constrain segmentation to the relevant part of the scene, but it does not by itself supply the boundary information required to separate individual crowns where neighboring vegetation is visually continuous.

Registration confidence and SAM2 mask quality describe different uncertainties. Registration confidence records uncertainty in placing the field-informed point on the aerial image. SAM2 predicted IoU records the model's internal estimate of its resulting mask quality. Neither quantity independently establishes individual-tree segmentation accuracy.

No PT_02 points, confidence labels, SAM2 thresholds, masks, or model settings were modified after inspecting the resulting segmentations.

BEFORE and AFTER PT_02 masks are not interpreted as tree-level temporal change. The A01 through A22 identifiers represent independently registered slots rather than confirmed longitudinal physical-tree identities, and differences in mask area or geometry may reflect viewing conditions, manual registration uncertainty, canopy connectivity, or model behavior.