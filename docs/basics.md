# Basics: `ALL_PLOT` and shared options

Every plot in this repository goes through one class, [`ALL_PLOT`](../ALL_PLOTS.py).
You create it once with the settings you want to share across plots, then call
`plot()` once per image. This page covers the settings that work for every plot
type. The plot-specific pages list the rest:

- [Line plots](line.md): `plt_type="line"`
- [Bar charts and histograms](hist.md): `plt_type="bar"`
- [Heatmaps](heatmap.md): `plt_type="heatmap"`
- [Radar plots and word clouds](misc.md): `plt_type="radar"`, `plt_type="word_cloud"`
- [Scatter plots](scatter.md): `plt_type="scatter"`

## How a plot is made

```python
from ALL_PLOTS import ALL_PLOT
from colors_set import DISTINCT_3_6

# 1. Shared settings for every plot made with PLOT_FN
PLOT_FN = ALL_PLOT(
    figsize=(6, 4),
    colors=DISTINCT_3_6,
    Y_label_fontsize=10, X_label_fontsize=10,
    line_width=3,                     # plot-specific options can go here too
)

# 2. One call per image: plot type, output name, data, and any overrides
PLOT_FN.plot(
    plt_type="line",
    name="Pictures/Lines/my_plot",    # saved as Pictures/Lines/my_plot.png
    Lines=[[[0, 1, 2], [10, 40, 25]]],
    X_label_fontsize=14,              # applies to this call only
)
```

`plot()` does the following, in order:

1. Creates a new figure of size `figsize`.
2. Adjusts the colors by `artificial_darkening`.
3. Draws the data with the plot type's own function.
4. Builds the axis ticks, grid, and axis lines.
5. Adds a legend if `legend=True`.
6. Saves `<name>.png`.

The folder in `name` must already exist.

## Three ways to set an option

| Where you set it | How long it lasts |
| --- | --- |
| `ALL_PLOT(...)` | Every later `plot()` call, until you change it. |
| `PLOT_FN.plot(..., option=value)` | That one call. The previous value comes back afterwards. |
| `PLOT_FN.update(dict(option=value))` | Every later call. Only works for the options named in the table below. |

`update()` raises an error for any name that isn't a constructor option in the
table below, such as `line_width`. To change one of those, pass it per call, or
create a new `ALL_PLOT`.

```python
# Swap to horizontal layout for all following plots
PLOT_FN.update(dict(
    figsize=(4, 5.5),
    grid_shape="x",
    switch_off_xaxis=True,
))
```

## Constructor options

### Figure and saving

| Option | Default | What it does |
| --- | --- | --- |
| `figsize` | `(8, 6)` | Figure width and height in inches. |
| `subplot_kw` | `None` | Passed to `plt.subplots`. Use `{"projection": "polar"}` for radar plots. |
| `polaroid_coordinates` | `False` | Set `True` with a polar projection so axis lines and label offsets use the circular layout. |
| `name` | `None` | Default output name. Usually given per call instead. |
| `pad_inches` | `0.1` | White space around the saved image, in inches. |
| `legend` | `False` | Draw a legend from the plot's labels. |
| `dpi` *(per call)* | `300` | Resolution of the saved PNG. |
| `transparent` *(per call)* | `False` | Save with a transparent background. |

### Colors

| Option | Default | What it does |
| --- | --- | --- |
| `colors` | `None` | One color, a list of colors, or a dict of label → color. Lists in [`colors_set.py`](../colors_set.py) such as `DISTINCT_3_6` or `GRADIENT_9` work directly. |
| `artificial_darkening` | `0.8` | Multiplies each color's lightness. Below `1` darkens, `1` keeps the color, above `1` lightens. |

### Axis ticks

Tick positions are generated automatically from the data unless you pass
`X_range`/`X_labels` or `Y_range`/`Y_labels` yourself. The automatic ticks are
`points + 1` evenly spaced values from `min(data) - down_offset` to
`max(data) + up_offset`.

| Option | Default | What it does |
| --- | --- | --- |
| `y_points`, `x_points` | `2`, `2` | Number of intervals between automatic ticks (3 ticks for `2`). |
| `y_up_offset`, `y_down_offset` | `0`, `0` | Extend the automatic y-ticks above the data maximum and below the data minimum, in data units. |
| `x_up_offset`, `x_down_offset` | `0`, `0` | The same for the x-axis. |
| `decimal_places` | `1` | Decimal places in automatic tick labels. |
| `X_range`, `X_labels` *(per call)* | auto | Explicit x-tick positions and their text. |
| `Y_range`, `Y_labels` *(per call)* | auto | Explicit y-tick positions and their text. |
| `y_ticks_allowed`, `x_ticks_allowed` | `True` | Set `False` to hide that axis's tick labels. |
| `Y_label_fontsize`, `X_label_fontsize` | `20`, `25` | Tick-label font size. |
| `Y_label_rotate`, `X_label_rotate` | `0`, `0` | Tick-label rotation in degrees. |
| `Y_label_opacity`, `X_label_opacity` | `1`, `1` | Tick-label opacity, from `0` (invisible) to `1` (solid). |

