# Heatmaps

These examples follow [`test_heatmap.py`](../test_heatmap.py). The test calls
[`ALL_PLOT.plot`](../ALL_PLOTS.py) with `plt_type="heatmap"` to draw annotated
heatmaps from a pandas DataFrame. DataFrame rows become heatmap rows and
DataFrame columns become heatmap columns.

## Setup

The test configures shared styling once, then overrides settings for specific
plots:

```python
from ALL_PLOTS import ALL_PLOT
from colors_set import DISTINCT_2_1, DISTINCT_2_7, GRADIENT_GREEN_6
import numpy as np
import pandas as pd

PLOT_FN = ALL_PLOT(
    figsize=(6, 4),
    X_label_fontsize=8,
    X_label_rotate=45,
    Y_label_rotate=0,
    Y_label_fontsize=8,
    annot=True,
    annot_decimal_places=2,
    annot_font_size=9,
    switch_off_yaxis=True,
    switch_off_xaxis=True,
    colors=DISTINCT_2_7,
    artificial_darkening=1,
    grid_opacity=1,
    grid_color="white",
    grid_widths=0.2,
    grid_shape="xy",
    pad_inches=0.06,
)
```

| Setup parameter | What it does |
| --- | --- |
| `figsize=(6, 4)` | Sets the figure size in inches. A plot call can override it. |
| `X_label_fontsize=8`, `Y_label_fontsize=8` | Sets the x- and y-axis tick-label sizes. |
| `X_label_rotate=45`, `Y_label_rotate=0` | Rotates x-axis labels 45 degrees and leaves y-axis labels horizontal. |
| `annot=True` | Writes each visible cell's value in the cell. |
| `annot_decimal_places=2` | Formats cell values to two decimal places. |
| `annot_font_size=9` | Sets the annotation font size; individual plots can override it. |
| `switch_off_yaxis=True`, `switch_off_xaxis=True` | Hides the left and bottom axis spines without hiding tick labels. |
| `colors=DISTINCT_2_7` | Sets the default blue-to-light-blue heatmap palette. |
| `artificial_darkening=1` | Multiplies palette lightness by 1 (no change); values below 1 darken the palette. |
| `grid_shape="xy"` | Draws both directions of cell grid lines; `"both"` is equivalent. |
| `grid_opacity=1`, `grid_color="white"`, `grid_widths=0.2` | Sets fully opaque, white grid lines that are 0.2 points wide. |
| `pad_inches=0.06` | Sets padding around the tightly cropped saved image in inches. |

## Data

The DataFrame contains six noise conditions and twelve distortion measurements
per condition. `Noise` becomes the row index, so its values label the y-axis;
the remaining column names label the x-axis:

```python
data = [
    ["OG", 0.28055, 0.31158, 0.29258, 0.26106, 0.24943, 0.28391, 0.30787, 0.29770, 0.24134, 0.24697, 0.18378, 0.18099],
    ["Pixel Drop", 0.32030, 0.31650, 0.30429, 0.26057, 0.24561, 0.28561, 0.30278, 0.29277, 0.23024, 0.24792, 0.18063, 0.18516],
    ["ISO", 0.28526, 0.33376, 0.30581, 0.26062, 0.23708, 0.28597, 0.30110, 0.29686, 0.23022, 0.24723, 0.18088, 0.18308],
    ["Rain", 0.28413, 0.31994, 0.29493, 0.26391, 0.24224, 0.28614, 0.30456, 0.29054, 0.22817, 0.26122, 0.18915, 0.17661],
    ["Snow", 0.28874, 0.31019, 0.28975, 0.25547, 0.24122, 0.27872, 0.30408, 0.29134, 0.22660, 0.24992, 0.20279, 0.18498],
    ["Atmospheric", 0.28827, 0.31609, 0.29267, 0.26541, 0.25755, 0.30398, 0.30282, 0.29951, 0.24740, 0.24463, 0.18213, 0.20890],
]

df = pd.DataFrame(
    data,
    columns=[
        "Noise", "Pixel Drop", "ISO", "Salt", "Low Res", "Focus Blur",
        "JPG", "Chromatic", "Motion Blur", "Fog", "Rain", "Snow",
        "Atmospheric",
    ],
)
df.set_index("Noise", inplace=True)
```

## Annotated heatmap

The first call saves `Pictures/Heatmap/test_heatmap.png`. It uses the shared
palette and settings, keeps the cell aspect ratio flexible, and sets a
luminance cutoff for annotation text:

```python
PLOT_FN.plot(
    plt_type="heatmap",
    name="Pictures/Heatmap/test_heatmap",
    df=df,
    make_square=False,
    Y_label_rotate=0,
    annot_black_threshold=0.27,
)
```

`make_square=False` lets the figure shape determine cell proportions.
`annot_black_threshold=0.27` selects white text for cells below this
luminance and black text otherwise. The default automatic annotation color can
be overridden with `annot_kws={"color": "..."}`.

