"""Server for character builder app"""

from flask import (Flask, render_template, request, flash, 
                   session, redirect, jsonify, url_for)
from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud
import helpers
import schemas


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
                # form_stat_list = form.getlist(key)
                form_stat_list = form.get(key)
                # First time trying list comprehension
                form_stat_list_ints = [int(i) for i in form_stat_list]
                build_search_args.update({key : form_stat_list_ints})
            else:
                form_stat = int(form.get(key))
                build_search_args.update({key : form_stat})
        if key == 'elemental_mastery':
            if form.get(key):
                # element_list = form.getlist('mastery_element')
                element_list = form.get('mastery_element')
                build_search_args[key] = build_search_args.get(key, {})
                build_search_args[key]['mastery_element'] = build_search_args[key].get(
                    'mastery_element', [])
                build_search_args[key]['mastery_element'].extend(element_list)
        if key == 'elemental_res':
            if form.get(key):
                # element_list = form.getlist('res_element')
                element_list = form.get('res_element')
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

def get_search_api_args(form):
    """Return a dict of the non-null form values from build search params"""

    params_dict = {}

    for param in form:
        value = form.get(param)
        # Only non-null values
        if value:
            if param.startswith('min_'):
                value = int(value)
                key = param[4:]
                params_dict[key] = params_dict.get(key, {})
                params_dict[key].update({'min' : value})
            elif param.startswith('max_'):
                value = int(value)
                key = param[4:]
                params_dict[key] = params_dict.get(key, {})
                params_dict[key].update({'max' : value})
            elif isinstance(value, list):
                params_dict[param] = params_dict.get(param, [])
                params_dict[param].extend(value)
            else:
                params_dict[param] = params_dict.get(param, value)

    return params_dict


            

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
                   'boots', 'main_hand', 'off_hand', 'two_hand',
                   'emblem', 'pet', 'mount']
    intelligence_order = crud.INTELLIGENCE_ORDER
    strength_order = crud.STRENGTH_ORDER
    agility_order = crud.AGILITY_ORDER
    fortune_order = crud.FORTUNE_ORDER
    major_order = crud.MAJOR_ORDER
    equip_stat_order = ['ap', 'mp', 'wp', 'hp',
                        ]
    
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

    # combo = crud.get_build_characteristic_cap_base_stat_by_build_id(build_id)
    # build = combo[0]
    # base_stats = combo[2]
    # characteristic_caps = combo[1]
    
    # crud.set_build_with_total_stats_by_build_and_base_stats(
    #     tuple([build, base_stats]))

    session['equipment_search_params'] = None
    b, bs, cc = helpers.get_build_base_stats_char_caps_by_build_id(build_id)

    cc = schemas.CharacteristicCapSchema().dump(cc)
    char_multipliers = crud.CHARACTERISTIC_MULTIPLIERS_DICT

    return render_template('build.html', build=b,
                           base_stats=bs,
                           characteristic_caps=cc,
                           char_multipliers=char_multipliers)

    


@app.route('/search_equipments', methods=['POST'])
def get_equipment_results():

    session['equipment_search_params'] = get_search_args(request.form)
    build_id = request.form.get('build_id')

    equips = crud.get_equipments_by_search_params_and_language(
        session['equipment_search_params'], session['lang'])
    
    combo = crud.get_build_characteristic_cap_base_stat_by_build_id(build_id)
    build = combo[0]
    build_dict = schemas.BuildSchema().dump(build)
    base_stats = combo[2]
    characteristic_caps = combo[1]
    
    crud.set_build_with_total_stats_by_build_and_base_stats(
        tuple([build, base_stats]))

    
    return render_template('build.html', build=build,
                           base_stats=base_stats,
                           characteristic_caps=characteristic_caps,
                           equipments=equips,
                           build_dict=build_dict)


@app.route('/api/equip_search', methods=['POST'])
def get_equip_results():

    session['equipment_search_params'] = get_search_args(request.json)

    equips_and_names = crud.get_equipments_by_search_params_and_language(
        session['equipment_search_params'], session['lang'])
    
    equip_dict_list = []
    name_dict = {}

    if equips_and_names:
        equip_schema = schemas.EquipmentSchema()
        name_schema = schemas.NameTranslationSchema()

        for equip, name in equips_and_names:
            equip_dict_list.append(equip_schema.dump(equip))
            name_dict.update({name.name_id : name_schema.dump(name)})

    return jsonify(equip_dict_list, name_dict)


@app.route('/api/add_equip', methods=['POST'])
def update_equip():

    # # equip = request.json.get('equip')
    # build = request.json.get('build')

    # # print(f'\n\n{equip}\n\n')
    # print(f'\n\n{build}\n\n')

    # e_schema = schemas.EquipmentSchema()
    # b_schema = schemas.BuildSchema(load_instance=False)

    # # print(f'\n\n{type(equip)}\n\n')
    # print(f'\n\n{type(build)}\n\n')

    # data = request.get_json()
    # print(f'\n\n{data}\n\n')

    build_id = request.json.get('build_id')
    equip_id = request.json.get('equip_id')

    build = crud.get_build_by_id(int(build_id))
    equip = crud.get_equipment_by_id(int(equip_id))

    # Add the equipment only if it's level appropriate for build
    if equip.level <= build.level:
        crud.update_equipment_set_by_build_equipment(build, equip)
        db.session.commit()

    set_schema = schemas.EquipmentSetSchema()
    equip_set = set_schema.dump(build.equipment_set)

    totals_build = helpers.get_total_build_stats_by_build_id(build_id)
    total_stats_dict = helpers.get_total_stats_dict_by_build(totals_build)
    
    return jsonify(equip_set=equip_set,
                   stat_totals=total_stats_dict)


