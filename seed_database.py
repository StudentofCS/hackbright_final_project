"""Seed the equipments, spells, passives, and name_translations tables with data"""

import crud
import json
import os
import re

from model import db, connect_to_db
from server import app

os.system("dropdb wakfuData")
os.system("createdb wakfuData")

connect_to_db(app)
app.app_context().push()
db.create_all()
    

def calculate_params_stat(params, level, index):
    """Calculate and return the params stat value"""

    stat = params[index] + (level * params[index + 1])

    return stat



def combine_dict_values_lists(dict):
    """Return a list of all the dict key value lists combined into one list"""
    all_values = []

    for value in dict.values():
        all_values.extend(list(value))

    return all_values


def get_data_from_json(filename):
    """Return the data from a JSON file."""

    with open(f'data/{filename}.json', 'r') as f1:
                return json.load(f1)


def get_ids_from_types_and_states(filename):
    """Return a dict of a parent id with a list of their children id's"""
    """Only works with equipmentItemTypes and itemTypes"""
    
    if 'Type' in filename or 'states' in filename:

        data = get_data_from_json(filename)
        # Make a dict of all ids with their parent id as the key
        ids_dict = {}

        for line in data:
            # Simplify keys
            definition = line['definition']
            line_id = definition['id']

            if 'parentId' in definition:
                parentId = definition['parentId']
                # Add id to the parentId key's list() value in dictionary
                ids_dict[parentId] = ids_dict.get(parentId, list())
                ids_dict[parentId].append(line_id)
            # If no parentId (ie. states.json file)
            else:
                ids_dict[filename] = ids_dict.get(filename, list())
                ids_dict[filename].append(line_id)

        return ids_dict
    

def get_titles_from_actions(filename):
    """Return a dict of an id and it's title/name as the value"""
    """Only works with actions"""

    if 'actions' in filename:

        data = get_data_from_json(filename)
        # Make a dict of all parent ids with their title
        titles_dict = {}

        for line in data:
            # Simplify keys
            line_id = line['definition']['id']
            title = line.get('description', {}).get('en', "") 

            # Add title to the title dict
            titles_dict[line_id] = titles_dict.get(line_id, title) 

        return titles_dict
    

def get_titles_of_states():
    """Return dict of state ids and their titles"""
    data = get_data_from_json('states')
    state_titles = {}

    for line in data:
        if 'title' in line.keys():
            id = line['definition']['id']
            title = line['title']['en']
            state_titles[id] = line.get(id, '')
            state_titles[id] = title

    return state_titles
    

