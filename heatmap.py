import numpy as np
from matplotlib.colors import TwoSlopeNorm
from numbers import Integral
from typing import Literal
from plot_add import *
from plot_utils import range_calc

def generate_axis(df):
    X_labels = list(df.columns)
    Y_labels = list(df.index)
    X_range = [index + 0.5 for index in range(len(X_labels))]
    Y_range = [index + 0.5 for index in range(len(Y_labels))]
    return X_range, X_labels, Y_range, Y_labels


def create_color_gradient(colors, n_bins=100):
    if isinstance(colors, dict):
        assert False 
    colors_template = LinearSegmentedColormap.from_list('custom_gradient', colors, N=n_bins)
    return colors_template


def _annotation_text_color(rgba, annot_black_threshold):
    channels = np.asarray(rgba[:3])
    linear_channels = np.where(
        channels <= 0.04045,
        channels / 12.92,
        ((channels + 0.055) / 1.055) ** 2.4,
    )
    luminance = np.dot(linear_channels, [0.2126, 0.7152, 0.0722])
    return "white" if luminance < annot_black_threshold else "black"

def params_to_return(ncols, nrows, X_range, X_labels, Y_range, Y_labels):
    add_params = {
        "ncols": ncols,
        "nrows": nrows,
        "X_range": X_range,
        "X_labels": X_labels,
        "Y_range": Y_range,
        "Y_labels": Y_labels,

        "grid_shape": None, 
        "grid_opacity": 0, 
        "grid_color": None, 

        'x_axis_pos_offset' : 0.5,
        'y_axis_end_limit_offset' : 0.5, 
        'y_axis_pos_offset': 0.5, 
        'x_axis_end_limit_offset': 0.5, 
    }
    return add_params

def make_grid(grid_shape='xy', grid_color=RED, grid_opacity=1, grid_widths=2, ax=None, x_edges=None, y_edges=None, nrows=10, ncols=10):
    if grid_shape == "xy":
        grid_shape = "both"
    if grid_shape not in ("both", "x", "y", None):
        raise ValueError("grid_shape must be one of 'both', 'xy', 'x', or 'y'")
    if grid_shape in ("both", "x"):
        ax.vlines(
            x_edges,
            0,
            nrows,
            color=grid_color,
            alpha=grid_opacity,
            linewidth=grid_widths,
        )
    if grid_shape in ("both", "y"):
        ax.hlines(
            y_edges,
            0,
            ncols,
            color=grid_color,
            alpha=grid_opacity,
            linewidth=grid_widths,
        )

def heatmap_plt(
    ax,
    df=None,
    mask=None,
    make_square=True, 
    
    colors = [ORANGE, BLUE, PINK],
    n_bins = 100, 

    vmin=None,
    vmax=None,
    center=None,
    
    cbar=False,
    cbar_kws={
        'shrink': 0.5,  ## size of color bar
        'pad': 0.03  ## x axis distance from plot 
    },
    cbar_labels = None, 
    cbar_count=3, 
    cbar_label_fontsize=5,
    cbar_label_rotate=0,
    
    annot=True,
    annot_kws=None,
    annot_font_size=5, 
    annot_decimal_places=0, 
    annot_black_threshold=0.3, 

    vline_offset = 10,
    hline_offset = 10,
    line_width=1,

    grid_shape: Literal["both", "xy", "x", "y"] = "both",
    grid_opacity=1, 
    grid_color='white', 
    grid_widths=2,

    **args,
    ):

    if df is None:
        raise ValueError("df must contain a two-dimensional heatmap")
    data = np.ma.masked_invalid(np.ma.asarray(df, dtype=float))
    if data.ndim != 2 or not all(data.shape):
        raise ValueError("df must contain a non-empty two-dimensional heatmap")
    if mask is not None:
        data = np.ma.masked_where(np.asarray(mask, dtype=bool), data)

    colors = create_color_gradient(colors, n_bins=n_bins)

    if make_square:
        ax.set_aspect("equal")
    
    X_range, X_labels, Y_range, Y_labels = generate_axis(df)
    nrows, ncols = data.shape
    x_edges = np.arange(ncols + 1)
    y_edges = np.arange(nrows + 1)


    ####### In case 3+ colors, center == middle color 
    norm = None
    if center is not None:
        values = data.compressed()
        norm = TwoSlopeNorm(
            vmin=vmin if vmin is not None else values.min(),
            vcenter=center,
            vmax=vmax if vmax is not None else values.max(),
        )

    ####### Heatmap
    mesh = ax.pcolormesh(
        x_edges,
        y_edges,
        data,
        shading="flat",
        cmap=colors,
        vmin=None if norm is not None else vmin,
        vmax=None if norm is not None else vmax,
        norm=norm,
        edgecolors="none",
        linewidth=0,
    )

    ####### Grid
    make_grid(grid_shape=grid_shape, grid_color=grid_color, 
        grid_opacity=grid_opacity, grid_widths=grid_widths, 
        ax=ax, x_edges=x_edges, y_edges=y_edges, nrows=nrows, ncols=ncols)
    
    ####### Annotation 
    if annot:
        annotation_formatter = lambda x: f"{x:.{annot_decimal_places}f}"
        annotation_options = {"ha": "center", "va": "center", 'zorder':15, 'fontsize': annot_font_size, }
        annotation_options.update(annot_kws or {})
        for row in range(nrows):
            for column in range(ncols):
                value = data[row, column]
                if not np.ma.is_masked(value):
                    cell_annotation_options = annotation_options
                    if "color" not in annotation_options:
                        cell_annotation_options = {
                            **annotation_options,
                            "color": _annotation_text_color(mesh.to_rgba(value), annot_black_threshold),
                        }
                    ax.text(
                        column + 0.5, row + 0.5, annotation_formatter(value), 
                        **cell_annotation_options,
                    )
        
        
    VALUES = data.data.reshape(-1)
    ####### Color Bars 
    if cbar:
        colorbar = ax.figure.colorbar(mesh, ax=ax, **(cbar_kws or {}))
        if cbar_labels:
            cbar_pos, cbar_vals = range_calc(VALUES, cbar_count-1, decimal_places=annot_decimal_places)
            colorbar.set_ticks(cbar_pos)
            colorbar.set_ticklabels(cbar_vals, fontsize=cbar_label_fontsize, rotation=cbar_label_rotate)
            # colorbar.set_label('Custom Label')
        else:
            colorbar.set_ticks([])
            colorbar.set_ticklabels('')

    X_values = [0, ncols]
    Y_values = [0, nrows]

    local_X, local_Y = plot_background_lines_shades(hline_offset=hline_offset, vline_offset=vline_offset, ax=ax,
        X_values=X_values, Y_values=Y_values, line_width=line_width, **args)
    X_values += local_X
    Y_values += local_Y

    #### Plot derived parametes
    add_params = params_to_return(ncols, nrows, X_range, X_labels, Y_range, Y_labels)
    

    return X_values, Y_values, add_params
