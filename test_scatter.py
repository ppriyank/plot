from ALL_PLOTS import ALL_PLOT
from line import line_plot
from colors_set import *
import torch

Scatter_config = dict(
    scatter_boder_color='black', scatter_alpha=0.9,
)

PLOT_FN = ALL_PLOT(
    figsize=(6, 6), 
    colors=DISTINCT_3_6, artificial_darkening=0.8,
    decimal_places=0,
    y_up_offset=20, y_down_offset=20,
    x_up_offset=20, x_down_offset=20,
    x_axis_end_limit_offset=0.1, y_axis_end_limit_offset=0.1, 
    grid_opacity=0.3, 
    Y_label_fontsize=10, X_label_fontsize=10,
    **Scatter_config 
    )


N_POINTS=100


POINTS = torch.randn(N_POINTS, 2) * 100
Labels = torch.randint(0, 3, (N_POINTS,))
SIZES = torch.randint(50, 500, (N_POINTS,))

################## Normal scatter plot 
PLOT_FN.plot(plt_type="scatter", name="Pictures/Scatter/test_scatter",
    Points=POINTS, Labels=Labels, Sizes=SIZES
)

################## Shade y-axis regioin


##########################################################################################
# SWAP AXISES 
UPDATE = dict(
    y_ticks_allowed=True, 
    switch_off_yaxis=True,
    y_points=5,
)
PLOT_FN.update_params(UPDATE)


PLOT_FN.plot(plt_type="scatter", name="Pictures/Scatter/test_scatter_shade",
    Points=POINTS, Labels=Labels, Sizes=SIZES,
    h_line_shade=[[-50, 50], [50, 300]], h_line_shade_color=DISTINCT_2_8, h_line_shade_color_alpha=0.3, line_width=1,     
    vline_offset = 50, hline_offset = 50,
)






    
    

# cd ~/plot/
# python test_scatter.py
