# Data

This directory documents the input data used by the project.

## Raw Imagery

Original drone imagery is stored locally in the `data/raw/` directory.

The `data/raw/` directory is excluded from Git version control.

Original images should remain unchanged after they are added to the project.

## Derived Data

Intermediate or transformed data products may be stored locally in the `data/derived/` directory.

The `data/derived/` directory is excluded from Git version control by default.

## Image Manifest

A machine-readable image manifest will be maintained at `data/manifest.csv`.

The manifest will provide stable identifiers and metadata for every image included in an experiment.

Model inference scripts should reference images through the manifest rather than relying on manually entered file paths.