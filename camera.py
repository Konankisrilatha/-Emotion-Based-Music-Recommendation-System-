import cv2
from deepface import DeepFace

# Try different camera indexes if 0 does not work
cap = cv2.VideoCapture(0)

# Wait for the webcam to initialize
if not cap.isOpened():
    print("Error: Could not access the webcam. Try changing the camera index (e.g., 1 or 2).")
    exit()

# Set camera resolution (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Load OpenCV's pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Convert frame to grayscale for better face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract face region
        face_roi = frame[y:y + h, x:x + w]

        try:
            # Analyze facial expression using DeepFace
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

            # Get detected emotion
            dominant_emotion = result[0]['dominant_emotion']
            print(f"Detected Emotion: {dominant_emotion}")

            # Draw bounding box around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display detected emotion on the frame
            cv2.putText(frame, f"Emotion: {dominant_emotion}", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        except Exception as e:
            print("Error in emotion detection:", str(e))

    # Display the webcam feed
    cv2.imshow('Real-Time Emotion Detector', frame)

    # Press 'q' to exit the webcam
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
