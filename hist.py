from colors import * 
from plot_utils import range_calc
from style import simplify_hist

# x_padding_factor == position of y axis (& y axis labels) (hortizontal)
# y_padding_factor == position of y axis labels  (veritical)
def bar_graph_X_Y(Hists, COLORS=[ORANGE, BLUE], OVERLAPING_COLORS=None, 
    figsize=(8, 6), name="test_hx_hy", artificial_darkening=1, decimal_places=0, bar_opacity=1, 
    barWidth = 0.3, lw=1.5, ec="white", 
    x_ticks_allowed=None, X_labels=None, X_labels_pos=None, X_label_fontsize=25, x_padding_factor=0.1, x_padding=0.1, x_label_rotate=0, 
    y_points=3, y_up_offset=1, y_down_offset=1,  Y_label_fontsize=20, switch_off_yaxis=True, y_padding_factor=-0.01, 
    bar_label_formatter=lambda x: f"{x:.1f}", bar_labels = None, bar_labels_y_offset=0.1, bar_labels_x_offset=0.1, bar_color=BAR_LABEL, bar_labels_font_size=5, 
    hline=None, hline_color='black', line_width=1.5, hline_style="-.", h_line_alpha=0.5,
    ):
    
    fig, ax = plt.subplots(figsize=figsize)
    
    if artificial_darkening:
        COLORS = [lighten_color(e, amount=artificial_darkening)  for e in COLORS]

    X_pos = [] 
    Y_pos = []
    
    for i,hist in enumerate(Hists):
        X, Y = hist
        Y_pos += Y
        X_pos += X
        if OVERLAPING_COLORS:
            ax.bar(X, Y, width = barWidth, color=COLORS, lw=lw, ec=ec, capsize=7, zorder=2, alpha=bar_opacity)
        else:
            ax.bar(X, Y, width = barWidth, color=COLORS[i], lw=lw, ec=ec, capsize=7, zorder=2, alpha=bar_opacity)
    
    if bar_labels == True:
        for i,hist in enumerate(Hists):
            X, Y = hist
            for x,y in zip(X,Y):
                ax.text( x + bar_labels_x_offset, y + bar_labels_y_offset, bar_label_formatter(y),  ha="right", va="baseline", fontsize=bar_labels_font_size, color=bar_color )
    
    if hline:
        Y_pos += hline
        for h_line in hline:
            ax.plot([min(X_pos) - barWidth, max(X_pos) + barWidth], [h_line, h_line], color=hline_color, lw=line_width, linestyle=hline_style, alpha=h_line_alpha, zorder=0)
            
    
    Y_range, Y_range_label = range_calc(Y_pos, y_points, y_up_off = y_up_offset , y_down_off=y_down_offset, decimal_places=decimal_places)
        
    if X_labels is None:
        X_range =   X_pos
        X_range_label = X_pos
    else:
        X_range = X_labels_pos
        X_range_label = X_labels 
    
    simplify_hist(ax, Y_range, Y_range_label, X_range, X_range_label, Y_label_fontsize, X_label_fontsize,
        x_padding = x_padding , y_padding_factor=y_padding_factor, x_padding_factor=x_padding_factor, x_ticks_allowed=x_ticks_allowed , x_min=min(X_pos) - barWidth, x_max= max(X_pos) + barWidth, switch_off_yaxis=switch_off_yaxis, x_label_rotate=x_label_rotate)

    plt.tight_layout()
    plt.savefig(f"{name}.png")
    

def bar_graph_X_Y_Gradient(Hists, COLORS=['#89CFF0', '#000080', '#000000'], 
    figsize=(8, 6), name="test_hx_hy", artificial_darkening=1, decimal_places=0, bar_opacity=1,
    barWidth = 0.3, lw=1.5, ec="white", 
    x_ticks_allowed=None, X_labels=None, X_labels_pos=None, X_label_fontsize=25, x_padding_factor=0.1, x_padding=0.1, x_label_rotate=0,
    y_points=3, y_up_offset=1, y_down_offset=1,  Y_label_fontsize=20, switch_off_yaxis=True, y_padding_factor=-0.01, 
    bar_label_formatter=lambda x: f"{x:.1f}", bar_labels = None, bar_labels_y_offset=0.1, bar_labels_x_offset=0.1, bar_color=BAR_LABEL, bar_labels_font_size=5, 
    hline=None, 
    ):
    
    fig, ax = plt.subplots(figsize=figsize)
    
    if artificial_darkening:
        COLORS = [lighten_color(e, amount=artificial_darkening)  for e in COLORS]
    

    SIZE = []
    for hist in Hists:
        SIZE += hist[2]
    diff_in_szie= max(SIZE) - min(SIZE) + 1
    colors_template = LinearSegmentedColormap.from_list('custom_gradient', COLORS, N=diff_in_szie)
    colors = [colors_template(i/diff_in_szie) for i in range(diff_in_szie)]
    
    X_pos = [] 
    Y_pos = []
    for i,hist in enumerate(Hists):
        X, Y, Size = hist
        Y_pos += Y
        X_pos += X
        for x,y,s in zip(X,Y,Size):
            s = (s - min(SIZE)) // 1
            ax.bar(x, y, width = barWidth, color=colors[s], lw=lw, ec=ec, capsize=7, zorder=2, alpha=bar_opacity)

    if bar_labels == True:
        for i,hist in enumerate(Hists):
            X, Y, _ = hist
            for x,y in zip(X,Y):
                ax.text( x + bar_labels_x_offset, y + bar_labels_y_offset, bar_label_formatter(y),  ha="right", va="baseline", fontsize=bar_labels_font_size, color=bar_color )
    
    Y_range, Y_range_label = range_calc(Y_pos, y_points, y_up_off = y_up_offset , y_down_off=y_down_offset, decimal_places=decimal_places)
        
    if X_labels is None:
        X_range =   X_pos
        X_range_label = X_pos
    else:
        X_range = X_labels_pos
        X_range_label = X_labels 

    simplify_hist(ax, Y_range, Y_range_label, X_range, X_range_label, Y_label_fontsize, X_label_fontsize,
        x_padding = x_padding , y_padding_factor=y_padding_factor, x_padding_factor=x_padding_factor, x_ticks_allowed=True , x_min=min(X_pos) - barWidth, x_max= max(X_pos) + barWidth, switch_off_yaxis=switch_off_yaxis, x_label_rotate=x_label_rotate)

    plt.tight_layout()
    plt.savefig(f"{name}.png")
    