def seed_all_equipments():
    """Return a list of dicts of the id, level, and stats of all the equipable equipment."""
    # The ids of the equipmentTypes that aren't wearable equipment
    non_equipment_ids = [525, 647, 837]
    equip_dicts = get_ids_from_types_and_states('equipmentItemTypes')
    equip_ids = combine_dict_values_lists(equip_dicts)
    item_data = get_data_from_json('items')
    state_titles = get_titles_of_states()

    equipment_list = []

    # Loop through all the dicts in the items data
    for line in item_data:
        equipment_dict = {}
        item_type_id = line['definition']['item']['baseParameters']['itemTypeId']
        # Check if item has a title, if not then skip (likely unfinished item)
        if 'title' not in line.keys():
             continue
        # Check if the item id is the item id for an equipable item
        if item_type_id in equip_ids and item_type_id not in non_equipment_ids:
            # Item id, level, and rarity
            id = line['definition']['item']['id']
            level = line['definition']['item']['level']
            # If pet (582) or mount (611), make max level (50)
            if item_type_id == 582 or item_type_id == 611:
                level = 50
            # The list of stats on an item
            equip_effects = line['definition']['equipEffects']
            rarity = line['definition']['item']['baseParameters']['rarity']

            equipment_dict = {'id' : id,
                              'level' : level,
                              'equip_type_id' : item_type_id,
                              # Rarity 5 = relic, 6 = souvenir, 7 = epic
                              'rarity' : rarity}
            
            # Loops through the equip effects 
            for effect in equip_effects:
                
                params = effect['effect']['definition']['params']
                if params:
                    action_id = effect['effect']['definition']['actionId']
                    # stat = action_titles[action_id]
                    # stat = stat.replace('[#1]', str(params[0]))
                    # pattern = r"\[.*?\]"
                    # stat = re.sub(pattern, "", stat)
                    stat = calculate_params_stat(params, level, 0)
                    
                    if action_id == 20:
                        equipment_dict.update({'hp' : stat})
                    if action_id == 21:
                        equipment_dict.update({'hp_neg' : stat})
                    if action_id == 26:
                        equipment_dict.update({'healing_mastery' : stat})
                    if action_id == 31:
                        equipment_dict.update({'ap' : stat})
                    if action_id == 39:
                        # if 'description' not in effect['effect'].keys():
                        #     continue
                        # if 'given' in effect['effect']['description']['en']:
                        #     equipment_dict.update({'armor_given' : stat})
                        # # If not armor given then it's armor received
                        # else:
                        #     equipment_dict.update({'armor_received' : stat})
                        if (len(params) == 6 and 
                            calculate_params_stat(params, level, 4) == 121):
                            equipment_dict.update({'armor_received' : stat})
                        if (len(params) == 6 and 
                            calculate_params_stat(params, level, 4) == 120):
                            equipment_dict.update({'armor_given' : stat})
                    if action_id == 40:
                        if (len(params) == 6 and 
                            calculate_params_stat(params, level, 4) == 121):
                            equipment_dict.update({'armor_received_neg' : stat})
                        if (len(params) == 6 and 
                            calculate_params_stat(params, level, 4) == 120):
                            equipment_dict.update({'armor_given_neg' : stat})   
                    if action_id == 41:
                        equipment_dict.update({'mp' : stat})
                    if action_id == 56:
                        equipment_dict.update({'ap_neg' : stat})
                    if action_id == 57:
                        equipment_dict.update({'mp_neg' : stat})
                    if action_id == 71:
                        equipment_dict.update({'rear_res' : stat})
                    if action_id == 80:
                        equipment_dict.update({'elemental_res' : stat})
                    if action_id == 82:
                        equipment_dict.update({'fire_res' : stat})
                    if action_id == 83:
                        equipment_dict.update({'water_res' : stat})
                    if action_id == 84:
                        equipment_dict.update({'earth_res' : stat})
                    if action_id == 85:
                        equipment_dict.update({'air_res' : stat})
                    if action_id == 90:
                        equipment_dict.update({'elemental_res_neg' : stat})
                    if action_id == 96:
                        equipment_dict.update({'earth_res_neg' : stat})
                    if action_id == 97:
                        equipment_dict.update({'fire_res_neg' : stat})
                    if action_id == 98:
                        equipment_dict.update({'water_res_neg' : stat})
                    if action_id == 100:
                        equipment_dict.update({'elemental_res_neg' : stat})
                    if action_id == 120:
                        equipment_dict.update({'elemental_mastery' : stat})
                    if action_id == 122:
                        equipment_dict.update({'fire_mastery' : stat})
                    if action_id == 123:
                        equipment_dict.update({'earth_mastery' : stat})
                    if action_id == 124:
                        equipment_dict.update({'water_mastery' : stat})
                    if action_id == 125:
                        equipment_dict.update({'air_mastery' : stat})
                    if action_id == 130:
                        equipment_dict.update({'elemental_mastery_neg' : stat})
                    if action_id == 132:
                        equipment_dict.update({'fire_mastery_neg' : stat})
                    if action_id == 149:
                        equipment_dict.update({'crit_mastery' : stat})
                    if action_id == 150:
                        equipment_dict.update({'crit_hit' : stat})
                    if action_id == 160:
                        equipment_dict.update({'spell_range' : stat})
                    if action_id == 161:
                        equipment_dict.update({'spell_range_neg' : stat})
                    if action_id == 162:
                        equipment_dict.update({'prospecting' : stat})
                    if action_id == 166:
                        equipment_dict.update({'wisdom' : stat})
                    if action_id == 168:
                        equipment_dict.update({'crit_hit_neg' : stat})
                    if action_id == 171:
                        equipment_dict.update({'initiative' : stat})
                    if action_id == 172:
                        equipment_dict.update({'initiative_neg' : stat})
                    if action_id == 173:
                        equipment_dict.update({'lock' : stat})
                    if action_id == 174:
                        equipment_dict.update({'lock_neg' : stat})
                    if action_id == 175:
                        equipment_dict.update({'dodge' : stat})
                    if action_id == 176:
                        equipment_dict.update({'dodge_neg' : stat})
                    if action_id == 177:
                        equipment_dict.update({'force_of_will' : stat})
                    if action_id == 180:
                        equipment_dict.update({'rear_mastery' : stat})
                    if action_id == 181:
                        equipment_dict.update({'rear_mastery_neg' : stat})
                    if action_id == 184:
                        equipment_dict.update({'control' : stat})
                    if action_id == 191:
                        equipment_dict.update({'wp' : stat})
                    if action_id == 192:
                        equipment_dict.update({'wp_neg' : stat})
                    # 193 and 194 are subeffects
                    if action_id == 193:
                        equipment_dict.update({'wp' : stat})
                    if action_id == 194:
                        equipment_dict.update({'wp_neg' : stat})
                    if action_id == 304:
                        # 1284 is Makabraktion Ring
                        # if stat == 1284:
                        #     equipment_dict({'level' : 100})
                        if stat == 3416:
                            equipment_dict.update({'state' : '1 AP'})
                        elif stat == 4960:
                            equipment_dict.update({'state' : '1 MP (1 Turn)'})
                        else:
                            equipment_dict.update({'state' : state_titles[int(stat)]})
                    # if action_id == 330:
                    #     # Empty as of 5/17/2025
                        
                    # if action_id == 400:
                    #     # Empty as of 5/17/2025
                    # if action_id == 843:
                    #     # Empty as of 5/17/2025
                    # if action_id == 865:
                    #     # Empty as of 5/17/2025
                    if action_id == 875:
                        equipment_dict.update({'block' : stat})
                    if action_id == 876:
                        equipment_dict.update({'block_neg' : stat})
                    if action_id == 1020:
                        equipment_dict.update({'state' : 'Reflects 10% of damage'})
                    if action_id == 1052:
                        equipment_dict.update({'melee_mastery' : stat})
                    if action_id == 1053:
                        equipment_dict.update({'distance_mastery' : stat})
                    if action_id == 1055:
                        equipment_dict.update({'berserk_mastery' : stat})
                    if action_id == 1056:
                        equipment_dict.update({'crit_mastery_neg' : stat})
                    if action_id == 1059:
                        equipment_dict.update({'melee_mastery_neg' : stat})
                    if action_id == 1060:
                        equipment_dict.update({'distance_mastery_neg' : stat})
                    if action_id == 1061:
                        equipment_dict.update({'berserk_mastery_neg' : stat})
                    if action_id == 1062:
                        equipment_dict.update({'crit_res_neg' : stat})
                    if action_id == 1063:
                        equipment_dict.update({'rear_res_neg' : stat})
                    if action_id == 1068:
                        equipment_dict.update({'random_masteries' : stat})
                        num_of_randoms = calculate_params_stat(params, level, 2)
                        equipment_dict.update({'num_random_masteries' : num_of_randoms})
                    if action_id == 1069:
                        equipment_dict.update({'random_resistances' : stat})
                        num_of_randoms = calculate_params_stat(params, level, 2)
                        equipment_dict.update({'num_random_resistances' : num_of_randoms})
                    # if action_id == 1083:
                    #     # Empty for now
                    # if action_id == 1084:
                    #     # Empty for now
                    if action_id == 2001:
                        job = calculate_params_stat(params, level, 2)
                        if job == 64:
                            equipment_dict.update({'farmer' : stat})
                        if job == 71:
                            equipment_dict.update({'lumberjack' : stat})
                        if job == 72:
                            equipment_dict.update({'herbalist' : stat})
                        if job == 73:
                            equipment_dict.update({'miner' : stat})
                        if job == 74:
                            equipment_dict.update({'trapper' : stat})
                        if job == 75:
                            equipment_dict.update({'fisherman' : stat})
                    
        
                    # subequip_effects = equip_effects['subEffects']
            
            equipment_list.append(crud.create_equipment(equipment_dict))
    
    db.session.add_all(equipment_list)
    db.session.commit()


