from ALL_PLOTS import ALL_PLOT
from line import line_plot
from colors_set import *
import torch
import pandas as pd 
from math import log 

PLOT_FN = ALL_PLOT(
    figsize=(6, 4), 
    artificial_darkening=1,
    pad_inches=0.1, 
    
    # X_label_fontsize=8,
    # X_label_rotate=45,

    # Y_label_rotate=0,
    # Y_label_fontsize=8,

    # annot=True,
    # annot_decimal_places=2, 
    # annot_font_size=9,

    # switch_off_yaxis=True,
    # switch_off_xaxis=True,

    # colors=DISTINCT_2_7, 
    
    
)




######### WORD CLOUD 
# Nodes, Values (colors), Size

names = ['ImageNet', 'ImageNet-Sketch', 'ImageNet-A', 'ImageNet-V2', 'ImageNet-R', 'Caltech', 'DTD', 'food101', 'SUN397', 'Stanford-Cars', 'FGVC-Aircraft', 'Oxford-Pets', 'Oxford-Flowers102', 'EuroSAT', 'UCF101']

sizes = ['50000', '50000', '7500', '10000', '30000', '6085', '1880', '25250', '19850', '8041', '3333', '3669', '6149', '5000', '1794']
sizes = [ int(e)  for e in sizes]

rng = np.random.default_rng(seed=42)
values = rng.standard_normal(len(sizes)).tolist()

PLOT_FN.plot(plt_type="word_cloud", name="Pictures/Misc/test_word_cloud",
    Nodes=names, Sizes=sizes, Values=values,    
    colors=DISTINCT_2_2, 
    word_cloud_shape = (650, 850),
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

# ######### HEAT MAP
# cmap = None 
# cmap = 'viridis'
# cmap = 'YlGnBu'
# cmap = HEAT_MAP_COLOR

# X = torch.rand(12, 1025)
# X = F.normalize(X, p=2, dim=-1)

# dist = X.unsqueeze(1) - X.unsqueeze(0)
# dist = (dist ** 2).sum(-1)

# df = pd.DataFrame( dist.cpu(), columns=[f"Layer-{e+1}" for e in range(len(dist))])




# ######### RADAR PLOT 
# # 3 radars is top limit for visualization 

# A = torch.rand(10) * 100
# B = torch.rand(10) * 100
# C = torch.rand(10) * 100

# custom_Y_yxis = [10, 20, 30]
# custom_Y_yxis_label = ["10", "20", "30"]

# Radar_label = ['ImageNet', 'ImageNet-Sketch', 'ImageNet-A', 'ImageNet-V2', 'ImageNet-R', 'Caltech', 'DTD', 'food101', 'SUN397', 'Stanford-Cars']
# curve_names = ["Curve A", "Curve B", "Curve C"]

# if radar_plot:
#     radar_spider_plot([A,B,C], curve_points=Radar_label, curve_names=curve_names, name=f"test_radar1", 
#         ALPHAs=[1,1,1], artificial_darkening = 1, lw=2, alpha=0.2, 
#         x_axis_allowed=True, X_label_fontsize=10, X_pad=20, outer_circle=False,
#         y_axis_angle=10, Y_font_color='black', y_points=2, y_font_size=15, y_up_offset=2, y_down_offset=2, 
#         y_axis_allowed=False, Y_range=custom_Y_yxis, Y_range_label=custom_Y_yxis_label)


#     radar_spider_plot([A,B,C], curve_points=Radar_label, curve_names=curve_names, name=f"test_radar2", 
#         ALPHAs=[1,1,1], artificial_darkening = 1, lw=2, alpha=0.2, 
#         x_axis_allowed=True, X_label_fontsize=10, X_pad=20, outer_circle=False,
#         y_axis_angle=10, Y_font_color='black', y_points=2, y_font_size=15, y_up_offset=2, y_down_offset=2, 
#         y_axis_allowed=False)


# ######### Box PLot 
# if box_plot:
#     A = [42.4, 41.4, 39.6, 38.4, 42, 39.8, 38, 38]
#     B = [44.4, 43.1, 40.1, 39.0, 44, 42.7, 38, 37]
#     C = [40.4, 36.1, 50.1, 60.0, 44, 50.7, 40, 30]

#     Y = [A,B,C]
#     X_labels = ["Dataset_A", "Dataset_B", "Dataset_C"]

#     vals = []
#     for i,ele in enumerate(Y):
#         for val in ele:
#             vals.append([X_labels[i], val])

#     df = pd.DataFrame(vals, columns=["X", "Y"])
#     box_plt(df, name="test_box", figsize=(7, 10),
#         y_up_offset=5, y_down_offset=5, y_points=4, width=0.6)


#     box_plt(df, name="test_box_mean", figsize=(7, 10),
#         y_up_offset=5, y_down_offset=5, y_points=4, width=0.6, use_mean=True, x_padding_factor=0.5, )




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