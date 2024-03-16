import cv2


def showImage(image):
    cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
    cv2.imshow("Test", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
