import matplotlib.pyplot as plt


def simplify(ax, Y_range, Y_range_label, X_range, X_range_label, Y_label_fontsize, X_label_fontsize,
    x_padding = 0 , y_padding_factor=0, x_padding_factor=0, x_ticks_allowed=True ):
    
    # Customize y-axis ticks
    ax.yaxis.set_ticks( Y_range )
    ax.yaxis.set_ticklabels( Y_range_label )
    ax.yaxis.set_tick_params(labelleft=False, length=0)
    
    if x_ticks_allowed:
        ax.xaxis.set_ticks(X_range)
        ax.xaxis.set_ticklabels(X_range_label, fontsize=X_label_fontsize)
        ax.xaxis.set_tick_params(length=6, width=1.2)
    else:
        ax.xaxis.set_tick_params(labelbottom=False, length=0)

    # Make gridlines be below most artists.
    ax.set_axisbelow(True)

    # Add grid lines
    ax.grid(axis = "both", color="#A8BAC4", lw=1.2)

    # Remove all spines but the one in the bottom
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Customize bottom spine
    ax.spines["bottom"].set_lw(1.2)
    ax.spines["bottom"].set_capstyle("butt")

    y_max, y_min = max(Y_range), min(Y_range)
    ax.set_ylim(y_min, y_max)

    x_max, x_min = max(X_range), min(X_range)    
    # # Set custom limits
    
    # ax.set_ylim(y_min - y_offset, y_max + y_offset)
    ax.set_xlim(x_min - x_padding, x_max + x_padding)

    # # Add labels for vertical grid lines -----------------------
    # # The pad is equal to 1% of the vertical range (35 - 0)
    PAD = abs(y_max - y_min) * y_padding_factor
    for i, (label_pos, label) in enumerate(zip(Y_range, Y_range_label)):
        ax.text( x_min - x_padding + x_padding_factor, label_pos + PAD, str(label),  ha="right", va="baseline", fontsize=Y_label_fontsize, )
    

# x_padding_factor == position of y axis (& y axis labels) (hortizontal)
# y_padding_factor == position of y axis labels  (veritical)
def simplify_hist(ax, Y_range, Y_range_label, X_range, X_range_label, Y_label_fontsize, X_label_fontsize,
    x_padding = 0 , y_padding_factor=0, x_padding_factor=0, x_ticks_allowed=True , x_min=None, x_max=None, switch_off_yaxis=None,
    switch_off_x_axis=None, x_label_rotate=0, switch_off_xaxis=None, y_padding=0, grid_shape="y", y_label_rotate=0):
    
    # Customize y-axis ticks
    ax.yaxis.set_ticks( Y_range )
    ax.yaxis.set_ticklabels( Y_range_label )
    ax.yaxis.set_tick_params(labelleft=False, length=0)

    if x_ticks_allowed:
        ax.xaxis.set_ticks(X_range)
        ax.xaxis.set_ticklabels(X_range_label, fontsize=X_label_fontsize, rotation=x_label_rotate)
        ax.xaxis.set_tick_params(length=6, width=1.2)
        # Add grid lines
    else:
        ax.xaxis.set_tick_params(labelbottom=False, length=0)
        
        
    # Make gridlines be below most artists.
    ax.set_axisbelow(True)
    
    # Add grid lines

    ax.grid(axis = grid_shape, color="#A8BAC4", lw=1.2)
    # Remove all spines but the one in the bottom
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    if switch_off_yaxis:
        ax.spines["left"].set_visible(False)
    else:
        ax.spines["left"].set_linewidth(1.2)

    # Customize bottom spine
    if switch_off_xaxis:
        ax.spines["bottom"].set_visible(False)
    else:
        ax.spines["bottom"].set_lw(1.2)
        ax.spines["bottom"].set_capstyle("butt")

    # return 
    y_max, y_min = max(Y_range), min(Y_range)
    ax.set_ylim(y_min - y_padding, y_max + y_padding)
    ax.set_xlim(x_min - x_padding, x_max + x_padding)

    # # Add labels for vertical grid lines -----------------------
    # # The pad is equal to 1% of the vertical range (35 - 0)
    
    # plt.savefig(f"test_hx_hy.png")
    PAD = abs(y_max - y_min) * y_padding_factor
    for i, (label_pos, label) in enumerate(zip(Y_range, Y_range_label)):
        ax.text( x_min - x_padding + x_padding_factor, label_pos + PAD, str(label),  ha="right", va="baseline", fontsize=Y_label_fontsize, rotation=y_label_rotate)
        