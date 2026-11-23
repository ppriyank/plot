# Radar plots and word clouds

These examples come from [`test_misc.py`](../test_misc.py). For options shared by
all plots, see [basics](basics.md).

Run the examples with:

```bash
python test_misc.py
```

## Radar plot

`plt_type="radar"` draws each curve as a filled shape around a circle. Each
spoke is one category, and distance from the center is the value. Three curves
is about the most that stays readable.

### Setup

A radar plot needs a polar figure. Set both `subplot_kw` and
`polaroid_coordinates`:

```python
from ALL_PLOTS import ALL_PLOT
from colors_set import *
import torch

PLOT_FN = ALL_PLOT(
    subplot_kw={"projection": "polar"},   # polar figure
    polaroid_coordinates=True,            # polar-aware axis lines and label offsets

    figsize=(6, 4),
    colors=DISTINCT_3_6,
    artificial_darkening=1,

    grid_shape="x",                       # spokes only, no rings
    grid_opacity=1,
    switch_off_xaxis=True,                # hide the outer circle
    X_label_fontsize=10,                  # category labels
    Y_label_fontsize=8,                   # ring value labels

    x_axis_label_dist_x=10,               # rotate category labels 10 degrees
    x_axis_label_dist_y=0.1,              # and move them 0.1 inch outward
)
```

On a radar plot, the **x-axis** is the angle (the categories around the circle)
and the **y-axis** is the radius (the value rings).

### Data and call

```python
A = torch.rand(10) * 100
B = torch.rand(10) * 100
C = torch.rand(10) * 100

Radar_label = ["ImageNet", "ImageNet-Sketch", "ImageNet-A", "ImageNet-V2",
               "ImageNet-R", "Caltech", "DTD", "food101", "SUN397", "Stanford-Cars"]

PLOT_FN.plot(plt_type="radar", name="Pictures/Misc/test_radar",
    Curves=[A, B, C],
    Alphas=[0.5, 0.5, 0.5],
    Curves_names=["Curve A", "Curve B", "Curve C"],
    Y_range=[10, 50, 100], Y_labels=["10", "50", "100"],
    X_labels=Radar_label,
    colors=DISTINCT_3_2,
)
```

<p align="center">
  <img src="../Pictures/Misc/test_radar.png" alt="Radar plot of three random curves over ten dataset categories" width="50%">
</p>

### Radar options

| Option | Default | What it does |
| --- | --- | --- |
| `Curves` | required | List of curves. Each is a list or 1-D tensor with one value per category. All curves need the same length. |
| `Curves_names` | required | One name per curve. Shown in the legend when `legend=True`. |
| `Alphas` | required | Fill opacity per curve, e.g. `[0.5, 0.5, 0.5]`. Use `0` for an outline only. |
| `colors` | orange, blue, pink | One color per curve. |
| `X_labels` | angles | One category name per value, in order counter-clockwise starting from the right. |
| `Y_range` | required | Radii of the value rings, e.g. `[10, 50, 100]`. |
| `Y_labels` | `None` | Text for each ring. Pass `Y_labels=["", "", ""]` or `y_ticks_allowed=False` to hide the ring values. |
| `curve_line_width` | `1` | Outline thickness. |
| `curve_line_opacity` | `1` | Outline opacity. |
| `switch_off_xaxis` | `False` | Hide the outer circle. |
| `x_axis_width` | `1.2` | Thickness of the outer circle when it is shown. |
| `grid_shape` | `"both"` | `"x"` for spokes only, `"y"` for rings only, `"both"` for both, `None` for neither. |

### Positioning the category labels

On a radar plot, the x-label offsets work in circular terms:

| Option | Unit | Effect |
| --- | --- | --- |
| `x_axis_label_dist_x` | degrees | Rotates each label around the center. Positive is counter-clockwise. |
| `x_axis_label_dist_y` | inches | Moves each label away from the center. Negative moves it inward. |

Both take one number for all labels, or a dict to move single labels:

```python
PLOT_FN.plot(plt_type="radar", name="Pictures/Misc/my_radar",
    Curves=[A, B], Alphas=[0.4, 0.4], Curves_names=["A", "B"],
    Y_range=[10, 50, 100], Y_labels=["10", "50", "100"],
    X_labels=list(Radar_label),
    x_axis_label_dist_x=0,
    x_axis_label_dist_y={name: 0.2 if "ImageNet" in name else 0
                         for name in Radar_label},   # push ImageNet labels out
)
```

### Notes

- The plot adds the first category to the end of `X_labels` to close the
  circle, which changes the list you passed in. Pass a copy, e.g.
  `X_labels=list(Radar_label)`, if you reuse the list for another plot.
- `X_labels` must have one entry per value in a curve.
- `Y_range` has no automatic default for radar plots and must be passed.

## Word cloud

`plt_type="word_cloud"` draws words sized by a number such as a count or
frequency. You can also color each word by a second number. It needs the
`wordcloud` package (`pip install wordcloud`).

```python
from ALL_PLOTS import ALL_PLOT
from colors_set import *
import numpy as np

PLOT_FN = ALL_PLOT(
    figsize=(6, 4),
    artificial_darkening=1,
    pad_inches=0.1,
)

names = ["ImageNet", "ImageNet-Sketch", "ImageNet-A", "ImageNet-V2", "ImageNet-R",
         "Caltech", "DTD", "food101", "SUN397", "Stanford-Cars", "FGVC-Aircraft",
         "Oxford-Pets", "Oxford-Flowers102", "EuroSAT", "UCF101"]
sizes = [50000, 50000, 7500, 10000, 30000, 6085, 1880, 25250, 19850, 8041,
         3333, 3669, 6149, 5000, 1794]
values = np.random.default_rng(seed=42).standard_normal(len(sizes)).tolist()

PLOT_FN.plot(plt_type="word_cloud", name="Pictures/Misc/test_word_cloud",
    Nodes=names, Sizes=sizes,
    Values=values,                    # colors each word by its value
    colors=DISTINCT_2_2,
    word_cloud_shape=(650, 850),
)
```

<p align="center">
  <img src="../Pictures/Misc/test_word_cloud.png" alt="Word cloud of dataset names sized by dataset size" width="50%">
</p>

This call is commented out in `test_misc.py`. Uncomment it to regenerate the
image.

### Word cloud options

| Option | Default | What it does |
| --- | --- | --- |
| `Nodes` | required | The words. |
| `Sizes` | required | One number per word. Bigger numbers give bigger words. |
| `Values` | `None` | One number per word, mapped onto the `colors` gradient (low values get the first color). Without it, the word cloud picks colors from the gradient itself. |
| `colors` | orange, blue, pink | Two or more colors, blended into a gradient. |
| `n_bins` | `10` | Number of color steps in the gradient. |
| `word_cloud_shape` | `(2000, 3500)` | Canvas `(height, width)` in pixels. Sets the shape of the cloud. |
| `scale_factor` | `3` | Rendering scale. Higher gives sharper words and slower rendering. |

Ticks, grid and axis lines are turned off for word clouds. Only the figure and
saving options from [basics](basics.md) apply.
