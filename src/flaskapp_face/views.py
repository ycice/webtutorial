import io, os, requests
from flask import render_template, request, abort
from PIL import Image
from flaskapp_face.face_outline import find_face
from flaskapp_face import app


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

    STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
    img_io = io.BytesIO(img_dict['image'].read())
    img: Image.Image = Image.open(img_io)
    img.save(os.path.join(STATIC_DIR, 'dummy_img.jpg'))

    face_count = find_face()
    count_list = range(1, face_count+1)
    return render_template('img_show.html', count_list=count_list)

    # files = {'image': open(img_io, 'rb')}
