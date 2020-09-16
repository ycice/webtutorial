import io
import os
from PIL import Image
from flask import render_template, abort, jsonify, request, redirect, send_file
from werkzeug.utils import secure_filename
from flaskapp import app
from flaskapp.menus import STARBUCKS_MEUS


@app.route('/')
@app.route('/foundry')  # 두개 붙여쓰면 둘 중 어떤걸 해도 아래의 결과가 나옴
def route_foundry():
    return render_template('foundry.html')  # templates폴더 안에 있는건 import 없이 사용 가능


@app.route('/drinks')
def route_drinks():
    return render_template('drinks.html', STARBUCKS_MEUS=STARBUCKS_MEUS)


@app.route('/drinks/<int:drink_id>')  # 정수를 뒤에 받겠다는 의미. < >는 변수취급 하겠다는 의미
def route_drink_detail(drink_id: int):
    for menu in STARBUCKS_MEUS:
        if menu['product_cd'] == drink_id:
            return render_template('drink_detail.html', menu=menu)
    return abort(404)  # 404 에러를 띄운다


@app.errorhandler(404)  # 404에러 페이지 디자인
def erroe_404(e):
    return "니가 잘못했다.", 404


@app.route('/drinks/json/<int:drink_id>')
def route_drink_detail_json(drink_id: int):
    for menu in STARBUCKS_MEUS:
        if menu['product_cd'] == drink_id:
            return jsonify(menu)  # json파일로 반환
    return abort(404)


@app.route('/drinks/json_post', methods=['GET', 'POST'])
def route_drink_detail_json_post():
    form_dict = request.form.to_dict()  # 들어온 request의 form의 딕션너리부분을 읽는 것
    if 'drink_id' not in form_dict:
        return abort(400)

    drink_id: str = form_dict['drink_id']  # 여기까진 str로 받아짐
    if not drink_id.isdecimal():  # 자연수인지 판단해주는 함수. is~~는 뭐뭐인지 확인해주는 함수들
        return abort(400)

    drink_id: int = int(drink_id)  # 정수로 변환

    for menu in STARBUCKS_MEUS:
        if menu['product_cd'] == drink_id:
            return jsonify(menu)
    return abort(404)


@app.route('/drinks/search')
def route_drink_search():
    return render_template('search_drink.html')


@app.route('/drinks/search_detail', methods=['POST'])
def route_drink_search_detail():
    form_dict = request.form.to_dict()
    if 'drink_id' not in form_dict:  # /drinks/search 페이지에서 name='drink_id'를 해서 보냈기에 drink_id로 받는 것
        return abort(400)  # post로 온 정보에 drink_id에 대한 정보가 없으면 사용자 잘못이므로 400에러를 내보냄

    drink_id: str = form_dict['drink_id']  # 여기까진 str로 받아짐
    if not drink_id.isdecimal():  # 자연수인지 판단해주는 함수. is~~는 뭐뭐인지 확인해주는 함수들
        return abort(400)

    drink_id: int = int(drink_id)  # 정수로 변환

    for menu in STARBUCKS_MEUS:
        if menu['product_cd'] == drink_id:
            return redirect(f'/drinks/{menu["product_cd"]}')
    return abort(404)


@app.route('/dummy_login', methods=['GET', 'POST'])
def route_dummy_login():
    if request.method == 'GET':
        return render_template('dummy_login_form.html')
    else:
        form_dict = request.form.to_dict()
        if 'id' not in form_dict:
            return abort(400)

        file_dict = request.files.to_dict()  # request의 files에 담긴 정보를 읽는 것
        if "image" not in file_dict:
            return abort(400)
        if file_dict['image'].filename == '':  # image가 안왔을 경우 filename이 없다.
            return abort(400)

        USER_DATA_DIR = os.path.join(os.path.dirname(__file__), 'user_data')
        secured_filename = secure_filename(file_dict['image'].filename)  # 파일명을 안전한 이름으로 바꿔줌

        # io 객체 만들기(바이트로 이루어진 이미지 정보를 읽는 방법)
        img_io = io.BytesIO(file_dict['IMG'].read())  # io가 경로 역할을 대신함. read가 있어야 file form을 읽음
        pil_img: Image.Image = Image.open(img_io)  # pillow로 열은 이미지의 속성이 Image.Image

        # 원본 파일 저장
        img_original_path = os.path.join(USER_DATA_DIR, secured_filename)
        pil_img.save(img_original_path)

        # 파일 명 바꾸기 (확장자 유지)
        (fname, ext) = os.path.splitext(img_original_path)  # ext가 확장자 부분, fname이 파일 이름부분
        img_converted_path = fname + '_converted' + ext

        # 변환 및 저장
        pil_grayscale : Image.Image = pil_img.convert('L')
        pil_grayscale.save(img_converted_path)

        # IO 객체에 저장 - (아직) 안됨 ;;
        converted_io = io.BytesIO()
        pil_grayscale.save(converted_io, 'PNG')

        # 저장 없이 IO객체를 반환 - (아직) 안됨
        # return send_file(converted_io, mimetype='image/png', attachment_filename='converted.png', as_attachment=True)
        # return send_file(converted_io, mimetype='image/png')
        # return send_file(img_io, mimetype='image/png', attachment_filename='converted.png', as_attachment=True)

        # return f'{form_dict["id"]}님 환영합니다!'

        # 사진을 return값으로 반환. 즉, 화면에 사진을 띄워줌
        return send_file(img_converted_path)  # as_attachment=True로 하면 다운받는 창이 뜸


@app.errorhandler(400)
def error_400(e):
    if 'message' in e.description:
        return f"사용자 오류입니다.<BR/>{e.description['message']}", 400
    else:
        return "사용자 오류입니다", 400


@app.route('/pep')
def route_pep():
    return render_template('pep_test.html')
