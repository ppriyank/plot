from ALL_PLOTS import ALL_PLOT
from line import line_plot
from colors_set import *
import torch
import pandas as pd 
from math import log 




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
torch.cuda.manual_seed_all(100)
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


PLOT_FN.plot(plt_type="radar", name="Pictures/Misc/test_radar",
    Curves=[A,B,C],  Alphas = [0.5,0.5,.5], 
    Curves_names = curve_names, 
    Y_range=Y_range, Y_labels= Y_labels, 
    X_labels= Radar_label, 
    x_axis_label_dist_y = Radar_label_dist,
)

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

PLOT_FN.plot(plt_type="radar", name="Pictures/Misc/test_radar_derive_ylabels",
    Curves=[A,B,C],  Alphas = 0.4, 
    X_labels= Radar_label, Curves_names = curve_names, x_axis_label_dist_y = Radar_label_dist, 
    colors=DISTINCT_3_3,
    y_points=3, Y_label_opacity=0.4,
    grid_shape='y', grid_opacity=0.5, 
    decimal_places=1,
    curve_line_opacity=0.1,
)




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

# heat_map = False 
# heat_map2=False 
# word_cloud = False 
# radar_plot = False 
# box_plot = False 
# bubble_plot = False  
# sankey_plot=True 







# ######### BUBBLE PLOT 
# if bubble_plot:
#     from math import log 
#     ### Nodes
#     class_name = ['lobster', 'jellyfish', 'hand', 'pistol', 'cottontail', 'raccoon', 'motorcycle']

#     ### Sizes (This will be used to bin)
#     class_sizes = [60, 155, 1515, 346, 46, 64, 330]

#     ### COLOR decider (between 0-1)
#     class_scores = [0.700000, 0.285235, 0.182759, 0.098592, 0.005739, 0.063559, 0.052960]

#     df = pd.DataFrame({ 'Nodes': class_name, 'Sizes': class_sizes, 'Score': class_scores})

#     # (This will be used to bin or clustered
#     df['Sizes'] = df['Sizes'].apply(log)
#     print(df)


#     network_bubble(df, column_to_be_binned='Sizes', node_column='Nodes', column_to_be_colored='Score', 
#         plt_name="bubble_plot", figsize=(20, 20), 
#         N_CLUSTERS = 3, ## no of clusters
#         node_size_formula = lambda x: (x ** 1.5) / 2, ## Node size calculator
#         node_edge_width=0.2, node_labels=True, 
#         node_labels_font_size=8, ### Node label prop to node size (5 is base size)
#         N_BINS_COLORS = 100, ### Binning of colors [Score ==0 -> white , Score == 1 --> black]
#         node_edge_color="black",
#         edge_width=0.5, edge_alpha=0.5, 
#     )


# if sankey_plot:    
#     url = "https://raw.githubusercontent.com/anazalea/pySankey/master/pysankey/fruits.txt"
#     df = pd.read_csv(url, sep=" ", names=["true", "predicted"])
    
#     COLORS_LEFT = [lighten_color( DISTINCT_2_8[1], amount= 0.5 + 0.3 * i ) for i,k in enumerate(df.true.unique())]
#     random.shuffle(COLORS_LEFT)
#     COLORS_RIGHT = [lighten_color( DISTINCT_2_8[0], amount= 0.5 + 0.2 * i ) for i,k in enumerate(df.predicted.unique())]
#     random.shuffle(COLORS_RIGHT)
    
#     left_axis_colors = {k.split(" ")[-1].replace("(", "").replace(")", ""): color for k, color in zip(df.true.unique(), COLORS_LEFT)}
#     right_axis_colors = {k.split(" ")[-1].replace("(", "").replace(")", ""): color for k,color in zip(df.predicted.unique(), COLORS_RIGHT)}


#     Sankey_web(df, left_axis='true', right_axis='predicted', gradient=True, 
#     left_axis_colors=left_axis_colors, right_axis_colors=right_axis_colors, edges=True, edge_width=1, edgecolor='white', edge_alpha=0.6, 
#     flow_width=1, 
#     figsize=(5, 5),
#     name=os.path.join('Pictures', "test_sankey"), 
#     )
    
    

# # cd ~/plot/
# # python test_misc.py