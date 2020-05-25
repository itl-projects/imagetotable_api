import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'labreport/api_uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', }

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from modules import main as mn


# @app.route('/demo/')
# def front():
#     return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api', methods=['GET', 'POST'])
def get_reports():
    result = {'status': False,
              'message': "GET METHOD USED",
              'data': [{
                  'result': 'Failed'
              }]}
    if request.method == 'POST':  # check if the post request has the file part
        if 'file' not in request.files:
            result.update({'message': "Parameter Missing."})
            return jsonify(result)
        file = request.files['file']  # if user does not select file, browser also
        if file.filename == '':  # submit an empty part without filename
            result.update({'message': "No File Found."})
            return jsonify(result)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print(getTxts(file.filename, 'PdfText'))
            page, label, idDict = mn.main(filename)
            data = setDict(file.filename, page, label, idDict)
            print(data)
            result.update({'status': True, 'message': "success", 'data': [data]})
            return jsonify(result)
    return jsonify(result)


def setDict(filename, page, label, idDict):
    data = {}
    data.update({'filename': filename, 'pageCount': len(page)})
    filename = filename.split('.pdf')[0]

    file_list = getTxts(filename, 'PdfText')

    for i in range(len(page)):
        innerDict = {}
        text_data = None
        page = "page" + str(i + 1)
        innerDict.update({'reportType': label[i]})
        for txt in file_list:
            if 'misc' not in txt:
                file = txt.split('Page')[1].split('.txt')[0]
            else:
                file = txt.split('Page')[1].split('.txt')[0].split('_misc')[0]
            print("File", file, "0th", file[0], "1th", file[1])
            print("i value is", i)
            if file[0] == '0' and file[1] == str(i+1):
                with open('PdfText/'+txt, 'r', encoding='utf-8', errors='ignore') as f:
                    text_data = f.read()
                break
            elif file == str(i+1):
                with open('PdfText/'+txt, 'r', encoding='utf-8', errors='ignore') as f:
                    text_data = f.read()
                break
        if text_data is None:
            text_data = "No text"
        innerDict.update({'text': text_data})
        data.update({page: innerDict})
    return data



def getTxts(filename, folder):
    path = "./"+folder + "/"
    file_list = []
    for files in os.listdir(path):
        if filename in files:
            file_list.append(files)
    return file_list


if __name__ == "__main__":
    app.run(debug=True, port=5000)
