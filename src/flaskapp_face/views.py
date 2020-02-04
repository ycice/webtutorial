import io
import os
from uuid import uuid4  # 랜덤한 이름을 생성해주는 함수
from flask import render_template, request, abort, send_file, session
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from flaskapp_face import app, USER_IMG_DIR, STATIC_DIR
from flaskapp_face.find_faces import find_face


@app.route('/face/<img_file_name>')
def route_user_face(img_file_name):
    secured_file_name = secure_filename(img_file_name)
    user_file_path = os.path.join(os.path.dirname(__file__), 'user_imgs', secured_file_name)
    if not os.path.exists(user_file_path):  # exists : 경로가 존재하는지 체크해줌
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

    threshold_size = 1200  # 사진이 너무 클 경우 사이즈 줄이기
    if max(img.width, img.height) > threshold_size:
        ratio = threshold_size / max(img.width, img.height)
        img = img.resize(size=(int(img.width * ratio), int(img.height * ratio)))

    unique_dummy_name = str(uuid4())
    img.save(os.path.join(USER_IMG_DIR, f'{unique_dummy_name}.jpg'))

    your_face_info_list: list = find_face(unique_dummy_name)
    session['info_list'] = your_face_info_list
    session['img_name'] = unique_dummy_name
    return render_template('img_show.html', your_face_info_list=your_face_info_list,
                           unique_dummy_name=unique_dummy_name)


@app.route('/face/tag_name', methods=['POST'])
def tag_name():
    form_dict = request.form.to_dict()
    original_img: Image.Image = Image.open(os.path.join(USER_IMG_DIR, f"{session['img_name']}.jpg"))
    draw = ImageDraw.Draw(original_img)
    font = ImageFont.truetype(os.path.join(STATIC_DIR, 'HoonWhitecatR.ttf'), 30)
    for i in range(len(form_dict)):
        name = form_dict[f"name_{i}"]
        (x1, y1, x2, y2) = session['info_list'][i]['shape']

        # 이름적을 공간이 위에 없을 경우, 있을 경우
        if y1 < 40:
            text_location = (x1 + 15, y2 + 32)
            text_box = [(x1, y2), (x1 + min(27 * len(name), x2 - x1), y2 + 40)]
        else:
            text_location = (x1 + 15, y1 - 32)
            text_box = [(x1, y1 - 40), (x1 + min(27 * len(name), x2 - x1), y1)]

        draw.rectangle((x1, y1, x2, y2), outline="red", width=3)

        # 이름이 없을 경우, 이름을 적지 않는다.
        if name != "":
            draw.rectangle(text_box, outline="red", width=3)
            draw.text(xy=text_location, text=name, fill=(255, 255, 255), font=font)

    face_file_name = str(uuid4())
    face_file_path = os.path.join(USER_IMG_DIR, f"{face_file_name}.jpg")
    original_img.save(face_file_path)
    session.clear()
    return send_file(face_file_path)

