
import matplotlib as mpl
import matplotlib.pyplot as plt
import torch  
from math import pi

from wordcloud import WordCloud
from colors_set import * 

from plot_utils import create_color_gradient, contrast_ratio
import numpy as np

import networkx as nx
from netgraph import Graph
import pandas as pd 
import random 


##############################################################################
######################## WORD CLOUD 
def word_cloud_plt(
    ax,
    word_cloud_shape = (2000, 3500),
    Nodes=None, # words
    Sizes=None, # Frequency / Size / Count 
    Values=None, # Decide color value 
    
    colors = [ORANGE, BLUE, PINK],
    n_bins=10, 
    scale_factor = 3, # HD-ness
    
    **args,
    ):
    
    fig_H, fig_W = word_cloud_shape
    colors = create_color_gradient(colors, n_bins=n_bins)
    
    wc = WordCloud(background_color='white', 
        colormap=colors,
        width = fig_W, height = fig_H, repeat=False,
        margin=0, 
        prefer_horizontal=0.9,
        relative_scaling=0.4,
        # collocations=False,
        # min_font_size=4,
        scale=scale_factor,
        )


    dict_freq = {}
    for node, size in zip(Nodes, Sizes) :
        dict_freq[node] = size

    wc = wc.generate_from_frequencies(dict_freq)

    #### Custom Colors based on Value     
    if Values:
        maxi, mini = max(Values), min(Values)
        N = int( (maxi - mini + 1)  // 1)
        color_dict ={ }
        for node, value in zip(Nodes, Values) :
            color_dict[node] =  mpl.colors.to_hex ( colors ( (value - mini) / N ) )
        
        layout_ = []
        for e in wc.layout_:
            # print(e)
            e = list(e)
            node = e[0][0]
            old_color = e[4]
            e[4] = color_dict[node]
            # e[4] = old_color
            layout_.append(e)
        wc.layout_ = layout_

    ax.imshow(np.flipud(wc))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    ax.margins(x=0, y=0)
    
    # plt.savefig("test_wordcloud.png", dpi=300)
    # X_values , Y_values 
    return [0, fig_W * scale_factor], [0, fig_H * scale_factor], {}



##############################################################################
######################## RADAR PLOT 
def overide_params(X_labels, Angles, Y_range, Y_values):
    if X_labels:
        X_labels += X_labels[:1]
    else:
        X_labels = Angles

    if Y_range:
        x_axis_pos_offset = min(Y_range)
    else:
        x_axis_pos_offset = min(Y_values)

    return {
        'X_range': Angles, 
        'X_labels': X_labels,
        'x_axis_pos_offset': x_axis_pos_offset, 
        }

# X - axis is angular distance rotating on fixed radius 
# Y - axis Radial Distance from center
def radar_spider_plot(ax,
    Curves=None, 
    Alphas=[], 
        
    colors = [ORANGE, BLUE, PINK],

    curve_line_width=1,
    curve_line_opacity=1,

    switch_off_yaxis=False, ## Radar plot has to plot its own y-axis
    Curves_names = None, ## X axis 
    X_labels = None, 
    Y_range = None, 
    Y_labels = None, 
    
    y_axis_angle=10, 
    y_axis_width=1,

    **args,
    ):
    
    if isinstance(Curves[0], torch.Tensor):
        Curves= [e.tolist() for e in Curves]
    
    N_of_X = len(Curves[0])
    Angles = [n / float(N_of_X) * 2 * pi for n in range(N_of_X)]
    Angles += Angles[:1]
    

    if isinstance(Alphas, int) or isinstance(Alphas, float):
        Alphas = [Alphas for i in Curves]

    X_values = Angles
    Y_values = [0, ]

    ####### Plot Curve 
    for i, curve in enumerate(Curves):
        Y_values += curve
        curve += curve[:1]
        # print(i, len(Angles), len(curve))

        ax.plot(Angles, curve, color=colors[i], linewidth=curve_line_width, linestyle='solid', label=Curves_names[i], alpha=curve_line_opacity, zorder=12)
        ax.fill(Angles, curve, color=colors[i], alpha=Alphas[i], zorder=14)
    

    ####### Plot Y-Axis
    ax.set_rlabel_position(y_axis_angle)
    if not switch_off_yaxis:
        label_angle_rad = np.deg2rad(y_axis_angle - 5)
        ax.plot(
            [label_angle_rad, label_angle_rad],
            [0, max(Y_range)],
            color="black",
            alpha=0.2,
            linewidth=y_axis_width,
            zorder=1,
        )
    
    # plt.savefig("test_radar.png", dpi=300)
    params = overide_params(X_labels.copy() if X_labels else None, Angles, Y_range, Y_values)
    # print(len(params['X_range']), len(params['X_labels']))
    return X_values, Y_values, params
    
    

    
##############################################################################
######################## Network PLOT 
# https://github.com/paulbrodersen/netgraph/blob/master/examples/plot_19_hyperlinks.py
def bin_histogram(data, n_bins, use_log=None):
    if not isinstance(data, torch.Tensor):
        data = torch.tensor(data)

    values = data.detach().cpu().flatten()
    if not values.is_floating_point():
        values = values.to(torch.float32)
    counts, edges = torch.histogram(values, bins=n_bins)
    cluster_ids = torch.bucketize(data, edges[1:])
    # for e in cluster_ids.unique():(cluster_ids==e).sum()
    return cluster_ids
    
def network_bubble_plot(ax, 
    Nodes=None, 
    Sizes=None, 
    Scores=None,
    Values=None,
    Labels =None, 
    n_cluster=None, 

    # Alphas=[],     
    colors = [ORANGE, BLUE, PINK],
    n_bins=10,
    
    node_value_formula=lambda x : x, 
    node_size_formula=lambda x : x,
    node_size_range=(1, 6),  # final netgraph node sizes (min, max) after the formula

    use_bunding=True,
    edges_with_cluster=False, 
    
    node_edge_width=0.1,
    node_edge_color='black',
    node_alpha=1, 
    node_labels_font_size=10,
    node_labels_colors='white',
    color_contrast_ratio_threshold=4.5,  # WCAG AA; below this labels switch to black

    connect_edge_width=0.1,
    connect_edge_alpha=0.1, 
    scale_x = 1, scale_y = 1,

    **args,
    ):


    colors = create_color_gradient(colors, n_bins=n_bins)
    # Convert torch tensors / lists to numpy so dict keys are plain Python
    # values (0-d torch tensors hash by identity, so they never match the
    # graph's node ids and netgraph reports node_size as incomplete).
    def _to_numpy(x):
        if isinstance(x, torch.Tensor):
            return x.detach().cpu().numpy()
        return np.asarray(x)

    Nodes = _to_numpy(Nodes)
    if isinstance(Sizes, (int, float)):
        Sizes = [Sizes for i in Nodes]
    if isinstance(Scores, (int, float)):
        Scores = [Scores for i in Nodes]
    Sizes = _to_numpy(Sizes).tolist()
    Scores = _to_numpy(Scores).tolist()
    if Values is None:
        Values = torch.tensor([0 for i in Nodes])


    ##### Node Size & Colors 
    node_size = {}    
    node_color = {}
    maxi, mini = max(Scores), min(Scores)
    N = int( (maxi - mini + 1)  // 1)
    # netgraph node_size is in 1/100 of axis width (default 3), so rescale the
    # formula output into node_size_range; otherwise huge raw sizes blow up
    # both the bubbles and the label font size (raster overflow on draw).
    raw_sizes = np.array([float(node_size_formula(s)) for s in Sizes])
    lo, hi = node_size_range
    span = raw_sizes.max() - raw_sizes.min()
    if span > 0:
        scaled_sizes = lo + (raw_sizes - raw_sizes.min()) / span * (hi - lo)
    else:
        scaled_sizes = np.full_like(raw_sizes, (lo + hi) / 2)
    for node, size, score in zip(Nodes.tolist(), scaled_sizes.tolist(), Scores):
        node_size[node] = size
        node_color[node] =  mpl.colors.to_hex ( colors ( (score - mini) / N ) )
    
    if Labels is None:
        Labels = bin_histogram(Values, n_cluster, use_log=None)
    Labels = _to_numpy(Labels)

    ########### beatutification 
    graph_style = dict(
        node_color=node_color, 
        node_edge_width=node_edge_width,     
        node_edge_color=node_edge_color,
        node_size = node_size,
        node_alpha=node_alpha,
        edge_width=connect_edge_width,        
        edge_alpha=connect_edge_alpha,        
        node_labels={n: str(n) for n in Nodes.tolist()},  # netgraph wants bool or dict
        node_label_fontdict=dict(
            size=node_labels_font_size, 
            color=node_labels_colors,
        ),
        reduce_edge_crossings=True,   
        scale=(scale_x, scale_y), 
    )
    if use_bunding:
        graph_style['edge_layout'] = 'bundled' # this is where bundling is made possible
    


    ##### Connecting points inside the cluster 
    # can also connect points to other clusters
    FROM = []
    TO = []
    all_nodes = Nodes.tolist()
    node_to_community = dict()
    for bucket in range(n_cluster+1):
        indices = Labels == bucket
        names = Nodes[indices].tolist()
        if names == []:continue 
        # print(bucket, names)
        if use_bunding:
            all_buckets = [e for e in range(n_cluster) if e != bucket]
            all_other_buckets  = [ ]
            for e in all_buckets: 
                index = Labels == e
                nodes = Nodes[index]
                if len(nodes) == 0: continue  # empty bin -> nothing to sample
                all_other_buckets += random.sample(nodes.tolist(), k=1)
        
        for i,name in enumerate(names): 
            node_to_community[name] = bucket 
            if edges_with_cluster:
                FROM +=  [name] * (len(names))
                TO += names
            elif use_bunding:
                FROM +=  [name] * (len(all_other_buckets))
                TO += all_other_buckets
            else:
                all_nodes.remove(name)
                FROM +=  [name] * (len(all_nodes))
                TO += all_nodes

    df = pd.DataFrame({ 'from': FROM, 'to':TO})
    G=nx.from_pandas_edgelist(df, 'from', 'to')

    # Graph(G)
    # nx.draw(G, with_labels=True)
    # plt.savefig("temp.png", dpi=300)

    graph_plot = Graph(G,
      node_layout='community', node_layout_kwargs=dict(node_to_community=node_to_community),
      ax=ax, **graph_style
    )

    ########### Chaning Node fone size and colors
    # Use netgraph's node -> Text mapping (label text is a str, dict keys are not)
    for node_name, text in graph_plot.node_label_artists.items():
        default_font_size = node_labels_font_size
        node_size_local = node_size[node_name]
        text.set_fontsize( node_size_local * default_font_size / 2 )

        node_color_local = node_color[node_name]
        default_label_color = node_labels_colors
        color_contrast_ratio = contrast_ratio(node_color_local, default_label_color)

        if color_contrast_ratio < color_contrast_ratio_threshold :
            text.set_color('black')

    # PLOTS.plot() expects (X_range, Y_range, params) like the other plot fns
    # return list(ax.get_xlim()), list(ax.get_ylim()), {}
    return None, None, {}
           


    
##############################################################################
######################## Sankey PLOT 

def _scale_sankey_flow_width(collection, width):
    for path in collection.get_paths():
        vertices = path.vertices.copy()
        if len(vertices) < 5:
            raise ValueError("Unexpected Sankey flow path; unable to scale its width.")

        lower_end = np.argmax(vertices[1:, 0]) + 1
        lower_indices = np.arange(1, lower_end + 1)
        upper_indices = np.arange(len(vertices) - 2, lower_end + 1, -1)
        if len(lower_indices) != len(upper_indices) or not np.allclose(
            vertices[lower_indices, 0], vertices[upper_indices, 0]
        ):
            raise ValueError("Unexpected Sankey flow path; unable to scale its width.")

        lower_y = vertices[lower_indices, 1]
        upper_y = vertices[upper_indices, 1]
        center_y = (lower_y + upper_y) / 2
        vertices[lower_indices, 1] = center_y + (lower_y - center_y) * width
        vertices[upper_indices, 1] = center_y + (upper_y - center_y) * width
        vertices[0, 1] = vertices[-1, 1] = vertices[upper_indices[0], 1]
        vertices[lower_end + 1, 1] = vertices[upper_indices[-1], 1]
        path.vertices[:] = vertices
    collection.stale = True

def _stack(labels, node_gap, side, weights):
    gap = node_gap * weights.sum()
    positions, bottom = {}, 0
    for label in labels:
        size = weights[side == label].sum()
        positions[label] = {'bottom': bottom, 'size': size}
        bottom += size + gap
    return positions, bottom - gap

def _smooth(values):
    kernel = 0.05 * np.ones(20)
    return np.convolve(np.convolve(values, kernel, mode='valid'), kernel, mode='valid')

    

def Sankey_plot(ax,
    Left=None, Right=None,
    
    left_weights=None, # Size of Label
    right_weights=None, # Size of Label

    left_axis_colors=BLUE,
    right_axis_colors=RED,
    
    flow_width=1,
    labels_font_size=15,
    aspect=20,
    node_gap=0.02,

    gradient=True,
    opacity=1,
    edges=True,
    edge_width=1,
    edgecolor='white',
    edge_alpha=0.6,

    **args
    ):
    """Draw a Sankey diagram (Left -> Right flows) on ``ax``.
    Layout follows pySankey, but everything is drawn on the supplied axis
    (pySankey's ``sankey`` always opens a new figure, so it can't be used with ALL_PLOT).
    flow_width scales ribbon thickness (1 keeps the original width).
    """
    if not np.isfinite(flow_width) or flow_width < 0:
        raise ValueError("flow_width must be a finite, non-negative number.")
    if Left is None or Right is None or len(Left) != len(Right):
        raise ValueError("Left and Right must be given and have the same length.")

    Left, Right = np.asarray(Left), np.asarray(Right)
    left_weights = np.ones(len(Left)) if left_weights is None else np.asarray(left_weights, dtype=float)
    right_weights = left_weights if right_weights is None else np.asarray(right_weights, dtype=float)

    left_labels = np.unique(Left)
    right_labels = np.unique(Right)

    if type(left_axis_colors) is not dict:
        left_axis_colors = {k: left_axis_colors for k in left_labels}
    if type(right_axis_colors) is not dict:
        right_axis_colors = {k: right_axis_colors for k in right_labels}


    # Size represents how big bar of the text is .... 
    # Too many mapping increases the size 
    #### Node positions (stacked bottom -> top with a gap between nodes)
    left_pos, left_top = _stack(left_labels, node_gap, Left, left_weights)
    right_pos, right_top = _stack(right_labels, node_gap, Right, right_weights)
    x_max = max(left_top, right_top) / aspect
    

    #### Nodes + labels
    for label, pos in left_pos.items():
        ax.fill_between([-0.02 * x_max, 0], 2 * [pos['bottom']], 2 * [pos['bottom'] + pos['size']],
                        color=left_axis_colors[label], alpha=0.99, linewidth=0)
        ax.text(-0.05 * x_max, pos['bottom'] + 0.5 * pos['size'], label,
                ha='right', va='center', fontsize=labels_font_size)
    for label, pos in right_pos.items():
        ax.fill_between([x_max, 1.02 * x_max], 2 * [pos['bottom']], 2 * [pos['bottom'] + pos['size']],
                        color=right_axis_colors[label], alpha=0.99, linewidth=0)
        ax.text(1.05 * x_max, pos['bottom'] + 0.5 * pos['size'], label,
                ha='left', va='center', fontsize=labels_font_size)

    # plt.savefig("test_sankey.png", dpi=300)
    #### Flows (smoothed ribbons)
    left_cursor = {k: v['bottom'] for k, v in left_pos.items()}
    right_cursor = {k: v['bottom'] for k, v in right_pos.items()}
    flow_collections, flow_pairs = [], []
    for left in left_labels:
        for right in right_labels:
            mask = (Left == left) & (Right == right)
            if not mask.any():
                continue
            l_w, r_w = left_weights[mask].sum(), right_weights[mask].sum()
            ys_d = _smooth(np.array(50 * [left_cursor[left]] + 50 * [right_cursor[right]]))
            ys_u = _smooth(np.array(50 * [left_cursor[left] + l_w] + 50 * [right_cursor[right] + r_w]))
            left_cursor[left] += l_w
            right_cursor[right] += r_w

            collection = ax.fill_between(np.linspace(0, x_max, len(ys_d)), ys_d, ys_u,
                                         color=left_axis_colors[left], alpha=0.65 * opacity, linewidth=0)
            flow_collections.append(collection)
            flow_pairs.append((left, right))

    ax.axis('off')
    # plt.savefig("test_sankey.png", dpi=300)
    if flow_width != 1:
        for collection in flow_collections:
            _scale_sankey_flow_width(collection, flow_width)

    #### Left -> Right colour gradient clipped to each ribbon
    if gradient:
        x_min, x_lim_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        gradient_values = np.linspace(0, 1, 256).reshape(1, -1)
        for collection, (left, right) in zip(flow_collections, flow_pairs):
            color_map = mpl.colors.LinearSegmentedColormap.from_list(
                "sankey_flow", [left_axis_colors[left], right_axis_colors[right]]
            )
            image = ax.imshow(
                color_map(gradient_values),
                extent=(x_min, x_lim_max, y_min, y_max),
                origin="lower",
                aspect="auto",
                interpolation="bilinear",
                alpha=opacity,
                zorder=collection.get_zorder(),
            )
            image.set_clip_path(collection.get_paths()[0], collection.get_transform())
            collection.set_visible(False)
        # imshow resets limits; restore the Sankey extent
        ax.set_xlim(x_min, x_lim_max)
        ax.set_ylim(y_min, y_max)

    # plt.savefig("test_sankey.png", dpi=300)
    if edges:
        for collection in flow_collections:
            outline = mpl.patches.PathPatch(
                collection.get_paths()[0],
                transform=collection.get_transform(),
                facecolor="none",
                edgecolor=edgecolor,
                linewidth=edge_width,
                zorder=collection.get_zorder() + 1,
                alpha=edge_alpha,
            )
            ax.add_patch(outline)

    # PLOTS.plot() expects (X_range, Y_range, params); None, None skips axis stylizing
    # plt.savefig("test_sankey.png", dpi=300)
    return None, None, {}


