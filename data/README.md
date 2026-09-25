# Data

This directory documents the input data used by the project.

## Raw Imagery

Original drone imagery is stored locally in the `data/raw/` directory.

The `data/raw/` directory is excluded from Git version control.

Original images should remain unchanged after they are added to the project.

## Derived Data

Intermediate or transformed data products may be stored locally in the `data/derived/` directory.

The `data/derived/` directory is excluded from Git version control by default.

- PT-02-BEFORE-WEEK1 Analysis (GIS Derivations)
- PT-02-AFTER-WEEK1 Analysis (GIS Derivations)
- PT-R1-BEFORE-WEEK1 Analysis (GIS Derivations)

## Image Manifest

A machine-readable image manifest will be maintained at `data/manifest.csv`.

The manifest will provide stable identifiers and metadata for every image included in an experiment.

Model inference scripts should reference images through the manifest rather than relying on manually entered file paths.

## Orthomosaic 

From geonadir.com. Uploaded automated imagery from DJI Mini 5 pro and created 10 Orthomosaics on 09/05/2026.

DSM/DTM Derived from Orthomosaic was attained through purchasing the geonadir pro subscription. 

RAW FILES -> Not currently publicly available. Will leverage cloud compute to set up an appropriate evironment.

This is where geonadir/RGB-processing software enters the equation and must be considered as part of our specific questions/research.

Collected 34 species data on 09/19/2026

Identified 2 more trees in R1 w/ expert guidance

Potentially a possible tool + workflow contribution

Transferred species info to input table

Input location data to input table

09/22/2026: Used DSM - DTM to gather estimated tree heights

Currently working on creating AOI based on RGB per orthomosaic.

# Derived Data

