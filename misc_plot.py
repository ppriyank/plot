import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib as mpl
from colors import LinearSegmentedColormap, sns, ALONE_COLORS, lighten_color, BLUE, ORANGE, generate_color_gradients2
from math import pi
from plot_utils import range_calc, binning, contrast_ratio
import numpy as np 

# vmin= hardlimit of start range
# vmax= hardlimit of end range
#### selective coloring of columns : mask (column index)
def heatmap_plt(df, name="test", figsize=(10, 10), xticklabels= 5, vmin=None, vmax=None,  cmap=None, yticklabels=False, center=None, 
    x_label_rotate=0, y_label_rotate=0, X_label_fontsize=25,  Y_label_fontsize=25, x_label_dist=0, y_label_dist=5, 
    color_bar_labels=None, color_bar_labels_range=None, color_label_fontsize=20, color_label_rotate=0, 
    grid_color='white', grid_alpha=1, ann_size=20, grid_width=.5 , annot=False, fmt=".2f", mask=False):
    fig, ax = plt.subplots(figsize=figsize)

    plt.clf()
    if center is None:
        center = (vmin + vmax)/ 2

    if x_label_dist is None:
        x_label_dist = [0 for _ in range(len(df.columns))]
    elif type(x_label_dist) != list:
        x_label_dist = [x_label_dist for _ in range(len(df.columns))]
        
    if y_label_dist is None :
        y_label_dist = [0 for _ in range(len(df.index))]
    elif type(y_label_dist) != list:
        y_label_dist = [y_label_dist for _ in range(len(df.index))]
    
    
    if vmin is None and vmax is None :
        ax = sns.heatmap(df, annot=annot, xticklabels=xticklabels, yticklabels=yticklabels, cmap=cmap, fmt=fmt,  annot_kws={"size": ann_size})
    elif mask is not False:
        mask_column = np.ones_like(df, dtype=bool)
        mask_column[:, 2] = False # Apply colormap to column 'C'
        ax = sns.heatmap(df, annot=annot, xticklabels=xticklabels, yticklabels=yticklabels, vmin=vmin, vmax=vmax, cmap=cmap, center = center, fmt=fmt, annot_kws={"size": ann_size}, mask=mask_column)
        sns.heatmap(df, annot=annot, xticklabels=xticklabels, yticklabels=yticklabels, vmin=vmin, vmax=vmax, cmap='gray', center = center, fmt=fmt, annot_kws={"size": ann_size}, mask=~mask_column, ax=ax, cbar=False)
    else:
        ax = sns.heatmap(df, annot=annot, xticklabels=xticklabels, yticklabels=yticklabels, vmin=vmin, vmax=vmax, cmap=cmap, center = center, fmt=fmt, annot_kws={"size": ann_size})

    # # Turn off the axis spines
    # ax.spines['top'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    
    if color_bar_labels is not None:
        if color_bar_labels_range == None:
            color_bar_labels_range = color_bar_labels
        # Get the colorbar
        colorbar = ax.collections[0].colorbar
        # Set custom labels for the colorbar
        colorbar.set_ticks(color_bar_labels_range)
        colorbar.set_ticklabels(color_bar_labels, fontsize=color_label_fontsize, rotation=color_label_rotate)
        # # Set the label for the colorbar
        # colorbar.set_label('Custom Label')
        
        
    for x_ticks in ax.get_xticklabels():
        x_ticks.set_size(X_label_fontsize)
        x_ticks.set_rotation(x_label_rotate)
    
    for i, label in enumerate(ax.get_xticklabels()):
        label.set_position((label.get_position()[0], label.get_position()[1] - x_label_dist[i] ))

    
    
    # # Add horizontal grid lines with custom opacity
    for y in range(1, len(df.index) ):
        ax.hlines(y, xmin=0, xmax=len(df.columns), color=grid_color, alpha=grid_alpha, linewidth=grid_width)
    # x axis 
    ax.hlines(len(df.index) , xmin=0, xmax=len(df.columns), color='black', alpha=grid_alpha, linewidth=1.2, zorder=12)
    
    for x in range(1, len(df.columns) ):
        ax.vlines(x, ymin=0, ymax=len(df.index), color=grid_color, alpha=grid_alpha, linewidth=grid_width)
    
    # y axis 
    ax.vlines(0, ymin=0, ymax=len(df.index), color='black', alpha=grid_alpha, linewidth=1.2, zorder=12)
    
    for y_ticks in ax.get_yticklabels():
        y_ticks.set_size(Y_label_fontsize)
        y_ticks.set_rotation(y_label_rotate)
    
    
    for i, label in enumerate(ax.get_yticklabels()):
        label.set_position((label.get_position()[0], label.get_position()[1] - y_label_dist[i] ))


    ax.set_xlabel('')
    ax.set_ylabel('')
    
    plt.tight_layout()
    plt.savefig(f"{name}.png", dpi=300)
    plt.clf()




