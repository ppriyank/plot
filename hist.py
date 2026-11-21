import matplotlib.pyplot as plt
from colors_set import * 
from plot_add import * 
import torch 
import numpy as np 
from collections import defaultdict
from math import log 


def process_colors_per_label(Labels, colors, Hists, Pattern, stack_colors=None, stack_brightness_factor=0.3):
    if stack_colors:
        assert False, "not yet implemented... "
    if Labels is None:
        Labels = range(len(Hists))
    unique_labels = set(Labels)

    if Pattern is None:
        Pattern = [None for e in unique_labels]

    label_dict = {}
    for label, hist in zip(unique_labels, Hists):
        label_dict[label] = []
        curr = 1
        for i in range (len(hist['y'])):
            if isinstance(colors, str):
                color = lighten_color(colors, amount=curr)
            elif isinstance(colors, list) and isinstance(colors[0], float):
                color = lighten_color(colors, amount=curr)
            elif isinstance(colors, list):
                color = lighten_color(colors[label], amount=curr)
            elif isinstance(colors, dict):
                color = lighten_color(colors[label], amount=curr)
            curr += stack_brightness_factor
            label_dict[label].append(color)
                
    colors = label_dict
    assert isinstance(colors, dict), "Colors should be dictionary of label = colors" 
    return Labels, colors, Pattern
    
def verify_shape(Hists):
    for hist in Hists:
        prev = None 
        for e in hist['y']:
            curr = len(e)
            if prev == None:
                prev = curr
            assert prev == curr , f"Invalid Histogram Shape, {hist}"

def adjust_batwidth(Hists, boder=0):
    All_x_Pos = []
    for e in Hists:
        All_x_Pos += e['x']
    All_x_Pos = sorted(All_x_Pos)
    diff = [abs(x-y) for x,y in zip(All_x_Pos, All_x_Pos[1:]) if x!= y ]

    # distance between two bars is : D = 
    # 1/2 barwidth (bar 1) + boder (bar 1) 
    # 1/2 barwidth (bar 2) + boder (bar 2) 

    # D = barwidth + 2 * boder (bar_sep)
    return min(diff) - 2 * boder
    
def adjust_X(Hists, bar_width=1, bar_boder=0, bar_group_sep=1):
    number_hist = len(Hists) # no of histogram side by side
    max_length = max([len(e['y'][0]) for e in Hists]) # no of time side by side occurs
    
    # half of the bar it self
    GAP = bar_width / 2

    # N-1 barboders * 2 (one from itself one from other)
    GAP += (number_hist - 1) * (2 * bar_boder)

    # N-1 bars 
    GAP += (number_hist - 1) * (bar_width)

    # Bar Group ended
    GAP += bar_group_sep

    # Second Group first bar 
    GAP += bar_width / 2

    new_Hists = []
    start = 0 
    for hist in Hists:
        x= [start +  GAP * i for i in range(len(hist['y'][0]))]
        
        # half of the bar it self
        start += bar_width / 2 
        # next bar
        start += bar_width / 2 
        # 2 boders in between 
        start += 2 * bar_boder
    
        new_Hists.append(
            {
                'x' : x, 'y': hist['y']
            }
        )
    return new_Hists
    
def add_patterns(Patterns, ax):
    for container in ax.containers:
        if len(Patterns) != len(container.patches):
            raise ValueError(
                f"Expected {len(container.patches)} patterns for bars, got {len(PATTERNS)}"
            )
        for patch, pattern in zip(container.patches, Patterns):
            patch.set_hatch(pattern)
            if hasattr(patch, "set_hatchcolor"):
                patch.set_hatchcolor(PATTERN_COLOR)
            else:
                patch._hatch_color = mcolors.to_rgba(
                    PATTERN_COLOR, patch.get_alpha()
                )


### color assigned by max color
def create_color_gradient(Hists, colors, bins=100):
    Y_values = []
    for hist in Hists:
        for y in hist['y']:
            Y_values += y
        
    diff_in_y= max(Y_values) - min(Y_values) + 1
    
    colors_template = LinearSegmentedColormap.from_list('custom_gradient', [lighten_color(colors, amount=0.5), colors, lighten_color(colors, amount=1.5)], N=bins)
    new_colors = []
    
    for hist in Hists:
        Previous_height = [0 for e in  hist['y'][0]]
        for y in hist['y']:
            Previous_height = [a + b for a,b in zip(Previous_height, y)]
        val = (max(Previous_height) - min(Y_values)) / diff_in_y
        new_colors.append(colors_template(val))
        
    return new_colors
    


def bin_histogram(Hists, n_bins, use_log=None):
    if not isinstance(n_bins, int) or n_bins <= 0:
        raise ValueError("Hist_N_Bins must be a positive integer")

    if isinstance(Hists, torch.Tensor):
        values = Hists.detach().cpu().flatten()
        if not values.is_floating_point():
            values = values.to(torch.float32)
        counts, edges = torch.histogram(values, bins=n_bins)
        counts = counts.tolist()
        edges = edges.tolist()
    else:
        values = np.asarray(Hists).flatten()
        counts, edges = np.histogram(values, bins=n_bins)
        counts = counts.tolist()
        edges = edges.tolist()

    Hists = []
    for i, (left, right) in enumerate(zip(edges[:-1], edges[1:])):
        x = (left + right) / 2
        y = counts[i]
        if use_log:
            y = log (y + 1e-6)
        Hists.append({
            'x': [x] , 'y': [[y]]
            }
        )
    return Hists

    


        





