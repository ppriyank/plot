from misc_plot import heatmap_plt, word_cloud_plt, radar_spider_plot
from colors import HEAT_MAP_COLOR
import pandas as pd 
import torch 
import torch.nn.functional as F
import torch.nn as nn
from math import log


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
heatmap_plt(df, name="test_heatmap", X_label_fontsize=25, figsize=(10, 10), xticklabels= 5, vmin=0, vmax=2,  cmap=cmap,
    linewidths=.5 , annot=False, fmt=".2f")
    

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



# cd ~/plot/
# python test_misc.py