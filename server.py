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


def get_search_args(form):
    """Return a dict of the non-null form values for build search"""
    """ex1. {'level' : {'min' : 5, 'max' : 50}}"""
    """ex2. {'build_name' : 'eca build'}"""

    build_search_args = {}
    non_min_max_params = ['build_name', 'character_class_id',
                          'main_role', 'content_type']
    param_lists = ['mastery_element', 'mastery_type',
                   'main_role', 'content_type']

    for key in crud.BUILD_SEARCH_PARAMS_DICT:
        min_key = 'min_' + key
        max_key = 'max_' + key
        
        if form.get(key):
            if key == 'build_name':
                form_stat = form.get(key)
                build_search_args.update({key : form_stat})
            elif key in param_lists:
                form_stat_list = form.getlist(key)
                # First time trying list comprehension
                form_stat_list_ints = [int(i) for i in form_stat_list]
                build_search_args.update({key : form_stat_list_ints})
            else:
                form_stat = int(form.get(key))
                build_search_args.update({key : form_stat})
        if key == 'elemental_mastery':
            element_list = form.getlist('mastery_element')
            build_search_args[key] = build_search_args.get(key, {})
            build_search_args[key]['mastery_element'] = build_search_args[key].get(
                'mastery_element', [])
            build_search_args[key]['mastery_element'].extend(element_list)
        if key == 'elemental_res':
            element_list = form.getlist('res_element')
            build_search_args[key] = build_search_args.get(key, {})
            build_search_args[key]['res_element'] = build_search_args[key].get(
                'res_element', [])
            build_search_args[key]['res_element'].extend(element_list)
        if form.get(min_key):
            min_stat = int(form.get(min_key))
            build_search_args[key] = build_search_args.get(key, {})
            build_search_args[key].update({'min' : min_stat})
        if form.get(max_key):
            max_stat = int(form.get(max_key))
            build_search_args[key] = build_search_args.get(key, {})
            build_search_args[key].update({'max' : max_stat})

    return build_search_args
            

@app.context_processor
def inject_main_stats_max_level_and_name_translations():

    main_stats_order = ['hp', 'ap', 'mp', 'wp', 'armor', 'spell_range']
    elemental_mastery_order =['fire_mastery', 'water_mastery',
                              'earth_mastery', 'air_mastery']
    elemental_res_order = ['fire_res', 'water_res',
                           'earth_res', 'air_res']
    battle_stat_order = ['dmg_inflicted', 'heals_performed',
                         'crit_hit', 'block',
                         'initiative', 'spell_range',
                         'dodge', 'lock',
                         'wisdom', 'prospecting',
                         'control', 'force_of_will']
    secondary_stat_order = ['crit_mastery', 'crit_res',
                            'rear_mastery', 'rear_res',
                            'melee_mastery', 'armor_given',
                            'distance_mastery', 'armor_received',
                            'healing_mastery', 'indirect_dmg',
                            'berserk_mastery', 'barrier']
    equip_order = ['helmet', 'cape', 'amulet', 'epaulettes',
                   'breastplate', 'belt', 'ring1', 'ring2',
                   'boots', 'off_hand', 'main_hand', 'two_hand',
                   'emblem', 'pet', 'mount']
    intelligence_order = ['intelligence', 'hp_percentage',
                          'elemental_res', 'barrier',
                          'heals_received', 'armor']
    strength_order = ['strength', 'elemental_mastery',
                      'melee_mastery', 'distance_mastery',
                      'hp']
    agility_order = ['agility', 'lock',
                     'dodge', 'initiative',
                     'lock_dodge', 'force_of_will']
    fortune_order = ['fortune', 'crit_hit',
                     'block', 'crit_mastery',
                     'rear_mastery', 'berserk_mastery',
                     'healing_mastery', 'rear_res',
                     'crit_res']
    major_order = ['major', 'ap',
                   'mp', 'spell_range',
                   'wp', 'control',
                   'dmg_inflicted', 'resistance']
    
    max_level = crud.MAX_LEVEL

    get_browser_lang()
    character_classes = crud.get_character_classes()
    # translations = 

    return dict(main_stats_order=main_stats_order,
                elemental_mastery_order=elemental_mastery_order,
                elemental_res_order=elemental_res_order,
                battle_stat_order=battle_stat_order,
                secondary_stat_order=secondary_stat_order,
                equip_order=equip_order,
                max_level=max_level,
                character_classes=character_classes,
                intelligence_order=intelligence_order,
                strength_order=strength_order,
                agility_order=agility_order,
                fortune_order=fortune_order,
                major_order=major_order)



