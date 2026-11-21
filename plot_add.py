from colors_set import * 

def V_line(v_lines=None, Y_values=None, vline_offset=0, ax=None, 
        vline_style="-.",  v_line_alpha=1,  vline_color=RED,  v_line_width=None, v_line_z_oder=9, **unused):
    """Draw vertical reference lines over the supplied y-value range."""
    for v_line in v_lines:            
        ax.plot([v_line, v_line], [min(Y_values) - vline_offset, max(Y_values) + vline_offset], color=vline_color, lw=v_line_width, linestyle=vline_style, alpha=v_line_alpha, zorder=v_line_z_oder)
    return v_lines

def H_line(h_lines=None, X_values=None, hline_offset=0, ax=None, 
        hline_style="-.",  h_line_alpha=1,  hline_color=RED,  h_line_width=None, h_line_z_oder=9, **unused):
    """Draw horizontal reference lines over the supplied x-value range."""
    for h_line in h_lines:            
        ax.plot([min(X_values) - hline_offset, max(X_values) + hline_offset], [h_line, h_line], color=hline_color, lw=h_line_width, linestyle=hline_style, alpha=h_line_alpha, zorder=h_line_z_oder)
    return h_lines

def H_line_Section(h_line_shade=None, X_values=None, hline_offset=0, ax=None, 
        h_line_shade_color=RED,  h_line_shade_color_alpha=0.5, 
        h_line_width=None, hline_style="-.", h_line_alpha=1, **unused):
    """Shade horizontal y-range sections and outline their boundaries."""
    local_vals = []
    shade_colors = h_line_shade_color
    if isinstance(h_line_shade_color, str):
        shade_colors = [h_line_shade_color for i in range(len(h_line_shade))] 
    x_min = min(X_values) - hline_offset
    x_max = max(X_values) + hline_offset
    for h_area, shade_color in zip(h_line_shade, shade_colors):
        local_vals += h_area    
        ax.fill_between([x_min, x_max], h_area[0], h_area[1], color=shade_color, alpha=h_line_shade_color_alpha, zorder=9)
        ax.plot([x_min, x_max], [h_area[0], h_area[0]], color=shade_color, lw=h_line_width, linestyle=hline_style, alpha=h_line_alpha, zorder=9)
        ax.plot([x_min, x_max], [h_area[1], h_area[1]], color=shade_color, lw=h_line_width, linestyle=hline_style, alpha=h_line_alpha, zorder=9)

    return local_vals
    
def V_line_Section(v_line_shade=None, Y_values=None, vline_offset=0, ax=None, 
        v_line_shade_color=RED,  v_line_shade_color_alpha=0.5,
        vline_style="-.",  v_line_alpha=1, v_line_width=None, **unused):
    """Shade vertical x-range sections and outline their boundaries."""
    local_vals = []
    shade_colors = v_line_shade_color
    if isinstance(v_line_shade_color, str):
        shade_colors = [v_line_shade_color for i in range(len(v_line_shade))] 
    y_min = min(Y_values) - vline_offset
    y_max = max(Y_values) + vline_offset    
    for v_area, shade_color in zip(v_line_shade, shade_colors):
        local_vals += v_area    
        ax.fill_betweenx([y_min, y_max], v_area[0], v_area[1], color=shade_color, alpha=v_line_shade_color_alpha, zorder=9)
        ax.plot([v_area[0], v_area[0]], [y_min, y_max], color=shade_color, lw=v_line_width, linestyle=vline_style, alpha=v_line_alpha, zorder=9)
        ax.plot([v_area[1], v_area[1]], [y_min, y_max], color=shade_color, lw=v_line_width, linestyle=vline_style, alpha=v_line_alpha, zorder=9)

    return local_vals

    
        
def plot_background_lines_shades(hline_offset=0, vline_offset=0, ax=None, X_values=None, Y_values=None, line_width=0, line_z_oder=9, **args):
    """Add configured horizontal and vertical lines and shaded sections to a plot."""
    local_Y = []
    local_X = []
    ### plot horizontal_lines
    h_lines  = args.pop('h_lines', None)
    if h_lines:
        local_Y += H_line(ax=ax, h_lines=h_lines, X_values=X_values, hline_offset=hline_offset, h_line_width=args.pop('h_line_width', line_width), h_line_z_oder=line_z_oder, **args)
    
    ### plot veritical
    v_lines  = args.pop('v_lines', None)
    if v_lines:
        local_X += V_line(ax=ax, v_lines=v_lines, Y_values=Y_values, vline_offset=vline_offset,  v_line_width=args.pop('v_line_width', line_width), v_line_z_oder=line_z_oder, **args)
        
    ### plot H-shaded area
    h_line_shade  = args.pop('h_line_shade', None)
    if h_line_shade:
        local_Y += H_line_Section(h_line_shade=h_line_shade, X_values=X_values, hline_offset=hline_offset, ax=ax, h_line_width=args.pop('h_line_width', line_width), **args)
        
    ### plot H-shaded area
    v_line_shade  = args.pop('v_line_shade', None)
    if v_line_shade:
        local_X += V_line_Section(v_line_shade=v_line_shade, Y_values=Y_values, vline_offset=vline_offset, ax=ax, **args)

    return local_X, local_Y
    