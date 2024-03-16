import cv2

from mysite.questionbox import checkQuestions
from mysite.xywh import infoSquare


def evaluate1(
    totalQuestions,
    markPerQuestion,
    isNegative,
    negativeMark,
    ansList,
    outputpath,
    mark,
    image,
    blur,
    areaList,
    areaListSort,
    squares,
    q1Index,
    q2Index,
    markIndex,
    setno,
):
    marks = 0
    if totalQuestions - 15 < 0:
        questions = totalQuestions
        totalQuestions = 0
    else:
        questions = 15
        totalQuestions -= 15
    marks += checkQuestions(
        questions,
        ansList[setno - 1][0],
        isNegative,
        image,
        blur,
        areaList,
        areaListSort,
        squares,
        q1Index,
        15,
        markPerQuestion,
        negativeMark,
    )

    if totalQuestions - 20 < 0:
        questions = totalQuestions
        totalQuestions = 0
    else:
        questions = 20
        totalQuestions -= 20
    if questions > 0:
        marks += checkQuestions(
            questions,
            ansList[setno - 1][1],
            isNegative,
            image,
            blur,
            areaList,
            areaListSort,
            squares,
            q2Index,
            20,
            markPerQuestion,
            negativeMark,
        )

    x, y, _, h = infoSquare(areaList, areaListSort, squares, markIndex)
    cv2.putText(
        image,
        f"{marks+mark}",
        (x, y + int(h / 1.4)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 0),
        2,
    )

    cv2.imwrite(outputpath, image)
    return marks
