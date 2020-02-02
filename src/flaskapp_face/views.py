import io
import os
from uuid import uuid4  # 랜덤한 이름을 생성해주는 함수
from flask import render_template, request, abort, send_file
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from flaskapp_face import app, USER_IMG_DIR, STATIC_DIR
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
    return render_template('img_show.html', your_face_info_list=your_face_info_list,
                           unique_dummy_name=unique_dummy_name)

    # files = {'image': open(img_io, 'rb')}


@app.route('/face/tag_name', methods=['POST'])
def tag_name():
    form_dict = request.form.to_dict()
    people_num = len(form_dict) // 2
    original_img: Image.Image = Image.open(os.path.join(USER_IMG_DIR, f"{form_dict['unique_dummy_name']}.jpg"))
    draw = ImageDraw.Draw(original_img)
    font = ImageFont.truetype(os.path.join(STATIC_DIR, 'HoonWhitecatR.ttf'), 30)
    for i in range(people_num):
        name = form_dict[f"name_{i}"]

        # shape를 int가 들어간 tuple로 바꾸기
        shape: str = form_dict[f"shape_{i}"]
        shape = shape.replace("(", "")
        shape = shape.replace(")", "")
        shape = shape.split(",")
        for j in range(4):
            shape[j] = int(shape[j])
        (x1, y1, x2, y2) = shape

        # 이름적을 공간이 위에 없을 경우, 있을 경우
        if y1 < 40:
            text_location = (x1 + 15, y2 + 32)
            text_box = [(x1, y2), (x1 + min(27 * len(name), x2 - x1), y2 + 40)]
        else:
            text_location = (x1 + 15, y1 - 32)
            text_box = [(x1, y1 - 40), (x1 + min(30 * len(name), x2 - x1), y1)]

        draw.rectangle(shape, outline="red", width=3)

        # 이름이 없을 경우, 이름을 적지 않는다.
        if name != "":
            draw.rectangle(text_box, outline="red", width=3)
            draw.text(xy=text_location, text=name, fill=(255, 255, 255), font=font)

    face_file_name = str(uuid4())
    face_file_path = os.path.join(USER_IMG_DIR, f"{face_file_name}.jpg")
    original_img.save(face_file_path)
    return send_file(face_file_path)
