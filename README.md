# CN_S3
# QoS Optimization in Video Streaming (Adaptive Bitrate Simulation)

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Course](https://img.shields.io/badge/Course-Computer_Networks-orange)

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Theoretical Background](#-theoretical-background)
- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
- [Algorithm Logic](#-algorithm-logic)
- [Prerequisites & Installation](#-prerequisites--installation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Results & Visualization](#-results--visualization)
- [Project Team](#-project-team)
- [References](#-references)

---

##  Project Overview

[cite_start]This project demonstrates the principles of **Adaptive Bitrate Streaming (ABS)**, a technique used by major platforms (YouTube, Netflix) to ensure uninterrupted video playback under fluctuating network conditions[cite: 433, 434]. 

The system implements a **Client-Server architecture** where:
1.  [cite_start]**The Server** streams video content at multiple quality levels (360p, 720p, 720p60, 1080p60) via HTTP[cite: 439].
2.  [cite_start]**The Client** simulates network bandwidth fluctuations and dynamically selects the optimal video quality to maximize user experience (QoE)[cite: 442].

[cite_start]This project was developed as part of the **22AIE204: Introduction to Computer Networks** course.

---

##  Theoretical Background

This implementation draws inspiration from **MPEG DASH (Dynamic Adaptive Streaming over HTTP)** concepts.

### The Problem
[cite_start]Internet throughput fluctuates due to cross-traffic, interference, and fading[cite: 101]. Delivering a static high-bitrate stream often leads to buffer underruns (stalling), while a static low-bitrate stream wastes available bandwidth and results in poor visual quality.

### The Solution: Receiver-Driven Adaptation
As detailed in *Miller et al. (2012)[cite_start]*, the receiver (client) estimates available throughput and requests segments at different quality levels[cite: 12].

Our simulation focuses on the **Throughput-Based Switching** logic:
$$R_{next} = f(BW_{est})$$
Where $R_{next}$ is the requested representation and $BW_{est}$ is the estimated bandwidth.

The client calculates the bitrate of incoming frames using:
$$\text{kbps} = \frac{\text{Frame Size (bits)}}{ \text{Frame Time (ms)}}$$

---

##  System Architecture

The project consists of two distinct Python applications communicating over `localhost`:

### 1. The Server (`server_code.py`)
-   Built using **Flask** and **OpenCV**.
-   Serves MJPEG (Motion JPEG) streams.
-   **Endpoints:**
    -   `/video/360p`
    -   `/video/720p`
    -   `/video/720p60`
    -   `/video/1080p60`
-   Loops video playback automatically to simulate a continuous live stream[cite: 503].

### 2. The Client (`client_code.py`)
-   **Multi-threaded application**:
    1.  **Video Fetch Thread:** Connects to the server, decodes MJPEG frames using OpenCV, and calculates real-time metrics.
    2.  **Bandwidth Simulation Thread:** Randomly fluctuates a `sim_bw` variable (300kbps - 4000kbps) to mimic unstable network conditions[cite: 488].
    3.  **Visualization Thread:** Uses **Matplotlib/Seaborn** to plot Bandwidth vs. Quality in real-time.

---

##  Key Features
* [cite_start]**Simulated Network Volatility:** Internally simulates bandwidth drops and spikes (jitter) without needing actual network tools[cite: 469].
* [cite_start]**Threshold-Based Adaptation:** Automatically switches video quality targets based on pre-defined bandwidth buckets[cite: 453].
* **Real-Time Visualization:** Live dual-graph plotting of:
    * Simulated Bandwidth (Blue Line).
    * Selected Quality Level (Green Line).
* [cite_start]**Concurrent Execution:** Uses Python `threading` to handle networking, processing, and rendering simultaneously[cite: 478].

---

##  Algorithm Logic

The client utilizes a **Threshold-Based Quality Selection Algorithm**. [cite_start]For every frame processed, the client compares the simulated bandwidth against the following rules[cite: 470, 471, 472, 473, 474]:

| Simulated Bandwidth ($BW$) | Selected Quality |
| :--- | :--- |
| $BW > 2000$ kbps | **1080p60** |
| $1000 < BW \leq 2000$ kbps | **720p60** |
| $500 < BW \leq 1000$ kbps | **720p** |
| $BW \leq 500$ kbps | **360p** |

[cite_start]*Note: While the logic selects the optimal quality, the current client implementation simulates the switch in statistics and logs, while maintaining the connection to demonstrate the adaptation logic visually[cite: 513].*

---

## 🛠 Prerequisites & Installation

### Requirements
* **Python 3.8+**
* **Video Files:** You need 4 versions of the same video (1080p, 720p60, 720p, 360p).

### Dependencies
Install the required Python libraries:
```bash
pip install flask opencv-python requests matplotlib numpy seaborn