# gap_between_groups is measured from the last bar (from group 1) and first bar (group 2)
def bar_graph_side_by_side(Hists, COLORS=[ORANGE, BLUE, BROWN], 
    figsize=(8, 6), name="test_hx_hy", artificial_darkening=1, decimal_places=0, bar_opacity=1,
    barWidth = 0.3, lw=1.5, ec="white", gap_between_bars = 1, gap_between_groups = 1, 
    x_ticks_allowed=None, X_labels=None, X_label_fontsize=25, x_padding_factor=0.1, x_padding=0.1, x_label_rotate=0,
    y_points=3, y_up_offset=1, y_down_offset=1,  Y_label_fontsize=20, switch_off_yaxis=True, y_padding_factor=-0.01, 
    bar_label_formatter=lambda x: f"{x:.1f}", bar_labels = None, bar_labels_y_offset=0.1, bar_labels_x_offset=0.1, bar_color=BAR_LABEL, bar_labels_font_size=5, 
    x_label_dist=None,
    ):
    
    fig, ax = plt.subplots(figsize=figsize)
    
    
    if artificial_darkening:
        COLORS = [lighten_color(e, amount=artificial_darkening)  for e in COLORS]

    
    N_of_groups = len(Hists[0])
    num_of_columns_per_group = len(Hists)
    group1 = np.arange(0, num_of_columns_per_group * gap_between_bars, gap_between_bars)
    
    # group1 
    # (group1[-1] + gap_between_groups) + group1 == 2 * group1 + gap_between_groups
    # ((2 * group1[-1] + gap_between_groups) + gap_between_groups ) + group1 ==  3 * group1 + 2 * gap_between_groups
    X_index = [ group1 + i * (group1[-1] + gap_between_groups) for i in range(N_of_groups)]
    X_index = np.array(X_index)

    X_pos = [] 
    Y_pos = []
    for i,hist in enumerate(Hists):
        Y = hist
        X = list(X_index[:,i])
        Y_pos += Y
        X_pos += X
        ax.bar(X, Y, width = barWidth, color=COLORS[i], lw=lw, ec=ec, capsize=7, zorder=2, alpha=bar_opacity)

    if bar_labels == True:
        for i,hist in enumerate(Hists):
            Y = hist
            X = list(X_index[:,i])
            for x,y in zip(X,Y):
                ax.text( x + bar_labels_x_offset, y + bar_labels_y_offset, bar_label_formatter(y),  ha="right", va="baseline", fontsize=bar_labels_font_size, color=bar_color )
    elif bar_labels != None:
        for i,hist in enumerate(Hists):
            Y = hist
            X = list(X_index[:,i])
            labels = bar_labels[i]
            for k, (x,y,l) in enumerate(zip(X,Y, labels)):
                if type(bar_color) == str:
                    ax.text( x + bar_labels_x_offset, y + bar_labels_y_offset, l,  ha="right", va="baseline", fontsize=bar_labels_font_size, color=bar_color )
                else:
                    ax.text( x + bar_labels_x_offset, y + bar_labels_y_offset, l,  ha="right", va="baseline", fontsize=bar_labels_font_size, color=bar_color[i][k] )

    Y_range, Y_range_label = range_calc(Y_pos, y_points, y_up_off = y_up_offset , y_down_off=y_down_offset, decimal_places=decimal_places)

    X_range, X_range_label=  None, None
    if X_labels:
        X_range = X_index.mean(-1)
        X_range_label = X_labels
        simplify_hist(ax, Y_range, Y_range_label, X_range, X_range_label, Y_label_fontsize, X_label_fontsize,
            x_padding = x_padding , y_padding_factor=y_padding_factor, x_padding_factor=x_padding_factor, x_ticks_allowed=True , x_min=min(X_pos) - barWidth, x_max= max(X_pos) + barWidth, switch_off_yaxis=switch_off_yaxis, x_label_rotate=x_label_rotate, x_label_dist=x_label_dist)
    else:
        simplify_hist(ax, Y_range, Y_range_label, X_range, X_range_label, Y_label_fontsize, X_label_fontsize,
            x_padding = x_padding , y_padding_factor=y_padding_factor, x_padding_factor=x_padding_factor, x_ticks_allowed=False , x_min=min(X_pos) - barWidth, x_max= max(X_pos) + barWidth, switch_off_yaxis=switch_off_yaxis, x_label_rotate=x_label_rotate, x_label_dist=x_label_dist)

    plt.tight_layout()
    plt.savefig(f"{name}.png")
    







