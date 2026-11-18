# pj-agsfx — sound effects by algorithm and by AI (public selection)

pj-agsfx is a project that makes sound effects on request. For each request it picks a procedural
(DSP) or generative method, predicts the result before listening, asks a listener, and keeps what was
learned. This public repository is a small **selection** of it: one route that runs on an ordinary
CPU, and the knowledge behind it.

| Path | What |
| --- | --- |
| `lab/tools/modal/` | modal impact synthesis in one file: extract decaying modes from one recorded hit, re-synthesise the hit with a synthetic or recorded attack, retune it |
| `wedo/wedo-sfx/` | submodule [iwaag/wedo-sfx](https://github.com/iwaag/wedo-sfx): the method card, the case (assumptions, prediction, listener verdict, lesson) and the recipe |
| `examples/wooden-knock/` | two renders made for this publication (P and the retuned Pv) and their `render.json` |

Get it with the submodule:

```bash
git clone --recurse-submodules https://github.com/iwaag/pj-agsfx.git
cd pj-agsfx
```

## Route: a tunable wooden knock from one recording

The case `wedo/wedo-sfx/cases/20261007-impact-wooden-box-knock/` asked for one dry, close knuckle knock on
a small wooden box, about 1 s, whose pitch and ring can be changed afterwards for variants. The recipe
measures 40 modes (frequency, amplitude, decay time T60) from the first 120 ms of a CC0 recording and
renders:

| File | What |
| --- | --- |
| `knock_P.wav` | P: the 40 modes plus a synthetic knuckle burst (2.5 kHz, 3 ms) — no recorded audio in the output |
| `knock_H.wav` | H: P's body plus the recording's own 50 ms attack, energy-matched to the burst |
| `knock_Hp.wav` | Hp: as H, with the attack at the recording's own attack/body ratio |
| `knock_Pv_up3st_ring06.wav` | Pv: P with every mode ×2^(3/12) (+3 semitones) and T60 ×0.6 (shorter ring) |
| `knock_reference.wav` | the recording, cropped from 1 ms before its onset to 1 s |
| `knock_P_<n>st_ring<r>.wav` | only with `--variant n:r` (repeatable, `--variant=-2:1.5` when negative): P retuned by n semitones with T60 × r; `--variant 3:0.6` equals Pv |
| `render.json` | onset, the 40 modes, gains, and a sha256 of each file's samples |

### Requirements

Python ≥ 3.10 with numpy, scipy and soundfile (here run through [uv](https://docs.astral.sh/uv/)), ffmpeg,
and curl. No GPU, model weights or credentials.

### Steps

```bash
mkdir -p refs
curl -L -o refs/812363_17517436-hq.mp3 https://cdn.freesound.org/previews/812/812363_17517436-hq.mp3
ffmpeg -i refs/812363_17517436-hq.mp3 -ac 1 -ar 48000 -c:a pcm_f32le refs/812363_17517436-hq.48k.wav
uv run --with numpy --with scipy --with soundfile python \
    wedo/wedo-sfx/cases/20261007-impact-wooden-box-knock/recipe/render.py --refs refs --out out
```

The recipe stops if the downloaded preview's sha256 is not `f3faa5284a41900a1282771a343ad8537a02880066b1a1420bf3c77bd0d0415b`.
It prints one line per file and writes `out/`. For variants, scale the modes' `f` and `t60` as Pv does
(the `pv = …` line in `render.py`, just before the Pv file is written; the reference crop comes after it).

### What was observed, by kind

- **Measured** (macOS 26.2 arm64, Python 3.13, numpy 2.5.4, scipy 1.18.1, soundfile 0.14.0, ffmpeg 9.0.2,
  2026-11-13): onset 0.377 s; 40 modes, lowest 128.43 Hz, largest 577.46 Hz; recorded attack/body energy
  −0.72 dB (a wood knock is attack-dominated); about 13 s including uv's first environment, the synthesis
  itself well under a second. Sample hashes (`samples_sha256_float32_of_pcm24` in `render.json`):

  | File | sha256 of samples |
  | --- | --- |
  | knock_P.wav | `5c3eaf7e230aa6260820e43795f08ec96fcaf51086eefc0b297d38f1c1ed23bb` |
  | knock_H.wav | `ede39bd37f1bd7bf592f2111e2a35e528681835a48beaeeec40a1902f2790fbd` |
  | knock_Hp.wav | `2bf3bf42ccd32d9dc143151482867cdaaeb6a54283e4c91fc73837cd68232db8` |
  | knock_Pv_up3st_ring06.wav | `1bb30406b25b27eced83282af2555de25adbccc2ea1b53e00cc7fe7c754ce198` |
  | knock_reference.wav | `19cef9bb3def7d7d85d77243d83bfdddf0191b2995f28be195cdce2a7c512537` |

  Other platforms or library versions may differ in the last bits (filters and FFTs); that has not been checked.
- **Predicted** before listening (by the agent that served the case): only Hp would be recognised; P, H and the
  retuned P would sound like a pitched woodblock.
- **Verdict** (1 listener — the project's owner — 1 session, 2026-10-07, on renders of the same recipe made on
  another machine): P, H, Hp and the retuned P all pass recognition, naturalness and fit. The prediction missed:
  a fully synthetic P from measured modes was enough, so a knock can be shipped as a ~4 kB tunable preset.
- **Not heard:** the files under `examples/` and any render made for this publication.

See the case and the method card for the assumptions made when moving the method from a metal pan to wood and
the failure modes (scrapes, overlapping sources, modes closer than about 40 Hz).

## Workflows and run records

`devdocs/workflows/create.yaml` (make an effect, screen it, let a person listen, record what was learned) and
`research.yaml` (survey, try, explain) are the two workflows a request can start. Three run records (under `devdocs/`, by workflow and run number) show them at
work: `create/run-001` (plucked string, procedural vs generated; inconclusive), `create/run-002`
(notification chime) and `research/run-001` (a stylised wind cue). They are the project's own reports, each with
one listener and one session, and they link to experiment code, literature notes and agent guides that are **not
published** here; those links do not resolve. Other run records stay internal.

## Not included

The project's other routes (generative models through a ComfyUI server, layered scenes, procedural textures),
its experiments, literature surveys, review tooling, other run records and the agents' operating guides. See
[NOTICE.md](NOTICE.md) for licences and the origin of this selection.
