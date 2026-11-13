# Example renders: wooden knock (P and Pv)

Made with the README's steps from this repository's files on 2026-11-13 (macOS arm64; versions in the main
README), converted losslessly from the recipe's 24-bit WAV to FLAC with ffmpeg (`-map_metadata -1`).

| File | What |
| --- | --- |
| `knock_P.flac` | P: 40 measured modes + synthetic knuckle burst; no recorded audio in the output |
| `knock_Pv_up3st_ring06.flac` | Pv: P retuned, modes ×2^(3/12), T60 ×0.6 |
| `render.json` | the recipe's log of that run: onset, the 40 modes, gains, sample hashes of all five files |

These files were **measured, not heard**: their samples equal the recipe's output on that host (sha256 in
`render.json`). The listener's verdict in the case was given on 2026-10-07 to renders of the same recipe made
on another machine, not to these bytes. Derived from Freesound 812363 (CuboRodante, CC0 1.0).
