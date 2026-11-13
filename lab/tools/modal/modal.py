"""Modal impact synthesis: a struck object as decaying sinusoids plus a short excitation.

Self-contained form of the functions the impact recipes first used as project experiment code (not
published) and its DSP helpers, so that a recipe needs only numpy and scipy. Same arithmetic, same RNG
order: renders were sample-identical to the experiment code on the same platform.

  extract_modes(crop, onset, fmin=...)   peaks of the first 50 ms after the onset -> [{f, amp, t60, peak_db}]
  components(params, sr, seed)           {"body", "transient"}: mode bank and synthetic burst, kept apart
  post(x, sr)                            the shared output stage (20 Hz high-pass, 0.3 ms / 30 ms fades)
  render_procedural(params, sr, seed)    post(body + transient)
  extract_attack(crop, sr)               300 Hz high-passed first 50 ms of a recording (5 ms end fade)
  calibrate(attack, comps, sr)           attack scaled to the synthetic burst's energy over 100 ms
  recorded_attack_ratio(crop, sr)        attack/body energy of a recording over its first 100 ms

params = {"modes": [{"f", "amp", "t60"}], "duration", "transient_cutoff", "transient_level_db",
"transient_ms", "random_phase"}. Tuning: scale every mode's f (pitch) and t60 (ring).
"""
import numpy as np
from scipy import signal

FS = 48000


# ---- DSP helpers

def bandpass(x, sr, fc, q, order=2):
    bw = fc / q
    lo = max(fc - bw / 2, 10.0)
    hi = min(fc + bw / 2, sr / 2 * 0.98)
    sos = signal.butter(order, [lo, hi], btype="band", fs=sr, output="sos")
    return signal.sosfilt(sos, x)


def highpass(x, sr, fc, order=2):
    sos = signal.butter(order, fc, btype="high", fs=sr, output="sos")
    return signal.sosfilt(sos, x)


def fade(x, sr, fade_in_ms=2.0, fade_out_ms=10.0):
    y = np.array(x, dtype=float, copy=True)
    ni = int(sr * fade_in_ms / 1000)
    no = int(sr * fade_out_ms / 1000)
    if ni > 0:
        y[..., :ni] *= 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, ni))
    if no > 0:
        y[..., -no:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, no))
    return y


def energy(x):
    return float(np.sum(np.asarray(x, np.float64) ** 2))


def raised_fade_out(n):
    return 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, n))


# ---- modal body

def extract_modes(crop, onset, fs=FS, win_s=0.05, nfft=65536, fmin=150.0, fmax=16000.0, thresh_db=-40.0,
                  min_sep_hz=30.0, max_modes=40):
    """Peaks of win_s after the onset (Hann, nfft), fmin-fmax, >= thresh_db re the largest, >= min_sep_hz apart,
    at most max_modes by amplitude, parabolic interpolation; per-mode T60 from a +-1.5 % band-pass 10 ms envelope
    slope (max to -30 dB), clamped to [0.03, 6] s. Amplitudes normalised to the largest mode."""
    n = int(win_s * fs)
    seg = crop[onset:onset + n] * np.hanning(n)
    F = np.abs(np.fft.rfft(seg, nfft))
    f = np.fft.rfftfreq(nfft, 1 / fs)
    L = 20 * np.log10(F + 1e-12)
    m = (f >= fmin) & (f <= fmax)
    idx = np.where(m)[0]
    pk, _ = signal.find_peaks(L[idx], distance=max(1, int(min_sep_hz / (fs / nfft))))
    pk = idx[pk]
    pk = pk[L[pk] >= L[pk].max() + thresh_db]
    pk = pk[np.argsort(-L[pk])][:max_modes]
    modes = []
    for k in sorted(pk):
        a, b, c = L[k - 1], L[k], L[k + 1]
        den = a - 2 * b + c
        p = 0.5 * (a - c) / den if den != 0 else 0.0
        fk = (k + p) * fs / nfft
        amp = 10 ** ((b - 0.25 * (a - c) * p) / 20)
        sos = signal.butter(2, [fk * 0.985, fk * 1.015], btype="band", fs=fs, output="sos")
        y = signal.sosfiltfilt(sos, crop[onset:])
        h = int(0.01 * fs)
        nn = len(y) // h
        e = 20 * np.log10(np.sqrt(np.mean(y[:nn * h].reshape(nn, h) ** 2, 1)) + 1e-12)
        t = (np.arange(nn) + 0.5) * 0.01
        i0 = int(np.argmax(e))
        stop = np.where(e[i0:] < e[i0] - 30)[0]
        i1 = i0 + (int(stop[0]) if len(stop) else nn - i0)
        if i1 - i0 >= 3:
            s = np.polyfit(t[i0:i1], e[i0:i1], 1)[0]
            t60 = -60 / s if s < 0 else 6.0
        else:
            t60 = 0.03
        modes.append({"f": round(float(fk), 2), "amp": float(amp), "t60": round(float(np.clip(t60, 0.03, 6.0)), 4),
                      "peak_db": round(float(b - L[pk].max()), 1)})
    amax = max(md["amp"] for md in modes)
    for md in modes:
        md["amp"] = round(md["amp"] / amax, 6)
    return modes, {"n_modes": len(modes), "n_peaks_above_thresh": int(len(pk)), "window_s": win_s, "nfft": nfft,
                   "largest_peak_hz": modes[int(np.argmax([md["amp"] for md in modes]))]["f"], "lowest_hz": modes[0]["f"]}


