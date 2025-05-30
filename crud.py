"""Create, read, update, and delete functions for database"""

from model import (db, connect_to_db, User, Build,
                   Characteristic, Characteristic_cap,
                   Equipment_set, Equipment,
                   Element, Selected_mastery_element,
                   Equipment_random_mastery_element,
                   Selected_resistance_element,
                   Equipment_random_resistance_element,
                   Base_stat, Character_class, Spell,
                   Selected_spell, Spell_slot_cap, Passive,
                   Selected_passive, Passive_slot_cap,
                   Name_translation
                   )
from sqlalchemy import func

MAX_LEVEL = 245

EQUIPMENT_SEARCH_PARAMS_DICT = {
    'id' : None,
    'equip_type_id' : None,
    'level' : None,
    'rarity' : None,
    'hp' : None,
    'hp_neg' : None,
    'armor' : None,
    'armor_neg' : None,
    'ap' : None,
    'ap_neg' : None,
    'mp' : None,
    'mp_neg' : None,
    'wp' : None,
    'wp_neg' : None,
    'elemental_mastery' : None,
    'elemental_mastery_neg' : None,
    'water_mastery' : None,
    'water_mastery_neg' : None,
    'air_mastery' : None,
    'air_mastery_neg' : None,
    'earth_mastery' : None,
    'earth_mastery_neg' : None,
    'fire_mastery' : None,
    'fire_mastery_neg' : None,
    'elemental_res' : None,
    'elemental_res_neg' : None,
    'water_res' : None,
    'water_res_neg' : None,
    'air_res' : None,
    'air_res_neg' : None,
    'earth_res' : None,
    'earth_res_neg' : None,
    'fire_res' : None,
    'fire_res_neg' : None,
    'dmg_inflicted' : None,
    'dmg_inflicted_neg' : None,
    'crit_hit' : None,
    'crit_hit_neg' : None,
    'initiative' : None,
    'initiative_neg' : None,
    'dodge' : None,
    'dodge_neg' : None,
    'wisdom' : None,
    'wisdom_neg' : None,
    'control' : None,
    'control_neg' : None,
    'heals_performed' : None,
    'heals_performed_neg' : None,
    'block' : None,
    'block_neg' : None,
    'spell_range' : None,
    'spell_range_neg' : None,
    'lock' : None,
    'lock_neg' : None,
    'prospecting' : None, 
    'prospecting_neg' : None, 
    'force_of_will' : None, 
    'force_of_will_neg' : None, 
    'crit_mastery' : None, 
    'crit_mastery_neg' : None, 
    'rear_mastery' : None, 
    'rear_mastery_neg' : None, 
    'melee_mastery' : None, 
    'melee_mastery_neg' : None, 
    'distance_mastery' : None, 
    'distance_mastery_neg' : None, 
    'healing_mastery' : None, 
    'healing_mastery_neg' : None, 
    'berserk_mastery' : None, 
    'berserk_mastery_neg' : None, 
    'crit_res' : None, 
    'crit_res_neg' : None, 
    'rear_res' : None, 
    'rear_res_neg' : None, 
    'armor_given' : None, 
    'armor_given_neg' : None, 
    'armor_received' : None, 
    'armor_received_neg' : None, 
    'indirect_dmg' : None, 
    'indirect_dmg_neg' : None, 
    'random_masteries' : None, 
    'num_random_masteries' : None, 
    'random_resistances' : None, 
    'num_random_resistances' : None, 
    'state' : None, 
    'farmer' : None, 
    'lumberjack' : None, 
    'herbalist' : None, 
    'miner' : None, 
    'trapper' : None, 
    'fisherman' : None
    }

