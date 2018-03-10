# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 10:27:14 2015

@author: joe
"""
import re
import xlrd
import os
from flask import Flask, request, url_for, render_template
from werkzeug import secure_filename

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')
ALLOWED_EXTENSIONS = set(['txt', 'html', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/joe5006/mysite/upload'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def match_list(list1, list2):
    for l1 in list1:
        for l2 in list2:
            if l1 == l2:
                return True
    return False

def match_list_order(list1, list2):
    # Assume true
    flag = True
    for l1, l2 in zip(list1, list2):
        # one not equal, then not match
        if l1 != l2:
            flag = False

    return flag


def check_black_list(list_file, black_list_file):
    #############
    # Authors List
    #############
    import re

    with open(list_file, 'r') as f:
        lines = f.readlines()

    offset = 2
    names_cec = []
    paper_id = []
    for l in lines[2:]:
        splited_text = re.split('\s{2}', l)
        names_cec.append(splited_text[0])
        paper_id.append(splited_text[-1].strip())

    #############
    # Black List
    #############
    data = xlrd.open_workbook(black_list_file)

    data.sheet_names()

    table = data.sheets()[0]

    names_black_list = []
    address_black_list = []
    paper_black_list = []

    begin_row = 8

    for i in range(begin_row, table.nrows):
        cell = table.row(i)
        if cell[2].value != '':
            names_black_list.append(cell[2].value)
            address_black_list.append(cell[3].value)
            paper_black_list.append(cell[4].value)






    #############
    #  Match
    #############
    info = []
    for i in range(len(names_cec)):
        flag = False
        name_full = names_cec[i]
        paper_ids = paper_id[i]
        names_splited = name_full.split(', ')
        # match black list
        for j in range(len(names_black_list)):
            name_black_full = names_black_list[j]
            name__black_full_splited = name_black_full.split(', ')
            if match_list_order(names_splited, name__black_full_splited):
                name1 = ' '.join(names_splited)
                line1 = i + offset

                name2 = ' '.join(name__black_full_splited)
                line2 = j + 1

                print("cec2018 :{} ({}) matched blacklist: {} ({})".format(name1, line1, name2, line2))
                print(address_black_list[j])
                print()
                info.append([name1, line1, name2, line2, address_black_list[j], paper_black_list[j]])
    return info



def process(file1):
    # import pdb
    # pdb.set_trace()

    ff1 = file1
    ff2 = '/home/joe5006/mysite/blacklist.xls'

    info = check_black_list(list_file=ff1, black_list_file=ff2)

    return info


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploadedFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploadedFile)


            ## Function Here
            try:
                info = process(uploadedFile)
                return render_template('UploadSuccessed.html', info=info)
            except Exception as e:
                # raise e
                return render_template('Error.html')

            # import pdb; pdb.set_trace()

    return render_template('fileUpload.html')

'''
if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=4000)
'''
