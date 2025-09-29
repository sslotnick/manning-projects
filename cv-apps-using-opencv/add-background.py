import cv2

cap = cv2.VideoCapture("video.mp4")

background = cv2.imread("background.jpg")
ret, frame = cap.read()
background = cv2.resize(background, (frame.shape[1], frame.shape[0]))

writer = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame.shape[1], frame.shape[0]))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # cv2.imshow("Frame", frame)
    blue = frame[:,:,0]
    green = frame[:,:,1]
    red = frame[:,:,2]

    _,green_thresh = cv2.threshold(green,200,255,cv2.THRESH_BINARY_INV)
    frame[green_thresh == 0] = background[green_thresh == 0]

    cv2.imshow("Frame", frame)
    writer.write(frame)

    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break

cap.release()
writer.release()
cv2.destroyAllWindows()