BUILD_SEARCH_PARAMS_DICT = {
    'build_name' : None,
    'character_class' : None,
    'level' : None,
    'hp' : None,
    'armor' : None,
    'ap' : None,
    'mp' : None,
    'wp' : None,
    'elemental_mastery' : None,
    'water_mastery' : None,
    'air_mastery' : None,
    'earth_mastery' : None,
    'fire_mastery' : None,
    'elemental_res' : None,
    'water_res' : None,
    'air_res' : None,
    'earth_res' : None,
    'fire_res' : None,
    'dmg_inflicted' : None,
    'crit_hit' : None,
    'initiative' : None,
    'dodge' : None,
    'wisdom' : None,
    'control' : None,
    'heals_performed' : None,
    'block' : None,
    'spell_range' : None,
    'lock' : None,
    'prospecting' : None, 
    'force_of_will' : None, 
    'crit_mastery' : None, 
    'rear_mastery' : None, 
    'melee_mastery' : None,
    'distance_mastery' : None,
    'healing_mastery' : None,
    'berserk_mastery' : None,
    'crit_res' : None,
    'rear_res' : None,
    'armor_given' : None,
    'armor_received' : None,
    'indirect_dmg' : None 
    }

def create_user(email, password):
    """Create and return a new user"""

    user = User(email = email, password = password)

    return user


def create_build(user=0, equipment_set=None, characteristic=None, 
                 character_class=None, level=None, build_name=None):
    """Create and return a build"""

    build = Build(user=user, equipment_set=equipment_set, 
                  characteristic=characteristic, 
                  character_class=character_class, level=level,
                  build_name=build_name)
    
    return build

# def create_characteristic(intelligence, hp_percentage, elem_res,
#                           barrier, heals_received, armor_hp,
#                           strength, elem_mastery, melee,
#                           distance, hp, agility, 
#                           lock, dodge, initiative,
#                           lock_dodge, force_of_will, fortune,
#                           crit_hit, block, crit_mastery,
#                           rear_mastery, berserk_mastery, healing_mastery,
#                           rear_res, crit_res, major,
#                           action_points, movement_points, spell_range,
#                           wakfu_points, control, dmg_inflicted,
#                           resistance):
#     """Create and return characteristic"""

#     characteristic = Characteristic(intelligence=intelligence, 
#                                     hp_percentage=hp_percentage, 
#                                     elem_res=elem_res, 
#                                     barrier=barrier, 
#                                     heals_received=heals_received, 
#                                     armor_hp=armor_hp,
#                                     strength=strength, 
#                                     elem_mastery=elem_mastery, 
#                                     melee=melee,
#                                     distance=distance, 
#                                     hp=hp, 
#                                     agility=agility, 
#                                     lock=lock, 
#                                     dodge=dodge, 
#                                     initiative=initiative,
#                                     lock_dodge=lock_dodge, 
#                                     force_of_will=force_of_will, 
#                                     fortune=fortune, 
#                                     crit_hit=crit_hit, 
#                                     block=block, 
#                                     crit_mastery=crit_mastery,
#                                     rear_mastery=rear_mastery, 
#                                     berserk_mastery=berserk_mastery, 
#                                     healing_mastery=healing_mastery,
#                                     rear_res=rear_res, 
#                                     crit_res=crit_res, 
#                                     major=major,
#                                     action_points=action_points, 
#                                     movement_points=movement_points, 
#                                     spell_range=spell_range,
#                                     wakfu_points=wakfu_points, 
#                                     control=control, 
#                                     dmg_inflicted=dmg_inflicted,
#                                     resistance=resistance)
    
#     return characteristic


def create_characteristic(dict):
    """Create and return characteristic"""

    characteristic = Characteristic(**dict)
    
    return characteristic


# def create_characteristic_cap(intelligence, hp_percentage, elem_res,
#                           barrier, heals_received, armor_hp,
#                           strength, elem_mastery, melee,
#                           distance, hp, agility, 
#                           lock, dodge, initiative,
#                           lock_dodge, force_of_will, fortune,
#                           crit_hit, block, crit_mastery,
#                           rear_mastery, berserk_mastery, healing_mastery,
#                           rear_res, crit_res, major,
#                           action_points, movement_points, spell_range,
#                           wakfu_points, control, dmg_inflicted,
#                           resistance):
#     """Create and return characteristic max values"""

