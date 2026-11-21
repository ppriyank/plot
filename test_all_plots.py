import os
import tempfile
import unittest
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")

from matplotlib.figure import Figure

from ALL_PLOTS import ALL_PLOT


class AllPlotsParameterTests(unittest.TestCase):
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

            plotter.update_params({"Y_label_fontsize": 15})
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
