# Scatter plots

These examples correspond to [`test_scatter.py`](../test_scatter.py). Scatter
plots accept 2D points, group labels, and marker sizes.

## Basic grouped scatter plot

```python
from ALL_PLOTS import ALL_PLOT
from colors_set import DISTINCT_3_6
import torch

plotter = ALL_PLOT(
    figsize=(6, 6),
    colors=DISTINCT_3_6,
    artificial_darkening=0.8,
    decimal_places=0,
    y_up_offset=20,
    y_down_offset=20,
    x_up_offset=20,
    x_down_offset=20,
    Y_label_fontsize=10,
    X_label_fontsize=10,
    scatter_boder_color="black",
    scatter_alpha=0.9,
)

points = torch.randn(100, 2) * 100
labels = torch.randint(0, 3, (100,))
sizes = torch.randint(50, 500, (100,))

plotter.plot(
    plt_type="scatter",
    name="Pictures/Scatter/test_scatter",
    Points=points,
    Labels=labels,
    Sizes=sizes,
)
```

<p align="center">
  <img src="../Pictures/Scatter/test_scatter.png" alt="Grouped scatter plot with variable sizes" width="70%">
</p>

Labels are assigned colors and marker shapes. Points are sorted by size before
drawing, so smaller markers are less likely to be hidden behind larger markers.

## Marker and label options

| Argument | Purpose |
| --- | --- |
| `Points` | Tensor or array of `[x, y]` coordinates |
| `Labels` | Group label for every point |
| `Sizes` | Single size or a size for every point |
| `Shapes` | String or list of marker shapes, keyed by label |
| `colors` | String, list, or label-to-color mapping |
| `scatter_boder` | Marker border width |
| `scatter_boder_color` | Marker border color |
| `scatter_alpha` | Marker transparency |
| `enable_relabeling` | Renumber labels for a compact label set |

## Scatter plot with shaded regions

[`plot_add.py`](../plot_add.py) annotations can be combined with scatter plots:

```python
from colors_set import DISTINCT_2_8

plotter.plot(
    plt_type="scatter",
    name="Pictures/Scatter/test_scatter_shade",
    Points=points,
    Labels=labels,
    Sizes=sizes,
    h_line_shade=[[-50, 50], [50, 300]],
    h_line_shade_color=DISTINCT_2_8,
    h_line_shade_color_alpha=0.3,
    vline_offset=50,
    hline_offset=50,
)
```

<p align="center">
  <img src="../Pictures/Scatter/test_scatter_shade.png" alt="Scatter plot with shaded regions" width="70%">
</p>

The same annotation arguments used in [`line.md`](line.md) are available:

- `h_lines` and `v_lines` draw guide lines.
- `h_line_shade` draws horizontal shaded bands.
- `v_line_shade` draws vertical shaded bands.
- `hline_offset` and `vline_offset` extend guide ranges beyond the data.

## Colors

Named colors and palette sets are available in
[`colors_set.py`](../colors_set.py).

```python
from colors_set import DISTINCT_3_6

plotter = ALL_PLOT(
    colors=DISTINCT_3_6,
    artificial_darkening=0.8,
)
```

The scatter helper accepts the following color forms:

| Color input | Behavior |
| --- | --- |
| `colors="blue"` | Apply one color to every label |
| `colors=[BLUE, ORANGE, RED]` | Assign colors to labels in sorted order |
| `colors={"category": "#hex", ...}` | Assign explicit colors to label values |
