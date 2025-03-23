from misc_plot import heatmap_plt, word_cloud_plt, radar_spider_plot, box_plt
from colors import HEAT_MAP_COLOR, generate_color_gradient, generate_color_gradients2
import pandas as pd 
import torch 
import torch.nn.functional as F
import torch.nn as nn
from math import log
import numpy as np 

heat_map = False 
heat_map2=True 
word_cloud = False 
radar_plot = False 
box_plot = False 

######### HEAT MAP
cmap = None 
cmap = 'viridis'
cmap = 'YlGnBu'
cmap = HEAT_MAP_COLOR

X = torch.rand(12, 1025)
X = F.normalize(X, p=2, dim=-1)

dist = X.unsqueeze(1) - X.unsqueeze(0)
dist = (dist ** 2).sum(-1)

df = pd.DataFrame( dist.cpu(), columns=[f"Layer-{e+1}" for e in range(len(dist))])
if heat_map:
    heatmap_plt(df, name="test_heatmap", X_label_fontsize=25, figsize=(10, 10), xticklabels= 5, vmin=0, vmax=2,  cmap=cmap,
        linewidths=.5 , annot=False, fmt=".2f")

    cmap = generate_color_gradient(1000)
    heatmap_plt(df, name="test_heatmap2", X_label_fontsize=25, figsize=(10, 10), xticklabels= 5, vmin=0, vmax=2,  cmap=cmap,
        linewidths=.5 , annot=False, fmt=".2f")


if heat_map2:
    df = [
        ['OG',0.46637,0.28055,0.31158,0.29258,0.26106,0.24943,0.28391,0.30787,0.29770,0.24134,0.24697,0.18378,0.18099],
        ['Pixel Drop' ,0.46270,0.32030,0.31650,0.30429,0.26057,0.24561,0.28561,0.30278,0.29277,0.23024,0.24792,0.18063,0.18516],
        ['ISO',0.46285,0.28526,0.33376,0.30581,0.26062,0.23708,0.28597,0.30110,0.29686,0.23022,0.24723,0.18088,0.18308],
        ['Rain',0.46222,0.28413,0.31994,0.29493,0.26391,0.24224,0.28614,0.30456,0.29054,0.22817,0.26122,0.18915,0.17661],
        ['Snow',0.46179,0.28874,0.31019,0.28975,0.25547,0.24122,0.27872,0.30408,0.29134,0.22660,0.24992,0.20279,0.18498],
        ['Atmospheric',0.46359,0.28827,0.31609,0.29267,0.26541,0.25755,0.30398,0.30282,0.29951,0.24740,0.24463,0.18213,0.20890]
    ]
    
    df = pd.DataFrame(df, columns=['LR-TK0','OG','Pixel Drop','ISO','Salt','Low Res','Focus Blur','JPG','Chromatic','Motion Blur','Fog','Rain','Snow','Atmospheric'])
    df.set_index('LR-TK0', inplace=True)
    df = df.sub(df.iloc[0])
    df = df * 100 
    print(df)

    mini= df.min().min()
    maxi= df.max().max()
    n_bins=  10 

    ## Min val ==> "#FF4500", 0 special case ==> 'black' , maxi ==> "#4169E1"
    zero_one_range = lambda x: (x - mini) / (maxi - mini)
    colors = [(zero_one_range(mini), "#FF4500"), (zero_one_range(0), 'black'), (zero_one_range(maxi), "#4169E1")]
    cmap = generate_color_gradients2(n_bins, colors)

    offset  =(maxi - mini) / n_bins
    color_bar_labels_range = [mini, 0, maxi]
    color_bar_labels=[f"{e:.1f}" for e in color_bar_labels_range]

    yticklabels=True
    x_font_size=13
    y_font_size = 15
    heatmap_plt(df, name="test_heatmap3", 
        X_label_fontsize=x_font_size, Y_label_fontsize=y_font_size, x_label_rotate=45,
        figsize=(10, 10), xticklabels= 1, vmin=mini, vmax=maxi, cmap=cmap, linewidths=.1 , annot=True, fmt=".1f", yticklabels=yticklabels, 
        color_bar_labels=color_bar_labels, color_bar_labels_range=color_bar_labels_range, color_label_fontsize=15, ann_size=14)




