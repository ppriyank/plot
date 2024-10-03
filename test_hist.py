from hist import bar_graph_X_Y


Hists = [
    [[0, 1, 2], [42.4, 41.4, 39.6]],
    [[4, 5, 6, 7, 8], [44.4, 43.1, 40.1, 39.0, 43.1]],
    ]

X_labels = ["Hist A", "Hist B"]
X_labels_pos = [ sum(e[0])/ len(e[0])  for  e  in Hists]

bar_graph_X_Y(Hists, name="test_hx_hy", artificial_darkening=1, decimal_places=0,
    barWidth=0.7, figsize=(6, 6),  x_ticks_allowed=False, bar_opacity=1,
    y_points=2, Y_label_fontsize=25, y_up_offset=1, y_down_offset=10, y_padding_factor=-0.03, switch_off_yaxis=True, 
    X_labels=X_labels, X_labels_pos = X_labels_pos, x_padding_factor=-0.1,
    bar_label_formatter=f":.1f"
    )



# bar_graph_X_Y_Gradient(Hists, name="test_hx_hy", artificial_darkening=1, decimal_places=0,
#     barWidth=0.7, figsize=(6, 6),  x_ticks_allowed=False, bar_opacity=1,
#     y_points=2, Y_label_fontsize=25, y_up_offset=1, y_down_offset=10, y_padding_factor=-0.03,
#     X_labels=X_labels, X_labels_pos = X_labels_pos, switch_off_yaxis=False, x_padding_factor=-0.1,
#     )




quit()
generate_color_gradient(n, colors = plt.cm.coolwarm(np.linspace(0, 1, n)))



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
# python test_hist.py