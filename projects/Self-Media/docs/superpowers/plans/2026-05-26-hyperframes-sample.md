# Hyperframes sample plan - Three-Minute Future VOL.002

## Goal
Create a short Hyperframes sample for the 2026-05-26 issue using the already approved visual framework. The sample must demonstrate real component animation instead of switching flattened page PNGs.

## Scope
- Source data: `daily/2026-05-26/three-minute-future/work/final.json`
- New reusable generator: `lines/three-minute-future/build_hyperframes_sample.py`
- Generated sample project: `lines/three-minute-future/hyperframes/vol-002-sample/`
- Sample output: cover scene plus the first two report scenes.

## Construction Details
- Canvas: 1080 x 1920.
- Cover card: uses the approved constructivist background, with title, subtitle, issue/date, hooks, and count/duration metadata animated as separate layers.
- Report scenes: use original report image assets, source label, title slab, short-news block, and thought block as separate animated components.
- Timing: cover around 6 seconds, each report around 9 seconds. The structure leaves timing hooks for later TTS alignment.
- Motion: fast editorial build, diagonal mask transition, staggered text entrance, subtle image parallax.

## Tradeoffs
- This sample uses only two reports so we can verify the motion language quickly.
- It does not generate or choose TTS audio. The user will choose TTS voice later.
- It does not replace the full Remotion draft yet.

## Deliverables
- Hyperframes project with `index.html`, `DESIGN.md`, and local assets.
- CLI lint/inspect results.
- Preview URL if the preview server starts.
- MP4 sample if Hyperframes render can complete on this machine.

## Verification
- `npx hyperframes lint`
- `npx hyperframes inspect`
- Preview through Hyperframes Studio.
- Rendered MP4 if FFmpeg/FFprobe are available.
