"""Server for character builder app"""

from flask import (Flask, render_template, request, flash, 
                   session, redirect, jsonify, url_for)
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
    """ex1. {'level' : {'min' : 5, 'max' : 50}}"""
    """ex2. {'build_name' : 'eca build'}"""

    build_search_args = {}
    non_min_max_params = ['build_name', 'character_class',
                          'main_role', 'content_type']

    for key in crud.BUILD_SEARCH_PARAMS_DICT:

        if form.get(key):
            if key in non_min_max_params:
                form_stat = form.get(key)
                build_search_args.update(key, form_stat)
            else:
                min_key = 'min_' + key
                max_key = 'max_' + key
                if form.get(min_key):
                    min_stat = form.get(min_key)
                    build_search_args.update(key, {'min' : min_stat})
                if form.get(max_key):
                    max_stat = form.get(max_key)
                    build_search_args.update(key, {'max' : max_stat})

    return build_search_args
            

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

    if not isinstance(builds):
        builds = crud.get_public_builds()
    
    session['build_stats'] = {}
    for build in builds:
        stats = crud.get_total_build_stats(build)
        session['build_stats'].update({build.id : stats})
    
    return render_template('homepage.html', builds=builds, 
                           character_classes=character_classes)


@app.route('/search')
def search_results():
    
    search_params = get_build_search_args()

    results = crud.get_build_ids_with_search_params()

    
    return redirect(url_for('homepage',
                            builds=results))
    


@app.route('/user/<user_id>')
def get_user(user_id):
    user = crud.get_user_by_id(user_id)
    builds = crud.get_builds_by_user(user.id)

    return render_template('user_builds.html', user=user, builds=builds)


@app.route('/new_build')
def create_new_build():
    if 'user_id' in session:
        build = crud.create_build(user=session['user'])
    
    else:
        build = crud.create_build()

    return render_template('build.html', build=build)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)