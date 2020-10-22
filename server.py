# -*- coding:utf-8 -*-
import time
import logging
import datetime
from logging.handlers import RotatingFileHandler

import os
from werkzeug import secure_filename
from flask import Flask, url_for, send_from_directory, request, jsonify

from cccd_1 import cccd

app = Flask(__name__)
app.secret_key = 'super secret key'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

'''
    TODO: cài đặt đường dẫn
'''
PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_new_folder(local_dir):
    ''' tạo folder trong đường dẫn (local_dir)
        nếu chưa có
    '''
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

'''
    TODO: routes
'''
# @app.route('/')
# def foo():
#     ''' Ví dụ cài đặt logger
#     '''
#     ts = time.time()
#     now_date = datetime.datetime.fromtimestamp(
#         ts).strftime('%Y-%m-%d %H:%M:%S')
#     app.logger.warning('A warning occurred (%d apples)', 42)
#     app.logger.error('{time} An error occurred'.format(time=now_date))
#     app.logger.info('Info')
#     app.logger.critical('hahahah')
#     return "foo"


@app.route('/', methods = ['POST'])
def extract_cccd():
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    file = request.files['image']
    if file and allowed_file(file.filename):
        # lưu ảnh vào /uploads
        img = request.files['image']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        img.save(saved_path)
        # ocr với tên ảnh
        data = cccd(saved_path)
        # log 
        now_date = datetime.datetime.fromtimestamp(
            time.time() ).strftime('%Y-%m-%d %H:%M:%S')
        app.logger.error(
            '{date} | ocr: {file}'.format(
                date=now_date,
                file=img_name ))
        return {"result":data}
    return "Error"

@app.route('/',methods=['GET'])
def upload():
    return '''
<html>
    <body>
        <h3>test api</h3>
        <form method="POST" action="http://localhost:5000/" enctype=multipart/form-data>
            file : <input type="file" name="image"><br />
            <input type="submit" value="submit"><br />
        </form>
    </body>
</html>
'''


if __name__ == '__main__':
    # cài đặt logger
    handler = RotatingFileHandler( 
        'server.log'
        , maxBytes=1000000
        , backupCount=1
    )
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # chạy server
    app.run( host='0.0.0.0', port=5000 )