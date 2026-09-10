# Urban Tree Vision Baselines

Reproducible evaluation of pretrained computer vision models for individual tree detection and segmentation in standardized urban drone imagery.

## Overview

This repository contains a reproducible research pipeline for evaluating pretrained computer vision models on standardized RGB drone imagery of urban vegetation.

The project examines how different model families behave under increasingly informative inputs, beginning with pretrained RGB baselines and progressing toward spatially guided segmentation.

The central goal is not to optimize models against the available field observations. Instead, model configurations, prompts, and preprocessing decisions are frozen before evaluation whenever possible so that observed behavior can be interpreted without ground-truth-informed tuning.

Experiment 001 currently includes:

1. Pretrained individual tree detection with DeepForest.
2. Zero-shot semantic analysis using DINOv3-based methods.
3. Pretrained RGB canopy segmentation and density estimation with TreeCountSegHeight.
4. Automatic segmentation with SAM2.
5. DeepForest box-guided SAM2 segmentation.
6. Field-informed point-guided SAM2 segmentation.

Additional geometric and photogrammetric baselines are planned in later phases.

## Research Questions

The current experiments examine several related questions:

- How well do pretrained tree-specific models transfer to high-resolution urban drone imagery without local fine-tuning?
- How does a general-purpose segmentation model behave when given no task-specific spatial guidance?
- How does SAM2 behavior change when spatial guidance comes from an upstream tree detector?
- How does SAM2 behavior change when spatial guidance comes from field-informed tree locations?
- Where do pretrained RGB models fail when vegetation is dense, contiguous, or visually ambiguous?
- Which implementation and preprocessing decisions must be recorded for these comparisons to remain reproducible?

## Experiment 001

Experiment 001 evaluates pretrained models on standardized RGB imagery collected under paired BEFORE and AFTER conditions.

The images are analyzed independently. Differences between BEFORE and AFTER model outputs are not automatically interpreted as biological change, pruning effects, canopy gain, or canopy loss.

The paired images differ in viewing conditions and orientation, and several methods are sensitive to localization, canopy connectivity, preprocessing, or prompt placement.

### Phase A: Pretrained RGB baselines

Phase A establishes model behavior before field-guided prompting or local fine-tuning.

Methods evaluated include:

- DeepForest individual tree crown detection.
- DINOv3-based zero-shot semantic segmentation.
- TreeCountSegHeight RGB canopy segmentation and density-based counting.

Additional candidate baselines were investigated but excluded when their official pretrained artifacts or required input modalities were not suitable for the available RGB imagery.

### Phase B: SAM2 spatial guidance

Phase B evaluates the same pretrained SAM2 model under progressively stronger spatial guidance.

#### B1: Automatic segmentation

SAM2 receives no tree-specific prompt information.

The model generates high-confidence scene masks across vegetation, built surfaces, and other visible objects.

These masks are generic scene-segmentation outputs and are not interpreted as tree counts.

#### B2: DeepForest-guided segmentation

Frozen DeepForest detections are mapped back to native image coordinates and supplied to SAM2 as bounding-box prompts.

This substantially narrows SAM2 toward candidate tree locations, but the resulting workflow inherits false positives, duplicates, and localization errors from the upstream detector.

#### B3: Field-informed point-guided segmentation

Field-informed tree locations are supplied to SAM2 using one positive point per registered location.

Two registration settings are currently represented:

- `PT_R1`: nine field-confirmed trees manually registered to the aerial imagery.
- `PT_02`: twenty-two field-count-constrained locations registered within a dense alleyway vegetation corridor.

For `PT_02`, high, medium, or low confidence is recorded for each manual registration. These confidence labels describe uncertainty in the human field-to-image registration and are not supplied to SAM2 as model inputs.

The results show that stronger spatial information can substantially improve task localization, but a single positive point does not guarantee individual-crown separation when neighboring vegetation is visually continuous.

## Experimental Guardrails

The project follows several rules intended to separate model behavior from later evaluation.

- Original standardized imagery remains unchanged.
- Model versions and checkpoints are recorded explicitly.
- Important model artifacts and research inputs are verified using SHA-256 hashes.
- Inference parameters are stored explicitly rather than relying on undocumented defaults.
- Raw model predictions are retained.
- Derived visualizations do not replace raw predictions.
- Model outputs are frozen before field-based evaluation whenever applicable.
- Field observations are not used to optimize baseline thresholds.
- Manual corrections are not applied to frozen predictions.
- Prompt locations are not adjusted after viewing SAM2 output.
- BEFORE and AFTER outputs are not treated as automatic evidence of temporal change.
- Large imagery, generated outputs, and downloaded model weights are excluded from Git.

## Reproducibility

The repository records enough information to reconstruct the main inference conditions used in each experiment.

Depending on the model, this includes:

- Input image identity.
- Input dimensions.
- Input SHA-256.
- Model name and version.
- Model checkpoint.
- Checkpoint SHA-256.
- Upstream source revision.
- Preprocessing configuration.
- Prompt construction method.
- Inference thresholds.
- Software environment.
- Hardware device.
- Runtime.
- Peak GPU memory usage.
- Raw prediction location.

The SAM2 experiments use a pinned official SAM2 source revision and a verified SAM2.1 Hiera Base+ checkpoint.

## Data and Outputs

Large research artifacts are intentionally excluded from Git.

This includes:

- Native drone imagery.
- Derived imagery.
- Model weights.
- SAM2 checkpoints.
- Large visualization files.
- Raw prediction outputs.

Small structured research inputs, such as frozen point-registration CSV files, may be tracked when they are necessary to reproduce an experiment.

Generated outputs are retained locally in the repository structure but are ignored by Git.

## Repository Structure

```text
urban-tree-vision-baselines/
├── configs/
│   └── treecountsegheight/
├── data/
│   ├── README.md
│   ├── raw/
│   ├── derived/
│   └── annotations/
├── docs/
│   └── experiment_001.md
├── environments/
├── models/
│   └── sam2/
├── outputs/
├── scripts/
├── src/
│   └── treevision/
├── tests/
├── tools/
│   └── point_register.html
├── .gitattributes
├── .gitignore
├── .python-version
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock