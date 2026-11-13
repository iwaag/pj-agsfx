# lab/tools/modal — modal impact synthesis

`modal.py`: a struck object as a bank of exponentially decaying sinusoids (frequency, amplitude,
T60 per mode) plus a short excitation, and the extraction of those modes from one clean recorded
hit. Needs numpy and scipy only.

It is the self-contained form of the functions the impact recipes took from the set2/p2
experiment (`lab/experiments/set2/p2/pan_modal.py`, `step4_pan.py`) and `lab/p2/sfx/common.py`;
those stay frozen as the experiment's record. Same arithmetic and RNG order, so a recipe moved to
this module renders the same samples on the same platform (checked for the wooden-knock recipe,
2026-11-13: all five files identical to the experiment-code run).

Used by: `wedo/wedo-sfx/cases/20261007-impact-wooden-box-knock/recipe/render.py`
(method card `wedo/wedo-sfx/methods/impact/modal-body-swapped-attack.md`).

```bash
uv run --with numpy --with scipy --with soundfile python \
  wedo/wedo-sfx/cases/20261007-impact-wooden-box-knock/recipe/render.py --refs <dir> --out <dir>
```
