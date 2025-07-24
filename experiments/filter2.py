import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Load Data
file_path = 'experiments/EMGData.txt'
with open(file_path, 'r') as f:
    raw_data = np.array([float(line.strip()) for line in f if line.strip()])

# Filtering Raw Input
window_size = 15
smoothed_data = np.convolve(np.abs(raw_data), np.ones(window_size) / window_size, mode='same')

# Classification
threshold = 100
digital_signal = (smoothed_data >= threshold).astype(int)

# Define scrolling function
def interactive_plot(data_series, labels, title, y_label):
    # Initial display window size
    window = 1000
    total_length = len(data_series[0])

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.subplots_adjust(bottom=0.2)

    lines = []
    for series, label, color in zip(data_series, labels, ['lightgray', 'blue', 'green']):
        line, = ax.plot(series[:window], label=label, color=color, linewidth=2 if color != 'lightgray' else 1)
        lines.append(line)

    ax.set_title(title)
    ax.set_xlabel('Sample Index')
    ax.set_ylabel(y_label)
    ax.legend()

    # Slider
    ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03])
    slider = Slider(ax_slider, 'Position', 0, total_length - window, valinit=0, valstep=1)

    def update(val):
        idx = int(slider.val)
        for i, series in enumerate(data_series):
            lines[i].set_ydata(series[idx:idx+window])
            lines[i].set_xdata(np.arange(idx, idx+window))
        ax.set_xlim(idx, idx+window)
        ax.relim()
        ax.autoscale_view(scaley=True)
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

# Plot Raw + Smoothed EMG with scroll
interactive_plot([raw_data, smoothed_data], ['Raw EMG', f'Smoothed EMG (window={window_size})'], 
                 'Raw vs Smoothed EMG', 'Amplitude')

# Plot Digital ON/OFF with scroll
interactive_plot([digital_signal], ['Digital Signal (ON/OFF)'], 
                 'Digital Classification of EMG', 'State (1=ON, 0=OFF)')
