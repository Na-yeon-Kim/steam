from flask import Flask, render_template, jsonify, send_from_directory
import os

app = Flask(__name__)

# 오디오 파일 디렉토리 경로
AUDIO_DIR = "audio"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/get-audio-files")
def get_audio_files():
    # 디렉토리 내 파일 목록 가져오기
    files = sorted(os.listdir(AUDIO_DIR))
    audio_files = [
        {"filename": file, "title": f"Broadcast #{i + 1}"}
        for i, file in enumerate(files) if file.endswith(".mp3")
    ]
    return jsonify(audio_files)

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
