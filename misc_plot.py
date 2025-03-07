import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib as mpl
from colors import LinearSegmentedColormap, sns, ALONE_COLORS, lighten_color, BLUE, ORANGE
from math import pi
from plot_utils import range_calc

# vmin= hardlimit of start range
# vmax= hardlimit of end range
def heatmap_plt(df, name="test", X_label_fontsize=25, figsize=(10, 10), xticklabels= 5, vmin=None, vmax=None,  cmap=None,
    linewidths=.5 , annot=False, fmt=".2f"):
    fig, ax = plt.subplots(figsize=figsize)
    default_size  = plt.rcParams['font.size']
    plt.rcParams.update({'font.size': X_label_fontsize})

    plt.clf()
    if vmin is None and vmax is None :
        sns.heatmap(df, annot=annot, xticklabels=xticklabels, yticklabels=False, cmap=cmap, linewidths=linewidths, fmt=fmt)
    else:
        sns.heatmap(df, annot=annot, xticklabels=xticklabels, yticklabels=False, vmin=vmin, vmax=vmax, cmap=cmap, center = (vmin + vmax)/ 2, linewidths=linewidths, fmt=fmt)

    plt.tight_layout()
    plt.savefig(f"{name}.png")
    plt.rcParams.update({'font.size': default_size})
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
    plt.savefig(f"{name}.png") 

    




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
    plt.savefig(f"{name}.png")
    



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
    plt.savefig(f"{name}.png")
    plt.clf()

