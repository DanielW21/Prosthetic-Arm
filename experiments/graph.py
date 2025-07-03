import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

file_path = 'experiments/EMGData.txt'
with open(file_path, 'r') as f:
    data = [float(line.strip()) for line in f if line.strip()]

window_size = 100 
max_index = len(data) - window_size

fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)

line, = ax.plot(range(window_size), data[:window_size], marker='o', linestyle='-')
ax.set_title('Scrollable Data Plot')
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.grid(True)

ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03]) 
slider = Slider(ax_slider, 'Position', 0, max_index, valinit=0, valstep=1)

def update(val):
    idx = int(slider.val)
    line.set_ydata(data[idx:idx + window_size])
    line.set_xdata(range(idx, idx + window_size))
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

slider.on_changed(update)

plt.show()
