from app import app
from waitress import serve

serve(app, listen='*:5000')

'''
if __name__ == "__main__":
    app.run(debug=True)
'''