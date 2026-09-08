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