### Axis limits

The visible area runs from the first tick to the last tick. These options
widen it:

| Option | Default | What it does |
| --- | --- | --- |
| `x_axis_pos_offset` | `0` | Moves the x-axis (bottom edge) down, away from the first y-tick, in data units. |
| `y_axis_pos_offset` | `0` | Moves the y-axis (left edge) left, away from the first x-tick, in data units. |
| `y_axis_end_limit_offset` | `0.1` | Extra space above the last y-tick. |
| `x_axis_end_limit_offset` | `0.1` | Extra space to the right of the last x-tick. |

### Grid and axis lines

| Option | Default | What it does |
| --- | --- | --- |
| `grid_shape` | `"both"` | `"both"`/`"xy"` for both directions, `"x"` for vertical lines only, `"y"` for horizontal lines only, `None` for no grid. |
| `grid_opacity` | `0.3` | Grid transparency, `0` to `1`. |
| `grid_color` | `"#A8BAC4"` | Grid color. |
| `switch_off_yaxis`, `switch_off_xaxis` | `False` | Hide the left / bottom axis line. Tick labels stay. On a radar plot, `switch_off_xaxis` hides the outer circle. |
| `y_axis_width`, `x_axis_width` | `1.2` | Thickness of the axis lines. |

### Moving tick labels

These are per-call or constructor options. Each one takes a single number for
all labels, or a dict of label text → number to move labels individually.

| Option | Normal plots | Radar plots |
| --- | --- | --- |
| `x_axis_label_dist_x` | Moves x-labels right, in inches. | Rotates each label around the center, in degrees. |
| `x_axis_label_dist_y` | Moves x-labels up, in inches. | Moves each label away from the center, in inches. |
| `y_axis_label_dist_x` | Moves y-labels right, in inches. | Same as normal plots. |
| `y_axis_label_dist_y` | Moves y-labels up, in inches. | Same as normal plots. |

Negative values move the other way. When you use a dict, every label shown on
that axis needs an entry.

```python
# Same shift for every label: move all x-labels 0.1 inch down
PLOT_FN.plot(..., x_axis_label_dist_y=-0.1)

# Different shift per label: the dict needs one entry per x-label
PLOT_FN.plot(..., x_axis_label_dist_y={"[A]": 0, "[B]": 0.1, "[C]": 0, "[D]": 0.1})
```

See the [heatmap page](heatmap.md#move-x-axis-labels) for a full per-label
example and the [radar page](misc.md#radar-plot) for the circular version.

## Reference lines and shaded bands

Line plots and bar charts can draw extra lines and bands from
[`plot_add.py`](../plot_add.py). Values are in data units. The axis range grows
to include them.

| Option | Example | What it draws |
| --- | --- | --- |
| `h_lines` | `[40, 60]` | Horizontal lines at y = 40 and y = 60. |
| `v_lines` | `[1.5]` | Vertical lines at x = 1.5. |
| `h_line_shade` | `[[10, 30]]` | A horizontal band from y = 10 to y = 30. Add more pairs for more bands. |
| `v_line_shade` | `[[1, 2.2]]` | A vertical band from x = 1 to x = 2.2. |

Styling options:

| Option | Default | Applies to |
| --- | --- | --- |
| `hline_color`, `vline_color` | red | Line color. |
| `hline_style`, `vline_style` | `"-."` | Matplotlib line style, e.g. `"-"`, `"--"`, `":"`. |
| `h_line_width`, `v_line_width` | plot's `line_width` | Line thickness. Also used for band edges. |
| `h_line_alpha`, `v_line_alpha` | `1` | Line opacity. Set `0` for a band with no edge lines. |
| `h_line_shade_color`, `v_line_shade_color` | red | Band color. A list gives one color per band. |
| `h_line_shade_color_alpha`, `v_line_shade_color_alpha` | `0.5` | Band opacity. |
| `hline_offset`, `vline_offset` | `10` | How far lines and bands extend past the data, in data units. |
| `line_z_oder` | `9` | Drawing order of reference lines. Use `50` to draw on top of the bars. |

## Colors in `colors_set.py`

Import with `from colors_set import *` or by name. Some useful groups:

| Name | Use |
| --- | --- |
| `BLUE`, `ORANGE`, `RED`, `GREEN`, `PINK`, `GREY_DARKER`, … | Single colors. |
| `DISTINCT_<n>_<k>` | Sets of *n* contrasting colors, e.g. `DISTINCT_3_6`, `DISTINCT_2_7`. |
| `GRADIENT_BLUE_6`, `GRADIENT_GREEN_6`, `GRADIENT_ORANGE_6`, `GRADIENT_9` | Ordered gradients. Good for heatmaps and many groups. |
| `ORANGE_BLUE_10`, `ORANGE_LIGHTBLUE_10`, `GREEN_ORANGE_10`, … | Ten-color diverging sets. |

Reverse a gradient with `[::-1]`, e.g. `GRADIENT_GREEN_6[::-1]`.