@app.route('/')
def homepage():

    if 'user_id' in session:
        return redirect(f"/user/{session['user_id']}")
    
    if session.get('build_search_params'):
        session['build_search_params'] = None

    # builds = None
    # if not session.get('build_results'):
    #     builds = crud.get_public_builds()
    # else:
    #     builds = session.get('build_results')
    
    # session['build_stats'] = {}
    # for build in builds:
    #     stats = crud.get_total_stats_by_build(build)
    #     session['build_stats'].update({build.id : stats})

    # builds = None
    # if not session.get('build_results'):
    #     builds_and_base_stats = crud.get_public_builds_with_base_stats()
    #     builds = []
    #     for combo in builds_and_base_stats:
    #         # Combo is tuple (build.model, Base_stat.model)
    #         crud.set_build_with_total_stats_by_build_and_base_stats(combo)
    #         # Add build instance to build list
    #         builds.append(combo[0])
    # else:
    #     builds = session.get('build_results')
    
    builds_and_base_stats = crud.get_public_builds_with_base_stats()
    builds = []
    for combo in builds_and_base_stats:
        # Combo is tuple (build.model, Base_stat.model)
        crud.set_build_with_total_stats_by_build_and_base_stats(combo)
        # Add build instance to build list
        builds.append(combo[0])

    return render_template('homepage.html', builds=builds)


@app.route('/search_builds')
def search_results():
    # session['request_args'] = request.args
    
    # session['build_params'] = get_search_args(request.args)

    # result_ids = crud.get_build_ids_with_search_params(
    #     session['build_stats'], session['build_params'])
    # ###
    # session['result_ids'] = result_ids
    # ###
    # session['build_results'] = []

    # for result_id in result_ids:
    #     session['build_results'].append(crud.get_build_by_id(result_id))

    
    session['build_search_params'] = get_search_args(request.args)

    # session['build_results'] = []

    # if session.get('public_builds'):
    #     for build in session['public_builds']:
    #         if crud.is_build_result(build, session['build_search_params']):
    #             session['build_results'].append(build)

    builds_and_base_stats = crud.get_public_builds_with_base_stats()
    builds = []
    for combo in builds_and_base_stats:
        # Combo is tuple (build.model, Base_stat.model)
        crud.set_build_with_total_stats_by_build_and_base_stats(combo)
        build = combo[0]
        if crud.is_build_result(build, session['build_search_params']):
            # Add build instance to build list
            builds.append(build)

    
    return render_template('homepage.html', builds=builds)
    


@app.route('/user/<user_id>')
def get_user(user_id):
    user = crud.get_user_by_id(user_id)
    session['user_builds'] = crud.get_builds_by_user(user.id)

    return render_template('user_builds.html', 
                           user=user, builds=session['user_builds'])


@app.route('/new_build')
def create_new_build():

    build = None
    if 'user_id' in session:
        build = crud.create_build(user=session['user'])
    else:
        build = crud.create_build()

    db.session.add(build)
    db.session.commit()

    return redirect(f'/build/{build.id}')


@app.route('/update_build')
def update_build():

    build = build

    return redirect(url_for('/build', build_id=build.id))


@app.route('/build/<build_id>')
def get_build(build_id):

    combo = crud.get_build_characteristic_cap_base_stat_by_build_id(build_id)
    build = combo[0]
    base_stats = combo[2]
    characteristic_caps = combo[1]
    session['equipment_search_params'] = None
    
    crud.set_build_with_total_stats_by_build_and_base_stats(
        tuple([build, base_stats]))

    return render_template('build.html', build=build,
                           base_stats=base_stats,
                           characteristic_caps=characteristic_caps)

@app.route('/search_equipments', methods=['POST'])
def get_equipment_results():

    session['equipment_search_params'] = get_search_args(request.json)
    build_id = request.form.get('build_id')

    equips = crud.get_equipments_by_search_params_and_language(
        session['equipment_search_params'], session['lang'])
    
    combo = crud.get_build_characteristic_cap_base_stat_by_build_id(build_id)
    build = combo[0]
    base_stats = combo[2]
    characteristic_caps = combo[1]
    
    crud.set_build_with_total_stats_by_build_and_base_stats(
        tuple([build, base_stats]))

    
    return render_template('build.html', build=build,
                           base_stats=base_stats,
                           characteristic_caps=characteristic_caps,
                           equipments=equips)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)