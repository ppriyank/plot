
from matplotlib.patheffects import withStroke
import matplotlib.colors as mc
import colorsys
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np 

from plot_utils import generate_color_gradient, generate_color_gradients2, colors_heat_map, lighten_color


BROWN = "#AD8C97"
BROWN_DARKER = "#7d3a46"
GREEN = "#2FC1D3"
LGREEN="#72ba00"
BLUE = "#0a84e3"
GREY = "#C7C9CB"
GREY_DARKER = "#5C5B5D"
RED = "#E3120B"
ORANGE = "#f8a600"
PINK="#f8a6e7"
YELLOW="#fdeb01"
# RED = "#D2042D"
	
path_effects = [withStroke(linewidth=10, foreground="white")]
font_path_effects = [withStroke(linewidth=4, foreground="white")]



ALL_COLORS = [c for c,hex in mc.CSS4_COLORS.items()]
ALL_XKCD_COLORS = [c for c,hex in mc.XKCD_COLORS.items()]
COLORS = [BLUE, RED]

COLOR_SET_20=["#c9fd60" ,"#682385" ,"#e4cfd3" ,"#08ca46" ,"#6dae9c" ,"#89aa81" ,"#ac39b4" ,"#db6900" ,"#944116" ,"#c276b6" ,"#3d3f59" ,"#52fd7a" ,"#747a39" ,"#b861d7" ,"#83dd1f" ,"#c08202" ,"#93a0b6" ,"#b44f2d" ,"#34ba31" ,"#c6c0b3"]
COLOR_SET_15=["#1a1816", "#c5e1f7", "#359032", "#acd1dd", "#f7ff89", "#82bb4d", "#b03010", "#b1b352", "#00c595", "#6455af", "#ce6694", "#ef0422", "#9b1167", "#2ff67a", "#36c28c"]
## Yellow - Blue 
COLOR_SET_15=["#FBE183FF", "#F4C40FFF", "#FE9B00FF", "#D8443CFF", "#9B3441FF", "#DE597CFF", "#E87B89FF", "#E6A2A6FF", "#AA7AA1FF", "#9F5691FF", "#633372FF", "#1F6E9CFF", "#2B9B81FF", "#92C051FF"]


# Create the colormap
HEAT_MAP_COLOR = LinearSegmentedColormap.from_list("custom_cmap", [ORANGE, RED, "black", BLUE, "white"][::-1])
BAR_LABEL = "#009933"

PAIRED_COLORS = sns.color_palette("Paired", as_cmap=True)
ALONE_COLORS = sns.color_palette("pastel", as_cmap=True)








#### LIGHT BLUE TO DARK 
GRADIENT_BLUE_6 = ["#CAF0F8", "#48CAE4", "#00B4D8", "#0096C7", "#0077B6", "#023E8A", "#03045E",]
GRADIENT_GREEN_6 = ["#CCFF33", "#70E000", "#38B000", "#008000", "#006400", "#004B23"]
GRADIENT_ORANGE_6  = ["#FFBA08", "#FAA307", "#F48C06", "#E85D04", "#DC2F02", "#D00000"]

# Orange Red White yellow black
ORANGE_5= ["#0D3B66", "#FAF0CA", "#F4D35E", "#EE964B", "#F95738"]
# Orange red white blue green  light-green
ORANGE_GREEN_7 = ["#005F73", '#0A9396', '#94D2BD', '#E9D8A6', '#EE9B00', '#CA6702', '#BB3E03', '#AE2012', '#9B2226', ]

# Black Red orange white pink 
DISTINCT_7 = ["#588B8B", '#FFFFFF', '#FFD5C2', '#F28F3B', '#C8553D', '#2D3047', '#93B7BE']

# Green - White - Orange - Red 
GRADIENT_9 = ["#F4F1DE", '#EAB69F', '#E07A5F', '#8F5D5D', '#3D405B', '#5F797B', '#81B29A', '#BABF95', '#F2CC8F', ]


#### BLUE - RED 
ORANGE_BLUE_10=["#033270", "#1368AA", "#4091C9", "#9DCEE2", "#FEDFD4", "#F29479", "#F26A4F", "#EF3C2D", "#CB1B16", "#65010C"]
#### DARK GREEN - ORANGE
GREEN_ORANGE_10=["#264653", "#287271", "#2A9D8F", "#8AB17D", "#BABB74", "#E9C46A", "#EFB366", "#F4A261", "#EE8959", "#E76F51"]
#### DARK BLUE - ORANGE
DARK_BLUE_RED_10=["#011A51", "#1957DB", "#487BEA", "#7EA3F1", "#C8D7F9", "#B83700", "#F06C00", "#FAB129", "#FBC55F", "#FDE9C3"]
#### ORANGE - LIGHT BLUE
ORANGE_LIGHTBLUE_10=["#CC4400", "#D66915", "#E08E29", "#F0C761", "#FFFF99", "#C2FCFF", "#7CC6DE", "#3890BC", "#1C489A", "#000077"]
#### BLACK - LIGHT GREEN
BROWN_GREEN_10=["#310906", "#633533", "#90605E", "#E9B6B4", "#F3EFE0", "#C1D3C8", "#8FB7B0", "#597380", "#3E5168", "#222E50"]







