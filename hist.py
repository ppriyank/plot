from colors import * 
from utils import range_calc
from style import simplify_hist


def bar_graph_X_Y(Hists, COLORS=[ORANGE, BLUE], 
    figsize=(8, 6), name="test_hx_hy", artificial_darkening=1, decimal_places=0, bar_opacity=1,
    barWidth = 0.3, lw=1.5, ec="white", 
    x_ticks_allowed=None, X_labels=None, X_labels_pos=None, X_label_fontsize=25, x_padding_factor=0.1, x_padding=0.1,
    y_points=3, y_up_offset=1, y_down_offset=1,  Y_label_fontsize=20, switch_off_yaxis=True, y_padding_factor=-0.01, 
    bar_label_formatter=lambda x: f"{x:.1f}", bar_labels = None, bar_labels_y_offset=0.1, bar_labels_x_offset=0.1, bar_color=BAR_LABEL, bar_labels_font_size=5, 
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
        ax.bar(X, Y, width = barWidth, color=COLORS[i], lw=lw, ec=ec, capsize=7, zorder=2, alpha=bar_opacity)

    if bar_labels == True:
        for i,hist in enumerate(Hists):
            X, Y = hist
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
        x_padding = x_padding , y_padding_factor=y_padding_factor, x_padding_factor=x_padding_factor, x_ticks_allowed=True , x_min=min(X_pos) - barWidth, x_max= max(X_pos) + barWidth, switch_off_yaxis=switch_off_yaxis)

    plt.tight_layout()
    plt.savefig(f"{name}.png")
    

def bar_graph_X_Y_Gradient(Hists, COLORS=['#89CFF0', '#000080', '#000000'], 
    figsize=(8, 6), name="test_hx_hy", artificial_darkening=1, decimal_places=0, bar_opacity=1,
    barWidth = 0.3, lw=1.5, ec="white", 
    x_ticks_allowed=None, X_labels=None, X_labels_pos=None, X_label_fontsize=25, x_padding_factor=0.1, x_padding=0.1,
    y_points=3, y_up_offset=1, y_down_offset=1,  Y_label_fontsize=20, switch_off_yaxis=True, y_padding_factor=-0.01, 
    bar_label_formatter=lambda x: f"{x:.1f}", bar_labels = None, bar_labels_y_offset=0.1, bar_labels_x_offset=0.1, bar_color=BAR_LABEL, bar_labels_font_size=5, 
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
        x_padding = x_padding , y_padding_factor=y_padding_factor, x_padding_factor=x_padding_factor, x_ticks_allowed=True , x_min=min(X_pos) - barWidth, x_max= max(X_pos) + barWidth, switch_off_yaxis=switch_off_yaxis)

    plt.tight_layout()
    plt.savefig(f"{name}.png")
    


# gap_between_groups is measured from the last bar (from group 1) and first bar (group 2)
def bar_graph_side_by_side(Hists, COLORS=[ORANGE, BLUE, BROWN], 
    figsize=(8, 6), name="test_hx_hy", artificial_darkening=1, decimal_places=0, bar_opacity=1,
    barWidth = 0.3, lw=1.5, ec="white", gap_between_bars = 1, gap_between_groups = 1, 
    x_ticks_allowed=None, X_labels=None, X_labels_pos=None, X_label_fontsize=25, x_padding_factor=0.1, x_padding=0.1,
    y_points=3, y_up_offset=1, y_down_offset=1,  Y_label_fontsize=20, switch_off_yaxis=True, y_padding_factor=-0.01, 
    bar_label_formatter=lambda x: f"{x:.1f}", bar_labels = None, bar_labels_y_offset=0.1, bar_labels_x_offset=0.1, bar_color=BAR_LABEL, bar_labels_font_size=5, 
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
            for x,y,l in zip(X,Y, labels):
                ax.text( x + bar_labels_x_offset, y + bar_labels_y_offset, l,  ha="right", va="baseline", fontsize=bar_labels_font_size, color=bar_color )

    Y_range, Y_range_label = range_calc(Y_pos, y_points, y_up_off = y_up_offset , y_down_off=y_down_offset, decimal_places=decimal_places)

    if X_labels is None:
        X_range =   X_pos
        X_range_label = X_pos
    else:
        X_range = X_labels_pos
        X_range_label = X_labels 

    simplify_hist(ax, Y_range, Y_range_label, X_range, X_range_label, Y_label_fontsize, X_label_fontsize,
        x_padding = x_padding , y_padding_factor=y_padding_factor, x_padding_factor=x_padding_factor, x_ticks_allowed=True , x_min=min(X_pos) - barWidth, x_max= max(X_pos) + barWidth, switch_off_yaxis=switch_off_yaxis)

    plt.tight_layout()
    plt.savefig(f"{name}.png")
    