#     characteristic_cap = Characteristic_cap(intelligence=intelligence, hp_percentage=hp_percentage, elem_res=elem_res,
#                           barrier=barrier, heals_received=heals_received, armor_hp=armor_hp,
#                           strength=strength, elem_mastery=elem_mastery, melee=melee,
#                           distance=distance, hp=hp, agility=agility, 
#                           lock=lock, dodge=dodge, initiative=initiative,
#                           lock_dodge=lock_dodge, force_of_will=force_of_will, fortune=fortune,
#                           crit_hit=crit_hit, block=block, crit_mastery=crit_mastery,
#                           rear_mastery=rear_mastery, berserk_mastery=berserk_mastery, healing_mastery=healing_mastery,
#                           rear_res=rear_res, crit_res=crit_res, major=major,
#                           action_points=action_points, movement_points=movement_points, spell_range=spell_range,
#                           wakfu_points=wakfu_points, control=control, dmg_inflicted=dmg_inflicted,
#                           resistance=resistance)
    
#     return characteristic_cap


def create_characteristic_cap():
    """Create and return a list of characteristic max values"""

    # Major caps 25,75,125,175
    # Intelligence, strength, agility, fortune alternate getting 1 each 
    sections = ['intelligence', 'strength', 'agility', 'fortune']
    major_caps = [25, 75, 125, 175]
    # Caps where -1 is unlimited
    characterics = {
        'level' : 1,
        'intelligence' : 0, 'hp_percentage' : -1, 'elem_res' : 10,
        'barrier' : 10, 'heals_received' : 5, 'armor_hp' : 10,
        'strength' : 0, 'elem_mastery' : -1, 'melee' : 40,
        'distance' : 40, 'hp' : -1, 'agility' : 0, 
        'lock' : -1, 'dodge' : -1, 'initiative' : 20,
        'lock_dodge' : -1, 'force_of_will' : 20, 'fortune' : 0,
        'crit_hit' : 20, 'block' : 20, 'crit_mastery' : -1,
        'rear_mastery' : -1, 'berserk_mastery' : -1, 'healing_mastery' : -1,
        'rear_res' : 20, 'crit_res' : 20, 'major' : 0,
        'action_points' : 1, 'movement_points' : 1, 'spell_range' : 1,
        'wakfu_points' : 1, 'control' : 1, 'dmg_inflicted' : 1,
        'resistance' : 1
    }

    characteristic_cap_list = [Characteristic_cap(**characterics)]
    index = 0

    for i in range(2,MAX_LEVEL + 1):
        characterics['level'] = i

        # Increase the major characteristic cap
        if i in major_caps:
            characterics['major'] += 1

        # Update cap for sections
        characterics[sections[index]] += 1
        index += 1
        characteristic_cap_list.append(Characteristic_cap(**characterics))
        # Have index loop 0-3 for sections' indices
        if index == 4:
            index = 0
    
    
    return characteristic_cap_list


# def create_equipment_set(helmet, amulet, breastplate,
#                          boots, ring1, ring2,
#                          cape, epaulettes, belt,
#                          pet, off_hand, main_hand,
#                          two_hander, emblem, mount):
#     """Create and return equipment set"""

#     equipment_set = Equipment_set(helmet=helmet, amulet=amulet, 
#                                   breastplate=breastplate, boots=boots, 
#                                   ring1=ring1, ring2=ring2,
#                                   cape=cape, epaulettes=epaulettes, 
#                                   belt=belt, pet=pet, 
#                                   off_hand=off_hand, main_hand=main_hand,
#                                   two_hander=two_hander, emblem=emblem, 
#                                   mount=mount)
    
#     return equipment_set


def create_equipment_set(dict):
    """Create and return equipment set"""

    equipment_set = Equipment_set(**dict)
    
    return equipment_set


