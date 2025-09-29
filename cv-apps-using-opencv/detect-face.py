# Project 4: Detect a face using haar cascades

import cv2;


cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
writer = cv2.VideoWriter(
    "face-detect-output.mp4",
    cv2.VideoWriter_fourcc(*'mp4v'), fps,
    (width, height))

classifier = cv2.CascadeClassifier()
classifier.load("haar-classifier.xml")

frame = None
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(100, 100))

    num_faces = len(faces)
    for i in range(num_faces):
        x, y, w, h = faces[i]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255 - i * 100), 2)

    cv2.imshow("Video", frame)
    writer.write(frame)

    key = cv2.waitKey(1)
    if key == ord('c') or key == 27:
        break



cap.release()
cv2.destroyWindow("Video")
writer.release()