def bar_graph_horizontal(Hists, COLORS=[ORANGE, BLUE, BROWN], side_by_side=None, 
    figsize=(8, 6), name="test_hx_hy", artificial_darkening=1, decimal_places=1, grid_shape="x",
    gap_between_bars = 1, barWidth = 0.3, bar_opacity=1,
    lw=1.5, ec="white", 
    y_ticks_allowed=None, Y_labels=None, Y_label_fontsize=25, 
    bar_labels = None, bar_labels_x_offset=0.1, bar_labels_y_offset=0.1, bar_labels_font_size=5, bar_color=None, 
    x_points=3, X_label_fontsize=20, x_left_offset=0.1, x_right_offset = 0.1, x_padding=0, x_ticks_allowed=True, switch_off_xaxis=True, x_label_rotate=0,
    switch_off_yaxis=True, y_padding=0, x_padding_factor=0.1, y_padding_factor=0, y_label_rotate=0):
    bar_label_formatter = lambda x: f"{x:.{decimal_places}f}"
    fig, ax = plt.subplots(figsize=figsize)
    
    
    if artificial_darkening:
        COLORS = [lighten_color(e, amount=artificial_darkening)  for e in COLORS]

    if side_by_side:
        assert False, "broken not yet verified"
        N_of_hist = len(Hists[0])
    else:
        N_of_hist = len(Hists)
    indices = []
    index = 0
    if bar_color:
        bar_color = [bar_color for i in range(N_of_hist)]
    elif bar_color is None:
        bar_color = COLORS

    for i in range(N_of_hist):
        index = index + gap_between_bars
        indices.append(index)
    y_index = np.array(indices)
    y_index = y_index[::-1]

    if side_by_side:
        X_pos = Hists[0]
    else:
        X_pos = Hists
    Y_pos = y_index
    if side_by_side:
        for hist in Hists:
            for i, (X,Y) in enumerate(zip(hist, y_index)):
                ax.barh(y=Y, width=X, height=barWidth, color=COLORS[i], lw=lw, ec=ec, capsize=7, zorder=2, alpha=bar_opacity)
    else:
        for i, (X,Y) in enumerate(zip(Hists, y_index)):
            ax.barh(y=Y, width=X, height=barWidth, color=COLORS[i], lw=lw, ec=ec, capsize=7, zorder=2, alpha=bar_opacity)
        

    if bar_labels == True:
        for i, (X,Y) in enumerate(zip(Hists, y_index)):
            ax.text( X + bar_labels_x_offset, Y + bar_labels_y_offset, bar_label_formatter(X),  ha="right", va="baseline", fontsize=bar_labels_font_size, color=bar_color[i] )
            print(X + bar_labels_x_offset, Y + bar_labels_y_offset)
    elif bar_labels != None:
        for i, (X,Y) in enumerate(zip(Hists, y_index)):
            label = bar_labels[i]
            ax.text( X + bar_labels_x_offset, Y + bar_labels_y_offset, label,  ha="right", va="baseline", fontsize=bar_labels_font_size, color=bar_color[i] )
        
        
    X_range, X_range_label = range_calc(X_pos, x_points, y_up_off = x_right_offset,  y_down_off=x_left_offset, decimal_places=decimal_places)

    
    # Y_range = Y_pos + 
    simplify_hist(ax, Y_pos, Y_labels, X_range, X_range_label, Y_label_fontsize, X_label_fontsize,
                  x_min=min(X_range), x_max= max(X_range), x_ticks_allowed=x_ticks_allowed , switch_off_yaxis=switch_off_yaxis, switch_off_xaxis=switch_off_xaxis,
                  y_padding=y_padding + barWidth, grid_shape=grid_shape, 
                  x_padding = x_padding, x_padding_factor=x_padding_factor, y_padding_factor=y_padding_factor,
                  x_label_rotate=x_label_rotate, y_label_rotate=y_label_rotate)
            
    plt.tight_layout()
    plt.savefig(f"{name}.png")
    


