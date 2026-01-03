# adaptive_server_fixed.py
from flask import Flask, Response
import cv2, time

app = Flask(__name__)

# Paths to your video files (update paths if necessary)
videos = {
    "1080p60": r"C:\Users\aparn\Downloads\The Prestige Edit  - After Dark_1080p.mp4",
    "720p60":  r"C:\Users\aparn\Downloads\The Prestige Edit  - After Dark _720_60p.mp4",
    "720p":    r"C:\Users\aparn\Downloads\The Prestige Edit  - After Dark_720p.mp4",
    "360p":    r"C:\Users\aparn\Downloads\The Prestige Edit  - After Dark_360p.mp4"
}

def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(1 / 24)  # ~24 fps

@app.route('/video/<quality>')
def video_feed(quality):
    if quality not in videos:
        return "Invalid quality", 404
    print(f"[Server] Streaming quality: {quality}")
    return Response(generate_frames(videos[quality]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
