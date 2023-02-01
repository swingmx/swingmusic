from app.api import create_api

if __name__ == '__main__':
    app = create_api()
    app.run(debug=False, threaded=True)
