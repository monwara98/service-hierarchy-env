from service_hierarchy.app import app

if __name__ == '__main__':
    try:
        app.run(port=9999,debug=True)
    except Exception as e:
        app.run(debug=True)