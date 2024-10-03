from line import line_plot, line_shade_plot

Y = [42.4, 41.4, 39.6, 38.4]
X = [0, 1, 2, 3]

Lines = [[X, Y]]
X_labels = ['[0]','[5]', '[8]', '[11]']
H_line = [38.0]


line_plot(Lines, 
    figsize=(6, 6), name="test", artificial_darkening=1,
    line_width=5, alpha_line=1, decimal_places=0,
    h_lines=H_line, hline_style="-", h_line_alpha=1, 
    y_padding_factor=-0.0, y_points=2, Y_label_fontsize=25, y_up_offset=0.5, y_down_offset=0.5,
    X_labels=X_labels, X_labels_pos = X, X_label_fontsize=25, x_padding_factor=-0.04, x_padding=0.08,
    use_scatter=True, scatter_size=300,
    )

X = [0, 1, 2, 3]

Y_max = [42.4, 41.4, 39.6, 38.4]
Y_min = [42, 39.8, 38, 38]
Y_min_mean = [(a + b)/2 for a,b in zip(Y_max, Y_min)]
Lines = [[X, Y_max, Y_min_mean, Y_min]]

Y_max = [44.4, 43.1, 40.1, 39.0]
Y_min = [44, 42.7, 38, 37]
Y_min_mean = [(a + b)/2 for a,b in zip(Y_max, Y_min)]
Lines += [[X, Y_max, Y_min_mean, Y_min]]


line_shade_plot(Lines, 
    figsize=(6, 6), name="test_shade", artificial_darkening=1,
    line_width=5, alpha_line=0.2, decimal_places=0,
    h_lines=None, 
    y_padding_factor=-0.0, y_points=2, Y_label_fontsize=25, y_up_offset=0.5, y_down_offset=0.5,
    X_labels=X_labels, X_labels_pos = X, X_label_fontsize=25, x_padding_factor=-0.04, x_padding=0.1,
    use_scatter=True, scatter_size=300, artificial_light=1.1
    )




# cd ~/plot/
# python test.py