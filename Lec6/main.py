from app import app, db 
from app.models import User, Post 


@app.shell_context_processor
def make_shell_context():
    return {
        'db' : db, 
        'app' : app, 
        'Post' : Post,
        'User' : User,
    }

