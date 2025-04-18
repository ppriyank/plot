
from matplotlib.patheffects import withStroke
import matplotlib.colors as mc
import colorsys
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np 

def lighten_color(color, amount=0.5):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    c= colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])
    c =[round(e, 15) for e in c]
    return c


def generate_color_gradient(n, colors = plt.cm.coolwarm(np.linspace(0, 1, 1000))):
    # Generate a gradient of colors from blue to orange
    colors = LinearSegmentedColormap.from_list("blue_to_orange", colors)
    return colors

def generate_color_gradients2(n, colors=["#4169E1", "#FF4500"]):
    colors_template = LinearSegmentedColormap.from_list('custom_gradient', colors, N=n)
    colors = [colors_template(i/n) for i in range(n)]
    return colors

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


#### BLUE - RED 
COLOR_SET_10=["#033270", "#1368AA", "#4091C9", "#9DCEE2", "#FEDFD4", "#F29479", "#F26A4F", "#EF3C2D", "#CB1B16", "#65010C"]
#### DARK GREEN - ORANGE
COLOR_SET_10_2=["#264653", "#287271", "#2A9D8F", "#8AB17D", "#BABB74", "#E9C46A", "#EFB366", "#F4A261", "#EE8959", "#E76F51"]
#### DARK BLUE - ORANGE
COLOR_SET_10_3=["#011A51", "#1957DB", "#487BEA", "#7EA3F1", "#C8D7F9", "#B83700", "#F06C00", "#FAB129", "#FBC55F", "#FDE9C3"]
#### ORANGE - LIGHT BLUE
COLOR_SET_10_4=["#CC4400", "#D66915", "#E08E29", "#F0C761", "#FFFF99", "#C2FCFF", "#7CC6DE", "#3890BC", "#1C489A", "#000077"]
#### BLACK - LIGHT GREEN
COLOR_SET_10_5=["#310906", "#633533", "#90605E", "#E9B6B4", "#F3EFE0", "#C1D3C8", "#8FB7B0", "#597380", "#3E5168", "#222E50"]


#### BLUE - ORANGE
COLOR_SET_5_1=["#0D3B66", "#FAF0CA", "#F4D35E", "#EE964B", "#F95738"]
#### BLUE - ORANGE
COLOR_SET_5_2=["#3D348B", "#7678ED", "#F7B801", "#F18701", "#F35B04"]


# distinct 8 colors  --> 16 colors in paris 
COLOR_SET_16_1 = ["#F00314", '#FF8019', '#FAE603', '#28E10A', '#3BB5FF', '#0500C7', '#5C03FA', '#DE00ED']
COLOR_SET_16_1 = [x for e in COLOR_SET_16_1 for x in (lighten_color(e, 1.2), lighten_color(e, 0.8))]

# distinct 8 colors  --> 16 colors in paris 
COLOR_SET_14_1 = ["#588B8B", '#FFFFFF', '#FFD5C2', '#F28F3B', '#C8553D', '#2D3047', '#93B7BE']
COLOR_SET_14_1 = [x for e in COLOR_SET_14_1 for x in (lighten_color(e, 1), lighten_color(e, 0.8))]






PAIRED_COLORS = sns.color_palette("Paired", as_cmap=True)
ALONE_COLORS = sns.color_palette("pastel", as_cmap=True)


# Create the colormap
HEAT_MAP_COLOR = LinearSegmentedColormap.from_list("custom_cmap", [ORANGE, RED, "black", BLUE, "white"][::-1])
BAR_LABEL = "#009933"


FIVE_COLOR_SET = ["#FFD700", lighten_color("#FFD700", 0.6), 
    "#FF4500", lighten_color("#FF4500", 0.6), 
    "#D2691E", lighten_color("#D2691E", 0.6), 
    "#4169E1", lighten_color("#4169E1", 0.6),
    "purple", lighten_color("purple", 0.6),
]


#### LIGHT BLUE TO DARK 
GRADIENT_COLORS_6 = [
    "#CAF0F8", "#48CAE4", "#00B4D8", "#0096C7", "#0077B6", "#023E8A", "#03045E",
]

#### LIGHT YELLOW TO DARK GREEN 
GRADIENT_COLORS_6_GREEN = [
    "#CCFF33", "#70E000", "#38B000", "#008000", "#006400", "#004B23"
]


DISTINCT_5 = [
    "#0D3B66", "#FAF0CA", "#F4D35E", "#EE964B", "#F95738"
]


# COLOR PALLETS : 
# https://coolors.co/palette/3a5a40-9ec7b9-bcd8e7-e58f65-e8b545-f8ddb0



if __name__ == 'main':
    ### Range specific colors 
    colors = [(0, "#FF4500"), (0.5, 'black'), (1, "#4169E1")]
    cmap = generate_color_gradients2(1000, colors=colors)
    cmap # is list of colors (RGB, val)
    # val == 1 =end color, val == 0 start color