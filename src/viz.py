import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Radar

def plot_player_radar(player_row, stats, title=None):
    """
    Creates a radar chart for one player (percentiles).
    Stat labels are automatically managed by mplsoccer.
    """
    # Stats to plot
    params = stats
    values = [player_row[f"{s}_per90_pct"] for s in stats]

    # Radar setup
    n_stats = len(params)
    lower = [0] * n_stats
    upper = [100] * n_stats
    radar = Radar(params, lower, upper)

    # --- Create figure ---
    fig, ax = plt.subplots(figsize=(6, 6))

    # Setup radar axis
    radar.setup_axis(ax=ax)
    radar.draw_circles(ax=ax, facecolor='#ddd', alpha=0.1)
    radar.draw_range_labels(ax=ax, fontsize=8)

    # Draw the radar values
    radar.draw_radar(values, ax=ax,
        kwargs_radar={'facecolor': '#1f77b4', 'alpha': 0.6})

    # ✅ Draw the parameter (stat) labels automatically
    radar.draw_param_labels(ax=ax, fontsize=9)

    # Title
    if title:
        ax.set_title(title, fontsize=14, pad=20)

    return fig, ax


