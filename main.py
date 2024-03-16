import os

from flask import Flask, make_response, request, send_file
from flask_cors import CORS

from mysite.delete import deleteFiles
from mysite.evaluatePage1 import evaluate1
from mysite.evaluatePage2 import evaluate2
from mysite.file import fileSetup
from mysite.pdf import imgToPDF
from mysite.rollset import getRollSet
from mysite.split import split_list

app = Flask(__name__)
CORS(
    app,
    expose_headers=["marks", "error", "idno", "setno"],
)


@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        totalQuestions = int(request.form.get("questionsCount"))
        numSet = int(request.form.get("setCount"))
        ansList = []
        for j in range(1, numSet + 1):
            ans = []
            sizes = [15, 20, 25, 22, 18]
            for i in range(1, totalQuestions + 1):
                key = "set" + str(j) + "Q" + str(i)
                ans.append(int(request.form.get(key)))
            ansList.append(split_list(ans, sizes))

        markPerQuestion = float(request.form.get("mpq"))
        isNegative = request.form.get("isNegative") == "true"
        negativeMark = float(request.form.get("negativeMark"))
        if not isNegative:
            negativeMark = 0
        isRoll = request.form.get("isRoll") == "true"
        digits = int(request.form.get("rollDigit"))
        files = request.files.getlist("file")

        current_dir = os.path.dirname(__file__)
        (
            inputpath1,
            inputpath2,
            outputpath1,
            outputpath2,
            pdf_output,
        ) = fileSetup(files, current_dir)

        (
            msg,
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
        ) = getRollSet(
            inputpath1,
            totalQuestions,
            isRoll,
            digits,
            numSet,
            outputpath1,
        )
        if setno == -1 and idno == -1:
            imgToPDF([outputpath1], pdf_output)
            response = make_response(send_file(pdf_output, as_attachment=True))
            response.headers["error"] = msg
        elif totalQuestions > 35:
            marks2, f = evaluate2(
                inputpath2,
                totalQuestions,
                markPerQuestion,
                isNegative,
                negativeMark,
                ansList,
                outputpath2,
                setno,
            )
            if f == -1:
                imgToPDF([outputpath2], pdf_output)
                response = make_response(send_file(pdf_output, as_attachment=True))
                response.headers["error"] = marks2
            else:
                marks1 = evaluate1(
                    35,
                    markPerQuestion,
                    isNegative,
                    negativeMark,
                    ansList,
                    outputpath1,
                    marks2,
                    image,
                    blur,
                    areaList,
                    areaListSort,
                    squares,
                    q1Index,
                    q2Index,
                    markIndex,
                    setno,
                )
                imgToPDF([outputpath1, outputpath2], pdf_output)
                response = make_response(send_file(pdf_output, as_attachment=True))
                response.headers["marks"] = marks1 + marks2
                response.headers["idno"] = idno
                response.headers["setno"] = setno
        else:
            marks = evaluate1(
                totalQuestions,
                markPerQuestion,
                isNegative,
                negativeMark,
                ansList,
                outputpath1,
                0,
                image,
                blur,
                areaList,
                areaListSort,
                squares,
                q1Index,
                q2Index,
                markIndex,
                setno,
            )

            imgToPDF([outputpath1], pdf_output)
            response = make_response(send_file(pdf_output, as_attachment=True))
            response.headers["marks"] = marks
            response.headers["idno"] = idno
            response.headers["setno"] = setno

        deleteFiles(
            pdf_output,
            inputpath1,
            outputpath1,
            inputpath2,
            outputpath2,
        )
        return response

    except Exception as e:
        print(e)
        deleteFiles(
            pdf_output,
            inputpath1,
            outputpath1,
            inputpath2,
            outputpath2,
        )
        return str(e)


@app.route("/")
def index():
    return "Hello!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
