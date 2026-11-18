import matplotlib.pyplot as plt
from colors import *
from inspect import signature
from plot_utils import range_calc
from style import simplify
from typing import Literal

class ALL_PLOT:
    """Class-based entry point for the plotting helpers in this package."""  # Provides shared setup and dispatch for every plot type.

    PLOT_METHODS = {
        # Map plot names and aliases to the class methods that implement them.
        "line": "line_plot",
        
    
        "bar": "bar_graph_X_Y",
        "histogram": "bar_graph_X_Y",
        "bar_graph_x_y": "bar_graph_X_Y",
        "gradient_histogram": "bar_graph_X_Y_Gradient",
        "bar_graph_x_y_gradient": "bar_graph_X_Y_Gradient",
        "side_by_side": "bar_graph_side_by_side",
        "bar_graph_side_by_side": "bar_graph_side_by_side",
        "horizontal_bar": "bar_graph_horizontal",
        "bar_graph_horizontal": "bar_graph_horizontal",
        "horizontal_stacked_bar": "bar_graph_horizontal2",
        "bar_graph_horizontal2": "bar_graph_horizontal2",
        "scatter": "scatter_plt",
        "scatter_plt": "scatter_plt",
        "heatmap": "heatmap_plt",
        "heatmap_plt": "heatmap_plt",
        "word_cloud": "word_cloud_plt",
        "word_cloud_plt": "word_cloud_plt",
        "radar": "radar_spider_plot",
        "radar_spider_plot": "radar_spider_plot",
        "box": "box_plt",
        "box_plt": "box_plt",
        "network_bubble": "network_bubble",
        "sankey": "Sankey_web",
        "sankey_web": "Sankey_web",
    }

    def __init__(self, figsize=(8, 6),  # Figure width and height in inches.
        name=None,  # Default base name for the saved PNG file.
        colors=None,  # Default color or mapping used to draw plot elements.
        artificial_darkening=1,  # Adjusts the darkness of supplied colors.
        decimal_places=1,  # Sets decimal precision for generated axis labels.
        y_points = 2, x_points = 2,  # Set the number of generated tick points on each axis.
        y_up_offset=0, y_down_offset=0,x_up_offset=0, x_down_offset=0,  # Extend or contract axis ranges around the data.

        grid_shape='both', grid_opacity=1, grid_color="#A8BAC4",  # Configure grid visibility, transparency, and color.
        switch_off_yaxis=False, switch_off_xaxis=False,  # Hide individual axis spines when enabled.
        y_axis_width=1.2, x_axis_width=1.2,  # Set the line width of the visible axis spines.
        y_ticks_allowed=True, x_ticks_allowed=True,  # Enable or disable tick labels on each axis.
        Y_label_fontsize=20, X_label_fontsize=25,  # Set axis tick-label font sizes.
        Y_label_rotate=0, X_label_rotate =0 ,  # Rotate axis tick labels by these angles.

        x_axis_pos_offset=0.1, y_axis_pos_offset=0.1,  # Add padding outside calculated axis limits.
        **kwargs):  # Extra plot, setup, or save options forwarded to plot helpers.
        # Store class-wide defaults used by setup and styling methods.
        
        self.figsize = figsize
        self.name = name
        self.defaults = kwargs
        self.fig = None
        self.ax = None


        self.colors = colors
        self.artificial_darkening = artificial_darkening

        #### Axis formatting 
        self.switch_off_yaxis = switch_off_yaxis
        self.switch_off_xaxis = switch_off_xaxis
        self.y_axis_width = y_axis_width
        self.x_axis_width = x_axis_width

        self.y_ticks_allowed = y_ticks_allowed
        self.x_ticks_allowed = x_ticks_allowed
        
        self.Y_label_fontsize = Y_label_fontsize
        self.X_label_fontsize = X_label_fontsize

        self.Y_label_rotate = Y_label_rotate
        self.X_label_rotate = X_label_rotate

        self.y_points = y_points
        self.x_points = x_points
        
        self.decimal_places = decimal_places
        self.grid_shape = grid_shape
        self.grid_opacity = grid_opacity
        self.grid_color = grid_color

        #### Axis Manipulate 
        self.y_up_offset = y_up_offset
        self.y_down_offset = y_down_offset
        self.x_up_offset = x_up_offset
        self.x_down_offset = x_down_offset

        self.x_axis_pos_offset = x_axis_pos_offset
        self.y_axis_pos_offset = y_axis_pos_offset

        self.kwargs = kwargs


    def basic_setup(self, **kwargs):
        # Create the Matplotlib figure and axes, optionally overriding the default size.
        figsize = kwargs.get('figsize', self.figsize)
        self.fig, self.ax = plt.subplots(figsize=figsize or self.figsize)
        return self.fig, self.ax

    def fix_colors(self, **kwargs):
        # Normalize colors and apply the configured darkness adjustment.
        colors = kwargs.get('colors', self.colors)
        artificial_darkening = kwargs.get('artificial_darkening', self.artificial_darkening)

        if isinstance(colors, dict):
            return {
                key: lighten_color(color, amount=artificial_darkening)
                for key, color in colors.items()
            }
        if isinstance(colors, str):
            return lighten_color(colors, amount=artificial_darkening)
        return [
            lighten_color(color, amount=artificial_darkening)
            for color in colors
        ]

    def style_grid(
        self,
        grid_shape: Literal["both", "xy", "x", "y"],  # Choose which axes receive grid lines.
        grid_opacity=1,  # Set grid-line transparency.
        switch_off_yaxis=False,  # Hide the left y-axis spine.
        switch_off_xaxis=False,  # Hide the bottom x-axis spine.
        grid_color=None,  # Set the grid-line color.
    ):
        # Configure grid lines and hide or style the visible axis spines.
        # Add grid lines
        if grid_shape == 'xy':
            grid_shape = 'both'
        
        if grid_shape == None:
            grid_shape = 'both'
            grid_opacity = 0 

        
        self.ax.grid(axis = grid_shape, color=grid_color, lw=1.2, alpha=grid_opacity)
        
        # Remove all spines but the one in the bottom
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["top"].set_visible(False)
        if switch_off_yaxis:
            self.ax.spines["left"].set_visible(False)
        else:
            self.ax.spines["left"].set_linewidth(self.y_axis_width)

        # Customize bottom spine
        if switch_off_xaxis:
            self.ax.spines["bottom"].set_visible(False)
        else:
            self.ax.spines["bottom"].set_lw(self.x_axis_width)
            self.ax.spines["bottom"].set_capstyle("butt")

    def style_axis(self, 
        Y_range=None, Y_labels=None,  # Set y-axis tick positions and labels.
        X_range=None, X_labels=None,  # Set x-axis tick positions and labels.
        xx_label_dist=0, xy_label_dist=0  # Shift x-axis tick labels horizontally and vertically.
    ):
        # Apply tick values, labels, fonts, rotations, and optional label offsets.
         
        if self.y_ticks_allowed:
            self.ax.yaxis.set_ticks( Y_range )
            self.ax.yaxis.set_ticklabels( Y_labels, fontsize=self.Y_label_fontsize, rotation=self.Y_label_rotate )
            self.ax.yaxis.set_tick_params(length=6, width=1.2)
        else:
            self.ax.yaxis.set_tick_params(labelbottom=False, length=0)

        if self.x_ticks_allowed:
            self.ax.xaxis.set_ticks(X_range)
            self.ax.xaxis.set_ticklabels(X_labels, fontsize=self.X_label_fontsize, rotation=self.X_label_rotate)
            self.ax.xaxis.set_tick_params(length=6, width=1.2)
        else:
            self.ax.xaxis.set_tick_params(labelbottom=False, length=0)

        # Make gridlines be below most artists.
        self.ax.set_axisbelow(True)

        if xx_label_dist or xy_label_dist:
            if isinstance(xx_label_dist, int):
                xx_label_dist = [xx_label_dist for i in self.ax.get_xticklabels()]
            if isinstance(xy_label_dist, int):
                xy_label_dist = [xy_label_dist for i in self.ax.get_xticklabels()]

            for i, label in enumerate(self.ax.get_xticklabels()):
                offset = transforms.ScaledTranslation( xx_label_dist[i], xy_label_dist[i], ax.figure.dpi_scale_trans)
                label.set_transform(label.get_transform() + offset)

        # PAD = abs(y_max - y_min) * y_padding_factor
        # for i, (label_pos, label) in enumerate(zip(Y_range, Y_range_label)):
        #     ax.text( x_min - x_padding + x_padding_factor, label_pos + PAD, str(label),  ha="right", va="baseline", fontsize=Y_label_fontsize, )
    
        
    def limit_axis(self, Y_range, X_range):
        # Expand and apply the y-axis and x-axis limits around the generated ranges.
        y_max, y_min = max(Y_range), min(Y_range)
        self.ax.set_ylim(y_min - self.x_axis_pos_offset, y_max + self.x_axis_pos_offset)

        x_max, x_min = max(X_range), min(X_range)    
        self.ax.set_xlim(x_min - self.y_axis_pos_offset, x_max + self.y_axis_pos_offset)

        return 
        

    def stylize(self,
            Y_values, X_values,  # Data ranges used to generate automatic ticks.
            X_range=None, X_labels = None,  # Optional explicit x-axis tick positions and labels.
            Y_range=None, Y_labels = None,  # Optional explicit y-axis tick positions and labels.

            grid_shape = None, grid_opacity=None, grid_color=None,  # Override default grid settings.
            switch_off_yaxis = None, switch_off_xaxis = None,  # Override default axis-spine visibility.
        **kwargs,  # Extra label-offset options forwarded to axis styling.
        ):
        if (not Y_range) and (not Y_labels):
            Y_range, Y_labels = range_calc(
                Y_values, self.y_points, y_up_off = self.y_up_offset , y_down_off=self.y_down_offset, decimal_places=self.decimal_places)

        if (not X_range) and (not X_labels):
            X_range, X_labels = range_calc(
                X_values, self.x_points, y_up_off = self.x_up_offset, y_down_off=self.x_down_offset, decimal_places=self.decimal_places)

        self.style_grid( 
            grid_shape=grid_shape or self.grid_shape, 
            grid_opacity=grid_opacity or self.grid_opacity, 
            grid_color = grid_color or self.grid_color,
            switch_off_yaxis=switch_off_yaxis or self.switch_off_yaxis, 
            switch_off_xaxis=switch_off_xaxis or self.switch_off_xaxis
        )
        
        self.style_axis(
            Y_range=Y_range, Y_labels=Y_labels,
            X_range=X_range, X_labels=X_labels,
            xx_label_dist= kwargs.get('xx_label_dist', 0),
            xy_label_dist= kwargs.get('xy_label_dist', 0)
        )

        self.limit_axis(
            Y_range=Y_range, X_range=X_range, 
        )
        
        return 
        
        
        
    
    def plot(self, plt_type="line", **kwargs):
        # Dispatch a plot type, style and render it, and save the resulting PNG.
        self.basic_setup(**kwargs, **self.kwargs)
        colors = self.fix_colors(**kwargs, **self.kwargs)
        if kwargs.get('colors', None) :
            kwargspop('colors')

        method_name = self.PLOT_METHODS.get(plt_type.lower())
        X_vals, Y_vals = getattr(self, method_name)(colors=colors, **kwargs, **self.kwargs)

        self.stylize( Y_values=Y_vals, X_values=X_vals, **kwargs, **self.kwargs)
        self.save_plot(**kwargs, **self.kwargs)

    
    def line_plot(self, **kwargs):
        # Forward line-plot options to the line plotting implementation.
        from line import line_plot
        plot_kwargs = {"ax": self.ax, **kwargs}
        return line_plot(**plot_kwargs)
        
    def save_plot(
        self,
        name=None,  # Override the output file's base name.
        transparent=False,  # Make the PNG background transparent.
        dpi=300,  # Set the saved image resolution.
        **kwargs,  # Accept layout and image-saving overrides.
        ):
        # Tighten the layout and save the current figure as a PNG.
        output_name = name or self.name
        self.fig.tight_layout()
        output_path = f"{output_name}.png"
        
        self.fig.savefig(
            output_path, dpi=dpi, 
            bbox_inches=kwargs.pop("bbox_inches", "tight"),
            pad_inches=kwargs.pop("pad_inches", 0),
            transparent=transparent,
        )
        return output_path







    # def _invoke_plot(self, plot_function, *args, output_name="name", **kwargs):
    #     options = {**self.defaults, **kwargs}
    #     if output_name != "name" and "name" in options and output_name not in options:
    #         options[output_name] = options.pop("name")

    #     plot_signature = signature(plot_function)
    #     bound = plot_signature.bind_partial(*args, **options)
    #     if "figsize" in plot_signature.parameters and "figsize" not in bound.arguments:
    #         bound.arguments["figsize"] = self.figsize
    #     if (
    #         self.name is not None
    #         and output_name in plot_signature.parameters
    #         and output_name not in bound.arguments
    #     ):
    #         bound.arguments[output_name] = self.name
    #     return plot_function(*bound.args, **bound.kwargs)

    
    # def bar_graph_X_Y(self, *args, **kwargs):
    #     from hist import bar_graph_X_Y

    #     return self._invoke_plot(bar_graph_X_Y, *args, **kwargs)

    # def bar_graph_X_Y_Gradient(self, *args, **kwargs):
    #     from hist import bar_graph_X_Y_Gradient

    #     return self._invoke_plot(bar_graph_X_Y_Gradient, *args, **kwargs)

    # def bar_graph_side_by_side(self, *args, **kwargs):
    #     from hist import bar_graph_side_by_side

    #     return self._invoke_plot(bar_graph_side_by_side, *args, **kwargs)

    # def bar_graph_horizontal(self, *args, **kwargs):
    #     from hist import bar_graph_horizontal

    #     return self._invoke_plot(bar_graph_horizontal, *args, **kwargs)

    # def bar_graph_horizontal2(self, *args, **kwargs):
    #     from hist import bar_graph_horizontal2

    #     return self._invoke_plot(bar_graph_horizontal2, *args, **kwargs)

    # def scatter_plt(self, *args, **kwargs):
    #     from scatter import scatter_plt

    #     return self._invoke_plot(scatter_plt, *args, **kwargs)

    # def heatmap_plt(self, *args, **kwargs):
    #     from misc_plot import heatmap_plt

    #     return self._invoke_plot(heatmap_plt, *args, **kwargs)

    # def word_cloud_plt(self, *args, **kwargs):
    #     from misc_plot import word_cloud_plt

    #     return self._invoke_plot(word_cloud_plt, *args, **kwargs)

    # def radar_spider_plot(self, *args, **kwargs):
    #     from misc_plot import radar_spider_plot

    #     return self._invoke_plot(radar_spider_plot, *args, **kwargs)

    # def box_plt(self, *args, **kwargs):
    #     from misc_plot import box_plt

    #     return self._invoke_plot(box_plt, *args, **kwargs)

    # def network_bubble(self, *args, **kwargs):
    #     from misc_plot import network_bubble

    #     return self._invoke_plot(network_bubble, *args, output_name="plt_name", **kwargs)

    # def Sankey_web(self, *args, **kwargs):
    #     from misc_plot import Sankey_web

    #     return self._invoke_plot(Sankey_web, *args, **kwargs)
