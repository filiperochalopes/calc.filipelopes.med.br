from app import app
from waitress import serve

serve(app, listen='0.0.0.0:5000', url_scheme='https')

'''
if __name__ == "__main__":
    app.run(debug=True)
'''