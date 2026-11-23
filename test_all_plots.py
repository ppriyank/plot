import os
import tempfile
import unittest
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")

from matplotlib.figure import Figure
from matplotlib.collections import LineCollection, QuadMesh

from ALL_PLOTS import ALL_PLOT


class AllPlotsParameterTests(unittest.TestCase):
    def test_heatmap_annotation_text_contrasts_with_cell_color(self):
        import matplotlib.pyplot as plt
        import pandas as pd

        from heatmap import heatmap_plt

        figure, ax = plt.subplots()
        try:
            heatmap_plt(
                ax,
                df=pd.DataFrame([[0, 1]]),
                colors=["black", "white"],
                grid_opacity=0,
            )
            self.assertEqual([text.get_color() for text in ax.texts], ["white", "black"])
        finally:
            plt.close(figure)

        figure, ax = plt.subplots()
        try:
            heatmap_plt(
                ax,
                df=pd.DataFrame([[0, 1]]),
                colors=["#808080", "white"],
                grid_opacity=0,
            )
            self.assertEqual([text.get_color() for text in ax.texts], ["white", "black"])
        finally:
            plt.close(figure)

        figure, ax = plt.subplots()
        try:
            heatmap_plt(
                ax,
                df=pd.DataFrame([[0, 1]]),
                colors=["black", "white"],
                annot_kws={"color": "magenta"},
                grid_opacity=0,
            )
            self.assertEqual(
                [text.get_color() for text in ax.texts], ["magenta", "magenta"]
            )
        finally:
            plt.close(figure)

    def test_heatmap_grid_shape_and_opacity_control_mesh_lines(self):
        import numpy as np
        import pandas as pd

        def draw_heatmap(grid_shape=None):
            plotter = ALL_PLOT()
            options = {"grid_opacity": 0.4}
            if grid_shape is not None:
                options["grid_shape"] = grid_shape
            plotter.plot(
                plt_type="heatmap",
                df=pd.DataFrame([[1, 2], [3, 4]]),
                cbar=False,
                name="heatmap-grid",
                **options,
            )
            return [
                collection
                for collection in plotter.ax.collections
                if isinstance(collection, LineCollection)
            ]

        with patch.object(Figure, "savefig", lambda figure, path, **kwargs: None):
            vertical = draw_heatmap("x")
            horizontal = draw_heatmap("y")
            default = draw_heatmap()
            xy = draw_heatmap("xy")

        self.assertEqual(len(vertical), 1)
        self.assertEqual(len(horizontal), 1)
        self.assertEqual(vertical[0].get_alpha(), 0.4)
        self.assertEqual(horizontal[0].get_alpha(), 0.4)
        for segment in vertical[0].get_segments():
            self.assertEqual(segment[0][0], segment[1][0])
        for segment in horizontal[0].get_segments():
            self.assertEqual(segment[0][1], segment[1][1])

        self.assertEqual(len(default), 2)
        self.assertEqual(len(xy), 2)
        for default_lines, xy_lines in zip(default, xy):
            np.testing.assert_array_equal(
                default_lines.get_segments(), xy_lines.get_segments()
            )

    def test_heatmap_uses_matplotlib_mesh_and_centered_dataframe_ticks(self):
        import numpy as np
        import pandas as pd

        plotter = ALL_PLOT()
        with patch.object(
            Figure, "savefig", lambda figure, path, **kwargs: None
        ):
            with patch.object(
                plotter, "style_grid", wraps=plotter.style_grid
            ) as style_grid:
                with patch.object(
                    plotter, "style_axis", wraps=plotter.style_axis
                ) as style_axis:
                    plotter.plot(
                        plt_type="heatmap",
                        df=pd.DataFrame(
                            [[1, 2, 3], [4, 5, 6]],
                            index=["first", "second"],
                            columns=["a", "b", "c"],
                        ),
                        cbar=False,
                        X_label_fontsize=11,
                        X_label_rotate=30,
                        Y_label_fontsize=12,
                        Y_label_rotate=15,
                        name="heatmap",
                    )
        style_grid.assert_called_once()
        style_axis.assert_called_once()

        mesh = next(
            collection
            for collection in plotter.ax.collections
            if isinstance(collection, QuadMesh)
        )
        np.testing.assert_array_equal(mesh.get_array(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(list(plotter.ax.get_xticks()), [0.5, 1.5, 2.5])
        self.assertEqual(list(plotter.ax.get_yticks()), [0.5, 1.5])
        self.assertEqual(plotter.ax.get_xticklabels()[0].get_fontsize(), 11)
        self.assertEqual(plotter.ax.get_xticklabels()[0].get_rotation(), 30)
        self.assertEqual(plotter.ax.get_yticklabels()[0].get_fontsize(), 12)
        self.assertEqual(plotter.ax.get_yticklabels()[0].get_rotation(), 15)
        self.assertEqual(
            [tick.get_text() for tick in plotter.ax.get_yticklabels()],
            ["first", "second"],
        )
        self.assertEqual(plotter.ax.get_ylim(), (2.0, 0.0))

    def test_heatmap_tick_options_support_disabled_and_interval_labels(self):
        import pandas as pd

        with patch.object(Figure, "savefig", lambda figure, path, **kwargs: None):
            plotter = ALL_PLOT()
            plotter.plot(
                plt_type="heatmap",
                df=pd.DataFrame(
                    [[1, 2, 3], [4, 5, 6]],
                    index=["first", "second"],
                    columns=["a", "b", "c"],
                ),
                xticklabels=2,
                yticklabels=False,
                cbar=False,
                name="heatmap-ticks",
            )

        self.assertEqual(list(plotter.ax.get_xticks()), [0.5, 2.5])
        self.assertEqual(
            [tick.get_text() for tick in plotter.ax.get_xticklabels()], ["a", "c"]
        )
        self.assertEqual(list(plotter.ax.get_yticks()), [])

    def test_heatmap_reference_lines_are_added_by_plot_wrapper(self):
        import pandas as pd

        with patch.object(Figure, "savefig", lambda figure, path, **kwargs: None):
            plotter = ALL_PLOT()
            plotter.plot(
                plt_type="heatmap",
                df=pd.DataFrame([[1, 2], [3, 4]]),
                h_lines=[1],
                v_lines=[1],
                cbar=False,
                name="heatmap-reference-lines",
            )

        self.assertEqual(len(plotter.ax.lines), 2)

    def test_heatmap_respects_plotter_tick_flags(self):
        import pandas as pd

        with patch.object(Figure, "savefig", lambda figure, path, **kwargs: None):
            plotter = ALL_PLOT(x_ticks_allowed=False, y_ticks_allowed=False)
            plotter.plot(
                plt_type="heatmap",
                df=pd.DataFrame([[1, 2], [3, 4]]),
                cbar=False,
                name="heatmap-hidden-ticks",
            )

        self.assertEqual(list(plotter.ax.get_xticks()), [])
        self.assertEqual(list(plotter.ax.get_yticks()), [])

    def test_bar_swap_axis_draws_horizontal_bars(self):
        with patch.object(Figure, "savefig", lambda figure, path, **kwargs: None):
            plotter = ALL_PLOT(colors=["red"])
            plotter.plot(
                plt_type="bar",
                Hists=[{"x": [10, 20], "y": [[3, 5]]}],
                swap_axis=True,
                bar_width=0.4,
                name="horizontal-bars",
            )

        bars = plotter.ax.patches
        self.assertEqual([bar.get_width() for bar in bars], [3, 5])
        for bar in bars:
            self.assertAlmostEqual(bar.get_height(), 0.4)
        self.assertEqual([bar.get_y() + bar.get_height() / 2 for bar in bars], [10, 20])

    def test_bar_axis_is_vertical_by_default(self):
        with patch.object(Figure, "savefig", lambda figure, path, **kwargs: None):
            plotter = ALL_PLOT(colors=["red"])
            plotter.plot(
                plt_type="bar",
                Hists=[{"x": [10], "y": [[3]]}],
                name="vertical-bars",
            )

        bar = plotter.ax.patches[0]
        self.assertEqual(bar.get_height(), 3)
        self.assertAlmostEqual(bar.get_width(), 0.8)

    def test_plot_kwargs_override_constructor_defaults(self):
        saved_options = {}

        def capture_savefig(figure, path, **kwargs):
            saved_options.update(kwargs)

        with tempfile.TemporaryDirectory() as output_dir, patch.object(
            Figure, "savefig", capture_savefig
        ):
            plotter = ALL_PLOT(
                colors=["red"],
                y_points=1,
                x_points=1,
                Y_label_fontsize=10,
                X_label_fontsize=10,
                y_axis_width=1,
                x_axis_width=1,
                switch_off_yaxis=True,
            )

            plotter.plot(
                Lines=[([0, 1], [0, 2])],
                name=os.path.join(output_dir, "overrides"),
                y_points=4,
                x_points=3,
                Y_label_fontsize=8,
                X_label_fontsize=7,
                y_axis_width=3,
                x_axis_width=4,
                switch_off_yaxis=False,
                grid_opacity=0,
                x_axis_end_limit_offset=0,
                pad_inches=0,
            )

            self.assertEqual(len(plotter.ax.get_yticks()), 5)
            self.assertEqual(len(plotter.ax.get_xticks()), 4)
            self.assertEqual(plotter.ax.yaxis.get_ticklabels()[0].get_fontsize(), 8)
            self.assertEqual(plotter.ax.xaxis.get_ticklabels()[0].get_fontsize(), 7)
            self.assertTrue(plotter.ax.spines["left"].get_visible())
            self.assertEqual(plotter.ax.spines["left"].get_linewidth(), 3)
            self.assertEqual(plotter.ax.spines["bottom"].get_linewidth(), 4)
            self.assertEqual(plotter.ax.get_xlim()[1], 1)
            self.assertEqual(saved_options["pad_inches"], 0)
            self.assertNotIn("y_points", plotter.kwargs)

            plotter.update({"Y_label_fontsize": 15})
            plotter.plot(
                Lines=[([0, 1], [0, 2])],
                name=os.path.join(output_dir, "updated-default"),
                X_range=[0, 1],
                X_labels=["a", "b"],
                Y_range=[0, 1, 2],
                Y_labels=["a", "b", "c"],
            )
            self.assertEqual(
                plotter.ax.yaxis.get_ticklabels()[0].get_fontsize(), 15
            )

    def test_plot_kwargs_can_disable_constructor_options(self):
        with tempfile.TemporaryDirectory() as output_dir, patch.object(
            Figure, "savefig", lambda figure, path, **kwargs: None
        ):
            plotter = ALL_PLOT(colors=["red"], legend=True)

            plotter.plot(
                Lines=[([0, 1], [0, 2])],
                name=os.path.join(output_dir, "disabled"),
                legend=False,
                y_ticks_allowed=False,
                x_ticks_allowed=False,
            )

            self.assertIsNone(plotter.ax.get_legend())
            self.assertFalse(plotter.ax.yaxis.get_major_ticks()[0].label1.get_visible())
            self.assertFalse(plotter.ax.xaxis.get_major_ticks()[0].label1.get_visible())
