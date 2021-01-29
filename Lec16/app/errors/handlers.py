from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404_handler(error):
    """
    Это обработчик для Not Found/Bad Request
    """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403_handler(error):
    """
    Unauth
    """
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500_handler(error):
    """
    Это обработчик для Not Found/Bad Request
    """
    return render_template('errors/500.html'), 500

"""
Так же можно описыват ьвсе остальные ошибки по статус кодам
.....
.....
"""
