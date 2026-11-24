from ALL_PLOTS import ALL_PLOT
from line import line_plot
from colors_set import *
import torch
import pandas as pd 
from math import log 
import random 



############################################################################################################
#################################### WORD CLOUD 
# Nodes, Values (colors), Size
PLOT_FN = ALL_PLOT(
    figsize=(6, 4), 
    artificial_darkening=1,
    pad_inches=0.1,     
)

names = ['ImageNet', 'ImageNet-Sketch', 'ImageNet-A', 'ImageNet-V2', 'ImageNet-R', 'Caltech', 'DTD', 'food101', 'SUN397', 'Stanford-Cars', 'FGVC-Aircraft', 'Oxford-Pets', 'Oxford-Flowers102', 'EuroSAT', 'UCF101']

sizes = ['50000', '50000', '7500', '10000', '30000', '6085', '1880', '25250', '19850', '8041', '3333', '3669', '6149', '5000', '1794']
sizes = [ int(e)  for e in sizes]

rng = np.random.default_rng(seed=42)
values = rng.standard_normal(len(sizes)).tolist()

# PLOT_FN.plot(plt_type="word_cloud", name="Pictures/Misc/test_word_cloud",
#     Nodes=names, Sizes=sizes, 
#     Values=values, ## override default colors based on Values     
#     colors=DISTINCT_2_2, 
#     word_cloud_shape = (650, 850),
# )


############################################################################################################
#################################### RADAR PLOT 
# 3 radars is top limit for visualization 

## Needs to setup figure in 'polar'
PLOT_FN = ALL_PLOT(
    subplot_kw={'projection': 'polar'}, 
    polaroid_coordinates=True, 

    figsize=(6, 4), 
    colors=DISTINCT_3_2, 
    artificial_darkening=0.8,
    
    grid_shape='xy', 
    grid_opacity=0.3, 
    switch_off_xaxis=True,
    switch_off_yaxis=True,
    X_label_fontsize=10,
    Y_label_fontsize=8,

    x_axis_label_dist_y = 0.2, # radial distance 
    x_axis_label_dist_x = 0, # angular distance 

    y_axis_end_limit_offset=10, # extra ticks beyond plot y axis   
    y_axis_angle=10, 
)

torch.manual_seed(100)
A = torch.rand(10) * 100 # "Curve A"
B = torch.rand(10) * 100 # "Curve B"
C = torch.rand(10) * 100 # "Curve C"

curve_names = ["Curve A", "Curve B", "Curve C"]

v_max = max(max(A), max(B), max(C))
Y_range = [50,   v_max]
Y_labels = ["50", f"{v_max:.0f}"]

Radar_label = ['ImageNet', 'ImageNet-Sketch', 'ImageNet-A', 'ImageNet-V2', 'ImageNet-R', 'Caltech', 'DTD', 'food101', 'SUN397', 'Stanford-Cars']
Radar_label_dist = {
    'ImageNet': 0.12, 
    'ImageNet-Sketch': 0.12, 
    'ImageNet-A': -0.1, 
    'ImageNet-V2': -0.1, 
    'ImageNet-R': 0, 
    'Caltech': 0.04, 
    'DTD': -0.08, 
    'food101': -0.1, 
    'SUN397': -0.1, 
    'Stanford-Cars': 0.1, 
}

# PLOT_FN.plot(plt_type="radar", name="Pictures/Misc/test_radar",
#     Curves=[A,B,C],  Alphas = [0.5,0.5,.5], 
#     Curves_names = curve_names, 
#     Y_range=Y_range, Y_labels= Y_labels, 
#     X_labels= Radar_label, 
#     x_axis_label_dist_y = Radar_label_dist,
# )

torch.manual_seed(random.randint(1, 2e3))
A = torch.rand(10) * 100 # "Curve A"
B = torch.rand(10) * 100 # "Curve B"

