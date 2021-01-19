from app import app # Из пакета app достаем объект app, который определяется в __init__.py

@app.route("/home")
@app.route('/')
def homepage():
    return "Hello Web from Decompose Solution!!"