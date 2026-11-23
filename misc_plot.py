
import matplotlib as mpl
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from colors_set import * 

from plot_utils import range_calc, create_color_gradient


# from colors import LinearSegmentedColormap, sns, ALONE_COLORS, lighten_color, BLUE, ORANGE, generate_color_gradients2
# from math import pi
# from plot_utils import range_calc, binning, contrast_ratio
# import numpy as np 

# import numpy as np
# from matplotlib.colors import TwoSlopeNorm
# from numbers import Integral
# from typing import Literal
# from plot_add import *

# import matplotlib.pyplot as plt

# from plot_add import * 


  


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


    




def radar_spider_plot(X, curve_points, name=None, curve_names =[], figsize=(6,6), 
    artificial_darkening=None, ALPHAs=[], COLORS=ALONE_COLORS, decimal_places=1, alpha=0.1, lw=1, 
    x_axis_allowed=True, X_label_fontsize=10, X_pad=10, outer_circle= True,
    Y_range=None, Y_range_label=None, y_points=3, y_down_offset= 1, y_up_offset=0, y_axis_angle=0, y_axis_allowed = True, Y_font_color="grey", y_font_size=20, y_font_alpha=0.6,
    radar_labels=None, radar_label_formatter=lambda x: f"{x:.1f}", radar_labels_font_size=25, radar_label_offset=10,
    grid_opacity_y=1, grid_opacity_x=1, grid_color_y = "#A8BAC4", grid_color_x = "#A8BAC4",
    y_padding = 0, grid_above=False):
    
    if type(X) != list :
       X = [list(e) for e in X] 
    if curve_names == []:
        curve_names = ["random" for e in X]
        
    plt.clf()
    fig, ax = plt.subplots(figsize=figsize, subplot_kw={'projection': 'polar'})
    
    if artificial_darkening:
        COLORS = [lighten_color(e, amount=artificial_darkening)  for e in COLORS]


    categories = curve_points
    no_of_categories = len(curve_points)
    angles = [n / float(no_of_categories) * 2 * pi for n in range(no_of_categories)]
    angles += angles[:1]

    if ALPHAs == []:
        ALPHAs = [1 for i in X]
    
    Y_pos =[]
    for i,x in enumerate(X):
        Y=x
        Y_pos += Y
        Y += Y[:1]
        print(i, len(angles), len(Y), len(curve_names), len(ALPHAs))
        # print(i, len(COLORS), len(curve_names), COLORS[i], curve_names[i])
        ax.plot(angles, Y, color=COLORS[i], linewidth=lw, linestyle='solid', label=curve_names[i], alpha=ALPHAs[i], zorder=14)
        ax.fill(angles, Y, color= COLORS[i], alpha=alpha, zorder=14)
        if radar_labels == True:
            for ang, val in zip(angles[:-1], Y[:-1]):
                ax.text( ang, val + radar_label_offset, radar_label_formatter(val), ha="center", va="baseline", fontsize=radar_labels_font_size, color=COLORS[i])
                
    if x_axis_allowed:
        ax.xaxis.set_ticks(angles[:-1])
        ax.xaxis.set_ticklabels(curve_points, fontsize=X_label_fontsize)
        ax.xaxis.set_tick_params(pad=X_pad)
        ax.xaxis.set_zorder(12)
    
    if not outer_circle:
        ax.spines['polar'].set_visible(False)

    if Y_range is None :
        Y_range, Y_range_label = range_calc(Y_pos, y_points, y_up_off = y_up_offset , y_down_off=y_down_offset, decimal_places=decimal_places)
        plt.ylim(min(Y_range),  max(Y_range))
    else:
        plt.ylim(min(Y_pos) - y_down_offset,  max(Y_pos) + y_up_offset)

    # ax.set_rlabel_position(y_axis_angle)
    ax.yaxis.set_ticks(Y_range)
    ax.yaxis.set_zorder(12)
    # if y_axis_allowed:
        # ax.yaxis.set_ticklabels(Y_range_label, fontsize=y_font_size , color=Y_font_color, alpha=y_font_alpha, )
    # else:
    ax.yaxis.set_ticklabels([], fontsize=y_font_size , color=Y_font_color, alpha=y_font_alpha, )
    
    if grid_above:
        grid_z_order = 13
    else:
        grid_z_order = 12

    for r, label in zip(Y_range, Y_range_label):
        ax.text(y_axis_angle * pi / 180 , r + y_padding, label,
            fontsize=y_font_size, color=Y_font_color, alpha=y_font_alpha, ha='center', va='center', zorder=grid_z_order + 1)
    
    

    ax.grid(axis = "y", color=grid_color_y, lw=1.2, alpha=grid_opacity_y, zorder=grid_z_order )
    ax.grid(axis = "x", color=grid_color_x, lw=1.2, alpha=grid_opacity_x, zorder=grid_z_order )

    plt.tight_layout()
    plt.savefig(f"{name}.png", dpi=300)
    




