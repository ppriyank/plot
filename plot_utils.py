import matplotlib.colors as mc
import colorsys
from matplotlib.colors import LinearSegmentedColormap

import colorsys
import matplotlib.colors as mc

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

