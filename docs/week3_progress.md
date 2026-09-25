# Week 3 Benchmark Progress

## Input Images

- PT_R1 BEFORE SHA-256: `6f9b0c5d0f65bc9201153eb7ff4460cf620cbc7842a51df090e633d249bde9c9`
- PT_R1 AFTER SHA-256: `18e0835a58da6a97601bec1db088f8f611f1b26d5e7fdc4b711ba56999e4f393`
- PT_02 BEFORE SHA-256: `fbb8a74a05c2e8730fb9bed565b9935ff6256e276fb791ed66660f3f9ee98a98`
- PT_02 AFTER SHA-256: `d93ac2b2d5f76169790fe78563ee08436de237e04b1fb9b1027a3dd19f047aef`

## M01 DeepForest Native

| Image | Detections | Prediction CSV SHA-256 |
| --- | ---: | --- |
| PT_R1 BEFORE | 3013 | `54ed2c5d7c08669bcc358a53f2bb0d4bcd112598dffaa454db16c57e3ce4c413` |
| PT_R1 AFTER | 3949 | `df38cad3f1138a1ece57ebeec54cc87eb6c3f349882483595ca13695c4f6159d` |
| PT_02 BEFORE | 4002 | `58f9c736dc417e806f378b20836223b274e541147603d86652b229b01e1dc547` |
| PT_02 AFTER | 5545 | `fa9f8568707f6b27a9cfd0147be6e866ed7d6b7b91323589be025b92b221b3f8` |

## M02 DeepForest GSD-Corrected

Target deployment GSD: `7.89 cm/pixel`.

| Image | Detections | Prediction CSV SHA-256 |
| --- | ---: | --- |
| PT_R1 BEFORE | 273 | `68a26e6ed4ff71c00272fc56d25673aa0d414876310c180ff9a820380564a37d` |
| PT_R1 AFTER | 319 | `c37a5befc46708877a2e9e3992bfaa8da2923ba9e490c391db5735fec746937b` |
| PT_02 BEFORE | 373 | `7489266b9fc62ba55ae0bcc66664c1d16eab3f64309e95d5d918ba09865a5aeb` |
| PT_02 AFTER | 427 | `0d5ad474d3779bd52a1dcdaf0132ed85f48c414f1265ed6c000000aad2591d58` |

## M03 TreeCountSegHeight

Preprocessing is complete for all four Week 3 images.

- Native GSD assumption: `1.67 cm/pixel`
- Target GSD: `20.00 cm/pixel`
- Output dimensions: `684 x 513`
- Resampling: Lanczos
- Format: three-band RGB TIFF

| Image | Derived TIFF SHA-256 |
| --- | --- |
| PT_R1 BEFORE | `63e0cf4a8ae848b09905e36357e81c7b4e27baa30f6d044c286a87f985d2affb` |
| PT_R1 AFTER | `cbf3844bb67ee5cf083f61cdaa4d576924529bd342d1e2be8b21d41c64373f46` |
| PT_02 BEFORE | `fade86a8e5f95e1f6f6712faf0ae2a96fa68f23dd92a9c586e896141558764e7` |
| PT_02 AFTER | `4edc99267737a0a1a95b19aa85723398a6b67e97824ad856769c1962ad2a975e` |

## Exact Resume Point

M03 model inference has **not** started.

Next task:

1. Verify Docker is available.
2. Verify the local official TreeCountSegHeight image.
3. Confirm its digest matches the previously frozen artifact:
   `sha256:fab4a8e16d7bc085440724c9fa522c957dc04299c625fcab7617b87c1c154e13`
4. Inspect `configs/treecountsegheight/hyperps_rgb.yaml`.
5. Run the four Week 3 TreeCountSegHeight Docker inference jobs without modifying the frozen configuration.

No Week 3 TreeCountSegHeight model outputs currently exist.