def seed_equipment_name_translations():
    """Seed the name_translations table"""

    equips = crud.get_equipments()
    data = get_data_from_json('items')

    # Loop through equips and find them in items data
    for equip in equips:
        id = equip.id
        
        translation = {'id' : id}

        for line in data:
            line_id = line['definition']['item']['id']
            if line_id == id:
                title = line['title']
                translation.update({'en' : title['en']})
                translation.update({'fr' : title['fr']})
                translation.update({'es' : title['es']})
                translation.update({'pt' : title['pt']})

        translation_dict = crud.create_name_translation(translation)

        db.session.add(translation_dict)

    db.session.commit()


def seed_character_classes():
    """Seed all the character classes"""

    char_classes = crud.create_character_class()

    db.session.add_all(char_classes)
    db.session.commit()


def seed_characteristic_caps():
    """Seed all the characteristic caps"""

    characteristic_caps = crud.create_characteristic_cap()

    db.session.add_all(characteristic_caps)
    db.session.commit()


def seed_elements():
    """Seed the elements"""

    elements = crud.create_element()

    db.session.add_all(elements)
    db.session.commit()


def seed_base_stats():
    """Seed the base stats"""

    base_stats = crud.create_base_stat()

    db.session.add_all(base_stats)
    db.session.commit()


def seed_spell_and_passive_slot_caps():
    """Seed the spell and passive slot caps"""

    spell_slot_caps = crud.create_spell_slot_cap()
    passive_slot_caps = crud.create_passive_slot_cap()

    db.session.add_all(passive_slot_caps)
    db.session.add_all(spell_slot_caps)
    db.session.commit()


seed_all_equipments()
seed_equipment_name_translations()
seed_character_classes()
seed_characteristic_caps()
seed_elements()
seed_base_stats()
seed_spell_and_passive_slot_caps()