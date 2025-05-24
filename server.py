"""Server for character builder app"""

from flask import (Flask, render_template, request, flash, 
                   session, redirect, jsonify)
from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud


app = Flask(__name__)

app.app_context().push()
app.secret_key = "is_this_secret_enough"
app.jinja_env.undefined = StrictUndefined


def get_browser_lang():
    supported_languages = ['en', 'fr', 'es', 'pt']
    session['lang'] = request.accept_languages.best_match(supported_languages)
    if session['lang'] == None:
        session['lang'] = 'en'


@app.route('/')
def homepage():
    get_browser_lang()
    
    return render_template('homepage.html')




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)