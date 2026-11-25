#!/usr/bin/env python3
"""Compute the strict content-based merge of activity units across GO-CAM models.

Merge rule (strict): two activity units are "the same" iff ALL of these match:
  - enabled_by  (gene product, or complex = GO term + sorted has_part members)
  - molecular_function (MF)
  - part_of     (BP, the activity's direct part_of term)
  - occurs_in   (CC)
  - inputs      (sorted molecular_associations: predicate + molecule term)
  - targets     (sorted causal edges: predicate + downstream unit's INTRINSIC key)

Evidence and references are deliberately ignored.
"""
import glob
import os
import re
import sys
import yaml

MODELS_DIR = os.path.join(os.environ.get("GOCAM_DIR") or os.getcwd(), "models")

# species suffix curators append to gene-product labels (e.g. "RHO Hsap"); strip
# it from display labels. Add more codes here if needed.
_SPECIES_SUFFIX = re.compile(r"\s+(Hsap|Mmus|Rnor|Dmel|Scer|Cele|Xlae|Drer)$")


def clean_label(label):
    return _SPECIES_SUFFIX.sub("", label) if isinstance(label, str) else label


def load_models():
    models = {}
    for path in sorted(glob.glob(os.path.join(MODELS_DIR, "*.yaml"))):
        with open(path) as fh:
            m = yaml.safe_load(fh)
        if m and "id" in m:
            models[m["id"]] = m
    return models


def label_map(models):
    labels = {}
    for m in models.values():
        for obj in m.get("objects", []) or []:
            labels[obj["id"]] = clean_label(obj.get("label", obj["id"]))
    return labels


def molecule_terms(model):
    """local molecule id -> ontology term (UniProtKB/CHEBI)."""
    return {mol["id"]: mol.get("term") for mol in model.get("molecules", []) or []}


def enabled_by_key(act):
    eb = act.get("enabled_by") or {}
    term = eb.get("term")
    parts = eb.get("has_part")
    if parts:
        members = tuple(sorted(p.get("term") for p in parts))
        return ("complex", term, members)
    return ("gp", term)


def inputs_key(act, molterms):
    out = []
    for ma in act.get("molecular_associations", []) or []:
        mol = ma.get("molecule")
        term = molterms.get(mol, mol)
        out.append((ma.get("predicate"), term))
    return tuple(sorted(out))


def intrinsic_key(act):
    """Key WITHOUT edges/inputs -- used to identify a unit and to resolve targets."""
    return (
        enabled_by_key(act),
        (act.get("molecular_function") or {}).get("term"),
        (act.get("part_of") or {}).get("term"),
        (act.get("occurs_in") or {}).get("term"),
    )


def build_index(models):
    """Map every activity's local id -> its intrinsic key, per model."""
    idx = {}
    for mid, m in models.items():
        for act in m.get("activities", []) or []:
            idx[act["id"]] = intrinsic_key(act)
    return idx


def targets_key(act, idx):
    out = []
    for ca in act.get("causal_associations", []) or []:
        down = ca.get("downstream_activity")
        out.append((ca.get("predicate"), idx.get(down)))
    return tuple(sorted((p, str(k)) for p, k in out))


def strict_key(act, molterms, idx):
    return (intrinsic_key(act), inputs_key(act, molterms), targets_key(act, idx))


def fmt_intrinsic(key, labels):
    (eb, mf, bp, cc) = key
    if eb and eb[0] == "complex":
        ebs = f"complex {labels.get(eb[1], eb[1])}"
    elif eb:
        ebs = labels.get(eb[1], str(eb[1]))
    else:
        ebs = "?"
    return f"{ebs}  |  MF {labels.get(mf, mf)}  |  BP {labels.get(bp, bp)}  |  CC {labels.get(cc, cc)}"


def main():
    models = load_models()
    labels = label_map(models)
    idx = build_index(models)

    groups = {}  # strict_key -> list of (model_id, act_id)
    for mid, m in models.items():
        molterms = molecule_terms(m)
        for act in m.get("activities", []) or []:
            k = strict_key(act, molterms, idx)
            groups.setdefault(k, []).append((mid, act["id"]))

    total_acts = sum(len(m.get("activities", []) or []) for m in models.values())
    print(f"Models: {len(models)}   Activity units: {total_acts}   "
          f"Distinct units after strict merge: {len(groups)}\n")

    cross = []
    for k, members in groups.items():
        model_ids = {mid for mid, _ in members}
        if len(model_ids) > 1:
            cross.append((k, members, model_ids))

    if not cross:
        print("No activity units merge ACROSS models under the strict rule.")
    else:
        print(f"=== {len(cross)} shared unit(s) that BRIDGE models ===\n")
        for k, members, model_ids in cross:
            print(fmt_intrinsic(k[0], labels))
            print(f"    merges {len(members)} units across {len(model_ids)} models:")
            for mid, aid in members:
                print(f"      - {mid.split(':')[1]}  ({aid.split('/')[-1]})")
            print()

    # also flag intra-model duplicates (same key, same model) -- unusual but possible
    dups = [(k, members) for k, members in groups.items()
            if len({mid for mid, _ in members}) == 1 and len(members) > 1]
    if dups:
        print(f"=== {len(dups)} duplicate unit(s) WITHIN a single model ===")
        for k, members in dups:
            print(f"  {fmt_intrinsic(k[0], labels)}  x{len(members)}  in {members[0][0]}")


if __name__ == "__main__":
    main()
