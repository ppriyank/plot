from ALL_PLOTS import ALL_PLOT
from line import line_plot
from colors_set import *
import torch

Line_config = dict(
    line_width=5, alpha_line=1, 
    use_scatter=True, scatter_size=300, scatter_boder_color='black', scatter_alpha=0.5,
)

PLOT_FN = ALL_PLOT(
    figsize=(6, 6), 
    colors=DISTINCT_3_6, artificial_darkening=0.8,
    decimal_places=1,
    y_up_offset=5, y_down_offset=2,
    x_up_offset=3, x_down_offset=2,
    x_axis_end_limit_offset=0.1, y_axis_end_limit_offset=1, 
    grid_opacity=0.3, 
    x_axis_pos_offset=3, 
    y_axis_pos_offset=0.1,
    **Line_config 
    )



X = [0, 1, 2, 3]
X_labels = ['[A]','[B]', '[C]', '[D]']
Lines = [[X, torch.rand(4) * 100] for e in range(3)]


################## Normal line plot 
PLOT_FN.plot(plt_type="line", name="Pictures/Lines/test_lines",
    Lines=Lines, h_lines=[40, 60], hline_color='black', h_line_width=3,
    X_range=X, X_labels=X_labels, 
)
################## Shade y-axis regioin
PLOT_FN.plot(plt_type="line", name="Pictures/Lines/test_lines_h_shade",
    Lines=Lines, 
    X_range=X, X_labels=X_labels, 
    h_line_shade=[[40, 60]], h_line_shade_color='black', h_line_shade_color_alpha=0.15, h_line_width=3,
)
################## Shade x-axis regioin
PLOT_FN.plot(plt_type="line", name="Pictures/Lines/test_lines_v_shade",
    Lines=Lines, 
    X_range=X, X_labels=X_labels, 
    v_line_shade=[[1, 2.2]], v_line_shade_color='black', v_line_shade_color_alpha=0.15, v_line_width=3,
)


################## Shade line plot 
Shades_MAX = [(e[0], e[1] + torch.randint(20, (4,))  )  for e in Lines]
Shades_MIN = [(e[0], e[1] - torch.randint(20, (4,)) )  for e in Lines]
## Normal line plot + up - down Shades for each line 
PLOT_FN.plot(plt_type="line", name="Pictures/Lines/test_lines_shade",
    Lines=Lines, 
    X_range=X, X_labels=X_labels, 
    shade=True, shade_up=Shades_MAX, shade_down=Shades_MIN, 
)

################## Error Bar line plot 
STD = [(e[0], torch.randint(10, (4,))  )  for e in Lines]
## Normal line plot + up - down standard_deviation 
PLOT_FN.plot(plt_type="line", name="Pictures/Lines/test_lines_error",
    Lines=Lines, 
    X_range=X, X_labels=X_labels, 
    error_bar=True, error_std=STD, error_bar_color=None, error_bar_width=4,
)



##########################################################################################
# SWAP AXISES 
UPDATE = dict(
    x_axis_pos_offset=0.1, 
    y_axis_pos_offset=3,
    Y_label_fontsize=25, 
    X_label_fontsize=20,
    x_axis_end_limit_offset=1, 
    y_axis_end_limit_offset=0.1, 
)
PLOT_FN.update_params(UPDATE)
##########################################################################################


################## Normal line plot 
PLOT_FN.plot(plt_type="line", name="Pictures/Lines/test_lines_axis_swap",
    Lines=Lines, v_lines=[40], vline_color='black', v_line_width=3,
    Y_range=X, Y_labels=X_labels, swap_axis=True 
)

################## Shade line Inverse plot 
PLOT_FN.plot(plt_type="line", name="Pictures/Lines/test_lines_shade_swap",
    Lines=Lines, 
    shade=True, shade_up=Shades_MAX, shade_down=Shades_MIN, 
    Y_range=X, Y_labels=X_labels, swap_axis=True,
)

################## Error Plot Inverse Plot 
PLOT_FN.plot(plt_type="line", name="Pictures/Lines/test_lines_error_swap",
    Lines=Lines, 
    error_bar=True, error_std=STD, error_bar_color=None, error_bar_width=4,
    Y_range=X, Y_labels=X_labels, swap_axis=True,
)












# cd ~/plot/
# python test_line.py




