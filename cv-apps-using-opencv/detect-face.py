# Project 4: Detect a face using haar cascades

import cv2;

def captureImage():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    writer = cv2.VideoWriter(
        "face-detect-output.mp4",
        cv2.VideoWriter_fourcc(*'mp4v'), fps,
        (width, height))

    frame = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Video", frame)
        key = cv2.waitKey(1)
        if key == ord('c') or key == 27:
            break

        writer.write(frame)

    cap.release()
    cv2.destroyWindow("Video")
    writer.release()
    return frame

if __name__ == "__main__":
    captureImage()