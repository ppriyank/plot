import matplotlib.pyplot as plt
from colors_set import *
from inspect import signature
from plot_utils import range_calc
from typing import Literal
import matplotlib.transforms as transforms


class ALL_PLOT:
    """Class-based entry point for the plotting helpers in this package."""  # Provides shared setup and dispatch for every plot type.

    PLOT_METHODS = {
        # Map plot names and aliases to the class methods that implement them.

        # Frequently Used & matplot supported
        "line": "line_plot",
        "scatter": "scatter_plt",
        "bar": "bar_plt",
        

        # Misc Plots 
        "heatmap": "heatmap_plt",
        
        # "word_cloud": "word_cloud_plt",
        # "word_cloud_plt": "word_cloud_plt",
        # "radar": "radar_spider_plot",
        # "radar_spider_plot": "radar_spider_plot",
        # "box": "box_plt",
        # "box_plt": "box_plt",
        # "network_bubble": "network_bubble",
        # "sankey": "Sankey_web",
        # "sankey_web": "Sankey_web",
    }

    MISC_PLOTS = set(
        "heatmap", 
    )

    

    def __init__(self, figsize=(8, 6),  # Figure width and height in inches.
        name=None,  # Default base name for the saved PNG file.
        pad_inches = 0.1,  # Padding around the saved figure, in inches.
        colors=None,  # Default color or mapping used to draw plot elements.
        artificial_darkening=0.8,  # Adjusts the darkness of supplied colors.
        decimal_places=1,  # Sets decimal precision for generated axis labels.
        legend = False , 
        
        y_points = 2, x_points = 2,  # Set the number of generated tick points on each axis.
        y_up_offset=0, y_down_offset=0, x_up_offset=0, x_down_offset=0,  # Extend or contract axis ranges around the data.

        grid_shape='both', grid_opacity=0.3, grid_color="#A8BAC4",  # Configure grid visibility, transparency, and color.
        switch_off_yaxis=False, switch_off_xaxis=False,  # Hide individual axis spines when enabled.
        y_axis_width=1.2, x_axis_width=1.2,  # Set the line width of the visible axis spines.
        y_ticks_allowed=True, x_ticks_allowed=True,  # Enable or disable tick labels on each axis.
        Y_label_fontsize=20, X_label_fontsize=25,  # Set axis tick-label font sizes.
        Y_label_rotate=0, X_label_rotate =0 ,  # Rotate axis tick labels by these angles.

        x_axis_pos_offset=0, y_axis_pos_offset=0,  # Move the y/x axis origin outward by the given data-range padding.
        x_axis_end_limit_offset=0.1, y_axis_end_limit_offset=0.1,  # Extend the x/y upper limit beyond the calculated maximum.

        **kwargs):  # Extra plot, setup, or save options forwarded to plot helpers.
        # Store class-wide defaults used by setup and styling methods.
        
        self.figsize = figsize
        self.name = name
        self.defaults = kwargs
        self.fig = None
        self.ax = None
        self.pad_inches = pad_inches
        self.legend = legend

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
        if x_axis_pos_offset != 0 or y_axis_pos_offset != 0:
            print("\n\n\n.... Shifting the axis away from origin!! \n\n\n")

        self.x_axis_end_limit_offset=x_axis_end_limit_offset 
        self.y_axis_end_limit_offset=y_axis_end_limit_offset 

        self.kwargs = kwargs
        self.storage = {} # save all init params in case they are overwritten
        self.newly_added = set() # all params passed for that run 

    def basic_setup(self, **kwargs):  # kwargs may override figsize with a per-plot figure size.
        # Create the Matplotlib figure and axes, optionally overriding the default size.
        figsize = kwargs.get('figsize', self.figsize)
        self.fig, self.ax = plt.subplots(figsize=figsize or self.figsize)
        return self.fig, self.ax

    def fix_colors(self, **kwargs):  # kwargs may provide colors and artificial_darkening overrides.
        # Normalize colors and apply the configured darkness adjustment.
        colors = kwargs.get('colors', self.colors)
        artificial_darkening = kwargs.get('artificial_darkening', self.artificial_darkening)

        if colors is None:
            return None

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
        **kwargs,
        ):
        # Configure grid lines and hide or style the visible axis spines.
        # Add grid lines
        if grid_shape == 'xy':
            grid_shape = 'both'
        
        if grid_shape == None:
            grid_shape = 'both'
            grid_opacity = 0 

        
        self.ax.grid(axis=grid_shape, color=grid_color, lw=1.2, alpha=grid_opacity, zorder=1)
        
        # Remove all spines but the one in the bottom
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["top"].set_visible(False)
        if switch_off_yaxis:
            self.ax.spines["left"].set_visible(False)
        else:
            self.ax.spines["left"].set_linewidth(
                kwargs.get("y_axis_width", self.y_axis_width)
            )
        self.ax.spines["left"].set_zorder(50)

        # Customize bottom spine
        if switch_off_xaxis:
            self.ax.spines["bottom"].set_visible(False)
        else:
            self.ax.spines["bottom"].set_lw(
                kwargs.get("x_axis_width", self.x_axis_width)
            )
            self.ax.spines["bottom"].set_capstyle("butt")
        self.ax.spines["bottom"].set_zorder(50)
        
        

    def style_axis(self,
        Y_range=None, Y_labels=None,  # Set y-axis tick positions and labels.
        X_range=None, X_labels=None,  # Set x-axis tick positions and labels.
        x_axis_label_dist_x=0, x_axis_label_dist_y=0,  # Shift x-axis tick labels horizontally and vertically.
        y_axis_label_dist_x=0, y_axis_label_dist_y=0,  # Shift y-axis tick labels horizontally and vertically.
        **kwargs
        ):
        # Apply tick values, labels, fonts, rotations, and optional label offsets.
        if kwargs.get('y_ticks_allowed', self.y_ticks_allowed):
            self.ax.yaxis.set_ticks( Y_range )
            self.ax.yaxis.set_ticklabels(Y_labels)
            self.ax.yaxis.set_tick_params(
                length=6,
                width=1.2,
                labelsize=kwargs.get("Y_label_fontsize", self.Y_label_fontsize),
                labelrotation=kwargs.get("Y_label_rotate", self.Y_label_rotate),
            )
        else:
            self.ax.yaxis.set_tick_params(labelbottom=False, length=0)

        if kwargs.get('x_ticks_allowed', self.x_ticks_allowed):
            self.ax.xaxis.set_ticks(X_range)
            self.ax.xaxis.set_ticklabels(X_labels)
            self.ax.xaxis.set_tick_params(
                length=6,
                width=1.2,
                labelsize=kwargs.get("X_label_fontsize", self.X_label_fontsize),
                labelrotation=kwargs.get("X_label_rotate", self.X_label_rotate),
            )
        else:
            self.ax.xaxis.set_tick_params(labelbottom=False, length=0)

        # print(Y_range, Y_labels)
        # print(X_range, X_labels)

        # Make gridlines be below most artists.
        self.ax.set_axisbelow(True)
        
        ###### distatnce of x labels from x axis 
        if x_axis_label_dist_x or x_axis_label_dist_y:
            for i, x_label_obj in enumerate(self.ax.get_xticklabels()):
                x_label = x_label_obj.get_text()
                if isinstance(x_axis_label_dist_x, int):
                    x_label_pos_x = x_axis_label_dist_x
                elif isinstance(x_axis_label_dist_x, dict):
                    x_label_pos_x = x_axis_label_dist_x[x_label]

                if isinstance(x_axis_label_dist_y, int):
                    x_label_pos_y = x_axis_label_dist_y
                elif isinstance(x_axis_label_dist_y, dict):
                    x_label_pos_y = x_axis_label_dist_y[x_label]

                offset = transforms.ScaledTranslation( x_label_pos_x, x_label_pos_y, self.ax.figure.dpi_scale_trans)
                x_label_obj.set_transform(x_label_obj.get_transform() + offset)

        ###### distatnce of y labels from y axis 
        if y_axis_label_dist_x or y_axis_label_dist_y:
            for i, y_label_obj in enumerate(self.ax.get_yticklabels()):
                y_label = y_label_obj.get_text()
                if isinstance(y_axis_label_dist_x, int):
                    y_label_pos_x = y_axis_label_dist_x
                elif isinstance(y_axis_label_dist_x, dict):
                    y_label_pos_x = y_axis_label_dist_x[y_label]

                if isinstance(y_axis_label_dist_y, int):
                    y_label_pos_y = y_axis_label_dist_y
                elif isinstance(y_axis_label_dist_y, dict):
                    y_label_pos_y = y_axis_label_dist_y[x_label]

                offset = transforms.ScaledTranslation( y_label_pos_x, y_label_pos_y, self.ax.figure.dpi_scale_trans)
                y_label_obj.set_transform(y_label_obj.get_transform() + offset)

        # PAD = abs(y_max - y_min) * y_padding_factor
        # for i, (label_pos, label) in enumerate(zip(Y_range, Y_range_label)):
        #     ax.text( x_min - x_padding + x_padding_factor, label_pos + PAD, str(label),  ha="right", va="baseline", fontsize=Y_label_fontsize, )

    ##### Sets the limit of plot and position of axis     
    def limit_axis(
        self,
        Y_range,  # Tick range used to determine the y-axis bounds.
        X_range,  # Tick range used to determine the x-axis bounds.
        Y_values,  # Unused data values retained for the styling interface.
        X_values,  # Unused data values retained for the styling interface.
        **kwargs
        ):
        # Derive the lower-left origin from the actual data ranges.
        y_max, y_min = max(Y_range), min(Y_range)
        x_max, x_min = max(X_range), min(X_range)

        self.ax.set_ylim(
            y_min - kwargs.get("x_axis_pos_offset", self.x_axis_pos_offset),
            y_max + kwargs.get("y_axis_end_limit_offset", self.y_axis_end_limit_offset), 
        )
        
        
        self.ax.set_xlim(
            x_min - kwargs.get("y_axis_pos_offset", self.y_axis_pos_offset),
            x_max + kwargs.get("x_axis_end_limit_offset", self.x_axis_end_limit_offset), 
        )

        return 
        
    def stylize(self,
            Y_values, X_values,  # Data ranges used to generate automatic ticks.
            X_range=None, X_labels = None,  # Optional explicit x-axis tick positions and labels.
            Y_range=None, Y_labels = None,  # Optional explicit y-axis tick positions and labels.
            grid_shape = None, grid_opacity=None, grid_color=None,  # Override default grid settings.
            switch_off_yaxis = None, switch_off_xaxis = None,  # Override default axis-spine visibility.
            **kwargs,  # Extra label-offset options forwarded to axis styling.
        ):
        if Y_range is None and Y_labels is None:
            Y_range, Y_labels = range_calc(
                Y_values,
                kwargs.get("y_points", self.y_points),
                y_up_off=kwargs.get("y_up_offset", self.y_up_offset),
                y_down_off=kwargs.get("y_down_offset", self.y_down_offset),
                decimal_places=kwargs.get("decimal_places", self.decimal_places),
            )

        if X_range is None and X_labels is None:
            X_range, X_labels = range_calc(
                X_values,
                kwargs.get("x_points", self.x_points),
                y_up_off=kwargs.get("x_up_offset", self.x_up_offset),
                y_down_off=kwargs.get("x_down_offset", self.x_down_offset),
                decimal_places=kwargs.get("decimal_places", self.decimal_places),
            )

        self.style_grid( 
            grid_shape=self.grid_shape if grid_shape is None else grid_shape,
            grid_opacity=self.grid_opacity if grid_opacity is None else grid_opacity,
            grid_color=self.grid_color if grid_color is None else grid_color,
            switch_off_yaxis=(
                self.switch_off_yaxis
                if switch_off_yaxis is None
                else switch_off_yaxis
            ),
            switch_off_xaxis=(
                self.switch_off_xaxis
                if switch_off_xaxis is None
                else switch_off_xaxis
            ),
            **kwargs
        )

        self.style_axis(
            Y_range=Y_range, Y_labels=Y_labels,
            X_range=X_range, X_labels=X_labels,
            **kwargs
        )

        # plt.savefig("test.png", dpi=300)
        self.limit_axis(
            Y_range=Y_range, X_range=X_range,
            Y_values=Y_values, X_values=X_values,
            **kwargs
        )
        return 
        
        
    def update(self, vals : dict):  # vals maps existing instance attribute names to new values.
        # key = 'switch_off_yaxis'
        # self.__dict__[key]
        for key, value in vals.items():
            if hasattr(self, key):
                self.__dict__[key] = value 
            else:
                assert False, f"Parameter {key} not yet intialized"

    def add_legends(self, **kwargs):
        if kwargs.get('legend', self.legend):
            legend = self.ax.legend()
            legend.set_zorder(50)
    
    def check_update_params(self, kwargs):
        for key, value in kwargs.items():
            self.newly_added.add(key)
            if key in self.kwargs:
                self.storage[key] = self.kwargs[key] 
            self.kwargs[key]  = value 
        
    def restore_params(self, ):
        while self.newly_added:
            key = self.newly_added.pop()
            if key in self.storage:
                self.kwargs[key] = self.storage.pop(key)
            else:
                self.kwargs.pop(key, None)
        
    
    def line_plot(self, **kwargs):  # kwargs are forwarded to line_plot from line.py.
        # Forward line-plot options to the line plotting implementation.
        from line import line_plot
        plot_kwargs = {"ax": self.ax, **kwargs}
        return line_plot(**plot_kwargs)
    
    def scatter_plt(self, **kwargs):  # kwargs are forwarded to scatter_plt from scatter.py.
        from scatter import scatter_plt
        plot_kwargs = {"ax": self.ax, **kwargs}
        return scatter_plt(**plot_kwargs)

    def bar_plt(self, **kwargs):
        from hist import bar_plt
        plot_kwargs = {"ax": self.ax, **kwargs}
        return bar_plt(**plot_kwargs)

    def heatmap_plt(self, **kwargs):
        from heatmap import heatmap_plt
        plot_kwargs = {
            "ax": self.ax, 
            **kwargs
        }
        
        additional_params = {}
        if 'grid_shape' not in kwargs:
            additional_params['grid_shape'] = self.grid_shape
        if 'grid_opacity' not in kwargs:
            additional_params['grid_opacity'] = self.grid_opacity
        if 'grid_color' not in kwargs:
            additional_params['grid_color'] = self.grid_color
        
        plot_kwargs.update(additional_params)
        return heatmap_plt(**plot_kwargs)

        
        
    def update_plot_kwargs(self, Add_parms, plot_kwargs):
        for k,v in Add_parms.items():
            # if plot_kwargs.get(k, None) is None:
            plot_kwargs[k] = v
        return plot_kwargs



    def plot(
        self,
        plt_type="line",  # Plot implementation or alias to dispatch.
        **kwargs,  # Per-plot options, including setup, styling, data, and save overrides.
        ):

        self.check_update_params(kwargs)
        plot_kwargs = self.kwargs.copy()
        self.basic_setup(**plot_kwargs)

        colors = self.fix_colors(**plot_kwargs)
        plot_kwargs.pop('colors', None)

        method_name = self.PLOT_METHODS.get(plt_type.lower())
        X_vals, Y_vals, Add_parms = getattr(self, method_name)(
                colors=colors, **plot_kwargs
            )

        plot_kwargs = self.update_plot_kwargs(Add_parms, plot_kwargs)
        
        self.stylize(Y_values=Y_vals, X_values=X_vals, **plot_kwargs)
        self.add_legends(**plot_kwargs)
        self.save_plot(**plot_kwargs)

        self.restore_params()


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
            pad_inches=kwargs.get("pad_inches", self.pad_inches),
            transparent=transparent,
        )
        return output_path









    
    
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
