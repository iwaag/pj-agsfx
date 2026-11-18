# Final report — create/run-001: plucked-string sound, procedural vs AI generation

## Request and result

The braindump asked for a plucked-string sound effect, comparing a procedural route against an AI-generation
route. The run produced 6 candidates (3 Karplus-Strong procedural, 3 Stable Audio 3 Small-SFX generated), screened
them (technical checks + predicted verdict), presented them as a labelled review video (presentation `p1`), and
asked the person to judge recognition, naturalness and which route fits the stated use.

**The comparison came back inconclusive by construction, not as a quality gap.** The person heard the procedural
route (P01-P03) as a pure string vibration with no instrument body assumed — close to a click on first listen —
and the generated route (G01-G03) as an instrument's string being played. Both readings are valid for an
unqualified "plucked string" request; the two routes answered an ambiguity the request itself left open (is an
instrument body implied?), and are not comparable on one axis without first equalising that assumption (e.g.
adding a resonance-body stage to the procedural route). The person declined to do that extra work in this run (it
would expand scope beyond the request) and asked to record the finding and end here. `wfe run decide` recorded
this as `accepted` (q2); the full wording is in `report-review.md`.

## What was produced

- `lab/experiments/create-run-001/`: `karplus_strong.py` (new procedural driver), `comfy_sa3_pluck.py` (new
  generative driver, talks to the networked ComfyUI service over HTTP), `screen.py`, 6 rendered WAVs (+ FLAC
  originals for the generated 3), `checks.json`, `self_eval.md`.
- Presentation `p1` (a review video, stopped and verified gone at `cleanup`).
- `wedo/wedo-sfx` additions (new `string` family): case
  `cases/20261013-string-pluck-procedural-vs-generated/` (case + recipe with every delivered file's sha256),
  method card `methods/string/karplus-strong-pluck.md`, an evidence line on `methods/generative/stable-audio-3.md`,
  a `string` row and a new "is a body implied?" question in `guide.md`, a row in `cases/index.md`, a row in
  `calibration.md`, and an escalation (`escalations/20261013-string-pluck-body-ambiguity.md`) recommending the
  `string` family's intake ask about an implied instrument body before routing, since this run's request did not.

## Evidence trail

- `report-produce.md`, `report-screen.md`, `report-present.md`, `report-review.md`, `report-record.md`,
  `report-cleanup.md` — one per authored node, each with what was done and verified.
- The listener's verdict is the person's own words (q2, taken up), quoted and interpreted in `report-review.md`
  and in the case; no machine measure was written as a verdict (technical checks and self_eval.md predictions are
  proxies, per the project's evidence vocabulary).

## Uncertain / what's next

- The escalation is low priority by the person's own choice; it only matters if another `string`-family request
  arrives, and should be read before routing one.
- No per-candidate verdict exists for either route — the person's answer was at the route level — so a future
  `string` case with a per-candidate review could sharpen the method cards further.
- This run ends here per the person's explicit request; no further produce/present round is pending.
