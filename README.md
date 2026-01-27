# MTM Methods

** Jacob Pease and James E. Stine **  
SBTM/STAM/MTM Generator
Oklahoma State University

---

## Running the Project

To run this project, use the following command:

```bash
python -m src.main
```

## Dependencies
This project was developed using Python 3.12.7 on MacOS. You can use `pyenv` to upgrade your global Python installation to 3.12.7 as the default version pre-installed on the Mac is likely not going to work or have the latest DearPyGUI.

After updating Python, install the following dependencies:

```bash
pip3 install dearpygui sphinx pytest numpy matplotlib
```

## Multipartite Implementation

This particular implementation of the Multipartite method changes a few things about how the tables are calculated. These changes are summarized in the list below:

1. Calculations are now all done in the floating point range instead of the integer range. This means that anywhere in the orignal paper where there was a $`a + (b-a) x`$ in the equation has now been simplified to assume that $`b = 1`$ and $`a = 0`$. Additionally, functions passed to a multipartite object are assumed to be normalized, meaning that the desired input range is on the interval [0,1) and the output range is also [0,1). So for the sine function with the range of $`\left[0, \frac{\pi}{2}\right)`$ and the domain of $`\left[0, 1\right)`$ is wrapped with:

```python
def wrapper(x):
	return math.sin(a + (b-a)*x)/(d - c)
```
A wrapper class is planned that would automatically normalize the given function with the given range and domain. This class would be callable, so there would be no perceived difference between using a regular function and this class. Also, eventually, the feature for closed interval ranges will be added.

2. The lists `beta` and `TO` are the same as they are in the Multipartite paper, but with reversed indices. This makes iterating through the lists easier as every calculation starts from the left (most significant) to the right (least significant). As a consequence of this, output tables are indexed in the reverse order, with the table holding the offsets with the greatest magnitude now called $`TO_0`$ instead of $`TO_m`$. $`\beta`$

3. The list $`p_i`$ has been completely done away with, simplifying the number of parameters needed to be stored in the object. Now calculations are done with alpha and beta exclusively. The only reason $`p_i`$ existed to begin with was to deal with an edge case where $`p_0`$ needed to be equal to 0 due to indexing reasons. However, this same edge case can be dealt with without a list. The identity

```math
\delta_i = a + (b - a) 2^{-w_I + p_i} (2^{\beta_i} - 1)
```

considering that $`p_i = \sum_{j = 0}^{i - 1} \beta_j`$ can be rewritten as:

```math
\begin{align*}
	&\delta_i = 2^{-\alpha - \beta_0 - \ldots - \beta_{i}} (2^{\beta_i} - 1) \\\\
	\Longrightarrow &\delta_i = 2^{-\alpha -\beta_{0:i-1}} - 2^{-\alpha - \beta_{0:i}}
\end{align*}
```

When the index $`i-1 < 0`$ then the result is zero. Therefore:

```math
\begin{align*}
	&\delta_0 = 2^{-\alpha} - 2^{-\alpha - \beta_0} \\\\
	&\delta_1 = 2^{-\alpha - \beta_0} - 2^{-\alpha - \beta_0 - \beta_1} \\\\
	&\ldots
\end{align*}
```

This corresponds to setting all of the bits of a particular partition of $`B`$ to 1s. For example, given a decomposition where $`w_I = 10`$, $`\alpha = 5`$, $`\beta_0 = 2`$, and $`\beta_1 = 3`$ (remember, I reversed the indice ordering), $`\delta_0`$ would be equal to the following in fixed point binary with an implied point just before the most significant bit:

```
00000_11_000
```

And $`\delta_1`$ would be equal to:

```
00000_00_111
```

4. Assuming we are dealing exclusively with a symmetric table method and not a non-symmetric table with double the values stored, the output sizes in bits of each table is stored with one less bit. For some reason, the original implementation decides to store the larger output size but doesn't use it.


