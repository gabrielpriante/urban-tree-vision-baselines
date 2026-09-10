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