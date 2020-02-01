import requests, os
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
    
    num = 0
    for person in people_info:
        num += 1
        (x, y, w, h) = person['roi'].values()
        shape = (x - 0.33 * w, y - 0.33 * h, x + 1.33 * w, y + 1.33 * h)
        face_img = img.crop(shape)
        face_resized = face_img.resize((400, 400), resample=4)
        face_resized.save(os.path.join(STATIC_DIR, f'face_{num}.jpg'))

    return len(people_info)
