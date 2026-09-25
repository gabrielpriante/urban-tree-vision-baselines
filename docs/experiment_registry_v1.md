# Experiment Registry v1.0

## Study Scope

- **Study:** Multi-model urban tree benchmark
- **Sites:** PT_R1 and PT_02
- **Conditions:** BEFORE and AFTER
- **Collection periods:** Week 1, Week 3, Week 4
- **Target image count:** 12 standardized RGB drone images
- **Primary outcome:** estimated individual-tree count
- **Secondary outcome:** repeatability of predicted counts across collection weeks
- **Field truth:** defined independently from model outputs
- **Freeze rule:** no prompts, thresholds, inference settings, or field annotations may be changed in response to Week 3 or Week 4 results

## Week 3 Input Registry

| Image ID | Site | Condition | Week | Source path | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| PT-R1-BEFORE-WEEK3 | PT_R1 | BEFORE | 3 | `C:\Users\gabpe\OneDrive\Documents\work\frontlinegig\drones\drone-footage\wilkinsburg\week-3\STANDARDIZED-IMAGERY\BEFORE\PT-R1-BEFORE-WEEK3.JPG` | Pending |
| PT-R1-AFTER-WEEK3 | PT_R1 | AFTER | 3 | `C:\Users\gabpe\OneDrive\Documents\work\frontlinegig\drones\drone-footage\wilkinsburg\week-3\STANDARDIZED-IMAGERY\AFTER\PT-R1-AFTER-WEEK3.JPG` | Pending |
| PT-02-BEFORE-WEEK3 | PT_02 | BEFORE | 3 | Pending | Pending |
| PT-02-AFTER-WEEK3 | PT_02 | AFTER | 3 | Pending | Pending |

**Provenance** here simply means the record showing where each image came from and exactly which file was used. For this experiment, provenance includes the source path, site, condition, collection week, filename, and SHA-256 hash once verified.

## Repeated Model / Pipeline Registry

| ID | Method | Input | Frozen configuration | Independent tree count? | Primary role |
| --- | --- | --- | --- | --- | --- |
| M01 | DeepForest Native | Native standardized RGB JPEG | Pretrained DeepForest 2.1.0; existing native-resolution settings; no fine-tuning | Yes | Native-resolution tree detection |
| M02 | DeepForest GSD-Corrected | RGB resampled to established 7.89 cm/pixel deployment scale | Same pretrained DeepForest model and inference settings as M01 | Yes | Scale-corrected tree detection |
| M03 | TreeCountSegHeight | RGB resampled to 20 cm/pixel | Official pretrained RGB model; segmentation threshold 0.5; official packaged defaults otherwise | Yes | Density-based tree-count baseline |
| M04 | SAM2 Automatic | Native standardized RGB JPEG | SAM2.1 Hiera Base+; points_per_side=32; points_per_batch=4; predicted IoU threshold=0.80; stability threshold=0.95; no crop layers; no postprocessing | No | Unguided segmentation baseline |
| M05 | DeepForest GSD -> SAM2 | Native RGB + frozen M02 boxes | One frozen M02 box per SAM2 prompt; multimask_output=false; no manual filtering or correction | No | Machine-guided segmentation refinement |
| M06 | TreePseCo | Standardized RGB imagery | Not open source; use only a legitimate reproducible author-supported implementation/access path; no local reconstruction labeled as TreePseCo; no local fine-tuning | Yes, if executable | Specialized crown-instance baseline |
| M07 | SAM3-family instance segmentation | Native standardized RGB JPEG | Exact model/checkpoint frozen before first Week 3 run; text concept `tree crown`; no points; no boxes; no prompt refinement | Yes | Open-vocabulary tree-crown instance detection |
| M08 | Claude | One untouched standardized RGB JPEG | Fresh chat; one image; frozen VLM prompt; no prior context; no follow-up; no field truth | Yes | General multimodal model visual count |
| M09 | ChatGPT | One untouched standardized RGB JPEG | Fresh chat; one image; frozen VLM prompt; no prior context; no follow-up; no field truth | Yes | General multimodal model visual count |
| M10 | Gemini | One untouched standardized RGB JPEG | Fresh chat; one image; frozen VLM prompt; no prior context; no follow-up; no field truth | Yes | General multimodal model visual count |
| M11 | Microsoft Copilot | One untouched standardized RGB JPEG | Fresh chat; one image; frozen VLM prompt; no prior context; no follow-up; no field truth | Yes | General multimodal product visual count |

## Historical Attempted Baselines

| ID | Method | Status | Repeated across 12 images? |
| --- | --- | --- | --- |
| A01 | DINOv3 + dino.txt | Successfully attempted earlier; poor task match under tested zero-shot configuration | No |
| A02 | Detectree2 | Environment established; execution blocked by pretrained checkpoint/artifact availability | No |
| A03 | TreeCrownDelineation | Investigated; available pretrained configuration incompatible with RGB-only imagery | No |

These attempted methods remain part of the methodological record even though they are not completed 12-image benchmark conditions.

## Frozen VLM Prompt

> Examine this single overhead RGB drone image. Count the number of distinct individual trees visible in the image. Treat each visually distinguishable tree crown as one tree, including when neighboring crowns touch. Do not count shrubs, vines, herbaceous vegetation, buildings, shadows, or other non-tree objects. Use only the image provided. Return only one integer representing your estimated tree count.

## Primary Count Metrics

For methods that independently produce a tree count:

- `predicted_count`
- `field_count`
- `signed_error = predicted_count - field_count`
- `absolute_error`
- `percent_error`
- `week`
- `site`
- `condition`
- `image_sha256`
- `method`
- `model_version`

Across repeated collection weeks:

- mean predicted count
- standard deviation
- coefficient of variation
- minimum
- maximum
- range
- mean absolute error

## Secondary Outputs Retained

Where available, preserve:

- bounding boxes
- confidence scores
- segmentation masks
- mask areas
- model-internal quality scores
- inference runtime
- peak GPU memory
- preprocessing metadata
- source revision
- checkpoint identifier
- checkpoint SHA-256

## Interpretation Rules

- M01, M02, M03, M06, M07, M08, M09, M10, and M11 may participate directly in tree-count comparison when they produce autonomous counts.
- M04 automatic SAM2 mask counts are generic scene-mask counts and must not be labeled tree counts.
- M05 mask count is inherited from M02 because one SAM2 mask is generated per DeepForest box.
- BEFORE and AFTER differences are not automatically interpreted as biological change, pruning effects, canopy gain, or canopy loss.
- Field counts are never disclosed to models before inference.
- No selective reruns are allowed because a result appears implausible.
- No Week 3 or Week 4 result may be used to retune an already frozen benchmark configuration.

## Week 3 Execution Order

1. M01 DeepForest Native
2. M02 DeepForest GSD-Corrected
3. M03 TreeCountSegHeight
4. M04 SAM2 Automatic
5. M05 DeepForest GSD -> SAM2
6. M07 SAM3-family
7. M08 Claude
8. M09 ChatGPT
9. M10 Gemini
10. M11 Microsoft Copilot
11. M06 TreePseCo once reproducible access/setup is resolved

## Status

- Registry version: **v1.0**
- Week 3 PT_R1 image paths: **registered**
- Week 3 PT_02 image paths: **pending**
- Week 3 image hashes: **pending**
- Week 4 imagery: **pending collection**
