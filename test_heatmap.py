from ALL_PLOTS import ALL_PLOT
from line import line_plot
from colors_set import *
import torch
import pandas as pd 


PLOT_FN = ALL_PLOT(
    figsize=(6, 4), 
    
    X_label_fontsize=8,
    X_label_rotate=45,

    Y_label_rotate=0,
    Y_label_fontsize=8,

    annot=True,
    annot_decimal_places=2, 
    annot_font_size=9,

    switch_off_yaxis=True,
    switch_off_xaxis=True,

    colors=DISTINCT_2_7, 
    artificial_darkening=1,

    grid_opacity=1, 
    grid_color='white', 
    grid_widths=0.2,
    grid_shape='xy',
    pad_inches=0, 
    )




df = [
        ['OG', 0.28055,0.31158,0.29258,0.26106,0.24943,0.28391,0.30787,0.29770,0.24134,0.24697,0.18378,0.18099],
        ['Pixel Drop' , 0.32030,0.31650,0.30429,0.26057,0.24561,0.28561,0.30278,0.29277,0.23024,0.24792,0.18063,0.18516],
        ['ISO',  0.28526,0.33376,0.30581,0.26062,0.23708,0.28597,0.30110,0.29686,0.23022,0.24723,0.18088,0.18308],
        ['Rain', 0.28413,0.31994,0.29493,0.26391,0.24224,0.28614,0.30456,0.29054,0.22817,0.26122,0.18915,0.17661],
        ['Snow', 0.28874,0.31019,0.28975,0.25547,0.24122,0.27872,0.30408,0.29134,0.22660,0.24992,0.20279,0.18498],
        ['Atmospheric',  0.28827,0.31609,0.29267,0.26541,0.25755,0.30398,0.30282,0.29951,0.24740,0.24463,0.18213,0.20890]
    ]

df = pd.DataFrame(df, columns=['Noise', 'Pixel Drop','ISO','Salt','Low Res','Focus Blur','JPG','Chromatic','Motion Blur','Fog','Rain','Snow','Atmospheric'])
df.set_index('Noise', inplace=True)


################## Normal line plot 
PLOT_FN.plot(plt_type="heatmap", name="Pictures/Heatmap/test_heatmap",
    df=df, 
    make_square=False,
    Y_label_rotate=0,
    annot_black_threshold=0.27, 
)

################## Change x-axis_label y position
# Higher y-axis is higher position on y axis
x_axis_label_dist_y = {
    'Pixel Drop': 0.09,  'ISO' : 0.05, 'Salt' :0,
    'Low Res': 0.09, 'Focus Blur': 0.09,
    'JPG': 0, 'Chromatic': 0.09, 
    'Motion Blur': 0.09, 'Fog': 0.09,
    'Rain': 0.05, 'Snow': 0.05,
    'Atmospheric': 0.09,     
}

PLOT_FN.plot(plt_type="heatmap", name="Pictures/Heatmap/test_heatmap_x_axis_pos",
    df=df, colors=DISTINCT_2_1, 
    make_square=True,
    x_axis_label_dist_y=x_axis_label_dist_y, 
    artificial_darkening=0.8,
    annot_black_threshold=0.23, 
)


################## Plot with Color Bar 
# Higher y-axis is higher position on y axis
df =df.T
df = df.iloc[:-3]
PLOT_FN.plot(plt_type="heatmap", name="Pictures/Heatmap/test_heatmap_color_bar",
    df=df, colors=GRADIENT_GREEN_6[::-1], 
    n_bins=6, 
    grid_widths=0.3,
    annot_font_size=5, artificial_darkening=0.8,
    cbar=True,  cbar_labels=True,
    figsize=(4, 4), 
)



     
# cd ~/plot/
# python test_heatmap.py


