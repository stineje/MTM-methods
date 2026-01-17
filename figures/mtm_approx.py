#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters (from your TikZ)
# -----------------------------
nintervals = 4
intervalwidth = 1.0 / nintervals

# shared slope m = d/dx sqrt(x) at x=0.5
m = 1.0 / (2.0 * np.sqrt(0.5))

nsteps = 8
stepwidth = intervalwidth / nsteps
halfoffset = stepwidth / 2.0

# -----------------------------
# Helper: brace-ish annotation (Matplotlib doesn't have TikZ braces)
# We'll draw a double-headed arrow + label to mimic the epsilon bracket.
# -----------------------------
def epsilon_marker(ax, x, y1, y2, label, xshift=0.02):
    ya, yb = (y1, y2) if y1 >= y2 else (y2, y1)
    ax.annotate(
        "", xy=(x, ya), xytext=(x, yb),
        arrowprops=dict(arrowstyle="<->", lw=2.0, color="black")
    )
    ax.text(x + xshift, 0.5 * (ya + yb), label, va="center", ha="left")

# -----------------------------
# Plot setup (match axis style)
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 6))

ax.set_xlim(0, 1.1)
ax.set_ylim(0, 1.2)
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.grid(True, which="both", linestyle="-", linewidth=0.6)
ax.minorticks_on()

# axis lines=middle (through origin)
ax.spines["left"].set_position(("data", 0))
ax.spines["bottom"].set_position(("data", 0))
ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")
ax.xaxis.set_ticks_position("bottom")
ax.yaxis.set_ticks_position("left")

# -----------------------------
# True function sqrt(x) (blue)
# -----------------------------
x_true = np.linspace(0.0, 0.999, 100)
ax.plot(x_true, np.sqrt(x_true), linewidth=2.0, color="blue")

# -----------------------------
# Discretized line segments (black, const plot)
# -----------------------------
for i in range(nintervals):
    xi = i * intervalwidth
    xip = (i + 1) * intervalwidth
    a = 0.5 * (xi + xip)          # midpoint
    fa = np.sqrt(a)

    # Build points (xstep, ystep) for j=0..nsteps
    xs = np.array([xi + j * stepwidth for j in range(nsteps + 1)], dtype=float)
    ys = np.empty_like(xs)

    for j in range(nsteps + 1):
        xstep = xs[j]
        if j == nsteps:
            prevx = xi + (j - 1) * stepwidth
            prevy = m * (prevx + halfoffset - a) + fa
            ystep = prevy  # match last y-value to avoid vertical line
        else:
            ystep = m * (xstep + halfoffset - a) + fa
        ys[j] = ystep

    ax.step(xs, ys, where="post", linewidth=2.0, color="black")

# -----------------------------
# Epsilon markers (match your x locations/macros)
# -----------------------------
# epsilon_0 at x=0, compare segment of first interval vs sqrt(0)
xstart = 0.0
aone = 0.125
faone = np.sqrt(aone)
ystepzero = m * (xstart + halfoffset - aone) + faone
ysqrtzero = np.sqrt(xstart)
epsilon_marker(ax, xstart, ystepzero, ysqrtzero, r"$\epsilon_0$")

# epsilon_1 at x=1/nintervals - 1/64 (as in TikZ)
xend = 1.0 / nintervals - 1.0 / 64.0
ystepone = m * (xend + halfoffset - aone) + faone
ysqrtone = np.sqrt(xend)
epsilon_marker(ax, xend, ystepone, ysqrtone, r"$\epsilon_1$")

# epsilon_2 at x=(nintervals-1)/nintervals (left endpoint of last interval)
xlaststart = (nintervals - 1) / nintervals
alast = (xlaststart + 1.0) / 2.0
falast = np.sqrt(alast)
ysteptwo = m * (xlaststart + halfoffset - alast) + falast
ysqrttwo = np.sqrt(xlaststart)
epsilon_marker(ax, xlaststart, ysteptwo, ysqrttwo, r"$\epsilon_2$")

# epsilon_3 at x=0.984375 (as in TikZ)
xlastend = 0.984375
ystepthree = m * (xlastend + halfoffset - alast) + falast
ysqrtthree = np.sqrt(xlastend)
epsilon_marker(ax, xlastend, ystepthree, ysqrtthree, r"$\epsilon_3$")

plt.tight_layout()
plt.savefig("multipartite_error.png", dpi=300)
plt.show()

