# lab/tools/modal — modal impact synthesis

`modal.py`: a struck object as a bank of exponentially decaying sinusoids (frequency, amplitude,
T60 per mode) plus a short excitation, and the extraction of those modes from one clean recorded
hit. Needs numpy and scipy only.

Provenance: the functions were first written as project experiment code (not published) and
moved here unchanged, so a recipe rendered through this module gives the same samples as the
experiment code did on the same platform (checked once for the wooden-knock recipe, 2026-11-13: all
five files identical).

Used by: `wedo/wedo-sfx/cases/20261007-impact-wooden-box-knock/recipe/render.py`
(method card `wedo/wedo-sfx/methods/impact/modal-body-swapped-attack.md`).

```bash
uv run --with numpy --with scipy --with soundfile python \
  wedo/wedo-sfx/cases/20261007-impact-wooden-box-knock/recipe/render.py --refs <dir> --out <dir>
```

## Quick start (library)

Needs numpy, scipy and soundfile. Input: one clean recorded hit, mono, 48 kHz (`modal.FS`), cropped to
start about 1 ms before the onset; `onset` is the sample index where the hit starts. The snippet below
runs as is, with a made-up three-sine "hit" standing in for a recording (put the file in the same folder
as `modal.py`, or run it from there):

```python
import numpy as np, soundfile as sf
import modal

sr = modal.FS
t = np.arange(sr) / sr
hit = sum(a * np.exp(-t * 6.91 / t60) * np.sin(2 * np.pi * f * t)       # stand-in: replace with
          for f, a, t60 in [(180, 1.0, 0.25), (410, 0.6, 0.15), (950, 0.3, 0.08)])  # sf.read("hit.wav")
hit = np.concatenate([np.zeros(48), hit])
onset = 48

modes, info = modal.extract_modes(hit, onset, fmin=60.0)   # [{f (Hz), amp (re largest), t60 (s), peak_db}]
params = {"modes": modes, "duration": 1.0, "transient_cutoff": 2500, "transient_level_db": -6,
          "transient_ms": 3, "random_phase": True}          # burst: band-passed noise at 2.5 kHz, 3 ms decay
x, parts = modal.render_procedural(params, sr, seed=0)      # parts: {"body", "transient"}
sf.write("hit_P.wav", x, sr, subtype="PCM_24")

# retune: +3 semitones, ring 0.6x as long
up = dict(params, modes=[dict(m, f=m["f"] * 2 ** (3 / 12), t60=m["t60"] * 0.6) for m in modes])
sf.write("hit_up.wav", modal.render_procedural(up, sr, seed=0)[0], sr, subtype="PCM_24")
```

Notes and limits:

- `extract_modes` picks spectral peaks of the first 50 ms after the onset, so on a stand-in or a real
  recording it may return a few more peaks than physical modes (window leakage); inspect `modes` and
  `info` before relying on them. The defaults (`fmin=150`) were set for a metal pan; the wooden-knock
  recipe uses lower values and a shorter fit window (see the recipe README for the reasons).
- The same seed gives the same render on the same platform; other library versions may differ in the
  last bits (not checked).
- To keep a recorded attack instead of the synthetic burst use `extract_attack`, `calibrate`
  (scales the attack to the burst's energy) and `recorded_attack_ratio` (attack/body energy of a
  recording; decide from it whether a recorded attack matters). The wooden-knock recipe shows the full use.
- Whether the results sound right was only judged for the wooden knock (1 listener, 1 session); see the method card.
