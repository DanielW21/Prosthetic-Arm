import numpy as np
import matplotlib.pyplot as plt

file_path = 'experiments/EMGData.txt'
with open(file_path, 'r') as f:
    raw_data = np.array([float(line.strip()) for line in f if line.strip()])

# Filtering Raw Input
window_size = 15  # 1/n(sum x_i)
smoothed_data = np.convolve(np.abs(raw_data), np.ones(window_size)/window_size, mode='same')

plt.figure(figsize=(12, 6))
plt.plot(raw_data, label='Raw EMG', color='lightgray')
plt.plot(smoothed_data, label=f'Smoothed EMG (window={window_size})', color='blue', linewidth=2)
plt.legend()
plt.title('Raw vs Smoothed EMG')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.show()


# Final Output
threshold = 100  # Classification threshold
digital_signal = (smoothed_data >= threshold).astype(int)


plt.figure(figsize=(12, 4))
plt.plot(digital_signal, color='green', drawstyle='steps-post')
plt.title('Digital ON/OFF Classification of EMG')
plt.xlabel('Sample Index')
plt.ylabel('State (1=ON, 0=OFF)')
plt.ylim(-0.2, 1.2)
plt.show()