######### WORD CLOUD 

names = ['ImageNet', 'ImageNet-Sketch', 'ImageNet-A', 'ImageNet-V2', 'ImageNet-R', 'Caltech', 'DTD', 'food101', 'SUN397', 'Stanford-Cars', 'FGVC-Aircraft', 'Oxford-Pets', 'Oxford-Flowers102', 'EuroSAT', 'UCF101']
sizes = ['50000', '50000', '7500', '10000', '30000', '6085', '1880', '25250', '19850', '8041', '3333', '3669', '6149', '5000', '1794']
sizes = [int(e) for e in sizes]
sizes = [log(e+1000)  for e in sizes]

n_classes = ['1000', '1000', '200', '1000', '200', '102', '47', '102', '397', '196', '102', '37', '102', '10', '101']
n_classes = [int(e) for e in n_classes]

COLOR_INDEX = n_classes
SIZE = sizes
COLORS = ['#207eab', '#000080', '#000000']
COLORS = ['#FFAC1C', '#C04000', '#000000']
if word_cloud:
    word_cloud_plt(names, COLOR_INDEX=COLOR_INDEX, SIZE=SIZE, COLORS=COLORS, figsize=(2000, 3500), name="test_word_cloud")


######### RADAR PLOT 
# 3 radars is top limit for visualization 

A = torch.rand(10) * 100
B = torch.rand(10) * 100
C = torch.rand(10) * 100

custom_Y_yxis = [10, 20, 30]
custom_Y_yxis_label = ["10", "20", "30"]

Radar_label = ['ImageNet', 'ImageNet-Sketch', 'ImageNet-A', 'ImageNet-V2', 'ImageNet-R', 'Caltech', 'DTD', 'food101', 'SUN397', 'Stanford-Cars']
curve_names = ["Curve A", "Curve B", "Curve C"]

if radar_plot:
    radar_spider_plot([A,B,C], curve_points=Radar_label, curve_names=curve_names, name=f"test_radar1", 
        ALPHAs=[1,1,1], artificial_darkening = 1, lw=2, alpha=0.2, 
        x_axis_allowed=True, X_label_fontsize=10, X_pad=20, outer_circle=False,
        y_axis_angle=10, Y_font_color='black', y_points=2, y_font_size=15, y_up_offset=2, y_down_offset=2, 
        y_axis_allowed=False, Y_range=custom_Y_yxis, Y_range_label=custom_Y_yxis_label)


    radar_spider_plot([A,B,C], curve_points=Radar_label, curve_names=curve_names, name=f"test_radar2", 
        ALPHAs=[1,1,1], artificial_darkening = 1, lw=2, alpha=0.2, 
        x_axis_allowed=True, X_label_fontsize=10, X_pad=20, outer_circle=False,
        y_axis_angle=10, Y_font_color='black', y_points=2, y_font_size=15, y_up_offset=2, y_down_offset=2, 
        y_axis_allowed=False)


######### Box PLot 

if box_plot:
    A = [42.4, 41.4, 39.6, 38.4, 42, 39.8, 38, 38]
    B = [44.4, 43.1, 40.1, 39.0, 44, 42.7, 38, 37]
    C = [40.4, 36.1, 50.1, 60.0, 44, 50.7, 40, 30]

    Y = [A,B,C]
    X_labels = ["Dataset_A", "Dataset_B", "Dataset_C"]

    vals = []
    for i,ele in enumerate(Y):
        for val in ele:
            vals.append([X_labels[i], val])

    df = pd.DataFrame(vals, columns=["X", "Y"])
    box_plt(df, name="test_box", figsize=(7, 10),
        y_up_offset=5, y_down_offset=5, y_points=4, width=0.6)


    box_plt(df, name="test_box_mean", figsize=(7, 10),
        y_up_offset=5, y_down_offset=5, y_points=4, width=0.6, use_mean=True, x_padding_factor=0.5, )



# cd ~/plot/
# python test_misc.py