from ALL_PLOTS import ALL_PLOT
from line import line_plot
from colors_set import *
import torch


Hist_config = dict(
    artificial_darkening=0.7,
    automatic_adjust_width = False, 
)

# COLORS  = PAIR_CONTRAST[2:]
COLORS = DISTINCT_3_1
PLOT_FN = ALL_PLOT(
    figsize=(6, 4), 
    colors=COLORS, 
    y_up_offset=2, 
    y_axis_pos_offset=2, x_axis_end_limit_offset=3,
    Y_label_fontsize=10, X_label_fontsize=10,
    switch_off_yaxis=True,
    y_points=10,
    grid_shape='y',
    **Hist_config 
    )

Hists = [
    {'x': [0, 1, 2], 'y': [[42.4, 10, 39.6]] },
    {'x': [4, 5, 6, 7, 8], 'y': [[44.4, 43.1, 30, 39.0, 43.1]] },
    ]
X_labels = ["Hist A", "Hist B"]
X = [ sum(e['x'])/ len(e['x'])  for  e  in Hists]



################## Normal Hist plot (Predefined X Posiiton)
PLOT_FN.plot(plt_type="bar", name="Pictures/Hist/test_hist",
    Hists=Hists, 
    bar_labels=True, bar_labels_y_offset=1, bar_labels_font_size=10, bar_labels_color='black', bar_label_decimal_places=1,
    colors=COLORS[::2], 
    legend=True, 
    x_axis_end_limit_offset=4,
    X_range=X, X_labels=X_labels,
    automatic_adjust_width = True,
)



################## Stacked Hist plot (Predefined X Posiiton)
Hists = [
    {'x': [0, 1, 2], 'y': [[42.4, 41.4, 39.6], [2.4, 10.4, 3.4] ]},
    {'x': [4, 5, 6, 7, 8], 'y': [[44.4, 43.1, 40.1, 39.0, 43.1], [2.4, 5.1, 4.1, 10.0, 3.1]] },
    ]

PLOT_FN.plot(plt_type="bar", name="Pictures/Hist/test_hist_stacked",
    Hists=Hists, 
    colors=COLORS[1:], artificial_darkening=0.6, 
    stack_brightness_factor=0.4, stack_dist=0.3, 
    X_range=X, X_labels=X_labels, 
    h_lines=[25], hline_color=GREY_DARKER, h_line_width=2, h_line_alpha=1, line_z_oder=50,
)

################## Hist Side by Side (Assign X on the fly, using barWidth)
Hists = [
    {'y': [[42.4, 41.4, 39.6, 80]]}, ## histogram 1
    {'y': [[30, 35, 55, 20], [10, 4, 2, 10]] },  ## histogram 2
    {'y': [[50, 65, 40]]} ## histogram 3
]

PLOT_FN.plot(plt_type="bar", name="Pictures/Hist/test_hist_side",
    Hists=Hists, 
    colors=COLORS, 
    x_axis_end_limit_offset=1, y_axis_pos_offset=0.5,
    automatic_adjust_width=True, bar_border_width=0.06,
    x_ticks_allowed=False,
    bar_labels=True, bar_labels_font_size=10, bar_labels_color='black', bar_label_decimal_places=1, bar_labels_y_offset=1,
)



################## Hist Side by Side + Pattern 
Hists = [
    {'y': [[42.4, 41.4]]}, ## histogram 1
    {'y': [[30, 35], [50, 20]] },  ## histogram 2
    {'y': [[50, 65]]}, ## histogram 3
    {'y': [[20, 55], [50, 30]]}, ## histogram 4
    {'y': [[10, 60]]}, ## histogram 5
    {'y': [[40, 10]]}, ## histogram 6
    {'y': [[50, 90]]}, ## histogram 7
    {'y': [[70, 30]]}, ## histogram 8
]

PATTERN = ['/', '\\', '-', 'x', 'o', 'O', '.', '*']
PLOT_FN.plot(plt_type="bar", name="Pictures/Hist/test_hist_pattern",
    Hists=Hists, bar_border_color='black',
    stack_dist=1, bar_group_sep=2,
    colors=GRADIENT_9,  Pattern=PATTERN, 
    automatic_adjust_width=True, bar_border_width=0.06, 
    x_ticks_allowed=False,  x_axis_end_limit_offset=1, y_axis_pos_offset=1, 
    decimal_places=0, 
)


################## Given Data Bin it in form of histogram 
torch.manual_seed(100)
torch.cuda.manual_seed_all(100)
N_POINTS = 10000 
POINTS = torch.randn(N_POINTS) 
N_BINS = 50


PLOT_FN.plot(plt_type="bar", name="Pictures/Hist/test_hist_binning",
    Hists=POINTS, Hist_mode=True,  Hist_N_Bins=N_BINS,
    colors=BLUE, 
    automatic_adjust_width = True,
    y_points=10, x_points=10, decimal_places=0, y_axis_pos_offset=0.1, x_axis_end_limit_offset=0.01, y_up_offset=100,
    bar_border_width=0.01,
    Hist_gradient=True 
)



################## Swap axis of histogram 
Hists = [
    {'y': [[42.4, 41.4]]}, ## histogram 1
    {'y': [[30, 35], [50, 20]] },  ## histogram 2
    {'y': [[50, 65]]}, ## histogram 3
    {'y': [[20, 55], [50, 30]]}, ## histogram 4
    {'y': [[50, 90]]}, ## histogram 7
    {'y': [[70, 30]]}, ## histogram 8
]

PLOT_FN.update(dict(
        figsize=(4, 5.5), 
        X_label_fontsize=10,
        grid_shape='x', 
        switch_off_yaxis=False, switch_off_xaxis=True, 
        x_points=5, 
        
        y_up_offset=0,
        y_axis_pos_offset=0,
        x_axis_end_limit_offset=0,
        x_axis_pos_offset = 1, 
        y_axis_end_limit_offset=1,
        colors=GRADIENT_9, 
        y_ticks_allowed=False, 
    )
)

PLOT_FN.plot(plt_type="bar", name="Pictures/Hist/test_hist_swap",
    Hists=Hists, bar_border_color='black', swap_axis=True, 
    stack_dist=1, bar_group_sep=1,
    automatic_adjust_width=True, bar_border_width=0.06, 
    bar_labels=True, bar_labels_font_size=10, bar_labels_color='black', bar_label_decimal_places=1, bar_labels_x_offset=1,
)


################## Swap axis of histogram + V_shade 
V_SHADE_PARAMS = dict(
    v_line_shade=[[45,72]],
    v_line_shade_color=GREEN,
    v_line_shade_color_alpha=0.3, 
    v_line_alpha=0,
)
PLOT_FN.plot(plt_type="bar", name="Pictures/Hist/test_hist_hshade",
    Hists=Hists, bar_border_color='black', swap_axis=True, bar_opacity=1, 
    stack_dist=1, bar_group_sep=2,    
    automatic_adjust_width=True, bar_border_width=0.06,     
    **V_SHADE_PARAMS
)


# cd ~/plot/
# python test_hist.py