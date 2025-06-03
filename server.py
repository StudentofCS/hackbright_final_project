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


def get_build_search_args(form):
    """Return a dict of the non-null form values for build search"""

    build_search_args = {}

    for key, value in form.items():
        if form.get(key):
            pass
            

@app.context_processor
def inject_main_stats_max_level_and_name_translations():

    main_stats = ['ap', 'mp', 'wp', 'spell_range']
    max_level = crud.MAX_LEVEL
    # translations = 

    return dict(main_stats=main_stats, 
                max_level=max_level)



@app.route('/')
def homepage():
    get_browser_lang()
    character_classes = crud.get_character_classes()

    if 'user_id' in session:
        return redirect(f"/user/{session['user_id']}")

    builds = crud.get_builds()
    
    build_stats = {}
    for build in builds:
        stats = crud.get_total_build_stats(build)
        build_stats.update({build.id : stats})
    
    return render_template('homepage.html', builds=builds, 
                           character_classes=character_classes,
                           build_stats=build_stats)


@app.route('/search')
def search_results():
    min_level = request.args.get('min_level')
    max_level = request.args.get('max_level')

    if min_level == "" and max_level == "":
        print('Both empty')
    
    elif min_level != "" and max_level != "":
        print(f'Level: {min_level} to {max_level}')

    elif min_level != "":
        print(f'Min_level: {min_level}')

    elif max_level != "":
        print(f'Max_level: {max_level}')

    session['build_results'] = crud.get_builds()

    
    return redirect('/')
    


@app.route('/user/<user_id>')
def get_user(user_id):
    user = crud.get_user_by_id(user_id)
    builds = crud.get_builds_by_user(user.id)

    return render_template('user_builds.html', user=user, builds=builds)


@app.route('/new_build')
def create_new_build():
    if request.form.get(session['user']):
        build = crud.create_build(user=session['user'])
    
    else:
        build = crud.create_build()

    return render_template('build.html', build=build)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)