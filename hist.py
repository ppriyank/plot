from colors import * 
from utils import range_calc
from style import simplify_hist


def bar_graph_X_Y(Hists, COLORS=[ORANGE, BLUE], 
    figsize=(8, 6), name="test_hx_hy", artificial_darkening=1, decimal_places=0, bar_opacity=1,
    barWidth = 0.3, lw=1.5, ec="white", 
    x_ticks_allowed=None, X_labels=None, X_labels_pos=None, X_label_fontsize=25, x_padding_factor=0.1, x_padding=0.1,
    y_points=3, y_up_offset=1, y_down_offset=1,  Y_label_fontsize=20, switch_off_yaxis=True, y_padding_factor=-0.01, 
    bar_label_formatter=None, 
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

    # if bar_label_formatter:
    #     for i,hist in enumerate(Hists):
    #         X, Y = hist
    #         import pdb
    #         pdb.set_trace()
            # ax.text( x_min - x_padding + x_padding_factor, label_pos + PAD, str(label),  ha="right", va="baseline", fontsize=Y_label_fontsize, )
            # ax.bar(X, Y, width = barWidth, color=COLORS[i], lw=lw, ec=ec, capsize=7, )


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
    









# delta == Y axis labels position 
# y_header_label_delta == X-axis Position of labels on top of bars 
# bar_label_formatter=lambda x:f"{x:.2f}"
# b2_y_label_offset second bar label height
# b2_x_label_offset=None second bar label x position 
def bar_graph(X, Y=None, Y_range=[i * 0.1 for i in range(0, 11, 2)], Y_range_label=[i * 10 for i in range(0, 11, 2)], 
    X_labels = ['CAL', 'BM (Our)', 'RLQ (Our)'], name="gender", delta=-.4, y_header_label_delta=- 0.075, gap_between_bars=2,
    Y_label_fontsize=20, X_label_fontsize=25, bar_label_fontsize=20, enable_line=False, y_offset=None, barWidth = 0.3, figsize=(8, 6), bar_label_formatter=None, R1_axis=None,
    COLORS=None, h_line=None, b2_y_label_offset=None, b2_x_label_offset=None, use_default_colors=None, switch_off_yaxis=None, y_axis_labels=True, x_label_rotate = None, custom_bar_labels=None, custom_bar_label_colors="#009933"):
    if use_default_colors:
        assert COLORS is None
        COLORS = [BLUE, ORANGE]

    fig, ax = plt.subplots(figsize=figsize)
    
    # width of the bars
    
    # Choose the height of the blue bars
    C1 = X
    # Choose the height of the cyan bars
    C2 = Y

    if C2 == None:
        # The x position of bars
        N = len(C1)
        if R1_axis is None :
            r1 = [ i * (gap_between_bars + barWidth) for i in range( len(C1) )]
        else:
            r1 = R1_axis
        print("***", r1)
        if COLORS:
            for r, y, color in zip(r1, C1, COLORS):
                ax.bar(r, y, width = barWidth, color=color, lw=1.5, ec="white", capsize=7, zorder=12,)
        else:
            ax.bar(r1, C1, width = barWidth, color=BLUE, lw=1.5, ec="white", capsize=7, zorder=12,)
        
        if enable_line:
            ax.scatter(r1, C1, color=ORANGE, lw=6, zorder=15, path_effects=path_effects)
            ax.plot(r1, C1, color=ORANGE, lw=6, zorder=15, linestyle='dashed', alpha=1, )

        if bar_label_fontsize is not None:
            for x_pos,y_pos in zip(r1, C1):
                # y_pos = int( y_pos * 100 ) / 100  # 2.23
                y_pos_label = y_pos
                if bar_label_formatter: y_pos_label = bar_label_formatter(y_pos_label)
                if y_offset is None:
                    ax.text( x_pos  + y_header_label_delta, y_pos + max(Y_range) * 2 / 100 , y_pos_label , color='black', fontsize=bar_label_fontsize, ha="left", path_effects=font_path_effects , zorder=16) 
                else:
                    ax.text( x_pos  + y_header_label_delta, y_pos + y_offset , y_pos_label, color='black', fontsize=bar_label_fontsize, ha="left", path_effects=font_path_effects , zorder=16)
        if X_labels is not None  and len(r1) != len(X_labels):
            r1 = range(len(X_labels))

        if X_labels is not None :
            ax.xaxis.set_ticks(r1)
            if x_label_rotate:
                ax.xaxis.set_ticklabels( X_labels , fontsize=X_label_fontsize, rotation=x_label_rotate)
            else:
                ax.xaxis.set_ticklabels( X_labels , fontsize=X_label_fontsize)
                
            ax.xaxis.set_tick_params(length=6, width=1.2)
        else:
            ax.xaxis.set_tick_params(labelbottom=False, length=0)
        
    else:
        COLORS = [BLUE, ORANGE]
        # The x position of bars
        r1 = np.arange(len(C1))
        r2 = [x + barWidth for x in r1]
        print(r1,r2)
        # Create blue bars
        for index, (r, y, color) in enumerate(zip([r1,r2], [C1, C2], COLORS)):
            # ax.bar(r, y, width = barWidth, color=color, lw=1.5, ec="white", capsize=7, zorder=12,)
            ax.bar(r, y, width = barWidth, color=color, lw=1.5, ec="white", capsize=7, )
            # ax.plot(r, y, color=color, lw=6, zorder=12,)

            if y_offset is None:
                y_offset = max(Y_range) * 2 / 100
            if b2_y_label_offset and y == C2:
                y_offset += b2_y_label_offset
            if b2_y_label_offset and y == C2:
                y_header_label_delta += b2_x_label_offset
                
            bar_label_color = 'black'
            for index2, (x_pos,y_pos) in enumerate(zip(r,y)):
                y_pos_label = y_pos
                if bar_label_formatter: y_pos_label = bar_label_formatter(y_pos_label)

                if custom_bar_labels is not None:
                    y_pos_label = custom_bar_labels[index][index2]
                    bar_label_color = custom_bar_label_colors
                    
                    ax.text( x_pos  + y_header_label_delta, y_pos + y_offset , y_pos_label, fontweight='bold', color=bar_label_color, fontsize=bar_label_fontsize, ha="left", path_effects=font_path_effects )
                else:
                    ax.text( x_pos  + y_header_label_delta, y_pos + y_offset , y_pos_label, color=bar_label_color, fontsize=bar_label_fontsize, ha="left", path_effects=font_path_effects )
                
                # y_pos = y_pos.__round__(2)
                # y_pos = int( y_pos * 100 ) / 100  # 2.23
    
        ax.xaxis.set_ticks([ r + barWidth/2 for r in range(len(C1))])
        if X_labels is not None :
            if x_label_rotate:
                ax.xaxis.set_ticklabels(X_labels, fontsize=X_label_fontsize, rotation=x_label_rotate)
            else:
                ax.xaxis.set_ticklabels(X_labels, fontsize=X_label_fontsize)
        else:
            ax.xaxis.set_tick_params(labelbottom=False, length=0)
        ax.xaxis.set_tick_params(length=6, width=1.2)
    
    ax.yaxis.set_ticks( Y_range  )
    ax.yaxis.set_ticklabels(Y_range)
    ax.yaxis.set_tick_params(labelleft=False, length=0)
    # Customize y-axis ticks

    # # Make gridlines be below most artists.
    ax.set_axisbelow(True)

    # # Add grid lines
    ax.grid(axis = "y", color="#A8BAC4", lw=1.2)
    # Remove all spines but the one in the bottom
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    if switch_off_yaxis:
        ax.spines["left"].set_visible(False)
        ax.spines["left"].set_linewidth(5)

    # Customize bottom spine
    ax.spines["bottom"].set_lw(1.2)
    ax.spines["bottom"].set_zorder(16)
    ax.spines["bottom"].set_capstyle("butt")
    #  zorder=16
    # Set custom limits
    ax.set_ylim(min(Y_range), max(Y_range))

    x_axis_adjustment_factor = abs(min(r1) - barWidth / 2) * 40/ 100
    # (max(r1) - min(r1)) * 2 / 100
    min_x = min(r1) - barWidth / 2 - x_axis_adjustment_factor
    max_x = max(r1) + barWidth / 2 + x_axis_adjustment_factor
    if C2 == None:
        ax.set_xlim(  min_x, max_x)
    else:
        max_x = max(r2) + barWidth / 2 + x_axis_adjustment_factor
        ax.set_xlim(  min_x, max_x)

    if h_line:
        assert C2 is not None, "Not yet implemented"
        ax.plot([min_x, max_x], [h_line[0], h_line[0]], color=BLUE, lw=5, alpha=0.3, )
        ax.plot([min_x, max_x], [h_line[1], h_line[1]], color=ORANGE, lw=5, alpha=0.3)


        
    if y_axis_labels:
        PAD = 35 * 0.01
        for i,label in enumerate(Y_range_label):
            if type (label) is not str:
                label = label.__round__(2)
            # print(label)
            label_pos =  Y_range[i]
            ax.text( delta, label_pos , str(label),  ha="right", va="baseline", fontsize=Y_label_fontsize, )
    plt.tight_layout()
    plt.savefig(f"{name}.png")
    

#### X = historgrams, [ [Hist 1] , [Hist 2] , ... ]
def two_histograms(X, Y_range=[i * 0.1 for i in range(0, 11, 2)], Y_range_label=[i * 10 for i in range(0, 11, 2)], 
    X_labels = ['CAL', 'BM (Our)', 'RLQ (Our)'], name="gender", delta=-.4, y_header_label_delta=- 0.075, gap_between_bars=2,
    Y_label_fontsize=20, X_label_fontsize=25, bar_label_fontsize=20, enable_line=False, y_offset=None, barWidth = 0.3, figsize=(8, 6), bar_label_formatter=None, 
    COLORS=None, h_line=None, no_x_ticks=10, lw=1.5, bar_opacity=0.5) :
    fig, ax = plt.subplots(figsize=figsize)
    
    # Choose the height of the blue bars
    
    r1 = [ i * (gap_between_bars + barWidth) for i in range( len(X[0]) )]
    
    for y, color in zip(X, COLORS):
        ax.bar(r1, y, width = barWidth, color=color, lw=lw, ec="white", capsize=7, )
