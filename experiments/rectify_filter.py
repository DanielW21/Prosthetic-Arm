import numpy as np
import matplotlib.pyplot as plt

# Load raw EMG data
file_path = 'experiments/EMGData.txt'
with open(file_path, 'r') as f:
    raw_data = np.array([float(line.strip()) for line in f if line.strip()])

sample_rate = 1000  # Adjust if you know your EMG sampling rate (Hz), else just estimate

def emg_to_on_off(emg_signal, sample_rate, threshold=None, min_duration_ms=1):
    # 1. Rectify
    rectified = np.abs(emg_signal)

    # 2. Smooth (moving average window)
    window_size = int(sample_rate * 0.01)  # 50 ms window
    if window_size < 1:
        window_size = 1
    smooth = np.convolve(rectified, np.ones(window_size)/window_size, mode='same')

    # 3. Threshold
    if threshold is None:
        baseline = smooth[:sample_rate]  # First 1 sec assumed baseline
        threshold = baseline.mean() + 2 * baseline.std()
        print(f"Auto-calculated threshold: {threshold:.2f}")

    binary = (smooth > threshold).astype(int)

    # 4. Clean short bursts
    min_samples = int(sample_rate * (min_duration_ms / 1000))

    def clean_bursts(signal):
        cleaned = signal.copy()
        current_state = cleaned[0]
        count = 0
        for i in range(len(cleaned)):
            if cleaned[i] == current_state:
                count += 1
            else:
                # Only clean if OFF segment is too short
                if current_state == 0 and count < min_samples:
                    cleaned[i-count:i] = 1  # Flip short OFF to ON
                current_state = cleaned[i]
                count = 1
        # Check last segment
        if current_state == 0 and count < min_samples:
            cleaned[-count:] = 1
        return cleaned

    clean_binary = clean_bursts(binary)

    return smooth, threshold, clean_binary


# Run the improved algorithm
smoothed_data, threshold, digital_signal = emg_to_on_off(raw_data, sample_rate, threshold=50, min_duration_ms=50)

# Plot raw and smoothed EMG with threshold line
plt.figure(figsize=(12, 6))
plt.plot(raw_data, label='Raw EMG', color='lightgray')
plt.plot(smoothed_data, label='Smoothed EMG', color='blue', linewidth=2)
plt.axhline(threshold, color='red', linestyle='--', label=f'Threshold = {threshold:.2f}')
plt.legend()
plt.title('Raw vs Smoothed EMG with Threshold')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.show()

# Plot final binary on/off signal
plt.figure(figsize=(12, 4))
plt.plot(digital_signal, color='green', drawstyle='steps-post')
plt.title('Digital ON/OFF Classification of EMG (Cleaned)')
plt.xlabel('Sample Index')
plt.ylabel('State (1=ON, 0=OFF)')
plt.ylim(-0.2, 1.2)
plt.show()
