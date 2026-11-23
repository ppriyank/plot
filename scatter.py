import matplotlib.pyplot as plt
from colors_set import * 
from plot_add import * 
import torch 
import numpy as np 

def convert_to_tensor(x, Points=None, default_value=0, dtype=None):
    if x is None:
        x = [default_value for i in Points]
    if dtype is 'numpy':
        x = np.array(x)
        return x

    if type(x) != torch.Tensor:
        x = torch.tensor(x)
    return x




def scatter_plt(ax=None,
    Points=None, Labels=None, Sizes=50, Shapes='o', 
    colors = [ORANGE, BLUE, PINK],  
    scatter_boder=1.5,
    scatter_boder_color='white', 
    scatter_alpha=1, 

    vline_offset = 10,
    hline_offset = 10,
    line_width=1,
    
    enable_relabeling=None,     
    **args
    ):

    Points = convert_to_tensor(Points)
    Labels = convert_to_tensor(Labels, Points) ### Process labels
    unique_labels = sorted(Labels.unique())
    Sizes = convert_to_tensor(Sizes) ### Process Sizes
    
    
    ### Process Colors 
    # More colors if # labels > colors 
    if isinstance(colors, str):
        colors  = {e.item(): colors for i,e in enumerate(unique_labels)}
    if len(colors) < len(unique_labels):
        colors = ALL_XKCD_COLORS 
    if isinstance(colors, list):
        colors  = {e.item(): colors[i] for i,e in enumerate(unique_labels)}
    assert isinstance(colors, dict), "Colors should be dictionary of label = colors" 
    
    ### Process Shape
    if isinstance(Shapes, str):
        Shapes  = {e.item(): Shapes for i,e in enumerate(unique_labels)}
    elif isinstance(Shapes, list):
        Shapes  = {e.item(): Shapes[i] for i,e in enumerate(unique_labels)}
    
    assert isinstance(Shapes, dict), "Shapes should be dictionary of label = shape" 

    if enable_relabeling:
        unique_labels = {e.item():i for i,e in enumerate(unique_labels)}
        print("NEW LABELS : ", unique_labels)
        Labels= [unique_labels[e.item()] for e in Labels]
        Labels = convert_to_tensor(Labels) 
        colors = {unique_labels[key.item()]: colors[key] for key in unique_labels}
        Shapes = {unique_labels[key.item()]: Shapes[key] for key in unique_labels}

    
    indices = torch.argsort(Sizes, descending=True)
    Sizes = Sizes[indices]
    Points = Points[indices]
    Labels = Labels[indices]
    
    X_values = [Points[:,0].max(), Points[:,0].min() ]
    Y_values = [Points[:,1].max(), Points[:,1].min() ]
    
    
    for label in Labels.unique():
        indices = Labels == label
        X, Y = Points[indices][:,0], Points[indices][:,1]
        size  = Sizes[indices]
        shape = Shapes[label.item()]
        ax.scatter(X, Y, fc=colors[label.item()], s=size, zorder=12, ec=scatter_boder_color, lw=scatter_boder, alpha=scatter_alpha, marker=shape)

    local_X, local_Y = plot_background_lines_shades(hline_offset=hline_offset, vline_offset=vline_offset, ax=ax, X_values=X_values, Y_values=Y_values, line_width=line_width, **args)
    # Y_values += local_Y
    # X_values += local_X

    return X_values, Y_values, {}