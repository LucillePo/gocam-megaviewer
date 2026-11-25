#!/usr/bin/env python3
"""Build the interactive GO-CAM connectivity APP (app.html).

Unlike build_graph.py (which bakes one fixed graph), this embeds a CACHE of
compact per-model records for every model in models/. The page then does the
merge in the browser: you type a list of model IDs, hit Build, and it computes
the connected graph client-side, with draggable boxes and save/restore layout.
"""
import glob
import json
import os

import yaml

import merge  # reuse label/molecule helpers

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)          # skill root (holds vendor/)
WORK = os.environ.get("GOCAM_DIR") or os.getcwd()  # working dir (models/, app.html, layout.json)
HERE = WORK
MODELS_DIR = os.path.join(WORK, "models")
OUT = os.path.join(WORK, "app2.html")
VENDOR_DIR = os.path.join(SKILL_DIR, "vendor")

CAUSAL = {
    "RO:0002629": ("directly positively regulates", "pos"),
    "RO:0002630": ("directly negatively regulates", "neg"),
    "RO:0002304": ("causally upstream of, positive effect", "pos"),
    "RO:0002305": ("causally upstream of, negative effect", "neg"),
    "RO:0002413": ("provides input for", "input"),
    "RO:0002411": ("causally upstream of", "input"),
}
MOLPRED = {
    "RO:0002233": "has input",
    "RO:0002234": "has output",
    "RO:0012001": "has small molecule activator",
    "RO:0012002": "has small molecule inhibitor",
}


_PO, _OI, _HI, _HO = "BFO:0000050", "BFO:0000066", "RO:0002233", "RO:0002234"

def minerva_index(path):
    """Index a raw Minerva JSON model: individual id -> (type id, label), and subject -> facts."""
    if not os.path.exists(path):
        return None
    d = json.load(open(path))
    ind, by = {}, {}
    for i in d.get("individuals", []):
        t = (i.get("type") or [{}])[0]
        ind[i["id"]] = (t.get("id"), t.get("label") or t.get("id"))
    for f in d.get("facts", []):
        by.setdefault(f["subject"], []).append(f)
    return {"ind": ind, "by": by}

def part_of_chain(mx, node, limit=5):
    """Follow part_of from an individual: [{id,label}, ...] (nearest first)."""
    out, seen = [], set()
    while node and len(out) < limit:
        nxt = [f["object"] for f in mx["by"].get(node, []) if f["property"] == _PO]
        if not nxt or nxt[0] in seen:
            break
        node = nxt[0]; seen.add(node)
        tid, lbl = mx["ind"].get(node, (node, node))
        out.append({"id": tid, "label": lbl})
    return out

def enrich_from_minerva(rec, mx):
    """Add bp_chain / cc_chain (part_of chains) and protein inputs/outputs to an activity record."""
    if not mx:
        return rec
    facts = mx["by"].get(rec["local_id"], [])
    bp_ind = next((f["object"] for f in facts if f["property"] == _PO), None)
    cc_ind = next((f["object"] for f in facts if f["property"] == _OI), None)
    rec["bp_chain"] = part_of_chain(mx, bp_ind) if bp_ind else []
    rec["cc_chain"] = part_of_chain(mx, cc_ind) if cc_ind else []
    prot = []
    for f in facts:
        if f["property"] in (_HI, _HO):
            tid, lbl = mx["ind"].get(f["object"], (None, None))
            if tid and not str(tid).startswith("CHEBI:"):
                prot.append(["has input" if f["property"] == _HI else "has output", lbl, tid])
    rec["prot_io"] = prot
    # where each molecule individual is (located in, RO:0001025): appended as mols[i][4], mols[i][5] (user 2026-10-26)
    for m in rec.get("mols", []):
        loc = next((f["object"] for f in mx["by"].get(m[3], []) if f["property"] == "RO:0001025"), None)
        lid, llbl = mx["ind"].get(loc, (None, None)) if loc else (None, None)
        m[4:] = [lid, llbl]
    return rec

