import cv2

from mysite.area import findArea
from mysite.detect import detectSquares
from mysite.find import findSquares
from mysite.imgpre import imagePreprocess
from mysite.questionbox import checkQuestions


def evaluate2(
    image_path,
    totalQuestions,
    markPerQuestion,
    isNegative,
    negativeMark,
    ansList,
    outputpath,
    setno,
):
    image, blur, contours = imagePreprocess(image_path)

    totalQuestions -= 35
    box = 1
    if totalQuestions - 25 > 0:
        box += 1
        if totalQuestions - 47 > 0:
            box += 1

    squares = findSquares(contours)
    if len(squares) != box:
        detectSquares(outputpath, image, squares)
        return (
            "Page-2 Doesn't Match With The Given Info! Expected "
            + str(box)
            + " Box, Got "
            + str(len(squares))
            + " Box!",
            -1,
        )

    areaList, areaListSort = findArea(squares)

    marks = 0

    if totalQuestions - 25 < 0:
        questions = totalQuestions
        totalQuestions = 0
    else:
        questions = 25
        totalQuestions -= 25
    marks += checkQuestions(
        questions,
        ansList[setno - 1][2],
        isNegative,
        image,
        blur,
        areaList,
        areaListSort,
        squares,
        1,
        25,
        markPerQuestion,
        negativeMark,
    )

    if totalQuestions - 22 < 0:
        questions = totalQuestions
        totalQuestions = 0
    else:
        questions = 22
        totalQuestions -= 22
    if questions > 0:
        marks += checkQuestions(
            questions,
            ansList[setno - 1][3],
            isNegative,
            image,
            blur,
            areaList,
            areaListSort,
            squares,
            2,
            22,
            markPerQuestion,
            negativeMark,
        )

    if totalQuestions - 18 < 0:
        questions = totalQuestions
        totalQuestions = 0
    else:
        questions = 18
        totalQuestions -= 18
    if questions > 0:
        marks += checkQuestions(
            questions,
            ansList[setno - 1][4],
            isNegative,
            image,
            blur,
            areaList,
            areaListSort,
            squares,
            3,
            18,
            markPerQuestion,
            negativeMark,
        )

    cv2.imwrite(outputpath, image)
    return marks, 1
