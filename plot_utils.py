import matplotlib.colors as mc
import colorsys
from matplotlib.colors import LinearSegmentedColormap

import colorsys
import matplotlib.pyplot as plt
import numpy as np 

import matplotlib.pyplot as plt
import numpy as np 

def range_calc(y_vals, no, y_up_off = 0 , y_down_off=0, decimal_places=1):
    formatter = lambda x: f"{x:.{decimal_places}f}"
    MAX_Y = max(y_vals) + y_up_off
    MIN_Y = min(y_vals) - y_down_off
    offset = (MAX_Y - MIN_Y)/ no
    Y_range = [MIN_Y + offset * i  for i in range(no+1)]
    Y_range_label = [formatter(e) for e in Y_range]
    return Y_range, Y_range_label
    
def binning(row, n_bins = 10, mini=0, maxi=1):
    deci = (row - mini ) / ( maxi - mini)
    if type(deci) == np.array or type(deci) == np.ndarray:
        bucket = deci * n_bins // 1
    else:
        bucket = int(deci * n_bins // 1)
    return bucket

def luminance(color):
    """Calculate the relative luminance of an RGB color."""
    r, g, b = mc.to_rgb(color)
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(color1, color2):
    """Compute the contrast ratio between two RGB colors."""
    lum1 = luminance(color1)
    lum2 = luminance(color2)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)




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


def colors_heat_map(maxi,  mini, specific_values= [-2,0,2], n_bins=100 , specific_colors=None):
    zero_one_range = lambda x: (x - mini) / (maxi - mini)
    if specific_values is not None:
        if type(specific_values) == list:
            colors = [
                (zero_one_range(mini), lighten_color("#FF4500", 0.8) ), 
                (zero_one_range( specific_values[0] ), lighten_color("#FF4500", 1.5)), 
                (zero_one_range( specific_values[1] ), 'white'), 
                (zero_one_range( specific_values[2] ), lighten_color("#4169E1", 1.5)), 
                (zero_one_range(maxi), lighten_color("#4169E1", 0.8) )
            ]
        else:
            colors = [
                (zero_one_range(mini), lighten_color("#FF4500", 0.8) ), 
                (zero_one_range( specific_values ), 'white'), 
                (zero_one_range(maxi), lighten_color("#4169E1", 0.8) )
            ]
    else:
        colors = [
            (zero_one_range(mini), lighten_color("#FF4500", 0.8) ), 
            (zero_one_range(maxi), lighten_color("#4169E1", 0.8) )
        ]
    cmap = generate_color_gradients2(n_bins, colors)
    return cmap


