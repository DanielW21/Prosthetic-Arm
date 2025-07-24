file_path = 'experiments/EMGData.txt'
with open(file_path, 'r') as f:
    data = [float(line.strip()) for line in f if line.strip()]

threshold = 100  
min_duration = 5   

high_amp_sections = []

in_burst = False
burst_start = 0

for i, value in enumerate(data):
    if abs(value) >= threshold:
        if not in_burst:
            in_burst = True
            burst_start = i
    else:
        if in_burst:
            burst_end = i - 1
            if (burst_end - burst_start + 1) >= min_duration:
                high_amp_sections.append((burst_start, burst_end))
            in_burst = False

if in_burst:
    burst_end = len(data) - 1
    if (burst_end - burst_start + 1) >= min_duration:
        high_amp_sections.append((burst_start, burst_end))

print("High-amplitude sections (start, end):")
for section in high_amp_sections:
    print(section)
