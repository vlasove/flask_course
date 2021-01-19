from app import app 
from flask import render_template

@app.route("/home")
@app.route("/")
def homepage():
    context = {}
    current_user = {'username' : 'Evgeny Petrov'}
    current_user["age"] = 32
    context["current_user"] = current_user

    
    posts = [
        "First post",
        "Second post",
        "Third post",
    ]
    context["posts"] = posts 
    return render_template('home.html', context=context)

@app.route("/info")
def info():
    return render_template("info.html")

# Из .py в .json -> из .json в .js -> из .js в .html 

