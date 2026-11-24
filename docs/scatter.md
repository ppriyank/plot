# Scatter plots

`plt_type="scatter"` draws 2-D points colored by group, with a size and marker
shape per point. Every example below comes from
[`test_scatter.py`](../test_scatter.py). For options shared by all plots
(figure size, ticks, axis limits, grid, label offsets, reference lines), see
[basics](basics.md).

Run the examples with:

```bash
python test_scatter.py
```

The test data is random (`torch.randn`), so your images will differ from the
ones shown here.

## Data format

| Input | Shape | Meaning |
| --- | --- | --- |
| `Points` | `(N, 2)` | `[x, y]` per point. Tensor, array or nested list. |
| `Labels` | `(N,)` | Integer group per point. Points in a group share a color and shape. |
| `Sizes` | `(N,)` | Marker area per point. |

Points are drawn from largest to smallest, so small markers are not hidden
behind large ones.

## Setup used by the examples

```python
from ALL_PLOTS import ALL_PLOT
from colors_set import *
import torch

PLOT_FN = ALL_PLOT(
    figsize=(6, 6),
    colors=ORANGE_LIGHTBLUE_10,
    decimal_places=0,
    y_up_offset=20, y_down_offset=20,
    x_up_offset=20, x_down_offset=20,
    Y_label_fontsize=10, X_label_fontsize=10,
    scatter_boder_color="black", scatter_alpha=0.8,
)

N_POINTS = 100
POINTS = torch.randn(N_POINTS, 2) * 100
Labels = torch.randint(0, 9, (N_POINTS,))     # 9 groups
SIZES  = torch.randint(50, 500, (N_POINTS,))
```

## Scatter options

| Option | Default | What it does |
| --- | --- | --- |
| `Points` | required | `[x, y]` coordinates. |
| `Labels` | all `0` | Group per point. |
| `Sizes` | required | Marker area, one per point. A single number is not supported yet; use e.g. `torch.full((N,), 40)`. |
| `Shapes` | `"o"` | Marker shape: one shape for all, a list (one per group in sorted order), or a dict of label → shape. |
| `colors` | orange, blue, pink | A list (one per group in sorted order) or a dict of label → color. With fewer colors than groups, the XKCD palette is used instead. For one color, pass a one-item list such as `[BLUE]`. |
| `scatter_boder` | `1.5` | Marker edge thickness. |
| `scatter_boder_color` | `"white"` | Marker edge color. |
| `scatter_alpha` | `1` | Marker opacity. |
| `enable_relabeling` | `None` | Renumber the groups `0, 1, 2, …` in sorted order before drawing. Prints the mapping. |
| `line_width` | `1` | Default width of reference lines. |
| `hline_offset`, `vline_offset` | `10` | How far reference lines and bands extend past the data. |

Reference lines and shaded bands (`h_lines`, `v_lines`, `h_line_shade`,
`v_line_shade` and their styling) are listed in
[basics](basics.md#reference-lines-and-shaded-bands).

## Grouped scatter plot

```python
PLOT_FN.plot(plt_type="scatter", name="Pictures/Scatter/test_scatter",
    Points=POINTS, Labels=Labels, Sizes=SIZES,
)
```

<p align="center">
  <img src="../Pictures/Scatter/test_scatter.png" alt="Scatter plot with 100 points grouped by nine integer labels and drawn at variable sizes" width="50%">
</p>

## Marker shapes and a vertical band

A dict gives each group its own marker. Any
[Matplotlib marker](https://matplotlib.org/stable/api/markers_api.html) works.
This example also shades the x-range −50 to 50, with no edge lines
(`v_line_alpha=0`):

```python
SHAPE = {0: "o", 1: "v", 2: "*", 3: "^", 4: "<", 5: ">", 6: "8", 7: "s", 8: "P"}

PLOT_FN.plot(plt_type="scatter", name="Pictures/Scatter/test_scatter_shape",
    Points=POINTS, Labels=Labels, Sizes=SIZES, Shapes=SHAPE,
    v_line_shade=[[-50, 50]], v_line_shade_color="black",
    v_line_shade_color_alpha=0.2, v_line_alpha=0,
    vline_offset=50, hline_offset=50,
)
```

<p align="center">
  <img src="../Pictures/Scatter/test_scatter_shape.png" alt="Grouped scatter plot using a different marker shape for each label" width="50%">
</p>

## Horizontal bands

The test hides the left axis line and adds y-ticks for every later plot with
`update()`, then draws two colored bands:

```python
PLOT_FN.update(dict(
    switch_off_yaxis=True,
    y_points=5,
))

PLOT_FN.plot(plt_type="scatter", name="Pictures/Scatter/test_scatter_shade",
    Points=POINTS, Labels=Labels, Sizes=SIZES,
    h_line_shade=[[-50, 50], [50, 300]],
    h_line_shade_color=DISTINCT_2_8,      # one color per band
    h_line_shade_color_alpha=0.3,
    line_width=1,
    vline_offset=50, hline_offset=50,
)
```

<p align="center">
  <img src="../Pictures/Scatter/test_scatter_shade.png" alt="Scatter plot with two horizontal shaded bands" width="50%">
</p>

## Common changes

```python
# One color and size for everything
PLOT_FN.plot(plt_type="scatter", name="Pictures/Scatter/my_plain",
    Points=POINTS, Sizes=torch.full((N_POINTS,), 40), colors=[BLUE])

# Named colors per group
PLOT_FN.plot(plt_type="scatter", name="Pictures/Scatter/my_named",
    Points=POINTS, Labels=Labels % 2, Sizes=SIZES, colors={0: BLUE, 1: ORANGE})
```
