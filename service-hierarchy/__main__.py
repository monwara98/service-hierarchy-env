from service_hierarchy.app import app

if __name__ == '__main__':
    try: 
        # i was only using port 9999 because port 5000 (default port) seemed to already be in
        # use on my computer. feel free to change it back to 5000, or just take off the port
        # specifics in general. if you take off the port specifics you probably won't need a 
        # try-catch block
        app.run(port=9999,debug=True)
    except Exception as e:
        app.run(debug=True)