def bar_plt(ax=None,
    Hists=None, Labels=None, 
    colors = [ORANGE, BLUE, PINK],  
    swap_axis=None, 
    automatic_adjust_width = None, 
    
    bar_opacity=0.9, 
    bar_group_sep=1, 
    bar_width = 0.8, ## not really same as "x-coordiantes"
    bar_border_width=0.1, 
    bar_border_color="white", 
    
    bar_labels = None,
    bar_labels_y_offset=0, 
    bar_labels_x_offset=0,
    bar_labels_color=BAR_LABEL,
    bar_labels_font_size=5, 
    bar_label_decimal_places=0, 

    Pattern = None,
    bar_connector = None,
    
    Hist_mode = None, 
    Hist_N_Bins = 10, 
    Hist_gradient = None, 

    stack_colors = None, 
    stack_dist = 0.5, 
    stack_brightness_factor = 0.3, 
        
    vline_offset = 10,
    hline_offset = 10,
    line_width=1,

    **args
    ):

    if Hist_mode:
        Hists = bin_histogram(Hists, Hist_N_Bins)
        assert isinstance(colors, list) and len(colors) == 3, "Histogram should have consistent colors"
    
    verify_shape(Hists)

    if Hist_gradient:
        colors = create_color_gradient(Hists, colors, bins=Hist_N_Bins)
         


    Labels, colors, Pattern = process_colors_per_label(Labels, colors, Hists, Pattern, stack_colors=stack_colors, stack_brightness_factor=stack_brightness_factor,)
    

    if not all([('x' in e) for e in Hists]):
        Hists = adjust_X(Hists, bar_width=bar_width, bar_boder = bar_border_width, bar_group_sep=bar_group_sep)
        
    
    assert all([('x' in e and 'y' in e) for e in Hists])
    if automatic_adjust_width:
        bar_width = adjust_batwidth(Hists, boder=bar_border_width)

    # print(bar_width, bar_border_width, [e['x'] for e in Hists])


    hist_cofig_vals = dict(
        alpha=bar_opacity, lw=bar_border_width, ec=bar_border_color, zorder=12,
    )
    pos_bar_height = defaultdict(int)
    #### PLotting Bars 
    for k, (label, hist) in enumerate(zip(Labels, Hists)):
        X, Ys = hist['x'], hist['y'] 
        # In case bars are stacked (same x, different y)
        Previous_height = None
        for i, y in enumerate(Ys):
            if Previous_height is None:  
                Previous_height = [0 for i in y]
            else:
                Previous_height = [e + stack_dist for e in Previous_height]
                y = [e - stack_dist for e in y]
            
            if swap_axis:
                ax.barh(
                    X, y, height=bar_width, color=colors[label][i],
                    left=Previous_height, label=label, hatch=Pattern[k],
                    **hist_cofig_vals
                )
            else:
                ax.bar(
                    X, y, width=bar_width, color=colors[label][i],
                    bottom=Previous_height, label=label, hatch=Pattern[k],
                    **hist_cofig_vals
                )
            Previous_height = [a + b for a,b in zip(Previous_height, y)]

        for x,y in zip(X, Previous_height):
            pos_bar_height[x] = y
    
    
    
    
    #### Adding labels on top of bar 
    if bar_labels == True:
        bar_label_formatter = lambda x: f"{x:.{bar_label_decimal_places}f}"
        bar_text_onfig = dict(
                    fontsize=bar_labels_font_size, color=bar_labels_color, zorder=15,
        )
        for key in pos_bar_height:
            height = pos_bar_height[key]
            if swap_axis:
                ax.text(
                    height + bar_labels_x_offset, key + bar_labels_y_offset,
                    bar_label_formatter(height), ha="left", va="center_baseline",
                    **bar_text_onfig
                )
            else:
                ax.text(
                    key + bar_labels_x_offset, height + bar_labels_y_offset,
                    bar_label_formatter(height), ha="center", va="baseline",
                    **bar_text_onfig
                )

    
    
    
    # #### Conect Bar with Same label 
    if bar_connector == True:
        for k, (label, hist) in enumerate(zip(Labels, Hists)):
            X, Ys = hist['x'], hist['y'] 
            # In case bars are stacked (same x, different y)
            Previous_height = None
            for i, y in enumerate(Ys):
                if Previous_height is None:  
                    Previous_height = [0 for i in y]
                Previous_height = [a + b for a,b in zip(Previous_height, y)]
                
            if swap_axis:
                ax.plot(
                    Previous_height, X, color=colors[label][-1],
                    lw=line_width, alpha=bar_opacity, zorder=50,
                )
            else:
                ax.plot(
                    X, Previous_height, color=colors[label][-1],
                    lw=line_width, alpha=bar_opacity, zorder=50,
                )
            

    
    X_values = [0, 0] if swap_axis else []
    Y_values = [] if swap_axis else [0, 0]
    for key in pos_bar_height:
        if swap_axis:
            X_values.append(pos_bar_height[key])
            Y_values.append(key)
        else:
            Y_values.append(pos_bar_height[key])
            X_values.append(key)
    
    
    local_X, local_Y = plot_background_lines_shades(hline_offset=hline_offset, vline_offset=vline_offset, ax=ax, X_values=X_values, Y_values=Y_values, line_width=line_width, **args)
    Y_values += local_Y
    X_values += local_X

    # plt.savefig("test_hist.png", dpi=300)
    return X_values, Y_values