# def create_equipment(id, equip_type_id, level,
#                      hp, hp_neg,
#                      armor, armor_neg,
#                      ap, ap_neg, 
#                      mp, mp_neg, 
#                      wp, wp_neg, 
#                      water_mastery, water_mastery_neg, 
#                      air_mastery, air_mastery_neg, 
#                      earth_mastery, earth_mastery_neg, 
#                      fire_mastery, fire_mastery_neg, 
#                      water_res, water_res_neg, 
#                      air_res, air_res_neg, 
#                      earth_res, earth_res_neg, 
#                      fire_res, fire_res_neg, 
#                      dmg_inflicted, dmg_inflicted_neg, 
#                      crit_hit, crit_hit_neg, 
#                      initiative, initiative_neg, 
#                      dodge, dodge_neg, 
#                      wisdom, wisdom_neg,
#                      control, control_neg, 
#                      heals_performed, heals_performed_neg, 
#                      block, block_neg, 
#                      spell_range, range__neg, 
#                      lock, lock_neg, 
#                      prospecting, prospecting_neg, 
#                      force_of_will, force_of_will_neg, 
#                      crit_mastery, crit_mastery_neg, 
#                      rear_mastery, rear_mastery_neg, 
#                      melee_mastery, melee_mastery_neg, 
#                      distance_mastery, distance_mastery_neg, 
#                      healing_mastery, healing_mastery_neg, 
#                      berserk_mastery, berserk_mastery_neg, 
#                      crit_res, crit_res_neg, 
#                      rear_res, rear_res_neg, 
#                      armor_given, armor_given_neg, 
#                      armor_received, armor_received_neg, 
#                      indirect_dmg, indirect_dmg_neg, 
#                      random_masteries, random_resistances):
#     """Create and return equipment"""
    
#     equipment = Equipment(id=id, equip_type_id=equip_type_id, level=level,
#                      hp=hp, hp_neg=hp_neg,
#                      armor=armor, armor_neg=armor_neg,
#                      ap=ap, ap_neg=ap_neg, 
#                      mp=mp, mp_neg=mp_neg, 
#                      wp=wp, wp_neg=wp_neg, 
#                      water_mastery=water_mastery, water_mastery_neg=water_mastery_neg, 
#                      air_mastery=air_mastery, air_mastery_neg=air_mastery_neg, 
#                      earth_mastery=earth_mastery, earth_mastery_neg=earth_mastery_neg, 
#                      fire_mastery=fire_mastery, fire_mastery_neg=fire_mastery_neg, 
#                      water_res=water_res, water_res_neg=water_res_neg, 
#                      air_res=air_res, air_res_neg=air_res_neg, 
#                      earth_res=earth_res, earth_res_neg=earth_res_neg, 
#                      fire_res=fire_res, fire_res_neg=fire_res_neg, 
#                      dmg_inflicted=dmg_inflicted, dmg_inflicted_neg=dmg_inflicted_neg, 
#                      crit_hit=crit_hit, crit_hit_neg=crit_hit_neg, 
#                      initiative=initiative, initiative_neg=initiative_neg, 
#                      dodge=dodge, dodge_neg=dodge_neg, 
#                      wisdom=wisdom, wisdom_neg=wisdom_neg,
#                      control=control, control_neg=control_neg, 
#                      heals_performed=heals_performed, heals_performed_neg=heals_performed_neg, 
#                      block=block, block_neg=block_neg, 
#                      spell_range=spell_range, range__neg=range__neg, 
#                      lock=lock, lock_neg=lock_neg, 
#                      prospecting=prospecting, prospecting_neg=prospecting_neg, 
#                      force_of_will=force_of_will, force_of_will_neg=force_of_will_neg, 
#                      crit_mastery=crit_mastery, crit_mastery_neg=crit_mastery_neg, 
#                      rear_mastery=rear_mastery, rear_mastery_neg=rear_mastery_neg, 
#                      melee_mastery=melee_mastery, melee_mastery_neg=melee_mastery_neg, 
#                      distance_mastery=distance_mastery, distance_mastery_neg=distance_mastery_neg, 
#                      healing_mastery=healing_mastery, healing_mastery_neg=healing_mastery_neg, 
#                      berserk_mastery=berserk_mastery, berserk_mastery_neg=berserk_mastery_neg, 
#                      crit_res=crit_res, crit_res_neg=crit_res_neg, 
#                      rear_res=rear_res, rear_res_neg=rear_res_neg, 
#                      armor_given=armor_given, armor_given_neg=armor_given_neg, 
#                      armor_received=armor_received, armor_received_neg=armor_received_neg, 
#                      indirect_dmg=indirect_dmg, indirect_dmg_neg=indirect_dmg_neg, 
#                      random_masteries=random_masteries, random_resistances=random_resistances)
    
