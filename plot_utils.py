import matplotlib.colors as mc
import colorsys
from matplotlib.colors import LinearSegmentedColormap

def range_calc(y_vals, no, y_up_off = 0 , y_down_off=0, decimal_places=1):
    formatter = lambda x: f"{x:.{decimal_places}f}"
    MAX_Y = max(y_vals) + y_up_off
    MIN_Y = min(y_vals) - y_down_off
    offset = (MAX_Y - MIN_Y)/ no
    Y_range = [MIN_Y + offset * i  for i in range(no+1)]
    Y_range_label = [formatter(e) for e in Y_range]
    return Y_range, Y_range_label
    

