

import matplotlib.pyplot as plt
from colors import * 
from plot_utils import range_calc
from style import simplify

def line_plot(Lines, COLORS = [ORANGE, BLUE, PINK], 
    figsize=(8, 6), name="test", artificial_darkening=1, decimal_places=1, alpha_line=1, line_width=5, 
    y_up_offset=0, y_down_offset=0, Y_label_fontsize=20, y_points=3, y_padding_factor=0, 
    X_labels=None, X_labels_pos = None, x_points=3, x_up_offset=0, x_down_offset=0, X_label_fontsize=25, x_padding=0.04, x_padding_factor=0,
    use_scatter=True, scatter_size=50, scatter_boder=1.5, scatter_color="white",
    h_lines=None, hline_style="-.", h_line_alpha=1, hline_color=RED, 
    ):

    fig, ax = plt.subplots(figsize=figsize)
    COLORS = [lighten_color(e, amount=artificial_darkening)  for e in COLORS]
    assert len(COLORS) >= len(Lines), "COLORS < LINES (not all lines will be plotted"

    X_pos = [] 
    Y_pose = []
    for percentage, color in zip(Lines, COLORS):
        X, Y = percentage
        X_pos += X
        Y_pose += Y
        ax.plot(X, Y, color=color, lw=line_width, alpha=alpha_line)
        if use_scatter:ax.scatter(X, Y, fc=color, s=scatter_size, lw=scatter_boder, ec=scatter_color, zorder=12)

    if h_lines:
        Y_pose += h_lines
        for h_line in h_lines:            
            ax.plot([min(X_pos), max(X_pos)], [h_line, h_line], color=hline_color, lw=line_width, linestyle=hline_style, alpha=h_line_alpha, )


    Y_range, Y_range_label = range_calc(Y_pose, y_points, y_up_off = y_up_offset , y_down_off=y_down_offset, decimal_places=decimal_places)
    if X_labels:
        X_range_label = X_labels
        if X_labels_pos:
            X_range =  X_labels_pos    
        else:
            X_range = X_pos
    else:
        X_range, X_range_label = range_calc(X_pos, x_points, y_up_off = x_up_offset , y_down_off=x_down_offset, decimal_places=decimal_places)

    simplify(ax, Y_range, Y_range_label, X_range, X_range_label, Y_label_fontsize, X_label_fontsize, x_padding=x_padding, 
    y_padding_factor=y_padding_factor, x_padding_factor=x_padding_factor)

    plt.tight_layout()
    plt.savefig(f"{name}.png")



def line_shade_plot(Lines, COLORS = [ORANGE, BLUE, PINK], 
    figsize=(8, 6), name="test_shade", decimal_places=1, alpha_line=1, line_width=5, 
    y_up_offset=0, y_down_offset=0, Y_label_fontsize=20, y_points=3, y_padding_factor=0, 
    X_labels=None, X_labels_pos = None, x_points=3, x_up_offset=0, x_down_offset=0, X_label_fontsize=25, x_padding=0.04, x_padding_factor=0,
    use_scatter=True, scatter_size=50, 
    h_lines=None, hline_style="-.", h_line_alpha=1, hline_color=RED, 
    border_line_width=None, SHADE_Colors=None, artificial_darkening=1, artificial_light=2, 
    background_vline=None, vline_color="black", 
    ):

    fig, ax = plt.subplots(figsize=figsize)
    COLORS = [lighten_color(e, amount=artificial_darkening)  for e in COLORS]
    assert len(COLORS) >= len(Lines), "COLORS < LINES (not all lines will be plotted"

    # average line dark color
    mid_path_effects = [withStroke(linewidth=6, foreground="white")]

    
    if border_line_width == None:
        border_line_width = line_width
    if SHADE_Colors == None:
        SHADE_Colors = [lighten_color(e, amount=artificial_light)  for e in COLORS]

    if background_vline is not None:
        Y_pose = []
        for percentage in Lines:
            _, Y_max, Y_min_mean, Y_min = percentage
            Y_pose += Y_max + Y_min_mean + Y_min
        
        for v_line in background_vline:            
            ax.plot([v_line, v_line], [min(Y_pose) - y_down_offset, max(Y_pose) + y_up_offset], color=vline_color, lw=line_width, linestyle=hline_style, alpha=h_line_alpha, )


    X_pos = [] 
    Y_pose = []
    # Add lines with dots
    # Note the zorder to have dots be on top of the lines
    for percentage, color, shade_color in zip(Lines, COLORS, SHADE_Colors):
        X, Y_max, Y_min_mean, Y_min = percentage
        X_pos += X
        Y_pose += Y_max + Y_min_mean + Y_min
        ax.fill_between(X, Y_min, Y_max, color=shade_color, lw=border_line_width, zorder=12, alpha=alpha_line, ec="white")
        ax.plot(X, Y_min_mean, linestyle='--', color=color, lw=line_width, zorder=12, path_effects=mid_path_effects)    
        # ax.scatter(X_pos, percentage, fc=color, s=100,  )
        if use_scatter:ax.scatter(X, Y_min_mean, fc=color, s=scatter_size, lw=1.5, ec="white", zorder=12)

    if h_lines:
        Y_pose += h_lines
        for h_line in h_lines:            
            ax.plot([min(X_pos), max(X_pos)], [h_line, h_line], color=hline_color, lw=line_width, linestyle=hline_style, alpha=h_line_alpha, )

    Y_range, Y_range_label = range_calc(Y_pose, y_points, y_up_off = y_up_offset , y_down_off=y_down_offset, decimal_places=decimal_places)
    if X_labels:
        X_range_label = X_labels
        if X_labels_pos:
            X_range =  X_labels_pos    
        else:
            X_range = X_pos
    else:
        X_range, X_range_label = range_calc(X_pos, x_points, y_up_off = x_up_offset , y_down_off=x_down_offset, decimal_places=decimal_places)

    simplify(ax, Y_range, Y_range_label, X_range, X_range_label, Y_label_fontsize, X_label_fontsize, x_padding=x_padding, 
    y_padding_factor=y_padding_factor, x_padding_factor=x_padding_factor)


    plt.tight_layout()
    plt.savefig(f"{name}.png")
