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
db.create_all
    

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


def seed_all_equipments():
    """Return a list of dicts of the id, level, and stats of all the equipable equipment."""
    # The ids of the equipmentTypes that aren't wearable equipment
    non_equipment_ids = [525, 647, 837]
    equip_dicts = get_ids_from_types_and_states('equipmentItemTypes')
    equip_ids = combine_dict_values_lists(equip_dicts)
    item_data = get_data_from_json('items')
    action_titles = get_titles_from_actions('actions')

    equipment_list = []

    # Loop through all the dicts in the items data
    for line in item_data:
         equipment_dict = {}
         item_type_id = line['definition']['item']['baseParameters']['itemTypeId']
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
                        equipment_dict.update({'hp' : -stat})
                    if action_id == 26:
                        equipment_dict.update({'healing_mastery' : stat})
                    if action_id == 31:
                        equipment_dict.update({'ap' : stat})
                    if action_id == 39:
                        print(id, effect['effect']['description']['en'])


                # subequip_effects = equip_effects['subEffects']
    
