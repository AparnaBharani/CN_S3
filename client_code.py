# adaptive_client_final_v2.py
import cv2, time, requests, numpy as np
import threading, matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

SERVER_URL = "http://127.0.0.1:5000"
QUALITIES = ["360p", "720p", "720p60", "1080p60"]
THRESHOLDS = [500, 1000, 2000]  # kbps, adjust for simulation

# Stats for plotting
stats = {"time": [], "bandwidth": [], "quality": []}
start_time = time.time()
lock = threading.Lock()
current_quality = "720p"
prev_frame_time = time.time()

# Simulated bandwidth (initial value)
sim_bw = 2000

def choose_quality(bw):
    """Decide video quality based on bandwidth."""
    if bw > THRESHOLDS[2]:
        return "1080p60"
    elif bw > THRESHOLDS[1]:
        return "720p60"
    elif bw > THRESHOLDS[0]:
        return "720p"
    else:
        return "360p"

def fluctuate_bandwidth():
    """Simulate network bandwidth fluctuations."""
    global sim_bw
    while True:
        change = random.uniform(-1500, 1500)  # bandwidth drop or increase
        sim_bw = max(300, min(4000, sim_bw + change))  # clamp between 300 and 4000 kbps
        time.sleep(random.uniform(0.5, 1.5))  # random interval

def video_thread():
    """Fetch video frames continuously without reconnecting on quality change."""
    global current_quality, prev_frame_time
    try:
        # Request video stream of initial quality
        stream = requests.get(f"{SERVER_URL}/video/{current_quality}", stream=True, timeout=30)
        bytes_data = b""
        while True:
            for chunk in stream.iter_content(chunk_size=4096):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b + 2]
                    bytes_data = bytes_data[b + 2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    if frame is not None:
                        now = time.time()
                        frame_time = now - prev_frame_time
                        prev_frame_time = now

                        # Calculate kbps from frame
                        kbps = (len(jpg) * 8 / 1000) / max(frame_time, 1e-3)

                        # Apply simulated bandwidth
                        kbps = min(kbps, sim_bw)

                        # Determine new quality (simulated)
                        new_quality = choose_quality(kbps)
                        if new_quality != current_quality:
                            current_quality = new_quality
                            print(f"[Switch] Quality changed -> {current_quality} @ {kbps:.1f} kbps (simulated)")

                        with lock:
                            stats["time"].append(now - start_time)
                            stats["bandwidth"].append(kbps)
                            stats["quality"].append(QUALITIES.index(current_quality))

                        cv2.imshow("Adaptive Streaming", frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            cv2.destroyAllWindows()
                            return
    except Exception as e:
        print("[!] Error:", e)
        time.sleep(1)

def update_graph(i):
    """Update bandwidth and quality plot."""
    with lock:
        t = stats["time"][-100:]
        bw = stats["bandwidth"][-100:]
        q = stats["quality"][-100:]

    ax1.clear()
    ax2.clear()
    ax1.plot(t, bw, color='blue')
    ax1.set_ylabel("Bandwidth (kbps)")
    ax1.set_ylim(0, 4000)

    ax2.plot(t, q, color='green')
    ax2.set_ylabel("Quality Level")
    ax2.set_yticks(range(len(QUALITIES)))
    ax2.set_yticklabels(QUALITIES)
    ax2.set_xlabel("Time (s)")
    plt.tight_layout()

# Start simulated bandwidth fluctuation thread
threading.Thread(target=fluctuate_bandwidth, daemon=True).start()

# Start video fetching thread
threading.Thread(target=video_thread, daemon=True).start()

plt.style.use("seaborn-v0_8-darkgrid")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Fix FuncAnimation warning by disabling cache_frame_data
ani = FuncAnimation(fig, update_graph, interval=1000, cache_frame_data=False)
plt.show()
