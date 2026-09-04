# GO-CAM Mega Viewer

Interactive connectivity viewer for GO-CAM models. Enter one or more GO-CAM
model IDs (e.g. `gomodel:6918f23700000035`), click **Build graph**, and the app
fetches each model **live** from the GO production API
(`api.geneontology.org`) and merges them into a single network — activity units
that share a GO annotation become shared "bridge" nodes across models.

Self-contained single page (Cytoscape inlined). Only **production** GO-CAM
models are available via the public API; unreleased/dev models return "not found".

Live app: see the GitHub Pages URL for this repo.
