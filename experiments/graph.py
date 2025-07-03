import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

file_path = 'experiments/EMGData.txt'
with open(file_path, 'r') as f:
    data = [float(line.strip()) for line in f if line.strip()]

window_size = 100
max_index = len(data) - window_size

fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)

line, = ax.plot(range(window_size), data[:window_size], color='black', linewidth=1.2)

ax.set_title('EMG Signal', fontsize=16, weight='bold')
ax.set_xlabel('Sample Index', fontsize=12)
ax.set_ylabel('Amplitude (mV)', fontsize=12)
ax.grid(False)
ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')  
ax.set_ylim(-1500, 1500)  

ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
slider = Slider(ax_slider, 'Position', 0, max_index, valinit=0, valstep=1)

def update(val):
    idx = int(slider.val)
    segment = data[idx:idx + window_size]
    line.set_ydata(segment)
    line.set_xdata(range(idx, idx + window_size))
    ax.relim()
    ax.autoscale_view()
    ax.set_ylim(-1500, 1500)  
    fig.canvas.draw_idle()

slider.on_changed(update)

plt.show()
