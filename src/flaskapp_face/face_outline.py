import os
import requests
from uuid import uuid4
from PIL import Image


def find_face():
    STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

    naver_url = "https://openapi.naver.com/v1/vision/face"
    headers = {'X-Naver-Client-Id': '552ZS6v_QNFGoGORaPaD', 'X-Naver-Client-Secret': 'aLtCyh2VbL'}
    files = {'image': open(os.path.join(STATIC_DIR, 'dummy_img.jpg'), 'rb')}

    response = requests.post(url=naver_url, files=files, headers=headers)
    assert response.status_code // 100 == 2

    people_info = response.json()['faces']
    img: Image.Image = Image.open(os.path.join(STATIC_DIR, 'dummy_img.jpg'))

    uuid_filenames = []
    for person in people_info:
        (x, y, w, h) = person['roi'].values()
        shape = (x - 0.33 * w, y - 0.33 * h, x + 1.33 * w, y + 1.33 * h)
        face_img = img.crop(shape)
        face_resized = face_img.resize((400, 400), resample=4)

        uuid_filename = str(uuid4())
        face_resized.save(os.path.join(STATIC_DIR, f'face_{uuid_filename}.jpg'))
        uuid_filenames.append(uuid_filename)

    return uuid_filenames