def components(p, sr, seed):
    """Body (mode bank, peak 1) and synthetic transient, before the output stage. RNG: mode phases, then the burst."""
    rng = np.random.default_rng(seed)
    n = int(p["duration"] * sr)
    t = np.arange(n) / sr
    body = np.zeros(n)
    for md in p["modes"]:
        fk = md["f"]
        if fk > sr * 0.45:
            continue
        ph = rng.uniform(0, 2 * np.pi) if p.get("random_phase", True) else 0.0
        L = min(n, int(md["t60"] * 1.5 * sr))
        body[:L] += md["amp"] * np.exp(-t[:L] * 6.91 / md["t60"]) * np.sin(2 * np.pi * fk * t[:L] + ph)
    body /= np.max(np.abs(body)) + 1e-12
    tr = np.zeros(n)
    m = int(sr * 0.05)
    burst = rng.standard_normal(m) * np.exp(-np.arange(m) / sr / (p["transient_ms"] / 1000))
    burst = bandpass(burst, sr, p["transient_cutoff"], 1.2)
    burst /= np.max(np.abs(burst)) + 1e-12
    tr[:m] += 10 ** (p["transient_level_db"] / 20) * burst
    return {"body": body, "transient": tr, "_n_modes": len(p["modes"])}


def post(x, sr):
    return fade(highpass(x, sr, 20), sr, fade_in_ms=0.3, fade_out_ms=30)


def render_procedural(p, sr, seed):
    c = components(p, sr, seed)
    return post(c["body"] + c["transient"], sr), c


def place(attack, n):
    a = np.zeros(n)
    k = min(n, len(attack))
    a[:k] = attack[:k]
    return a


# ---- recorded attack

def hp300(x, sr=FS):
    sos = signal.butter(4, 300.0, btype="high", fs=sr, output="sos")
    return signal.sosfilt(sos, x)


def extract_attack(crop, sr=FS, support_ms=50):
    n = int(support_ms * sr / 1000)
    a = hp300(crop, sr)[:n].copy()
    nf = int(0.005 * sr)
    a[-nf:] *= raised_fade_out(nf)
    return a


def calibrate(attack, comps, sr=FS):
    m = int(0.1 * sr)
    g = np.sqrt(energy(comps["transient"][:m]) / energy(attack[:m]))
    return attack * g, float(g)


def recorded_attack_ratio(crop, sr=FS):
    m = int(0.1 * sr)
    a = hp300(crop, sr)[:m]
    b = crop[:m] - a
    return float(energy(a) / energy(b)), {"hp_energy_db": round(10 * np.log10(energy(a)), 2),
                                           "rest_energy_db": round(10 * np.log10(energy(b)), 2),
                                           "ratio_db": round(10 * np.log10(energy(a) / energy(b)), 2)}
