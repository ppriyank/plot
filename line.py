

import matplotlib.pyplot as plt
from colors import * 
from plot_utils import range_calc
from style import simplify

# def line_plot(Lines, colors = [ORANGE, BLUE, PINK], 
#     figsize=(8, 6), name="test", artificial_darkening=1, decimal_places=1, alpha_line=1, line_width=5, 
#     y_up_offset=0, y_down_offset=0, Y_label_fontsize=20, y_points=3, y_padding_factor=0, 
#     X_labels=None, X_labels_pos = None, x_points=3, x_up_offset=0, x_down_offset=0, X_label_fontsize=25, x_padding=0.04, x_padding_factor=0,
#     use_scatter=True, scatter_size=50,  scatter_color="white",
#     h_lines=None, hline_style="-.", h_line_alpha=1, hline_color=RED, add_black_outline=None, 
#     switch_off_yaxis=None, grid_opacity=1, grid_shape='y', X=None, ax=None
#     ):





#     Y_range, Y_range_label = range_calc(Y_pose, y_points, y_up_off = y_up_offset , y_down_off=y_down_offset, decimal_places=decimal_places)
#     if X_labels:
#         X_range_label = X_labels
#         if X_labels_pos:
#             X_range =  X_labels_pos    
#         else:
#             X_range = X_pos
#     else:
#         X_range, X_range_label = range_calc(X_pos, x_points, y_up_off = x_up_offset , y_down_off=x_down_offset, decimal_places=decimal_places)

#     simplify(ax, Y_range, Y_range_label, X_range, X_range_label, Y_label_fontsize, X_label_fontsize, x_padding=x_padding, 
#     y_padding_factor=y_padding_factor, x_padding_factor=x_padding_factor, switch_off_yaxis=switch_off_yaxis, grid_opacity=grid_opacity, 
#     grid_shape=grid_shape,)

    
    


def line_plot(ax=None,

    Lines=None, 
    colors = [ORANGE, BLUE, PINK],  
    
    line_width=5, 
    alpha_line=1, 
    
    use_scatter=True, 
    scatter_size=50, 
    scatter_boder=1.5,
    scatter_boder_color=None, 

    h_lines=None,  # [40]
    hline_style="-.", 
    h_line_alpha=1, 
    hline_color=RED, 
    hline_offset = 3,

    shade=False, 
    shade_up=None,
    shade_down=None,
    shade_line_width = 2,  
    shade_alpha=0.5, 
    shade_darkening=1, 
    
    v_lines=None, 
    vline_style="-.", 
    v_line_alpha=1, 
    vline_color=RED, 
    vline_offset = 3,
    
    **args
    ):

    assert len(colors) >= len(Lines), "COLORS < LINES (not all lines will be plotted"


    ### plot line 
    X_values = [] 
    Y_values = []
    for (X, Y), color in zip(Lines, colors):
        X_values += X
        Y_values += Y
        ax.plot(X, Y, color=color, lw=line_width, alpha=alpha_line, zorder=13)

    ### plot scatter
    if use_scatter:
        for (X, Y), color in zip(Lines, colors):
            ax.scatter(X, Y, fc=color, s=scatter_size, lw=scatter_boder, ec=scatter_boder_color, zorder=14)


    ### plot horizontal_lines
    if h_lines:
        Y_values += h_lines
        for h_line in h_lines:            
            ax.plot([min(X_values) - hline_offset, max(X_values) + hline_offset], [h_line, h_line], color=hline_color, lw=line_width, linestyle=hline_style, alpha=h_line_alpha, )

    ### plot horizontal_lines
    if v_lines:
        X_values += v_lines
        for v_line in v_lines:            
            ax.plot([v_line, v_line], [min(Y_values) - vline_offset, max(Y_values) + vline_offset], color=vline_color, lw=line_width, linestyle=hline_style, alpha=v_line_alpha, )
        
    
    vline_style="-.", 
    v_line_alpha=1, 
    vline_color=RED, 
    vline_offset = 3,


    ### plot shades
    if shade:
        shade_colors = [lighten_color(e, amount=shade_darkening)  for e in colors]

        for y_max, y_min, shade_color in zip(shade_up, shade_down, shade_colors):
            assert y_max[0] == y_min[0]
            X = y_max[0]
            
            y_up = y_max[1]
            y_down = y_min[1]
            
            Y_values += y_up 
            Y_values += y_down
            
            ax.fill_between(X, y_down, y_up, color=shade_color, alpha=shade_alpha, zorder=12, ec="white", lw=shade_line_width)
            
    # plt.savefig("test_multiple.png", dpi=300)
    return X_values, Y_values
    
    
    
    
    
    
    
