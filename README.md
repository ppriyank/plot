# Plot

Plot is a small collection of Matplotlib helpers for creating publication-ready
line, scatter, bar, histogram, heatmap, radar, box, word-cloud, network, and
Sankey plots.

## Documentation

- [Line plots](docs/line.md)
- [Scatter plots](docs/scatter.md)
- [Line examples](test_line.py)
- [Scatter examples](test_scatter.py)

## Quick start

```python
from ALL_PLOTS import ALL_PLOT
from colors_set import DISTINCT_3_6

plotter = ALL_PLOT(
    figsize=(6, 6),
    colors=DISTINCT_3_6,
    artificial_darkening=0.8,
)

plotter.plot(
    plt_type="line",
    name="Pictures/Lines/my_line_plot",
    Lines=[
        [[0, 1, 2, 3], [10, 45, 35, 75]],
        [[0, 1, 2, 3], [20, 30, 55, 60]],
    ],
)
```

## Installation

```bash
python -m pip install matplotlib torch numpy
python -m pip install seaborn wordcloud netgraph
```

Run the example scripts from the repository root:

```bash
python test_line.py
python test_scatter.py
```