Radar_label_dist = {
    'ImageNet': 0, 
    'ImageNet-Sketch': 0.12, 
    'ImageNet-A': -0.2, 
    'ImageNet-V2': -0.2, 
    'ImageNet-R': 0, 
    'Caltech': 0.0, 
    'DTD': -0.08, 
    'food101': -0.2, 
    'SUN397': -0.2, 
    'Stanford-Cars': 0, 
}
# PLOT_FN.plot(plt_type="radar", name="Pictures/Misc/test_radar_derive_ylabels",
#     Curves=[A,B],  Alphas = 0.6, 
#     curve_line_opacity=1,
#     X_labels= Radar_label, Curves_names = curve_names, x_axis_label_dist_y = Radar_label_dist, 
#     colors=DISTINCT_2_5,
#     y_points=3, Y_label_opacity = 0.4,
#     grid_shape='y', grid_opacity = 0.5, 
#     decimal_places=1,
#     figsize=(5, 8), 
# )



############################################################################################################
#################################### Network - Web / BUBBLE PLOT 
PLOT_FN = ALL_PLOT(
    figsize=(7, 7),  
    colors=DISTINCT_2_1, 
    artificial_darkening=0.8,
    node_size_formula = lambda x: (x ** 1.5) / 2, ## Node size calculator
    node_edge_width=0.2,
    node_labels=True, 
    node_labels_font_size=8,
    node_edge_color="black",
    connect_edge_width=0.5, 
    connect_edge_alpha=0.5, 
    use_bunding=True,
    edges_with_cluster=True,     
    
)

### Nodes
N_NODES = 30 
Nodes = torch.arange(start=0, end=N_NODES, step=1, )

### Sizes Size of Node 
Sizes = torch.rand(N_NODES) * 1000 # nodes 

### COLOR decider (between 0-1)
Scores = torch.rand(N_NODES)  # nodes 

### Binning used to determin grouping 
Values = torch.rand(N_NODES)  


# PLOT_FN.plot(plt_type="network_bubble", name="Pictures/Misc/test_net_bubble",
#     Nodes=Nodes, Sizes=Sizes, Scores=Scores,     
#     Values=Values, 
#     Labels = None, ## invokes binning of values 
#     n_cluster = 7,
#     node_size_range=(3, 6),
# )


############################################################################################################
#################################### Sankey PLOT 
PLOT_FN = ALL_PLOT(
    figsize=(7, 7),  
    # colors=DISTINCT_2_1, 
    # artificial_darkening=0.8,
    # node_size_formula = lambda x: (x ** 1.5) / 2, ## Node size calculator
    # node_edge_width=0.2,
    # node_labels=True, 
    # node_labels_font_size=8,
    # node_edge_color="black",
    # connect_edge_width=0.5, 
    # connect_edge_alpha=0.5, 
    # use_bunding=True,
    # edges_with_cluster=True,     
)

url = "https://raw.githubusercontent.com/anazalea/pySankey/master/pysankey/fruits.txt"
df = pd.read_csv(url, sep=" ", names=["true", "predicted"])

Color_Left = [lighten_color( DISTINCT_2_8[1], amount= 0.5 + 0.3 * i ) for i,k in enumerate(df.true.unique())]
random.shuffle(Color_Left)
Color_Right = [lighten_color( DISTINCT_2_8[0], amount= 0.5 + 0.2 * i ) for i,k in enumerate(df.predicted.unique())]
random.shuffle(Color_Right)

left_axis_colors = {k.split(" ")[-1].replace("(", "").replace(")", ""): color for k, color in zip(df.true.unique(), Color_Left)}
right_axis_colors = {k.split(" ")[-1].replace("(", "").replace(")", ""): color for k,color in zip(df.predicted.unique(), Color_Right)}

import pdb
pdb.set_trace()
PLOT_FN.plot(plt_type="sankey", name="Pictures/Misc/test_sankey",
    
)


# Sankey_web(df, left_axis='true', right_axis='predicted', gradient=True, 
# left_axis_colors=left_axis_colors, right_axis_colors=right_axis_colors, edges=True, edge_width=1, edgecolor='white', edge_alpha=0.6, 
# flow_width=1, 
# figsize=(5, 5),
# name=os.path.join('Pictures', "test_sankey"), 
# )
    
    

# cd ~/plot/
# python test_misc.py




















# from misc_plot import heatmap_plt, word_cloud_plt, radar_spider_plot, box_plt, network_bubble, Sankey_web
# from colors import *
# import pandas as pd 
# import torch 
# import torch.nn.functional as F
# import torch.nn as nn
# from math import log
# import numpy as np 
# import os 
# import random 








# cd ~/plot/
# python test_misc.py