import matplotlib.pyplot as plt
from colors_set import * 
from plot_add import * 

def line_plot(ax=None,
    Lines=None, 
    colors = [ORANGE, BLUE, PINK],  
    swap_axis=None, 
    vline_offset = 10,
    hline_offset = 10,

    line_width=5, 
    alpha_line=1, 
    
    use_scatter=True, 
    scatter_size=50, 
    scatter_boder=1.5,
    scatter_boder_color=None, 
    scatter_alpha=1, 

    shade=False, 
    shade_up=None,
    shade_down=None,
    shade_line_width = 2,  
    shade_alpha=0.5, 
    shade_darkening=1, 
        
    error_bar=None, 
    error_std=None, 
    error_darkening=0.5, 
    error_bar_color='black',
    error_bar_width = 1, 
    error_alpha=0.5, 

    **args
    ):

    assert len(colors) >= len(Lines), "COLORS < LINES (not all lines will be plotted"
    X_values = [] 
    Y_values = []

    ### plot line 
    for (X, Y), color in zip(Lines, colors):
        if swap_axis:
            X, Y = Y, X
        X_values += X
        Y_values += Y
        ax.plot(X, Y, color=color, lw=line_width, alpha=alpha_line, zorder=13)

    ### plot scatter
    if use_scatter:
        for (X, Y), color in zip(Lines, colors):
            if swap_axis:
                X, Y = Y, X
            ax.scatter(X, Y, fc=color, s=scatter_size, lw=scatter_boder, ec=scatter_boder_color, zorder=14, alpha=scatter_alpha, )

    ### error_bar plots line and error 
    if error_bar:
        if error_bar_color is None :
            error_bar_colors = [lighten_color(e, amount=error_darkening)  for e in colors]
        else:
            error_bar_colors = [lighten_color(error_bar_color, amount=error_darkening)  for e in error_std]
        for X_Y, X_E, error_color in zip(Lines, error_std, error_bar_colors):
            assert X_Y[0] == X_E[0]
            X = X_Y[0]
            Y = X_Y[1]
            std = X_E[1]

            Y_max = [(a+b) for a,b in zip(Y, std)]
            Y_min = [(a-b) for a,b in zip(Y, std)]
            
            if swap_axis:    
                X_values += Y_max
                X_values += Y_min
                plt.errorbar(Y,X, xerr=std, fmt='none', color=error_color, capsize=12, lw=error_bar_width, alpha=error_alpha)
            else:
                Y_values += Y_max
                Y_values += Y_min
                plt.errorbar(X, Y, yerr=std, fmt='none', color=error_color, capsize=12, lw=error_bar_width, alpha=error_alpha)
                
                
    ### plot shades
    if shade:
        shade_colors = [lighten_color(e, amount=shade_darkening)  for e in colors]
        for y_max, y_min, shade_color in zip(shade_up, shade_down, shade_colors):
            assert y_max[0] == y_min[0]
            X = y_max[0]
            y_up = y_max[1]
            y_down = y_min[1]
            
            if swap_axis:
                X_values += y_up 
                X_values += y_down
                # y, xmin , xmax
                ax.fill_betweenx(X, y_down, y_up, color=shade_color, alpha=shade_alpha, zorder=12, ec="white", lw=shade_line_width)
            else:
                Y_values += y_up 
                Y_values += y_down
                # x, ymin , ymax
                ax.fill_between(X, y_down, y_up, color=shade_color, alpha=shade_alpha, zorder=12, ec="white", lw=shade_line_width)



    local_X, local_Y = plot_background_lines_shades(hline_offset=hline_offset, vline_offset=vline_offset, ax=ax, X_values=X_values, Y_values=Y_values, line_width=line_width, **args)
    Y_values += local_Y
    X_values += local_X

      
    # plt.savefig("test_line.png", dpi=300)
    return X_values, Y_values, {}
    
    
  