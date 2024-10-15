
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
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def generate_color_gradient(n, colors = plt.cm.coolwarm(np.linspace(0, 1, 1000))):
    # Generate a gradient of colors from blue to orange
    colors = LinearSegmentedColormap.from_list("blue_to_orange", colors)
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

