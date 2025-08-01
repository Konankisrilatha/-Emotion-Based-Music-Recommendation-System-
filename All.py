# app.py
from flask import Flask, render_template, Response, request
import os
import cv2
import time
import pygame
import random
from deepface import DeepFace

app = Flask(__name__)
pygame.mixer.init()

current_emotion = None
last_emotion_time = 0

base_music_path = r"C:\Users\srila\Desktop\Music\song"
emotion_music_map = {
    "angry": os.path.join(base_music_path, "angry"),
    "sad": os.path.join(base_music_path, "sad"),
    "happy": os.path.join(base_music_path, "happy"),
    "neutral": os.path.join(base_music_path, "neutral"),
    "surprise": os.path.join(base_music_path, "surprise"),
    "fear": os.path.join(base_music_path, "fear"),
    "disgust": os.path.join(base_music_path, "disgust")
}

emotion_suggestions = {
    "angry": "Take a deep breath 😊",
    "sad": "It's okay, better days are ahead 💪",
    "happy": "Keep smiling! 😄",
    "neutral": "Stay calm and carry on 😌",
    "surprise": "Whoa! Hope it's good news! 😲",
    "fear": "Everything will be fine 🫂",
    "disgust": "Take a break and refresh 🌿"
}

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

def play_music_for_emotion(emotion):
    folder = emotion_music_map.get(emotion)
    if not folder or not os.path.isdir(folder):
        return
    songs = [song for song in os.listdir(folder) if song.endswith('.mp3')]
    if not songs:
        return
    song_path = os.path.join(folder, random.choice(songs))
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

def gen_frames():
    global current_emotion, last_emotion_time

    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            try:
                result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
                new_emotion = result[0]['dominant_emotion']

                if new_emotion != current_emotion and time.time() - last_emotion_time > 3:
                    play_music_for_emotion(new_emotion)
                    current_emotion = new_emotion
                    last_emotion_time = time.time()

            except Exception as e:
                print("Emotion detection error:", e)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html', emotion=current_emotion)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop', methods=['POST'])
def stop_music():
    pygame.mixer.music.stop()
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
