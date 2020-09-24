import cv2
import numpy as np

num_down = 2
num_bilateral = 7

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (540,380), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

    frame1 = frame
    for _ in range(num_down):
        frame1 = cv2.pyrDown(frame1)

    for _ in range(num_bilateral):
        frame1 = cv2.bilateralFilter(frame1, d=9, sigmaColor=9, sigmaSpace=7)

    for _ in range(num_down):
        frame1 = cv2.pyrUp(frame1)

    img_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)

    img_edge = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=9, C=2)

    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    img_cartoon = cv2.bitwise_and(frame1, img_edge)

    stack = np.hstack([frame, img_cartoon])
    cv2.imshow('Original vs Cartoonized ------> Press "q" to exit', stack)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()