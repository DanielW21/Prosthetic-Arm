import numpy as np
import matplotlib.pyplot as plt

R1 = 12000       
R5 = 24000       
R3 = 100000
Req = (R1*R3)/(R1+R3)    
C = 33e-9        
Vin = 1.92

# Frequency numpy array 
frequencies = np.logspace(0, 6, 10000)  #1 Hz to 1 MHz
omega = 2 * np.pi * frequencies
jw = 1j * omega

# Transfer function H(jw) 
numerator = -jw / (R1 * C)
denominator = (jw)**2 + 2 * jw / (R5 * C) + 1 / (Req * R5 * C**2)
H = numerator / denominator

# Output voltage
Vout = Vin * H
gain_db = 20 * np.log10(np.abs(H))

# Plotting Bode plot
plt.figure(figsize=(12, 7))
plt.semilogx(frequencies, gain_db, label='Theoretical Gain (dB)', linewidth=2)
plt.title("Bode Plot of Given Transfer Function", fontsize=16)
plt.xlabel("Frequency (Hz)", fontsize=14)
plt.ylabel("Gain (dB)", fontsize=14)
plt.grid(True, which='both', linestyle='--', linewidth=0.7)
plt.legend(fontsize=11)
plt.tight_layout()
plt.show()

# Displaying output voltage and gain at selected frequencies
selected_freqs = [10, 20, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000] 
print(f"{'Freq (Hz)':>10} | {'|V_out| (V)':>12} | {'|V_out/V_in|':>12}")
print("-" * 52)

for f in selected_freqs:
    idx = np.argmin(np.abs(frequencies - f))
    vout_mag = np.abs(Vout[idx])
    gain_mag = np.abs(H[idx])
    vout_phase = np.angle(Vout[idx], deg=True)
    print(f"{frequencies[idx]:10.0f} | {vout_mag:12.6f} | {gain_mag:12.6f}")