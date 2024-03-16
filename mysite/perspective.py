import cv2
import numpy as np

from mysite.show import showImage


def adjust_perspective_if_needed(image, output_width=720, output_height=1080):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.adaptiveThreshold(
    #     gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    # )
    _, gray = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    edged = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(
        edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    epsilon = 0.1 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    image_area = image.shape[0] * image.shape[1]
    contour_area = w * h
    coverage_ratio = contour_area / image_area

    if coverage_ratio > 0.3:
        pts_src = np.array(
            [approx[1][0], approx[0][0], approx[3][0], approx[2][0]], dtype=np.float32
        )

        pts_dst = np.array(
            [
                [0, 0],
                [output_width - 1, 0],
                [output_width - 1, output_height - 1],
                [0, output_height - 1],
            ],
            dtype=np.float32,
        )

        matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

        result = cv2.warpPerspective(image, matrix, (output_width, output_height))

        showImage(result)

        return result

    return image
