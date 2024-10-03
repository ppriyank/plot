
from matplotlib.patheffects import withStroke
import matplotlib.colors as mc
import colorsys

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


def lighten_color(color, amount=0.5):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

