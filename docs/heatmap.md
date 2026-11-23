# Heatmaps

These examples follow [`test_heatmap.py`](../test_heatmap.py). The class-based
[`ALL_PLOT`](../ALL_PLOTS.py) interface supplies axis styling, color handling,
and image saving; the heatmap itself is drawn by [`heatmap.py`](../heatmap.py).

## Basic heatmap

Pass a two-dimensional pandas DataFrame to `ALL_PLOT.plot` with
`plt_type="heatmap"`. The DataFrame's index and columns are used for the y- and
x-axis tick labels:

```python
import pandas as pd

from ALL_PLOTS import ALL_PLOT
from colors_set import DISTINCT_2_1

data = pd.DataFrame(
    [[0.28, 0.31, 0.25], [0.32, 0.26, 0.18]],
    index=["Original", "Filtered"],
    columns=["Pixel Drop", "Low Res", "Snow"],
)

plotter = ALL_PLOT(
    figsize=(6, 4),
    colors=DISTINCT_2_1,
    artificial_darkening=0.8,
    annot=True,
    annot_decimal_places=2,
    annot_font_size=9,
    grid_shape="xy",
    grid_color="white",
    grid_widths=0.3,
)

plotter.plot(
    plt_type="heatmap",
    name="Pictures/Heatmap/my_heatmap",
    df=data,
    make_square=False,
)
```

By default, each cell displays its value. Automatic annotation text switches
between black and white according to the cell's luminance. Set
`annot_kws={"color": "..."}` to explicitly choose the annotation color.

## Annotations, missing values, and masks

| Argument | Purpose |
| --- | --- |
| `annot` | Show or hide cell values |
| `annot_decimal_places` | Digits after the decimal point in each value |
| `annot_font_size` | Annotation font size |
| `annot_kws` | Matplotlib text options; a supplied `color` overrides automatic text color |
| `annot_black_threshold` | Luminance cutoff for annotation color; lower values use white text on fewer cells |
| `mask` | Boolean array; `True` cells are omitted |

Non-finite values such as `NaN` are masked automatically. For example, to hide
selected cells and fine-tune the text contrast:

```python
import numpy as np

masked = np.array([
    [False, False, True],
    [False, False, False],
])

plotter.plot(
    plt_type="heatmap",
    name="Pictures/Heatmap/masked_heatmap",
    df=data,
    mask=masked,
    annot_black_threshold=0.27,
)
```

## Palette, value range, and colorbar

`colors` is a sequence of colors defining the continuous color gradient.
`n_bins` controls its number of discrete color levels. `vmin` and `vmax`
control the displayed value range. Use `center` to center the normalization on
a meaningful value:

```python
from colors_set import GRADIENT_GREEN_6

plotter.plot(
    plt_type="heatmap",
    name="Pictures/Heatmap/centered_heatmap",
    df=data,
    colors=GRADIENT_GREEN_6,
    n_bins=6,
    vmin=0,
    center=0.25,
    vmax=0.5,
    cbar=True,
    cbar_labels=True,
)
```

Set `cbar_labels=False` to hide colorbar tick labels, or customize colorbar
placement and appearance with `cbar_kws`. With labeled ticks,
`cbar_count` controls the number of requested values and
`cbar_label_fontsize` and `cbar_label_rotate` control their presentation.

## Cell shape and grid

`make_square=True` (the default) gives cells equal width and height. Set it to
`False` to let the plot dimensions determine cell shape. `grid_shape` accepts
`"both"` or `"xy"` for both directions, `"x"` for vertical lines, `"y"` for
horizontal lines, or `None` for no cell grid. Use `grid_color`,
`grid_opacity`, and `grid_widths` to style the grid.

The test script also demonstrates custom x-axis label positions and a
colorbar-backed heatmap:

<p align="center">
  <img src="../Pictures/Heatmap/test_heatmap.png" alt="Annotated heatmap with row and column labels" width="48%">
  <img src="../Pictures/Heatmap/test_heatmap_color_bar.png" alt="Heatmap with a colorbar" width="40%">
</p>
