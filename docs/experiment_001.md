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