<p align="center">
  <img src="../Pictures/Heatmap/test_heatmap.png" alt="Annotated heatmap with noise conditions and distortion types" width="60%">
</p>

## Change x-axis label positions

`x_axis_label_dist_y` moves the x-axis labels independently. Positive values
move labels higher; the values are offsets in inches. Each label shown on the
axis must have a matching entry in the dictionary:

```python
x_axis_label_dist_y = {
    "Pixel Drop": 0.09, "ISO": 0.05, "Salt": 0,
    "Low Res": 0.09, "Focus Blur": 0.09,
    "JPG": 0, "Chromatic": 0.09,
    "Motion Blur": 0.09, "Fog": 0.09,
    "Rain": 0.05, "Snow": 0.05,
    "Atmospheric": 0.09,
}

PLOT_FN.plot(
    plt_type="heatmap",
    name="Pictures/Heatmap/test_heatmap_x_axis_pos",
    df=df,
    colors=DISTINCT_2_1,
    make_square=True,
    x_axis_label_dist_y=x_axis_label_dist_y,
    artificial_darkening=0.8,
    annot_black_threshold=0.23,
)
```

Here, `DISTINCT_2_1` changes the palette to black-to-orange and
`make_square=True` gives the cells equal width and height. The per-call
`artificial_darkening=0.8` darkens the palette. The lower annotation cutoff
means fewer cells use white text than in the first plot.

<p align="center">
  <img src="../Pictures/Heatmap/test_heatmap_x_axis_pos.png" alt="Heatmap with individually adjusted x-axis label positions" width="60%">
</p>

## Transpose the data and add a colorbar

The next example transposes the DataFrame so distortion types become rows and
noise conditions become columns. `df.iloc[:-3]` drops its final three rows,
leaving a 9-by-6 table. The call uses a reversed green palette with six color
levels and adds a labeled colorbar:

```python
df = df.T
df = df.iloc[:-3]

PLOT_FN.plot(
    plt_type="heatmap",
    name="Pictures/Heatmap/test_heatmap_color_bar",
    df=df,
    colors=GRADIENT_GREEN_6[::-1],
    n_bins=6,
    grid_widths=0.3,
    annot_font_size=5,
    artificial_darkening=0.8,
    cbar=True,
    cbar_labels=True,
    figsize=(4, 4),
)
```

`cbar=True` displays the colorbar, while `cbar_labels=True` enables its
automatically generated tick labels. `figsize=(4, 4)` overrides the shared
figure size, and `annot_font_size=5` makes the annotations smaller to fit the
denser plot.

<p align="center">
  <img src="../Pictures/Heatmap/test_heatmap_color_bar.png" alt="Transposed heatmap with a labeled green colorbar" width="55%">
</p>

## Mask cells

The final example uses a boolean array with the same 9-by-6 shape as `df`.
In this heatmap API, `True` means show the cell and `False` means hide it:

```python
mask = np.array([
    [True, True, False, False, True, True],
    [False, False, True, True, True, True],
    [False, False, True, False, True, True],
    [False, False, True, False, True, True],
    [False, True, True, False, True, True],
    [True, False, True, True, True, True],
    [True, False, True, True, True, True],
    [False, True, False, False, True, True],
    [False, True, True, True, False, False],
])

PLOT_FN.plot(
    plt_type="heatmap",
    name="Pictures/Heatmap/test_heatmap_mask",
    df=df,
    mask=mask,
    colors=GRADIENT_GREEN_6[::-1],
    n_bins=6,
    grid_widths=0.3,
    annot_font_size=5,
    artificial_darkening=0.8,
    figsize=(4, 4),
)
```

The same palette, grid width, annotation size, darkening, and figure size are
used as in the colorbar example. Cells excluded by the mask are left blank and
have no annotation.

<p align="center">
  <img src="../Pictures/Heatmap/test_heatmap_mask.png" alt="Heatmap with selected cells hidden by a boolean mask" width="55%">
</p>

## Other heatmap options

| Parameter | Effect |
| --- | --- |
| `annot=False` | Hides cell-value annotations. |
| `annot_decimal_places` | Sets the number of decimal places shown in annotations. |
| `annot_kws` | Passes Matplotlib text options to annotations; `color` overrides automatic contrast. |
| `vmin`, `vmax` | Set the lower and upper values mapped to the palette. |
| `center` | Centers the color normalization on a chosen value. |
| `cbar_kws` | Passes options such as size and spacing to the colorbar. |
| `cbar_count`, `cbar_label_fontsize`, `cbar_label_rotate` | Configure the count, font size, and rotation of colorbar tick labels. |
| `grid_shape` | Uses `"both"`/`"xy"` for both grid directions, `"x"` for vertical, `"y"` for horizontal, or `None` for no grid. |
| `grid_color`, `grid_opacity`, `grid_widths` | Style the cell grid. |
| `make_square` | Sets equal cell width and height when `True`. |

Non-finite values such as `NaN` are omitted automatically. `mask` must match
the data shape; `True` cells are shown and `False` cells are omitted.