# https://github.com/paulbrodersen/netgraph/blob/master/examples/plot_19_hyperlinks.py
# column_to_be_colored  should be between 0 to 1 
def network_bubble(df, column_to_be_binned='Images_log', node_column='Images_log', column_to_be_colored=None, different_size_column=None,
    N_CLUSTERS = 10,  plt_name="test", figsize=(20, 20), COLOR_MAP=None, map_vals_to_colors=True , N_BINS_COLORS = 1000,
    use_bunding=True, edge_width=0.1,   edge_alpha=0.1, node_edge_width=0.1, node_edge_color='black',
    node_size_formula=lambda x :x, 
    node_labels=True, node_labels_font_size=10, node_labels_colors='white', node_alpha=1, 
    edges_with_cluster = True, color_contrast_ratio_threshold= 4.5, 
    scale_x = 1, scale_y = 1):

    import networkx as nx
    from netgraph import Graph
    import pandas as pd 


    ##### Range of values 0 --> white and 1 --> black (intermediate blue)
    if map_vals_to_colors:
        colors = [(0, "white"), (0.5, "#4169E1"), (1, 'black')]
        cmap = generate_color_gradients2(N_BINS_COLORS+1, colors=colors)
        
        color_bucket_column = column_to_be_colored + "_color_bucket"
        df[color_bucket_column] = df[column_to_be_colored] * N_BINS_COLORS  // 1
        df[color_bucket_column] = df[color_bucket_column].astype(int)
    else:
        assert False, "custom Color values not yet tasted...."


    ##### Node Size & Colors 
    node_size = {}    
    node_color = {}
    all_nodes = df[node_column].tolist()
    for name in all_nodes:
        if different_size_column:
            size = df[df[node_column] == name][different_size_column]
        else:
            size = df[df[node_column] == name][column_to_be_binned]
        size = size.item()
        node_size[name] = node_size_formula(size)

        color_index  = df[df[node_column] == name][color_bucket_column]
        color_index = color_index.item()
        node_color[name] = cmap[color_index]
            

    
    ##### Making Clusters of Nodes based on specific column
    bucket_column = column_to_be_binned + '_bucket'
    df[ bucket_column ] = df[column_to_be_binned].apply( binning, 
        **dict(
            n_bins=N_CLUSTERS,
            mini= df[column_to_be_binned].min(),
            maxi=df[column_to_be_binned].max()) 
    )
    
    for cluster in range(N_CLUSTERS+1):
        selected_cluster = df[df[ bucket_column ] == cluster]
        if len(selected_cluster) > 0:
            mini = selected_cluster[column_to_be_binned].min()
            maxi = selected_cluster[column_to_be_binned].max()
            names = selected_cluster[node_column]
            print(cluster, mini, maxi, names.tolist()[:10])
    
    
    ##### Connecting points inside the cluster 
    # can also connect points to other clusters
    FROM = []
    TO = []
    node_to_community = dict()
    all_nodes = df[node_column].tolist()
    for bucket in range(N_CLUSTERS+1):
        names = df[df[bucket_column] == bucket][node_column].tolist()
        print(bucket, names)
        if use_bunding:
            # all_other_buckets = df[df[bucket_column] != bucket][node_column].tolist()
            buckets= df[bucket_column].unique()
            all_other_buckets  = [ ]
            for e in buckets: 
                if e != bucket:
                    # all_other_buckets += df[df[bucket_column] == e].sample(frac=0.25)[node_column].tolist()
                    all_other_buckets += df[df[bucket_column] == e].sample(n=1)[node_column].tolist()
             
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

    plt.clf()
    fig, ax = plt.subplots(figsize=figsize)
    
    # Graph(G)
    # nx.draw(G, with_labels=True)
    # plt.savefig("temp.png", dpi=300)



    ########### beatutification 
    graph_style = dict(
        node_color=node_color, 
        node_edge_width=node_edge_width,     
        node_edge_color=node_edge_color,
        node_size = node_size,
        node_alpha=node_alpha,

        edge_width=edge_width,        
        edge_alpha=edge_alpha,
        
        node_labels=node_labels,  
        node_label_fontdict=dict(
            size=node_labels_font_size, 
            color=node_labels_colors,
            # rotation=20,
        ),

        reduce_edge_crossings=True,   
        ## size of node (larger number means smaller nodes)
        scale=(scale_x, scale_y), 
    )

    if use_bunding:
        graph_style['edge_layout'] = 'bundled' # this is where bundling is made possible
    
    
    graph_plot = Graph(G,
      node_layout='community', node_layout_kwargs=dict(node_to_community=node_to_community),
      ax=ax,
      **graph_style
    )

    ########### Chaning Node fone size and colors
    for i,e in enumerate(ax._children):
        if type(e) == mpl.text.Text:
            node_name = e.get_text()

            default_font_size = node_labels_font_size
            node_size_local = node_size[node_name]
            ax._children[i].set_fontsize( node_size_local * default_font_size / 2 )

            node_color_local = node_color[node_name]
            default_label_color = node_labels_colors
            color_contrast_ratio = contrast_ratio(node_color_local, default_label_color)

            if color_contrast_ratio < color_contrast_ratio_threshold :
                ax._children[i].set_color('black')
            
           
           
    
    plt.tight_layout()
    plt.savefig(f"{plt_name}.png", dpi=300)
    plt.clf()


    

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