def word_cloud_plt(X, SIZE, COLOR_INDEX, COLORS=None, figsize=(500,500), colors_template=None, name="temp"):
    plt.clf()
    fig_H, fig_W = figsize
    
    maxi, mini = max(COLOR_INDEX), min(COLOR_INDEX)
    N = int( (maxi - mini + 1)  // 1)

    if COLORS:
        colors_template = LinearSegmentedColormap.from_list('custom_gradient', COLORS, N=N)
    else:
        colors_template = LinearSegmentedColormap.from_list('custom_gradient', ['#18aef5', '#000080', '#000000'], N=N)
    
    colors = [colors_template(i/N) for i in range(N)]

    dict_freq = {}
    colors_freq = {}
    for data_name,size,n_c in sorted(list(zip(X, SIZE, COLOR_INDEX)), key=lambda x : -x[1]):
        dict_freq[data_name] = size
        colors_freq[data_name] = mpl.colors.to_hex(colors[n_c - mini])
    
    
    wc = WordCloud(background_color='white', colormap = 'binary',
        width = fig_W, height = fig_H, repeat=False)
    wc = wc.generate_from_frequencies(dict_freq)

    layout_ = []
    for e in wc.layout_:
        e = list(e)
        e[4] = colors_freq[e[0][0]]
        layout_.append(e)

    wc.layout_ = layout_
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{name}.png", dpi=300) 

    




def radar_spider_plot(X, curve_points, name=None, curve_names =[], figsize=(6,6), 
    artificial_darkening=None, ALPHAs=[], COLORS=ALONE_COLORS, decimal_places=1, alpha=0.1, lw=1, 
    x_axis_allowed=True, X_label_fontsize=10, X_pad=10, outer_circle= True,
    Y_range=None, Y_range_label=None, y_points=3, y_down_offset= 1, y_up_offset=0, y_axis_angle=0, y_axis_allowed = True, Y_font_color="grey", y_font_size=20,
    ):
    
    if type(X):
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
        print(len(angles), len(Y), len(curve_names), len(ALPHAs))
        ax.plot(angles, Y, color=COLORS[i], linewidth=lw, linestyle='solid', label=curve_names[i], alpha=ALPHAs[i])
        ax.fill(angles, Y, color= COLORS[i], alpha=alpha)
    
    if x_axis_allowed:
        ax.xaxis.set_ticks(angles[:-1])
        ax.xaxis.set_ticklabels(curve_points, fontsize=X_label_fontsize)
        ax.xaxis.set_tick_params(pad=X_pad)
        ax.xaxis.set_zorder(12)

    if not outer_circle:
        ax.spines['polar'].set_visible(False)
    
    ax.set_rlabel_position(y_axis_angle)
    if Y_range is None :
        Y_range, Y_range_label = range_calc(Y_pos, y_points, y_up_off = y_up_offset , y_down_off=y_down_offset, decimal_places=decimal_places)
        plt.ylim(min(Y_range),  max(Y_range))
    else:
        plt.ylim(min(Y_pos) - y_down_offset,  max(Y_pos) + y_up_offset)

    if y_axis_allowed:
        ax.yaxis.set_ticks(Y_range)
        ax.yaxis.set_ticklabels(Y_range_label, fontsize=y_font_size , color=Y_font_color, alpha=0.6, )
        ax.yaxis.set_zorder(12)
    else:
        ax.yaxis.set_ticks(Y_range)
        ax.yaxis.set_ticklabels([], fontsize=y_font_size , color=Y_font_color, alpha=0.6, )
        ax.yaxis.set_zorder(12)

    
    ax.grid(axis = "y", color="#A8BAC4", )

    plt.tight_layout()
    plt.savefig(f"{name}.png", dpi=300)
    



def box_plt(df, name="test", width=0.6, X_label_fontsize=25, figsize=(10, 10), cmap=None,
    linewidths=.5 , decimal_places=1, COLOR= ALONE_COLORS,
    y_points=3, y_up_offset=0, y_down_offset=0, y_font_size=20, use_mean=None,
    x_padding_factor=0.5, ):
    
    plt.clf()
    fig, ax = plt.subplots(figsize=figsize)
    
    COLORS = {e:COLOR[i] for i,e in enumerate(df["X"].unique())}
    
    

    if not use_mean:
        boxplot = sns.boxplot(x="X", y="Y",  data=df, palette=COLORS, width=width)
        boxplot.set_xticklabels(boxplot.get_xticklabels(), fontsize=X_label_fontsize)
        boxplot.set(xlabel='', ylabel="")
    else:
        # Calculate mean and standard deviation
        means = df.groupby('X')['Y'].mean()
        stds = df.groupby('X')['Y'].std()
        # Overlay mean and standard deviation
        for i, day in enumerate(means.index):
            plt.scatter(i, means[day], color=COLOR[i], marker='o', s=500, label='Mean' if i == 0 else "", zorder=12)
            plt.errorbar(i, means[day], yerr=stds[day], fmt='none', color="black", capsize=12, lw=2)
        ax.xaxis.set_ticks(range(len(means.index)))
        ax.xaxis.set_ticklabels(means.index, fontsize=X_label_fontsize)
        ax.xaxis.set_zorder(12)
        plt.xlim(0 - x_padding_factor,  len(means.index) -1 + x_padding_factor)

    

    Y_range, Y_range_label = range_calc(df["Y"].tolist(), y_points, y_up_off = y_up_offset , y_down_off=y_down_offset, decimal_places=decimal_places)
    plt.ylim(min(Y_range),  max(Y_range))
    ax.yaxis.set_ticks(Y_range)
    ax.yaxis.set_ticklabels(Y_range_label, fontsize=y_font_size)
    ax.yaxis.set_zorder(12)

    ax.set_axisbelow(True)
    ax.grid(axis = "both", color="#A8BAC4", lw=1.2)

    plt.tight_layout()
    plt.savefig(f"{name}.png", dpi=300)
    plt.clf()



# https://github.com/paulbrodersen/netgraph/blob/master/examples/plot_19_hyperlinks.py
# column_to_be_colored  should be between 0 to 1 
def network_plt(df, column_to_be_binned='Images_log', node_column='Images_log', column_to_be_colored=None, different_size_column=None,
    N_CLUSTERS = 10,  plt_name="test", figsize=(20, 20), COLOR_MAP=None, map_vals_to_colors=True , N_BINS_COLORS = 1000,
    use_bunding=True, edge_width=0.1,   edge_alpha=0.1, node_edge_width=0.1, node_edge_color='black',
    node_size_formula=lambda x :x, 
    node_labels=True, node_labels_font_size=10, node_labels_colors='white',
    edges_with_cluster = True, color_contrast_ratio_threshold= 4.5
    ):

    
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
        node_alpha=0.95,

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
        # scale=(2, 2), 
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


    

             
