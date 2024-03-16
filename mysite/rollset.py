from mysite.area import findArea
from mysite.detect import detectSquares
from mysite.find import findSquares
from mysite.imgpre import imagePreprocess
from mysite.index import boxIndex
from mysite.rollbox import checkRoll
from mysite.setbox import checkSet


def getRollSet(
    image_path,
    totalQuestions,
    isRoll,
    digits,
    numSet,
    outputpath,
):
    image, blur, contours = imagePreprocess(image_path)

    if totalQuestions > 35:
        totalQuestions = 35

    q2Index, q1Index, rollIndex, setIndex, markIndex, box = boxIndex(
        totalQuestions, isRoll, numSet
    )

    squares = findSquares(contours)
    areaList, areaListSort = findArea(squares)
    if len(squares) != box:
        detectSquares(outputpath, image, squares)
        return (
            "Page-1 Doesn't Match With The Given Info! Expected "
            + str(box)
            + " Box, Got "
            + str(len(squares))
            + " Box!",
            -1,
            -1,
            image,
            blur,
            areaList,
            areaListSort,
            squares,
            q1Index,
            q2Index,
            markIndex,
        )

    idno = -1
    if isRoll:
        marked_index, x, y, w, h = checkRoll(
            digits, image, blur, areaList, areaListSort, squares, rollIndex
        )
        roll = ""
        for i in marked_index:
            if i == -1:
                break
            roll += str(i)
        if len(roll) == digits:
            idno = roll
        else:
            detectSquares(outputpath, image, squares, x, y, w, h)
            return (
                "ID Number is Less Than " + str(digits) + " Digits!",
                -1,
                -1,
                image,
                blur,
                areaList,
                areaListSort,
                squares,
                q1Index,
                q2Index,
                markIndex,
            )

    setno = 1
    if numSet > 1:
        marked_circle_index, x, y, w, h = checkSet(
            image, blur, areaList, areaListSort, squares, setIndex, numSet
        )
        if len(marked_circle_index) > 1:
            detectSquares(outputpath, image, squares, x, y, w, h)
            return (
                "Multiple Set is Marked!",
                -1,
                -1,
                image,
                blur,
                areaList,
                areaListSort,
                squares,
                q1Index,
                q2Index,
                markIndex,
            )
        elif len(marked_circle_index) == 0:
            detectSquares(outputpath, image, squares, x, y, w, h)
            return (
                "No Set is Marked!",
                -1,
                -1,
                image,
                blur,
                areaList,
                areaListSort,
                squares,
                q1Index,
                q2Index,
                markIndex,
            )
        else:
            setno = marked_circle_index[0] + 1

    return (
        "OK",
        idno,
        setno,
        image,
        blur,
        areaList,
        areaListSort,
        squares,
        q1Index,
        q2Index,
        markIndex,
    )
