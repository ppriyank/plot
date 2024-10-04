from hist import bar_graph_X_Y, bar_graph_X_Y_Gradient, bar_graph_side_by_side


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
    bar_labels=True, bar_labels_y_offset=0.2, bar_labels_x_offset=0.7, bar_labels_font_size=20, bar_color="black",
    )


Hists = [
    [[0, 1, 2], [42.4, 41.4, 39.6], [1,2,1]],
    [[4, 5, 6, 7, 8], [44.4, 43.1, 40.1, 39.0, 43.1], [3,2,2,1,3]],
    ]


bar_graph_X_Y_Gradient(Hists, name="test_hx_hy_gradient", artificial_darkening=1, decimal_places=0,
    barWidth=0.8, figsize=(6, 6),  x_ticks_allowed=False, bar_opacity=1,
    y_points=2, Y_label_fontsize=25, y_up_offset=1, y_down_offset=10, y_padding_factor=-0.03, switch_off_yaxis=True, 
    X_labels=X_labels, X_labels_pos = X_labels_pos, x_padding_factor=-0.1, x_padding=-0.3,
    bar_labels=True, bar_labels_y_offset=0.2, bar_labels_x_offset=0.6, bar_labels_font_size=18, bar_color="black",
    )



Hists = [
    [42.4, 41.4, 39.6],
    [41.8, 38.8, 40.6],
    [44.4, 39.0, 43.1],
]

bar_graph_side_by_side(Hists, name="test_hist_side", artificial_darkening=1, decimal_places=0,
    barWidth=0.4, gap_between_bars=0.5,  gap_between_groups=1,
    figsize=(6, 6),  x_ticks_allowed=False, bar_opacity=1,  
    y_points=2, Y_label_fontsize=25, y_up_offset=1, y_down_offset=10, y_padding_factor=-0.03, switch_off_yaxis=True, 
    X_labels=X_labels, X_labels_pos = X_labels_pos, x_padding_factor=-0.1, x_padding=-0.09,
    bar_labels=True, bar_labels_y_offset=0.2, bar_labels_x_offset=0.3, bar_labels_font_size=15, bar_color="black",
    )




Hists = [
    [42.4, 41.4, 39.6],
    [41.8, 38.8, 40.6],
]

custom_labels = [
    ["" for i in Hists[0]],
]
diff_array = []
for i in range(len(Hists[0])):
    diff = Hists[1][i] - Hists[0][i] 
    diff_array.append(f"{diff:.1f}")
custom_labels.append(diff_array)    


bar_graph_side_by_side(Hists, name="test_hist_side_diff_labels", artificial_darkening=1, decimal_places=0,
    barWidth=0.4, gap_between_bars=0.5,  gap_between_groups=1,
    figsize=(6, 6),  x_ticks_allowed=False, bar_opacity=1,  
    y_points=2, Y_label_fontsize=25, y_up_offset=1, y_down_offset=10, y_padding_factor=-0.03, switch_off_yaxis=True, 
    X_labels=X_labels, X_labels_pos = X_labels_pos, x_padding_factor=-0.1, x_padding=-0.09,
    bar_labels=custom_labels, bar_labels_y_offset=0.2, bar_labels_x_offset=0.18, bar_labels_font_size=20,
    )



# cd ~/plot/
# python test_hist.py