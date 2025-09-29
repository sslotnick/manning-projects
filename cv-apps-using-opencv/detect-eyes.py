# Project 5: Detect eyes using haar cascades and hough transformation

import cv2;

classifier = cv2.CascadeClassifier()
classifier.load("haar-classifier-eyes.xml")

image = cv2.imread("eye-sample.jpg")

gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
eye_areas = classifier.detectMultiScale(gray_image)
for (x, y, w, h) in eye_areas:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyWindow("Image")