#     return equipment


def create_equipment(dict):
    """Create and return an equipment"""
    
    equipment = Equipment(**dict)
    
    return equipment


def create_element():
    """Create and return list of elements"""
    # order: fire > water > earth > air

    element_dicts = [{ 'id' : 1, 'name' : 'fire',
                      'resistance_id' : 82, 'mastery_id' : 122},
                     { 'id' : 2, 'name' : 'water',
                      'resistance_id' : 83, 'mastery_id' : 124}, 
                     { 'id' : 3, 'name' : 'earth',
                      'resistance_id' : 84, 'mastery_id' : 123}, 
                     { 'id' : 4, 'name' : 'air',
                      'resistance_id' : 85, 'mastery_id' : 125}]
    elements = []

    for dict in element_dicts:
        elements.append(Element(**dict))

    return elements


def create_selected_mastery_element(build, element, position):
    """Create and return a selected mastery element"""
    
    mastery_element = Selected_mastery_element(build=build, 
                                               element=element, 
                                               position=position)

    return mastery_element


def create_equipment_random_mastery_element(equipment, element):
    """Create and return an equipment random mastery element"""

    random_mastery_element = Equipment_random_mastery_element(
        equipment=equipment, element=element)
    
    return random_mastery_element


def create_selected_resistance_element(build, element, position):
    """Create and return a selected resistance element"""
    
    resistance_element = Selected_resistance_element(build=build, 
                                               element=element, 
                                               position=position)

    return resistance_element


def create_equipment_random_resistance_element(equipment, element):
    """Create and return an equipment random resistance element"""

    random_resistance_element = Equipment_random_resistance_element(
        equipment=equipment, element=element)
    
    return random_resistance_element


def create_base_stat():
    """Create and return a list of base stats"""

    # Formula 50 + (level * 10)
    base_stat_list = []

    for i in range(1, MAX_LEVEL + 1):
        hp = 50 + (i * 10)
        base_stat_list.append(Base_stat(level=i, hp=hp))

    return base_stat_list


def create_character_class():
    """Create and return a list of character classes"""

    classes = [
        'feca', 'osa', 'enu',
        'sram', 'xelor', 'eca',
        'eni', 'iop', 'cra',
        'sadi', 'sac', 'panda',
        'rogue', 'mask', 'ougi',
        'fogger', 'elio', 'hupper'        
    ]

    char_classes = []

    for char_class in classes:
        char_classes.append(Character_class(name=char_class))

    return char_classes


def create_spell():
    """Create and return list of all spells"""

    pass


def create_selected_spell(build, spell):
    """Create and return a selected spell"""

    selected_spell = Selected_spell(build=build, spell=spell)

    return selected_spell


def create_spell_slot_cap():
    """Create and return a list of spell slot caps"""

    spell_cap_levels = [10, 20, 30, 40, 60, 80]
    spell_cap_list = []
    current_spell_cap = 6

    for i in range(1, MAX_LEVEL + 1):
        if i in spell_cap_levels:
            current_spell_cap += 1
            spell_cap_list.append(
                Spell_slot_cap(level=i, num_of_slots=current_spell_cap))
        else:
            spell_cap_list.append(
                Spell_slot_cap(level=i, num_of_slots=current_spell_cap))
            
    return spell_cap_list
            

def create_passive():
    """Create and return a list of all passives"""

    pass


def create_selected_passive(build, passive):
    """Create and return a selected passive"""

    selected_passive = Selected_passive(build=build, passive=passive)

    return selected_passive


def create_passive_slot_cap():
    """Create and return a list of passive slot caps"""

    passive_cap_levels = [10, 30, 50, 100, 150, 200]
    passive_cap_list = []
    current_passive_cap = 0

    for i in range(1, MAX_LEVEL + 1):
        if i in passive_cap_levels:
            current_passive_cap += 1
            passive_cap_list.append(
                Passive_slot_cap(level=i, num_of_slots=current_passive_cap))
        else:
            passive_cap_list.append(
                Passive_slot_cap(level=i, num_of_slots=current_passive_cap))
            
    return passive_cap_list
        

