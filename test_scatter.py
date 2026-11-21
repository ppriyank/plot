from ALL_PLOTS import ALL_PLOT
from line import line_plot
from colors_set import *
import torch

Scatter_config = dict(
    scatter_boder_color='black', scatter_alpha=0.8,
)

PLOT_FN = ALL_PLOT(
    figsize=(6, 6), 
    # colors=DISTINCT_3_6, 
    colors=ORANGE_LIGHTBLUE_10, 
    decimal_places=0,
    y_up_offset=20, y_down_offset=20,
    x_up_offset=20, x_down_offset=20,
    Y_label_fontsize=10, X_label_fontsize=10,
    **Scatter_config 
    )


N_POINTS=100

POINTS = torch.randn(N_POINTS, 2) * 100
Labels = torch.randint(0, 9, (N_POINTS,))
SIZES = torch.randint(50, 500, (N_POINTS,))
################## Normal scatter plot 
PLOT_FN.plot(plt_type="scatter", name="Pictures/Scatter/test_scatter",
    Points=POINTS, Labels=Labels, Sizes=SIZES
)




################## Different Shapes 
UPDATE = dict(
    switch_off_yaxis=True,
    y_points=5,
)

SHAPE={0: 'o' , 1:'v', 2:'*', 3:'^', 4:'<', 5:'>', 6:'8', 7:'s', 8:'P'}
PLOT_FN.plot(plt_type="scatter", name="Pictures/Scatter/test_scatter_shape",
    Points=POINTS, Labels=Labels, Sizes=SIZES, Shapes=SHAPE, 
    v_line_shade=[[-50, 50]], v_line_shade_color='black', v_line_shade_color_alpha=0.2, v_line_alpha=0,     
    vline_offset = 50, hline_offset = 50,
)

################## Shade y-axis regioin
PLOT_FN.update_params(UPDATE)
PLOT_FN.plot(plt_type="scatter", name="Pictures/Scatter/test_scatter_shade",
    Points=POINTS, Labels=Labels, Sizes=SIZES,
    h_line_shade=[[-50, 50], [50, 300]], h_line_shade_color=DISTINCT_2_8, h_line_shade_color_alpha=0.3, line_width=1,     
    vline_offset = 50, hline_offset = 50,
)







    
    

# cd ~/plot/
# python test_scatter.py
