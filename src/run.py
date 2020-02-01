from flaskapp import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1099, threaded=True)  # threaded는 여러 사람이 동시 접속을 가능하게 해줌

