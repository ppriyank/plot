import matplotlib.colors as mc
import colorsys
from matplotlib.colors import LinearSegmentedColormap

def lighten_color(color, amount=0.5):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

def range_calc(y_vals, no, y_up_off = 0 , y_down_off=0, formatter = lambda x: f"{x:.1f}"):
    MAX_Y = max(y_vals) + y_up_off
    MIN_Y = min(y_vals) - y_down_off
    offset = (MAX_Y - MIN_Y)/ no
    Y_range = [MIN_Y + offset * i  for i in range(no+1)]
    Y_range_label = [formatter(e) for e in Y_range]
    return Y_range, Y_range_label
    

def generate_color_gradient(n):
    # Generate a gradient of colors from blue to orange
    colors = plt.cm.coolwarm(np.linspace(0, 1, n))
    colors = LinearSegmentedColormap.from_list("blue_to_orange", colors)
    return colors


def get_color_gradient(c1, c2, n, use_colors=None):
    def hex_to_RGB(hex_str):
        """ #FFFFFF -> [255,255,255]"""
        #Pass 16 to the integer function for change of base
        return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]

def three_color_gradient(colors, n=256):
    gradient = np.zeros((n, 3))
    for i in range(3):
        gradient[:, i] = np.linspace(colors[0][i], colors[1][i], n//2)
        gradient[:, i] = np.concatenate((gradient[:, i], np.linspace(colors[1][i], colors[2][i], n//2)))
    return gradient

