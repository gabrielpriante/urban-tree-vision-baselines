# Urban Tree Vision Baselines

Reproducible evaluation of pretrained computer vision models for individual tree detection in standardized urban drone imagery.

## Overview

This repository contains a reproducible analysis pipeline for testing pretrained computer vision models on standardized RGB drone imagery collected before and after field work.

The project begins with two model families:

1. DeepForest for pretrained individual tree crown detection.
2. DINOv3-based approaches for pretrained and zero-shot visual analysis.

The initial experiments are intentionally performed without local fine-tuning so that model behavior can be evaluated before information from the field inventory is introduced.

## Experiment 001

The first experiment evaluates pretrained models on paired standardized imagery collected under before and after conditions.

The initial workflow is:

1. Preserve the original standardized imagery.
2. Run pretrained DeepForest inference.
3. Save raw predictions and inference metadata.
4. Run a DINOv3-based baseline on the same imagery.
5. Save raw predictions and inference metadata.
6. Freeze model outputs before comparison with field observations.

No local fine-tuning, manual correction, or ground-truth-informed threshold optimization is used during the baseline inference stage.

## Reproducibility Principles

This project follows several reproducibility rules:

- Model versions are recorded explicitly.
- Model identifiers and checkpoints are recorded explicitly.
- Inference parameters are stored explicitly rather than relying on undocumented defaults.
- Original input imagery is preserved unchanged.
- Raw model predictions are retained.
- Derived visualizations do not replace raw predictions.
- Field validation occurs after baseline predictions have been generated.
- Large imagery and downloaded model weights are not stored directly in the Git repository.

## Repository Structure

```text
urban-tree-vision-baselines/
├── configs/
├── data/
├── docs/
├── outputs/
├── scripts/
├── src/
│   └── treevision/
└── tests/