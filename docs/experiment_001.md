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

## Phase B: SAM2 spatial-guidance experiments

Phase B evaluates how a general-purpose segmentation model behaves under progressively stronger forms of spatial guidance.

The sequence is:

1. B1: no task-specific spatial guidance.
2. B2: machine-generated DeepForest bounding-box guidance.
3. B3: field-informed positive-point guidance.

All Phase B experiments use the same pretrained SAM2.1 Hiera Base+ model without local fine-tuning.

The SAM2 checkpoint used throughout Phase B is:

`models/sam2/checkpoints/sam2.1_hiera_base_plus.pt`

Checkpoint SHA-256:

`a2345aede8715ab1d5d31b4a509fb160c5a4af1970f199d9054ccfb746c004c5`

The official Meta SAM2 source was pinned to commit:

`2b90b9f5ceec907a1c18123530e92e794ad901a4`

Inference used CUDA with bfloat16 precision on an NVIDIA GeForce RTX 5070 Laptop GPU.

## Phase B1: Automatic SAM2 masks

Phase B1 evaluates SAM2 without tree-specific prompts.

The objective is to establish how the general segmentation model partitions the standardized aerial scenes when given no information about which objects should be treated as trees.

### Automatic-mask protocol

- Model: SAM2.1 Hiera Base+.
- Source imagery: native 8192 x 6144 standardized RGB JPEGs.
- Prompt generation: automatic point grid.
- Points per side: 32.
- Points per batch: 4.
- Predicted IoU threshold: 0.80.
- Stability-score threshold: 0.95.
- Crop layers: none.
- Mask representation: RLE.
- Additional model postprocessing: none.
- Inference precision: CUDA bfloat16.
- No tree-specific prompts were supplied.
- No local fine-tuning was performed.
- No manual filtering or ground-truth-informed threshold adjustment was performed.

The point batch size was reduced to four for GPU-memory compatibility before any successful automatic-mask result was inspected. This hardware adjustment did not alter the spatial prompt grid or mask-quality thresholds.

### Frozen automatic-mask outputs

| Image | Condition | SAM2 masks | Runtime (s) | Peak GPU memory (MB) |
| --- | --- | ---: | ---: | ---: |
| PT_R1 | Before | 91 | 12.36 | 4533 |
| PT_R1 | After | 96 | 23.61 | 4533 |
| PT_02 | Before | 93 | 17.76 | 4889 |
| PT_02 | After | 93 | 18.48 | 4701 |

The reported mask counts are generic SAM2 scene-segmentation outputs. They are not tree counts and must not be interpreted as numbers of individual crowns.

### B1 interpretation

Without task-specific guidance, SAM2 generated high-confidence masks across many types of visible scene structure.

The automatic outputs included visually coherent vegetation and tree-canopy regions, but they also segmented substantial non-tree content such as built surfaces and other scene objects.

B1 therefore demonstrates that generic SAM2 segmentation can identify meaningful spatial structure in high-resolution nadir RGB imagery, but automatic mask generation alone does not provide a tree-specific inventory or individual-crown delineation system.

No B1 masks or model settings were manually corrected after inspection.

## Phase B2: DeepForest-guided SAM2

Phase B2 evaluates whether tree-detector bounding boxes can provide useful machine-generated spatial guidance to SAM2.

DeepForest predictions were generated and frozen before SAM2 segmentation. Each frozen DeepForest bounding box was then used as one SAM2 box prompt.

No DeepForest box was manually removed, corrected, or replaced based on field observations or SAM2 output.

### DeepForest prompt source

The DeepForest deployment used imagery resampled to an effective GSD of 7.89 cm/pixel.

The derived DeepForest images were 1734 x 1300 pixels, while SAM2 operated on the corresponding native 8192 x 6144 RGB images.

DeepForest bounding boxes were mapped from the derived-image coordinate space back to native-image coordinates using the exact horizontal and vertical scale ratios between the two image dimensions.

### Frozen DeepForest box counts

| Image | Condition | DeepForest box prompts |
| --- | --- | ---: |
| PT_R1 | Before | 293 |
| PT_R1 | After | 302 |
| PT_02 | Before | 386 |
| PT_02 | After | 412 |

These values represent frozen DeepForest detections supplied as SAM2 prompts. They are not assumed to represent unique physical trees because DeepForest predictions may contain false positives, duplicate detections, or multiple detections associated with connected vegetation.

### SAM2 box-prompt protocol

- Model: SAM2.1 Hiera Base+.
- Source imagery: native 8192 x 6144 standardized RGB JPEGs.
- Prompt type: one frozen DeepForest bounding box per SAM2 prediction.
- Multimask output: false.
- One SAM2 mask retained per DeepForest box prompt.
- Manual mask selection: none.
- Additional SAM2 postprocessing: none.
- Local fine-tuning: none.
- Ground-truth-informed prompt filtering: none.

### Frozen DeepForest-guided outputs

| Image | Condition | Box prompts | SAM2 masks | Runtime (s) |
| --- | --- | ---: | ---: | ---: |
| PT_R1 | Before | 293 | 293 | 50.53 |
| PT_R1 | After | 302 | 302 | 52.46 |
| PT_02 | Before | 386 | 386 | 67.05 |
| PT_02 | After | 412 | 412 | 72.32 |

The one-to-one relationship between DeepForest box prompts and SAM2 masks is imposed by the inference protocol. These mask counts therefore must not be interpreted as independent SAM2 tree detections.

### B2 interpretation

DeepForest guidance substantially narrowed SAM2 segmentation toward regions that the tree detector had identified as candidate crowns.

Compared with B1 automatic segmentation, the B2 outputs contained substantially less unrelated scene segmentation because SAM2 was no longer being asked to segment arbitrary visible objects.

However, B2 inherits the behavior of the upstream detector. False-positive boxes, duplicate detections, and poorly localized DeepForest predictions can each generate corresponding SAM2 masks.

The experiment therefore separates two tasks that are otherwise easy to conflate:

1. DeepForest determines where candidate trees may be located.
2. SAM2 determines the segmentation geometry produced within each supplied detector prompt.

Improved segmentation geometry does not independently validate the underlying detector prediction as a unique physical tree.

No DeepForest prompts or resulting SAM2 masks were manually altered after output inspection.

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

## Phase B conclusion

Phase B establishes a progressive spatial-guidance comparison for pretrained SAM2 on standardized urban drone imagery.

B1 showed that unguided automatic mask generation can segment visually coherent scene structure but does not distinguish tree crowns from other visible objects.

B2 showed that machine-generated DeepForest boxes substantially focus SAM2 on candidate tree locations, but the resulting segmentation workflow inherits detector false positives, duplicates, and localization errors.

B3 showed that field-informed point prompts can provide much stronger task localization when the target trees can be registered confidently. PT_R1 produced several locally plausible crown masks from minimal point guidance, while the dense PT_02 alleyway demonstrated that single points remain insufficient for reliably separating individual crowns within connected vegetation.

Together, the three conditions demonstrate that stronger spatial information progressively reduces the localization problem presented to a general segmentation model, but spatial guidance alone does not solve individual-tree delineation in complex contiguous canopy.

Phase B is complete under the frozen protocols described above. No additional prompt variants, confidence-based filtering, threshold optimization, manual mask correction, or ground-truth-informed tuning are included in this phase.