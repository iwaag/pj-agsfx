# Final report — research/run-001: symbolic (game-cue) wind texture

## Question

Which existing route makes a wind texture read as a stylised, immediately recognisable, easy-to-time
game cue, rather than realistic wind on a microphone? Opened from escalation
[wedo/wedo-sfx/escalations/20261007-symbolic-texture.md](../../../../wedo/wedo-sfx/escalations/20261007-symbolic-texture.md).
Plan agreed in `plan.md` (q1/q2).

## What was done

- **survey** — `study/study-sfx/10-stylized-game-textures.md`: stylised/symbolic game textures use a
  peak-aligned envelope (sharp rise/fall around one clear peak, not a gradual real decay), a distinct
  tonal "signature" layer over the noise bed, and named exaggeration of that signature relative to a
  recording. Full detail and sources: `report-survey.md`.
- **practice** — `lab/experiments/research-run-001/`: rendered 5 clips — procedural wind engine (preset
  `selected_y9`) as-is and exaggerated, Stable Audio 3 with a stylisation prompt (2 seeds), and the
  Stable Audio 3 plain-prompt reference that had previously failed fit. Built a 5-item, ~32s listening
  package. MOSS-SoundEffect and the EzAudio ControlNet route were not tried — both need a GPU host not
  available here — and are reported as untried, not failing. Detail: `report-practice.md`.
- **present** — listening package reviewed by iwaag (q3). Verdicts: procedural baseline **passes**
  clearly ("風らしくてよい"); procedural exaggerated **passes**, not a clear improvement over baseline
  ("ピークが短いが悪くはない"); Stable Audio 3 stylisation prompt **fails** both seeds (reads as a generic
  retro game effect, not wind); Stable Audio 3 plain prompt **fails** harder than before (reported
  inaudible; checked not technically silent). Detail: `report-present.md`.
- **cleanup** — presentation p1 stopped and verified gone (process + port). `report-cleanup.md`.
- **explain** — findings and uncertainties written up; person's answer to q4 ("finish here") is
  permission to finish, taken up. `report-explain.md`.

## Knowledge updated

- `wedo/wedo-sfx/guide.md` — texture/symbolic row split into "wind" (default now the procedural swell
  preset `selected_y9`, pass/1 listener/1 session) and "other than wind" (still untried).
- `wedo/wedo-sfx/methods/texture/procedural-noise-and-drops.md` — wind-as-symbolic-cue evidence line
  added.
- `wedo/wedo-sfx/methods/generative/stable-audio-3.md` — stylisation-prompt wind failure and the
  plain-prompt reference's harder failure added to the "does not fit when" evidence.
- `wedo/wedo-sfx/escalations/20261007-symbolic-texture.md` — narrowed, not fully closed: wind is answered
  (procedural swell passes, Stable Audio 3 stylisation does not); MOSS/EzAudio on wind, and generalisation
  to other textures, stay open with concrete next tests named.

## What's uncertain

One listener, one session, one texture (wind) — evidence for a default, not a closed question for
textures generally. The exaggerated preset's parameters were a first guess, checked only by spectrogram
before the package; the listener's verdict ("not bad", not clearly better) is the actual result, with no
further tuning attempted this run. MOSS and EzAudio remain genuinely untried for wind.

## Outcome

Person's answer to q4, taken up: "finish here" — permission to finish given, no further investigation
requested this run.
