# plot

Reference : https://python-graph-gallery.com/

## Ussage 
Download the folder in your directory 
```
from plot.colors import ALL_COLORS, lighten_color
current_path = os.getcwd()
sys.path.append(os.path.join(current_path, "plot"))
from plot.hist import bar_graph_X_Y, bar_graph_X_Y_Gradient, bar_graph_side_by_side
```
## Line Plots `test_line.py`

<div style="display: flex; justify-content: space-around;">
  <div>
    <p style="text-align: center;">Simple Line</p>
    <img src="Pictures/test_line.png" alt="Simple Line" style="width: 50%;">    
    <p style="text-align: center;">Line + Shade</p>
    <img src="Pictures/test_shade.png" alt="Line + Shade" style="width: 50%;">    
    <p style="text-align: center;">Multiple Lines</p>
    <img src="Pictures/test_multiple.png" alt="Multiple Lines" style="width: 50%;">    
  </div>
</div>


## Histogram Plots `test_hist.py`

<div style="display: flex; justify-content: space-around;">
  <div>
    <p style="text-align: center;">Simple Hist X Y</p>
    <img src="Pictures/test_hx_hy.png" alt="Hist X Y" style="width: 50%;">
    <p style="text-align: center;">Hist X Y Z (Gradient)</p>
    <img src="Pictures/test_hx_hy_gradient.png" alt="Hist X Y Z" style="width: 50%;">
    <p style="text-align: center;">Multiple Hist Side by Side</p>
    <img src="Pictures/test_hist_side.png" alt="Hist X Y Z" style="width: 50%;">
    <p style="text-align: center;">Relative Comparison</p>
    <img src="Pictures/test_hist_side_diff_labels.png" alt="Hist X Y" style="width: 50%;">
    <p style="text-align: center;">Horizontal Plots</p>
    <img src="Pictures/test_hist_horizontal.png" alt="Hist Hist X Y" style="width: 50%;">
  </div>
</div>



## Scatter Plots `test_scatter.py`

<div style="display: flex; justify-content: space-around;">
  <div>
    <p style="text-align: center;">Scatter Plot</p>
    <img src="Pictures/test_scatter.png" alt="Hist X Y" style="width: 50%;">
  </div>
</div>




## Misc `test_misc.py` : Radar, Word Cloud, Heamtmp


<div style="display: flex; justify-content: space-around;">
  <div>
    <img src="Pictures/test_heatmap.png" alt="Heat map" style="width: 50%;">
    <p style="text-align: center;">Heat Map</p>
  </div>
  <div>
    <img src="Pictures/test_heatmap3.png" alt="Heat map" style="width: 50%;">
    <p style="text-align: center;">Heat Map</p>
  </div>
  <div>
    <img src="Pictures/test_word_cloud.png" alt="Word Cloud" style="width: 50%;">
    <p style="text-align: center;">Word Cloud</p>
  </div>
  <div>
    <img src="Pictures/test_radar2.png" alt="Multiple Lines" style="width: 50%;">
    <p style="text-align: center;">Radar Plot</p>
  </div>
  <div>
    <img src="Pictures/test_radar1.png" alt="Multiple Lines" style="width: 50%;">
    <p style="text-align: center;">Radar Plot2</p>
  </div>
  <div>
    <img src="Pictures/test_box.png" alt="Multiple Lines" style="width: 50%;">
    <p style="text-align: center;">Box Plot (median and qunatile)</p>
    <img src="Pictures/test_box_mean.png" alt="Multiple Lines" style="width: 50%;">
    <p style="text-align: center;">Box Plot (mean and std)</p>
  </div>
</div>

