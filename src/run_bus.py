from flaskapp_bus import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1099, threaded=True)

