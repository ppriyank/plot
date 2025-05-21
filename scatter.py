import matplotlib.pyplot as plt
from colors import * 
from plot_utils import range_calc
from style import simplify

import torch 

def scatter_plt(Points, Labels=None, SIZE=50, COLORS = ALONE_COLORS, #[ORANGE, BLUE, RED, GREEN], 
    figsize=(8, 6), name="test", artificial_darkening=1, decimal_places=1, alpha=1, ec="white", lw=1.5, enable_relabeling=None, 
    y_up_offset=0, y_down_offset=0, Y_label_fontsize=20, y_points=3, y_padding_factor=0, hard_y=None,
    x_up_offset=0, x_down_offset=0, X_label_fontsize=25, x_points=3, x_padding_factor=0, x_padding=0.04, hard_x=None,
    SHAPES = None, strict_order = None, 
    ):

    fig, ax = plt.subplots(figsize=figsize)
    
    if Labels is None:
        Labels = [0 for i in range(len(Points))]
    if type(Labels) == torch.Tensor:
        Labels = Labels.tolist()
    
    print(len(COLORS), len(set(COLORS)), len(set(Labels)))
    if enable_relabeling:
        unique = sorted(set(Labels))
        unique = {e:i for i,e in enumerate(unique)}
        print("NEW LABELS : ", unique)
        Labels= [unique[e] for e in Labels]
    
    
    if len(COLORS) < len(set(Labels)):
        COLORS = ALL_COLORS 
    if len(COLORS) < len(set(Labels)):
        COLORS = ALL_XKCD_COLORS 
    
    
    if artificial_darkening:
        COLORS = [lighten_color(e, amount=artificial_darkening)  for e in COLORS]
    if type(SIZE) == int or len(SIZE) == 1:
        SIZE = [SIZE for i in range(len(Points))]
        SIZE = torch.tensor(SIZE)
    elif type(SIZE)== list:
        SIZE = torch.tensor(SIZE)
    
    
    indices = torch.argsort(SIZE, descending=True)
    SIZE = np.array(SIZE)[indices]
    Points = np.array(Points)[indices]
    Labels = np.array(Labels)[indices]
    if SHAPES is not None:
        SHAPES = np.array(SHAPES)[indices]

    X_pos =  Points[:,0]
    Y_pos = Points[:,1]

    curret_order_of_loop = sorted(set(Labels)) 
    if strict_order is not None:
        curret_order_of_loop = strict_order
    for i,y in enumerate( curret_order_of_loop ):
        # print(i,y, COLORS[i])
        selected_index  = Labels == y
        X, Y = Points[selected_index][:,0], Points[selected_index][:,1]
        size  = SIZE[selected_index]
        y = int(y)
        if SHAPES is not None:
            shape = SHAPES[selected_index]
            if len(set(shape)) == 1:
                shape = shape[0]
                ax.scatter(X, Y, fc=COLORS[i], s=size, zorder=12, ec=ec, lw=lw, alpha=alpha, marker=shape)
            else:
                for s in set(shape):
                    ax.scatter(X[shape == s], Y[shape == s], fc=COLORS[i], s=size[shape == s], zorder=12, ec=ec, lw=lw, alpha=alpha, marker=s)
        else:
            ax.scatter(X, Y, fc=COLORS[i], s=size, zorder=12, ec=ec, lw=lw, alpha=alpha)
            # (0.4562745098039217, 0.2133333333333331, 1.000000000000000)
            # COLORS[i] =[round(e, 15) for e in COLORS[i]]
            # [0.4562745098039217, 0.2133333333333332, 1.0000000000000002]
            # (0.2048179271708681, 0.5431932773109239, 0.9069467787114849)
    
        
    
    if hard_y:
        Y_pos = Y_pos[Y_pos >= (min(hard_y) - y_down_offset) ]
        Y_pos = Y_pos[Y_pos <= (max(hard_y) + y_up_offset) ]

    if hard_x:
        X_pos = X_pos[X_pos >= min(hard_x) + x_down_offset]
        X_pos = X_pos[X_pos <= max(hard_x) - x_up_offset]
    
    Y_range, Y_range_label = range_calc(Y_pos, y_points, y_up_off = y_up_offset , y_down_off=y_down_offset, decimal_places=decimal_places)
    X_range, X_range_label = range_calc(X_pos, x_points, y_up_off = x_up_offset , y_down_off=x_down_offset, decimal_places=decimal_places)

    simplify(ax, Y_range, Y_range_label, X_range, X_range_label, 
        Y_label_fontsize, X_label_fontsize, x_padding=x_padding, 
        y_padding_factor=y_padding_factor, x_padding_factor=x_padding_factor)

    plt.tight_layout()
    plt.savefig(f"{name}.png", dpi=300)
    plt.clf()





