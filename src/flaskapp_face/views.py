import io
import os
from uuid import uuid4  # 랜덤한 이름을 생성해주는 함수
from flask import render_template, request, abort, send_file
from werkzeug.utils import secure_filename
from PIL import Image
from flaskapp_face import app, USER_IMG_DIR
from flaskapp_face.find_faces import find_face


@app.route('/face/<img_file_name>')
def route_user_face(img_file_name):
    secured_file_name = secure_filename(img_file_name)
    user_file_path = os.path.join(os.path.dirname(__file__), 'user_imgs', secured_file_name)
    if not os.path.exists(user_file_path):
        return abort(404)

    return send_file(user_file_path)  # 원하는 사진(또는 파일?)을 리턴함


@app.route('/face/main')
def img_upload():
    return render_template('img_upload.html')


@app.route('/face/find', methods=['POST'])
def img_request():
    img_dict = request.files.to_dict()
    if 'image' not in img_dict:
        return abort(400)
    if img_dict['image'].filename == '':
        return abort(400)

    img_io = io.BytesIO(img_dict['image'].read())
    img: Image.Image = Image.open(img_io)

    threshold_size = 1200
    if max(img.width, img.height) > threshold_size:
        if img.width > img.height:
            img = img.resize(size=(threshold_size, int(img.height * threshold_size / img.width)))
        else:
            img = img.resize(size=(int(img.width * threshold_size / img.height), threshold_size))

    unique_dummy_name = str(uuid4())
    img.save(os.path.join(USER_IMG_DIR, f'{unique_dummy_name}.jpg'))

    your_face_info_list = find_face(unique_dummy_name)
    return render_template('img_show.html', your_face_info_list=your_face_info_list)

    # files = {'image': open(img_io, 'rb')}


@app.route('/face/tag_name', methods=['POST'])
def tag_name():
    form_dict = request.form.to_dict()

    return 1