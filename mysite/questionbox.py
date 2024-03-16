import cv2
import numpy as np

from mysite.xywh import infoSquare


def checkQuestions(
    questions,
    ans,
    isNegative,
    image,
    blur,
    areaList,
    areaListSort,
    squares,
    num,
    n,
    markPerQuestion,
    negativeMark,
):
    x, y, w, h = infoSquare(areaList, areaListSort, squares, num)
    circle_radius = round(w / 14)
    marked_index = []
    marks = 0

    for i in range(0, questions):
        marked_circle_index = []
        min_intensity = 150
        for j in range(0, 4):
            mask = np.zeros(blur.shape, np.uint8)
            cv2.circle(
                mask,
                (
                    round((2 * x + (2 * j + 1) * w / 4) / 2),
                    round((2 * y + (2 * i + 1) * h / n) / 2),
                ),
                circle_radius,
                255,
                -1,
            )
            if ans[i] - 1 == j:
                cv2.circle(
                    image,
                    (
                        round((2 * x + (2 * j + 1) * w / 4) / 2),
                        round((2 * y + (2 * i + 1) * h / n) / 2),
                    ),
                    circle_radius,
                    (50, 220, 50),
                    -1,
                )

            circle_intensity = cv2.mean(blur, mask=mask)[0]

            if circle_intensity < min_intensity:
                marked_circle_index.append(j)
                if not ans[i]:
                    continue
                elif ans[i] - 1 != j:
                    cv2.circle(
                        image,
                        (
                            round((2 * x + (2 * j + 1) * w / 4) / 2),
                            round((2 * y + (2 * i + 1) * h / n) / 2),
                        ),
                        circle_radius,
                        (0, 0, 255),
                        -1,
                    )
                else:
                    cv2.circle(
                        image,
                        (
                            round((2 * x + (2 * j + 1) * w / 4) / 2),
                            round((2 * y + (2 * i + 1) * h / n) / 2),
                        ),
                        circle_radius,
                        (255, 0, 0),
                        -1,
                    )
        if ans[i] > 0:
            if len(marked_circle_index) > 1:
                marked_index.append(-1)
                if isNegative:
                    marks -= negativeMark
            elif len(marked_circle_index) == 0:
                marked_index.append(0)
            else:
                marked_index.append(marked_circle_index[0] + 1)
                if ans[i] - 1 != marked_circle_index[0]:
                    if isNegative:
                        marks -= negativeMark
                else:
                    marks += markPerQuestion
        elif ans[i] < 0:
            if len(marked_circle_index) > 0:
                if len(marked_circle_index) > 1:
                    marked_index.append(-1)
                else:
                    marked_index.append(marked_circle_index[0] + 1)
                if ans[i] == -2:
                    marks += markPerQuestion
                if ans[i] == -4 or ans[i] == -5:
                    marks -= negativeMark
            else:
                marked_index.append(0)
                if ans[i] == -2 or ans[i] == -3 or ans[i] == -5:
                    marks += markPerQuestion
    # print(f"For {n}'s Box: ", marked_index)

    return marks
