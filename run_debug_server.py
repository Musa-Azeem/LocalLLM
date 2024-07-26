from app import create_app
import sys

if __name__ == '__main__':
    app = create_app()
    if len(sys.argv) > 1 and sys.argv[1] == 'dev':
        app.run(port=8000, host='0.0.0.0', debug=False)
    else:
        app.run(port=8000, host='0.0.0.0', debug=True)