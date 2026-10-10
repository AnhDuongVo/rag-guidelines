"""A tiny bundled corpus of SYNTHETIC guideline and drug-label snippets.

The text here is written for the demo and is not copied from any real guideline or label; it stands in for
a corpus you would load from public sources. Each chunk has an id, its text, and the source it belongs to.
"""

from __future__ import annotations

from pydantic import BaseModel


class Chunk(BaseModel):
    id: str
    text: str
    source: str


CORPUS: list[Chunk] = [
    Chunk(
        id="met-1",
        source="Sample Metformin Label (synthetic)",
        text="The maximum recommended daily dose of metformin is 2550 mg, taken in divided doses with meals.",
    ),
    Chunk(
        id="met-2",
        source="Sample Metformin Label (synthetic)",
        text="Metformin is contraindicated in patients with an eGFR below 30 mL/min/1.73m2.",
    ),
    Chunk(
        id="t2d-1",
        source="Sample Type 2 Diabetes Guideline (synthetic)",
        text="Metformin is the preferred initial pharmacologic agent for the treatment of type 2 diabetes.",
    ),
    Chunk(
        id="t2d-2",
        source="Sample Type 2 Diabetes Guideline (synthetic)",
        text="An HbA1c target below 7 percent is appropriate for many non-pregnant adults with diabetes.",
    ),
    Chunk(
        id="htn-1",
        source="Sample Hypertension Guideline (synthetic)",
        text="Pharmacotherapy for hypertension is recommended when blood pressure remains at or above 140/90 mmHg despite lifestyle changes.",
    ),
    Chunk(
        id="htn-2",
        source="Sample Hypertension Guideline (synthetic)",
        text="First-line agents for hypertension include ACE inhibitors, ARBs, calcium channel blockers, and thiazide diuretics.",
    ),
    Chunk(
        id="lip-1",
        source="Sample Lipid Guideline (synthetic)",
        text="High-intensity statin therapy is recommended for patients with established atherosclerotic cardiovascular disease.",
    ),
    Chunk(
        id="ckd-1",
        source="Sample CKD Guideline (synthetic)",
        text="An SGLT2 inhibitor is recommended for patients with type 2 diabetes and chronic kidney disease to slow progression.",
    ),
]


def by_id(cid: str) -> Chunk | None:
    return next((c for c in CORPUS if c.id == cid), None)
