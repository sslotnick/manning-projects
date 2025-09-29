# Project 5: Detect eyes using haar cascades and hough transformation

import cv2;

classifier = cv2.CascadeClassifier()
classifier.load("haar-classifier-eyes.xml")


image = cv2.imread("eye-sample.jpg")

gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
eye_areas = classifier.detectMultiScale(gray_image)
for (x, y, w, h) in eye_areas:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    rows = gray_image.shape[0]
    search_area = gray_image[x:x+w, y:y+h]
    cv2.imshow("Search Area", search_area)

    circles = cv2.HoughCircles(search_area, cv2.HOUGH_GRADIENT, 2, rows/8, param1=100, param2=30, minRadius=1, maxRadius=200)
    for circle in circles[0]:
        center = [int(x + circle[0]), int(y + circle[1])]
        radius = int(circle[2])
        cv2.circle(image, center, radius, (255, 0, 0), 2)

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyWindow("Image")
cv2.destroyWindow("Search Area")