def Sankey_web(df, figsize=None, 
    name="test", 
    left_axis=None, right_axis=None, 
    labels_font_size=15,
    gradient=False, edges=True, edge_width=0.75, edgecolor='black',  
    left_axis_colors='black', right_axis_colors='blue', 
    edge_alpha=0.5, opacity=1, flow_width=0.5,
    ):
    """Create a Sankey plot; flow_width scales ribbon thickness (1 keeps the original width)."""
    if not np.isfinite(flow_width) or flow_width < 0:
        raise ValueError("flow_width must be a finite, non-negative number.")

    import pandas as pd
    from pySankey.sankey import sankey
    # python -m pip install pySankey

    left_labels = pd.unique(df[left_axis])
    right_labels = pd.unique(df[right_axis])
    
    if type(left_axis_colors) is not dict:
        left_axis_colors = {k:left_axis_colors for k in left_labels}
    if type(right_axis_colors) is not dict:
        right_axis_colors = {k:right_axis_colors for k in right_labels}
        
    Dummy_colors = {k:'blue' for k in set(left_labels).union(right_labels)}
    
    sankey(df[left_axis], df[right_axis], aspect=20, colorDict=Dummy_colors, fontsize=labels_font_size)
    plot_ax = plt.gca()
    if figsize:
        plot_ax.figure.set_size_inches(figsize, forward=True)
    node_count = len(left_labels) + len(right_labels)
    flow_collections = list(plot_ax.collections[node_count:])

    flow_pairs = [
            (left, right) for left in left_labels for right in right_labels if ((df[left_axis] == left) & (df[right_axis] == right)).any()
    ]

    assert len(flow_collections) == len(flow_pairs), "Unable to apply Sankey gradients: unexpected number of flow artists."
    if flow_width != 1:
        for collection in flow_collections:
            _scale_sankey_flow_width(collection, flow_width)

    if gradient:
        node_collections = plot_ax.collections[:node_count]
        for collection, label in zip(node_collections[:len(left_labels)], left_labels):
            collection.set_facecolor(left_axis_colors[label])
            collection.set_edgecolor(left_axis_colors[label])
        for collection, label in zip(node_collections[len(left_labels):], right_labels):
            collection.set_facecolor(right_axis_colors[label])
            collection.set_edgecolor(right_axis_colors[label])

        x_min, x_max = plot_ax.get_xlim()
        y_min, y_max = plot_ax.get_ylim()
        gradient_values = np.linspace(0, 1, 256).reshape(1, -1)

        for collection, (left, right) in zip(flow_collections, flow_pairs):
            color_map = mpl.colors.LinearSegmentedColormap.from_list(
                "sankey_flow", [left_axis_colors[left], right_axis_colors[right]]
            )
            image = plot_ax.imshow(
                color_map(gradient_values),
                extent=(x_min, x_max, y_min, y_max),
                origin="lower",
                aspect="auto",
                interpolation="bilinear",
                alpha=opacity,
                zorder=collection.get_zorder(),
            )
            image.set_clip_path(
                collection.get_paths()[0], collection.get_transform()
            )
    
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
            plot_ax.add_patch(outline)
            collection.remove()
            
    plt.tight_layout()
    plt.savefig(f"{name}.png", dpi=300)
    plt.clf()


    
             