LIGHT_DARK_PAIR = [
    # yellow 
    "#FFD700", lighten_color("#FFD700", 0.6), 
    # RED
    "#FF4500", lighten_color("#FF4500", 0.6), 
    # ORANGE - Brown 
    "#D2691E", lighten_color("#D2691E", 0.6), 
    # orange-red
    "#FFBA08" , "#D00000",
    # LIGHT BLUE 
    "#4169E1", lighten_color("#4169E1", 0.6),
    # DARK BLUE  
    "#00B4D8", "#03045E", 
    # PURPLE
    "purple", lighten_color("purple", 0.6),
    # Green 
    "#38B000", "#004B23", 
]





#### TEMPLACE   ### 1 (black - orange - blue - yellow )
# black - orange
DISTINCT_2_1 = ["#191716", "#EE964B"]
# black - orange - blue 
DISTINCT_3_1 = ["#191716", "#EE964B", "#8ECAE6", ]
# black - orange - blue - yellow 
DISTINCT_4_1 = ["#191716", "#EE964B", "#8ECAE6", '#F4D35E']
# blue purple green pink orange red
DISTINCT_6_1 = ["#ff9191", "#ffb75f", "#fff56a", "#64d380", "#5f8aee", "#a25fac"]


#### TEMPLACE   ### 2  (black - blue - orange - red )
# black - blue 
DISTINCT_2_2 = ['#032B43', "#3F88C5",]
# black - blue - orange 
DISTINCT_3_2 = ['#032B43', "#3F88C5", "#FFBA08",]
# black - blue - orange - red 
DISTINCT_4_2 = ['#032B43', "#3F88C5", "#FFBA08", "#D00000"]
# black blue green orange red yellow
DISTINCT_6_2 = ["#ef476f", "#ff99c8", "#ffd166", "#06d6a0", "#118ab2", "#073b4c"]


#### TEMPLACE   ### 3  (black - green - white - orange )
# black - orange 
DISTINCT_2_3 = ["#001524", '#FF7D00']
# black - green - orange 
DISTINCT_3_3 = ["#001524", "#15616D", '#FF7D00']
# black - green - white - orange 
DISTINCT_4_3 = ["#001524", "#15616D", "#8AB9F1", '#FF7D00']


#### TEMPLACE   ### 4  (blue, green, black yellow)
# black - green
DISTINCT_2_4 = ["#023047", '#219EBC']
# green - black orange 
DISTINCT_3_4 = ["#219EBC", "#023047", '#FFB703']
# blue - green - black - yellow 
DISTINCT_4_4 = ["#8ECAE6", "#219EBC", "#023047", '#FFB703']



#### TEMPLACE   ### 5  blue - blue - orange - red 
# black - blue
DISTINCT_2_5 = [lighten_color("#3a405a", 0.8), lighten_color("#aec5eb", 0.8)]
# black - blue orange 
DISTINCT_3_5 = [lighten_color("#3a405a", 0.8), lighten_color("#aec5eb", 0.8), lighten_color("#f9dec9", 0.8), ]
# black - blue - orange - red 
DISTINCT_4_5 = [lighten_color("#3a405a", 0.8), lighten_color("#aec5eb", 0.8), lighten_color("#f9dec9", 0.8), lighten_color('#e9afa3', 0.8)]


#### TEMPLACE   ### 6  blue - red  - orange 
# blue - orange
DISTINCT_2_6 = ["#26547C", "#FFD166"]
# blue - red  - orange 
DISTINCT_3_6 = ["#26547C", "#EF476F", "#FFD166"]


#### TEMPLACE   ### 7  blue - white - orange 
# blue - white
DISTINCT_2_7 = ["#0B3954", "#BFD7EA"]
# blue - white - orange 
DISTINCT_3_7 = ["#0B3954", "#BFD7EA", "#FF7D00"]
# Blue yellow orange red 
DISTINCT_5_7 = ["#0D3B66", "#BFD7EA", "#F4D35E", "#EE964B", "#F95738"]



#### TEMPLACE   ### 8  blue - white - orange 
# orange - grey
DISTINCT_2_8 = ["#dd6e42", "#4f6d7a"]
# orange - yellow - grey 
DISTINCT_3_8 = ["#dd6e42", "#e8dab2", "#4f6d7a"]





# COLOR PALLETS : 
# https://coolors.co/palette/3a5a40-9ec7b9-bcd8e7-e58f65-e8b545-f8ddb0



if __name__ == 'main':
    ### Range specific colors 
    colors = [(0, "#FF4500"), (0.5, 'black'), (1, "#4169E1")]
    cmap = generate_color_gradients2(1000, colors=colors)
    cmap # is list of colors (RGB, val)
    # val == 1 =end color, val == 0 start color