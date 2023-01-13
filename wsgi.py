from app import create_api

if __name__ == "__main__":
    app = create_api()
    app.run(debug=True, threaded=True)
