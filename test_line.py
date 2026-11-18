from ALL_PLOTS import ALL_PLOT
from line import line_plot
from colors import *

import torch




X = [0, 1, 2, 3]
X_labels = ['[0]','[5]', '[8]', '[11]']
Lines = [[X, torch.rand(4) * 100] for e in range(5)]


Line_config = dict(
    line_width=5, alpha_line=1, 
    use_scatter=True, scatter_size=300, scatter_boder_color='black',
    h_lines=[40, 60], 
)

PLOT_FN = ALL_PLOT(
    figsize=(6, 6), 
    colors=DISTINCT_7, artificial_darkening=0.7,
    decimal_places=1,
    y_up_offset=2, y_down_offset=2,
    x_up_offset=2, x_down_offset=2,
    x_axis_pos_offset=3, y_axis_pos_offset=0.1, 
    **Line_config 
    )


    
## Normal line plot 
PLOT_FN.plot(plt_type="line", name="test_lines",
    X=X, Lines=Lines, 
    X_range=X, X_labels=X_labels, 
)


Shades_MAX = [(e[0], e[1] + torch.randint(20, (4,))  )  for e in Lines]
Shades_MIN = [(e[0], e[1] - torch.randint(20, (4,)) )  for e in Lines]


## Normal line plot + up - down Shades for each line 
PLOT_FN.plot(plt_type="line", name="test_lines2",
    X=X, Lines=Lines, 
    X_range=X, X_labels=X_labels, 
    shade=True, shade_up=Shades_MAX, shade_down=Shades_MIN,
)














# cd ~/plot/
# python test_line.py