def create_name_translation(dict):
    """Create and return a name translations"""

    # Columns: id, en, fr, es, pt
    name_translation = Name_translation(**dict)

    return name_translation


def get_users():
    """Return a list of all users"""
    
    return db.session.query(User).all()


def get_user_by_id(id):
    """Return a user by their id"""

    return db.session.query(User).filter(User.id == id).one()


def get_builds():
    """Return a list of all builds"""

    return db.session.query(Build).all()


def get_build_by_id(id):
    """Return a build by it's id """

    return db.session.query(Build).filter(Build.id == id).one()


def get_builds_by_user(user_id):
    """Return all builds associated to a user id"""

    return db.session.query(Build).filter(Build.user_id == user_id).all()


def get_characteristic_by_id(id):
    """Return a characteristic by it's id"""

    return db.session.query(Characteristic).filter(Characteristic.id == id).one()


def get_characteristic_cap_by_level(level):
    """Return charateristic caps by level"""

    return (db.session.query(Characteristic_cap).
            filter(Characteristic_cap.level == level).one())


def get_equipments():
    """Return a list of all equipments"""

    return db.session.query(Equipment).all()


def get_equipment_set_by_id(id):
    """Return equipment_set by it's id"""

    return (db.session.query(Equipment_set).filter(Equipment_set.id == id).
            one())


def get_equipment_by_level_range(min_level=None, max_level=None):
    """Return all the equipment within a level range, inclusive"""

    # If there is an min and max level input
    if min_level and max_level:
        return (db.session.query(Equipment).
                filter(Equipment.level >= min_level, Equipment.level <= max_level)
                .all())
    # Get all equipment with a level at or higher than min        
    elif min_level:
        return (db.session.query(Equipment).
                filter(Equipment.level >= min_level).all())
    # Get all equipment with a level at or lower than max
    elif max_level:
        return (db.session.query(Equipment).
                filter(Equipment.level >= max_level).all())
    # Else return all equipment
    else:
        return get_equipments()


def get_equipment_by_stats(stat_dict):
    """Return all equipment with the stats in input dict"""

    query_object = db.session.query(Equipment)

    non_neg_stats = ['id', 'equip_type_id', 'level', 'rarity']

    for key, value in stat_dict.items():
        if key not in non_neg_stats:
            stat = key
            stat_neg = f'{key}_neg'
            # Func.coalesce replaces nulls with 0 while getattr allows variables
            query_object = query_object.filter(
                (func.coalesce(getattr(Equipment, stat), 0) 
                - func.coalesce(getattr(Equipment, stat_neg), 0))
                == value)
        else:
            stat = key
            query_object = query_object.filter(
                getattr(Equipment, stat) == value)

    return query_object.all()


def get_character_classes():
    """Return all character classes"""

    return db.session.query(Character_class).all()


def get_total_build_stats(build):
    """Return a dict with the total stats of a build"""

    total_stats = {}

    for stat in BUILD_SEARCH_PARAMS_DICT:
    
        pass



def get_specific_stat_total_from_equipment(equipment, stat_string):
    """Return the total of adding stat column with stat_neg column"""

    stat = stat_string
    stat_neg = stat_string + '_neg'

    if stat_neg in EQUIPMENT_SEARCH_PARAMS_DICT:
        positive = (getattr(equipment, stat))
        negative = (getattr(equipment, stat_neg))

        if positive and not negative:
            return -negative
        elif negative and not positive:
            return positive
        elif positive and negative:
            return  positive - negative
    
    else:
        return getattr(equipment, stat)


def get_total_equipment_stats(equipment):
    """Return a dict with the total stats of an equipment"""

    total_stats = {}

    for stat in EQUIPMENT_SEARCH_PARAMS_DICT:
    
        pass



def update_equipment_set(dict):
    """Update and return equipment set"""

    if 'id' not in dict:
        return

    equipment_set = Equipment_set(**dict)
    
    return equipment_set






if __name__ == '__main__':
    from server import app
    connect_to_db(app)



