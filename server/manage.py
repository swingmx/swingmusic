from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, threaded=True, host="0.0.0.0", port=9876, use_reloader=False)
