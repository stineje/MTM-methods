#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters (from your TikZ)
# -----------------------------
Nzero = 1
None_ = 2
Ntwo = 3
Nfull = Nzero + None_ + Ntwo

# Scales
ScaleOne  = 2 ** (Nzero + None_)
ScaleTwo  = 2 ** (Nzero)
ScaleFull = 2 ** (Nfull)

# Deltas
DeltaOne = 2 ** (-Nzero - 1) - 2 ** (-Nzero - None_ - 1)
DeltaTwo = 2 ** (-Nzero - None_ - 1) - 2 ** (-Nzero - None_ - Ntwo - 1)

# Xtwo(x) = mod(floor(x * 2^Nfull), 2^Ntwo) / 2^Nfull
def Xtwo(x):
    return (np.floor(x * ScaleFull) % (2 ** Ntwo)) / ScaleFull

# -----------------------------
# Build data
# -----------------------------
samples = 1024
x = np.linspace(0.0, 1.0, samples)

# floor(x*Scale)/Scale (vectorized)
x_floor_one = np.floor(x * ScaleOne) / ScaleOne
x_floor_two = np.floor(x * ScaleTwo) / ScaleTwo

# STAM-like approximation (as in your addplot expression)
y_approx = (
    np.sqrt(x_floor_one + DeltaTwo)
    + (1.0 / (2.0 * np.sqrt(x_floor_two + DeltaOne + DeltaTwo))) * (Xtwo(x) - DeltaTwo)
)

# True function
y_true = np.sqrt(x)

# -----------------------------
# Plot
# -----------------------------
fig, ax = plt.subplots(figsize=(10/2.54, 8/2.54))  # 10cm x 8cm

# "const plot" -> step plot
ax.step(x, y_approx, where="post", linewidth=2.0, color="black", label="STAM approx")

# dashed sqrt(x)
ax.plot(x, y_true, linestyle="--", color="black", label=r"$\sqrt{x}$")

# Axes / grid / ticks / limits
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticks([0, 0.5, 1.0])
ax.grid(True, which="both", linestyle="-", linewidth=0.6)

# "axis lines=middle" style (axes through origin)
# (With x,y in [0,1], this ends up at the lower-left corner, like TikZ here.)
ax.spines["left"].set_position(("data", 0))
ax.spines["bottom"].set_position(("data", 0))
ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")
ax.xaxis.set_ticks_position("bottom")
ax.yaxis.set_ticks_position("left")

# Optional label (your TikZ node location was outside the plotted range; place inside here)
ax.text(0.55, 0.90, r"$f(x)=\sqrt{x}$", transform=ax.transAxes)

# If you want a legend, uncomment:
# ax.legend(frameon=False)

plt.tight_layout()
plt.savefig("stam_approx.png", dpi=300)
plt.show()