def extract_activity(act, labels, molterms):
    eb = act.get("enabled_by") or {}
    parts = eb.get("has_part") or []
    mf = (act.get("molecular_function") or {}).get("term")
    bp = (act.get("part_of") or {}).get("term")
    cc = (act.get("occurs_in") or {}).get("term")
    # cell / anatomy the CC is part_of (CellTypeAssociation chain), e.g. CL:0000604 retinal rod cell
    cell_ids = []
    po = (act.get("occurs_in") or {}).get("part_of")
    while po and po.get("term"):
        cell_ids.append(po["term"]); po = po.get("part_of")
    cell_id = cell_ids[0] if cell_ids else None
    cell = " / ".join(labels.get(c, c) for c in cell_ids) if cell_ids else None
    mols = []
    for ma in act.get("molecular_associations", []) or []:
        pl = MOLPRED.get(ma.get("predicate"), ma.get("predicate"))
        molid = ma.get("molecule")              # the specific molecule INDIVIDUAL
        mt = molterms.get(molid, molid)
        mols.append([pl, labels.get(mt, mt), mt, molid])
    edges = []
    for ca in act.get("causal_associations", []) or []:
        lbl, cls = CAUSAL.get(ca.get("predicate"), (ca.get("predicate"), "input"))
        edges.append({"cls": cls, "label": lbl,
                      "downstream": ca.get("downstream_activity")})
    return {
        "local_id": act["id"],
        "gp": labels.get(eb.get("term"), eb.get("term")),
        "gp_id": eb.get("term"),
        "is_complex": bool(parts),
        # sorted by ID so complex_parts[i] <-> complex_part_ids[i] stay aligned (QC pairs label with accession)
        "complex_parts": [labels.get(p.get("term"), p.get("term")) for p in sorted(parts, key=lambda p: p.get("term") or "")],
        "complex_part_ids": sorted(p.get("term") for p in parts),
        "mf": labels.get(mf, mf), "mf_id": mf,
        "bp": labels.get(bp, bp), "bp_id": bp,
        "cc": labels.get(cc, cc), "cc_id": cc,
        "cell": cell, "cell_id": cell_id,
        "mols": mols,
        "edges": edges,
    }


def main():
    models = merge.load_models()
    labels = merge.label_map(models)
    # which server each model came from (written by fetch_live.py / refresh.sh): "live" or "DEV"
    srcs = {}
    sp = os.path.join(MODELS_DIR, "_sources.txt")
    if os.path.exists(sp):
        for line in open(sp):
            parts = line.split()
            if len(parts) >= 2:
                srcs["gomodel:" + parts[0].replace("gomodel:", "")] = parts[1].lower()
    cache = {}
    for mid, m in models.items():
        molterms = merge.molecule_terms(m)
        mx = minerva_index(os.path.join(MODELS_DIR, mid.split(":")[1] + ".minerva.json"))
        cache[mid] = {
            "id": mid,
            "title": m.get("title", mid),
            "status": m.get("status"),
            "_src": srcs.get(mid, "live"),   # baked from barista (live, or dev if not on live) — never the API snapshot
            "activities": [enrich_from_minerva(extract_activity(a, labels, molterms), mx)
                           for a in (m.get("activities", []) or [])],
        }
    default_ids = ""  # open with an empty box; the user types model IDs themselves

    # Optional saved layout/colours baked in as defaults (survives reopen even
    # though Jupyter's sandbox blocks localStorage). Populate layout.json from
    # the app's "save layout" blob.
    default_state = {}
    layout_path = os.path.join(HERE, "layout.json")
    if os.path.exists(layout_path):
        try:
            with open(layout_path) as fh:
                default_state = json.load(fh)
        except Exception as e:
            print(f"  (warning: could not read layout.json: {e})")

    libs = []
    for fn in ("cytoscape.min.js", "dagre.min.js", "cytoscape-dagre.min.js",
               "cytoscape-node-html-label.min.js"):
        p = os.path.join(VENDOR_DIR, fn)
        with open(p) as fh:
            libs.append(f"<!-- {fn} -->\n<script>{fh.read()}</script>")

    html = (APP_HTML
            .replace("__LIBS__", "\n".join(libs))
            .replace("__CACHE__", json.dumps(cache))
            .replace("__BUILD__", __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"))
            .replace("__DEFAULT_STATE__", json.dumps(default_state))
            .replace("__DEFAULT_IDS__", default_ids))
    with open(OUT, "w") as fh:
        fh.write(html)
    print(f"Wrote {OUT}")
    print(f"  cached {len(cache)} models, "
          f"{sum(len(c['activities']) for c in cache.values())} activity units"
          + (f"; baked-in layout for {len(default_state.get('layout', {}))} units" if default_state else ""))


# APP_HTML is assembled from parts in build_app_html.py to keep files readable.
from build_app_html import APP_HTML  # noqa: E402

if __name__ == "__main__":
    main()