@app.route('/api/update_characteristic', methods=['POST'])
def update_characteristics():

    char_name = request.json.get('characteristic')
    points = int(request.json.get('points'))
    build_id = request.json.get('build_id')
    section = request.json.get('section')

    # Get needed query results and update the characteristics
    characteristic, char_cap = crud.get_characteristic_and_characteristic_cap_by_build_id(build_id)
    # crud.verify_and_update_characteristic_section(characteristic, char_cap)
    # db.session.commit()
    crud.update_characteristics_by_characteristic_and_points(
        characteristic, section, char_name, points, char_cap)
    db.session.commit()

    crud.verify_and_update_characteristic_section(characteristic, char_cap)
    db.session.commit()
    
    # Serialize the data models
    characteristic = schemas.CharacteristicSchema().dump(characteristic)
    char_cap = schemas.CharacteristicCapSchema().dump(char_cap)
    
    # Get the updated stat totals after the characteristic change
    totals_build = helpers.get_total_build_stats_by_build_id(build_id)
    total_stats_dict = helpers.get_total_stats_dict_by_build(totals_build)

    return jsonify(char_cap=char_cap,
                   characteristic=characteristic,
                   stat_totals=total_stats_dict)


@app.route('/api/update_level', methods=['POST'])
def update_level():
    
    build_id = request.json.get('build_id')
    level = request.json.get('level')

    crud.update_level_by_build_id(build_id, level)
    db.session.commit()

    characteristic, char_cap = crud.get_characteristic_and_characteristic_cap_by_build_id(build_id)
    
    # Serialize the data models
    characteristic = schemas.CharacteristicSchema().dump(characteristic)
    char_cap = schemas.CharacteristicCapSchema().dump(char_cap)
    
    # Get the updated stat totals after the characteristic change
    totals_build = helpers.get_total_build_stats_by_build_id(build_id)
    total_stats_dict = helpers.get_total_stats_dict_by_build(totals_build)

    return jsonify(char_cap=char_cap,
                   characteristic=characteristic,
                   stat_totals=total_stats_dict)


@app.route('/api/update_role_and_content', methods=['POST'])
def update_role_and_content():

    build_id = request.json.get('build_id')
    category = request.json.get('type')
    value = request.json.get('value')

    crud.update_role_or_content_by_build_id(build_id, category, value)
    db.session.commit()
    return '', 204


@app.route('/api/update_build_name', methods=['POST'])
def update_build_name():

    build_id = request.json.get('build_id')
    build_name = request.json.get('build_name')

    crud.update_build_name_by_build_id(build_id, build_name)
    db.session.commit()
    return '', 204


@app.route('/api/update_class', methods=['POST'])
def update_class():

    build_id = request.json.get('build_id')
    class_id = int(request.json.get('class_id'))

    build = crud.get_build_by_id(build_id)

    crud.update_build_class_by_build(build, class_id)
    db.session.commit()

    char_class = crud.get_character_class_by_id(class_id)

    build = schemas.BuildSchema().dump(build)
    if char_class:
        char_class = schemas.CharacterClassSchema().dump(char_class)
    else:
        char_class = {}

    # Get the updated stat totals
    totals_build = helpers.get_total_build_stats_by_build_id(build_id)
    total_stats_dict = helpers.get_total_stats_dict_by_build(totals_build)

    return jsonify(build=build,
                   char_class=char_class,
                   stat_totals=total_stats_dict)


@app.route('/api/update_selected_elements', methods=['POST'])
def update_selected_elements():

    build_id = request.json.get('build_id')
    position = request.json.get('position')
    element_id = request.json.get('element_id')

    crud.update_selected_elements_by_build_id(build_id, position, element_id)
    db.session.commit()

    build, char_class = crud.get_build_and_char_class_by_build_id(build_id)

    build = schemas.BuildSchema().dump(build)
    if char_class:
        char_class = schemas.CharacterClassSchema().dump(char_class)

    # Get the updated stat totals
    totals_build = helpers.get_total_build_stats_by_build_id(build_id)
    total_stats_dict = helpers.get_total_stats_dict_by_build(totals_build)

    return jsonify(build=build,
                   char_class=char_class,
                   stat_totals=total_stats_dict)


@app.route('/api/initialize_build_info', methods=['POST'])
def initialize_build_info():
    build_id = request.json.get('build_id')

    build, char_class, char_cap = crud.get_build_and_char_class_char_cap_by_build(build_id)

    crud.verify_and_update_characteristic_section(
        build.characteristic, char_cap)
    db.session.commit()

    build = schemas.BuildSchema().dump(build)
    char_cap = schemas.CharacteristicCapSchema().dump(char_cap)
    if char_class:
        char_class = schemas.CharacterClassSchema().dump(char_class)
    

    # Get the updated stat totals
    totals_build = helpers.get_total_build_stats_by_build_id(build_id)
    total_stats_dict = helpers.get_total_stats_dict_by_build(totals_build)

    return jsonify(build=build,
                   char_class=char_class,
                   stat_totals=total_stats_dict,
                   char_cap=char_cap)


@app.route('/api/get_search_results')
def get_build_search_results():

    params_dict = get_search_api_args(request.args)

    build_totals_list = crud.get_api_build_search_results(params_dict)
    build_totals_dict_list = []

    for build in build_totals_list:
        build = helpers.get_total_stats_dict_by_build(build)
        build_totals_dict_list.append(build)

    name_translations = crud.get_name_translations()
    translations = helpers.get_name_translations_dict(
        name_translations, session['lang'])

    return jsonify(build_totals_list = build_totals_dict_list,
                   translations = translations)





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)