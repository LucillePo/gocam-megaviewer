#!/usr/bin/env python3
"""Fetch GO-CAM models from Noctua LIVE (falling back to DEV) as gocam-yaml, WITHOUT a token.

Uses barista's anonymous read endpoint (minerva_public m3Batch "get"), exactly what the
Noctua web UI uses for read-only viewing, then converts Minerva JSON -> GO-CAM YAML with
gocam-py (same code path as `noctua barista export-model -f gocam-yaml`).
Never uses the api.geneontology.org snapshot. READ-ONLY.

Usage:  python fetch_live.py <workdir>     (reads <workdir>/my-models.txt, writes <workdir>/models/*.yaml)
Run with an interpreter that has gocam + pyyaml (e.g. ~/.local/share/uv/tools/noctua/bin/python).
"""
import json, os, sys, urllib.parse, urllib.request
import yaml
from gocam.translation.minerva_wrapper import MinervaWrapper

SERVERS = [  # (label, base URL) — live first; dev only if the model is not on live
    ("live", "http://barista.berkeleybop.org/api/minerva_public/m3Batch"),
    ("DEV",  "http://barista-dev.berkeleybop.org/api/minerva_public_dev/m3Batch"),
]

def get_minerva(base, model_id):
    req = json.dumps([{"entity": "model", "operation": "get", "arguments": {"model-id": model_id}}])
    url = base + "?" + urllib.parse.urlencode({"requests": req})
    with urllib.request.urlopen(url, timeout=60) as r:
        d = json.load(r)
    if d.get("message-type") != "success" or not d.get("data", {}).get("individuals"):
        return None
    return d["data"]

def to_yaml(model_id, data):
    data.setdefault("id", model_id)
    if "title" not in data:
        data["title"] = next((a["value"] for a in data.get("annotations", []) if a.get("key") == "title"), "Untitled Model")
    m = MinervaWrapper.minerva_object_to_model(data)
    return yaml.dump(m.model_dump(exclude_none=True), default_flow_style=False, sort_keys=False)

def main():
    work = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    lst = os.path.join(work, "my-models.txt"); mdir = os.path.join(work, "models")
    os.makedirs(mdir, exist_ok=True)
    for f in os.listdir(mdir):
        if f.endswith(".yaml"): os.remove(os.path.join(mdir, f))
    ids = []
    for line in open(lst):
        line = line.split("#")[0].strip()
        if not line: continue
        line = line.split("=")[-1]
        ids.append(line[len("gomodel:"):] if line.startswith("gomodel:") else line)
    n = 0
    with open(os.path.join(mdir, "_sources.txt"), "w") as src_out:
        for bare in ids:
            mid = "gomodel:" + bare
            for label, base in SERVERS:
                try:
                    data = get_minerva(base, mid)
                except Exception as e:
                    # live unreachable: stop. Falling back to dev would show an old dev copy of a production model
                    # (curator rule 2026-11-25: live first, dev ONLY if the model is not in production).
                    if label == "live":
                        sys.exit(f"ABORT: live Noctua error for {bare}: {e}")
                    data = None; print(f"  ({label} error for {bare}: {e})", file=sys.stderr)
                if data: break
            else:
                print(f"FAIL {bare} (not on live or dev)"); continue
            state = next((a["value"] for a in data.get("annotations", []) if a.get("key") == "state"), "?")
            date  = next((a["value"] for a in data.get("annotations", []) if a.get("key") == "date"), "?")
            json.dump(data, open(os.path.join(mdir, bare + ".minerva.json"), "w"))   # raw Minerva JSON: keeps ALL annotations (yaml keeps one BP/CC per activity)
            open(os.path.join(mdir, bare + ".yaml"), "w").write(to_yaml(mid, data))
            print(f"OK  [{label:4}] {bare}  state={state} date={date}  {data['title'][:60]}")
            src_out.write(f"{bare} {label}\n"); n += 1
    print(f"--- fetched {n} of {len(ids)} model(s) into {mdir}")
    if n != len(ids):
        sys.exit(f"ABORT: only {n} of {len(ids)} models fetched")

if __name__ == "__main__":
    main()
