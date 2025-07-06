"""Create, read, update, and delete functions for database"""

from model import (db, connect_to_db, User, Build,
                   Characteristic, Characteristic_cap,
                   Equipment_set, Equipment,
                   Element, Selected_element, 
                #    Selected_mastery_element,
                #    Equipment_random_mastery_element,
                #    Selected_resistance_element,
                #    Equipment_random_resistance_element,
                   Base_stat, Character_class, Spell,
                   Selected_spell, Spell_slot_cap, Passive,
                   Selected_passive, Passive_slot_cap,
                   Name_translation
                   )
from sqlalchemy import func, case, and_, or_

MAX_LEVEL = 245

INTELLIGENCE_ORDER = ['intelligence', 'hp_percentage',
                          'elemental_res', 'barrier',
                          'heals_received', 'armor']
STRENGTH_ORDER = ['strength', 'elemental_mastery',
                    'melee_mastery', 'distance_mastery',
                    'hp']
AGILITY_ORDER = ['agility', 'lock',
                    'dodge', 'initiative',
                    'lock_dodge', 'force_of_will']
FORTUNE_ORDER = ['fortune', 'crit_hit',
                    'block', 'crit_mastery',
                    'rear_mastery', 'berserk_mastery',
                    'healing_mastery', 'rear_res',
                    'crit_res']
MAJOR_ORDER = ['major', 'ap',
                'mp', 'spell_range',
                'wp', 'control',
                'dmg_inflicted', 'resistance']

MAIN_ROLE_DICT = {
    1 : 'damage',
    2 : 'melee',
    3 : 'distance',
    4 : 'tank',
    5 : 'healer',
    6 : 'shielder',
    7 : 'positioner',
    8 : 'buff / debuff'
}

CONTENT_TYPE_DICT = {
    1 : 'solo',
    2 : 'group',
    3 : 'pvp',
    4 : 'rift',
    5 : 'ultimate boss'
}

EQUIPMENT_SEARCH_PARAMS_DICT = {
    'id' : None,
    'equip_type_id' : None,
    'level' : None,
    'rarity' : None,
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
    'indirect_dmg' : None,  
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
    'character_class_id' : None,
    'main_role' : None,
    'content_type' : None,
    'elemental_mastery' : None,
    'elemental_res' : None,
    'level' : None,
    'hp' : None,
    'armor' : None,
    'ap' : None,
    'mp' : None,
    'wp' : None,
    'water_mastery' : None,
    'air_mastery' : None,
    'earth_mastery' : None,
    'fire_mastery' : None,
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
    'indirect_dmg' : None,
    'barrier' : None
    }

CHARACTERISTIC_MULTIPLIERS_DICT = {
        'hp_percentage'  : 4,
        'elemental_res'  : 10,
        'barrier'  : 1,
        'heals_received'  : 6,
        'armor'  : 4,
        'elemental_mastery'  : 5,
        'melee_mastery'  : 8,
        'distance_mastery'  : 8,
        'hp'  : 20,
        'lock'  : 6,
        'dodge'  : 6,
        'initiative'  : 4,
        'lock_dodge'  : {'lock' : 4, 'dodge' : 4},
        'force_of_will'  : 1,
        'crit_hit'  : 1,
        'block'  : 1,
        'crit_mastery'  : 4,
        'rear_mastery'  : 6,
        'berserk_mastery'  : 8,
        'healing_mastery'  : 6,
        'rear_res'  : 4,
        'crit_res'  : 4,
        'ap'  : 1,
        'mp'  : {'mp' : 1, 'elemental_mastery' : 20},
        'spell_range'  : {'spell_range' : 1, 'elemental_mastery' : 40},
        'wp'  : 2,
        'control'  : {'control' : 2, 'elemental_mastery' : 40},
        'dmg_inflicted'  : 10,
        'resistance'  : 50,
    }


EQUIPMENT_SLOTS = {
    108 : 'main_hand',
    110 : 'main_hand',
    113 : 'main_hand',
    115 : 'main_hand',
    219 : 'main_hand',
    254 : 'main_hand',
    101 : 'two_hand',
    111 : 'two_hand',
    114 : 'two_hand',
    117 : 'two_hand',
    223 : 'two_hand',
    253 : 'two_hand',
    112 : 'off_hand',
    189 : 'off_hand',
    103 : 'ring',
    119 : 'boots',
    120 : 'amulet',
    132 : 'cape',
    133 : 'belt',
    134 : 'helmet',
    136 : 'breastplate',
    138 : 'epaulettes',
    582 : 'pet',
    611 : 'mount',
    480 : 'emblem',
    537 : 'emblem',
    646 : 'emblem',
}


def create_user(email, password):
    """Create and return a new user"""

    user = User(email = email, password = password)

    return user


# def create_build(user=0, equipment_set=None, characteristic=None, 
#                  character_class=None, level=None, build_name=None):
#     """Create and return a build"""

#     build = Build(user=user, equipment_set=equipment_set, 
#                   characteristic=characteristic, 
#                   character_class=character_class, level=level,
#                   build_name=build_name)
    
#     return build


def create_build(user=None):
    """Create and return a build"""

    equipment_set = create_equipment_set()
    characteristic = create_characteristic()

    build = Build(user=user, equipment_set=equipment_set, 
                  characteristic=characteristic)
    
    create_selected_element(build)
    
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


def create_characteristic():
    """Create and return characteristic"""

    sections = ['intelligence', 'strength', 'agility', 'fortune']

    characteristic = Characteristic()

    # for section in sections:
    #     section_cap_column = getattr(Characteristic_cap, section)
    #     print(characteristic)
    #     section_column = getattr(characteristic, section)
    #     section_points = db.session.query(section_cap_column).filter(
    #         Characteristic_cap.level == characteristic.build.level).scalar()
        
    #     section_column = section_points
    
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
        'intelligence' : 0, 'hp_percentage' : -1, 'elemental_res' : 10,
        'barrier' : 10, 'heals_received' : 5, 'armor' : 10,
        'strength' : 0, 'elemental_mastery' : -1, 'melee_mastery' : 40,
        'distance_mastery' : 40, 'hp' : -1, 'agility' : 0, 
        'lock' : -1, 'dodge' : -1, 'initiative' : 20,
        'lock_dodge' : -1, 'force_of_will' : 20, 'fortune' : 0,
        'crit_hit' : 20, 'block' : 20, 'crit_mastery' : -1,
        'rear_mastery' : -1, 'berserk_mastery' : -1, 'healing_mastery' : -1,
        'rear_res' : 20, 'crit_res' : 20, 'major' : 0,
        'ap' : 1, 'mp' : 1, 'spell_range' : 1,
        'wp' : 1, 'control' : 1, 'dmg_inflicted' : 1,
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


def create_equipment_set():
    """Create and return equipment set"""

    equipment_set = Equipment_set()
    
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

    element_dicts = [

                    # { 'id' : 1, 'name' : 'fire',
                    #   'resistance_id' : 82, 'mastery_id' : 122},
                    #  { 'id' : 2, 'name' : 'water',
                    #   'resistance_id' : 83, 'mastery_id' : 124}, 
                    #  { 'id' : 3, 'name' : 'earth',
                    #   'resistance_id' : 84, 'mastery_id' : 123}, 
                    #  { 'id' : 4, 'name' : 'air',
                    #   'resistance_id' : 85, 'mastery_id' : 125},
                      
                      {'id' : 122, 'name' : 'fire_mastery'},
                      {'id' : 124, 'name' : 'water_mastery'},
                      {'id' : 123, 'name' : 'earth_mastery'},
                      {'id' : 125, 'name' : 'air_mastery'},
                      {'id' : 82, 'name' : 'fire_res'},
                      {'id' : 83, 'name' : 'water_res'},
                      {'id' : 84, 'name' : 'earth_res'},
                      {'id' : 85, 'name' : 'air_res'}]
                    
    elements = []

    for dict in element_dicts:
        elements.append(Element(**dict))

    return elements


def create_selected_element(build):
    """Create and return a list of selected element"""
    # order: fire > water > earth > air

    default_elements = db.session.query(Element).all()
    selected_elements = []
    # Index for position
    i = 0
    for element in default_elements:
        selected_elements.append(Selected_element(build=build, 
                                                  element=element,
                                                  position=i))
        i += 1

    return selected_elements





# def create_selected_mastery_element(build, element, position):
#     """Create and return a selected mastery element"""
    
#     mastery_element = Selected_mastery_element(build=build, 
#                                                element=element, 
#                                                position=position)

#     return mastery_element


# def create_equipment_random_mastery_element(equipment, element):
#     """Create and return an equipment random mastery element"""

#     random_mastery_element = Equipment_random_mastery_element(
#         equipment=equipment, element=element)
    
#     return random_mastery_element


# def create_selected_resistance_element(build, element, position):
#     """Create and return a selected resistance element"""
    
#     resistance_element = Selected_resistance_element(build=build, 
#                                                element=element, 
#                                                position=position)

#     return resistance_element


# def create_equipment_random_resistance_element(equipment, element):
#     """Create and return an equipment random resistance element"""

#     random_resistance_element = Equipment_random_resistance_element(
#         equipment=equipment, element=element)
    
#     return random_resistance_element


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


def get_public_builds():
    """Return a list of all public builds"""

    return db.session.query(Build).filter(Build.public == True).all()


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


def get_equipment_by_id(id):
    """Return a single equipment by id"""

    return db.session.query(Equipment).filter(Equipment.id == id).one()


def get_equipment_set_by_id(id):
    """Return equipment_set by it's id"""

    return (db.session.query(Equipment_set).filter(Equipment_set.id == id).
            one())

def get_equipments_by_name(name, language):
    """Return a list of equipment by name"""

    equips = []
    name_ids = db.session.query(Name_translation.id).filter(
        getattr(Name_translation, language).ilike(f'%{name}%')).all()

    for item in name_ids:
        equips.append(get_equipment_by_id(item.id))
    
    return equips
    

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


def get_total_stats_by_build(build):
    """Return a dict with the total stats of a build"""

    characteristic_totals = get_characteristic_stat_totals(
        build.characteristic)
    equipment_totals = get_equipment_set_stat_totals(build.equipment_set)
    base_stats = get_base_stat_by_level(build.level)

    total_stats = get_stat_dict_sum(
        get_stat_dict_sum(characteristic_totals, equipment_totals), 
        base_stats.show())
    
    # Add build level, name, character_class
    if build.build_name:
        total_stats.update({'build_name' : build.build_name})
    if build.character_class_id:
        total_stats.update({'character_class' : build.character_class_id})
    total_stats.update({'level' : build.level})
    return total_stats


def get_stat_combined_with_neg_from_equipment(equipment, stat_string):
    """Return the total of adding stat column with stat_neg column"""
  
    # If stat_string is _neg column
    if '_neg' in stat_string:
        stat = stat_string[:-4]
        stat_neg = stat_string
    else:
        stat = stat_string
        stat_neg = stat_string + '_neg'

    positive = (getattr(equipment, stat))
    negative = (getattr(equipment, stat_neg))

    if positive and not negative:
        return {stat : positive}
    elif negative and not positive:
        return {stat : -(negative)}
    elif positive and negative:
        return  {stat : positive - negative}


def get_random_stats_from_equipment(stat_name, equipment, equipment_set):
    """Return a dict of the stat for the selected build elements"""

    stat_value = getattr(equipment, stat_name)
    num_random_stat = f'num_{stat_name}'
    num_randoms = getattr(equipment, num_random_stat)

    stats_dict = {}
    base = 0

    # if 'masteries' in stat_name:
    #     # Masteries are positions 0-3
    #     for i in range(num_randoms):
    #         selected_element = db.session.query(Selected_element).filter(
    #             Selected_element.build_id == equipment_set.build.id).filter(
    #                 Selected_element.position == i).one()
    #         element = selected_element.element.name
    #         stats_dict.update({element : stat_value})

    if 'resistances' in stat_name:
        # Resistances are positions 4-7
        base = 4

    for i in range(num_randoms):
        selected_element = db.session.query(Selected_element).filter(
            Selected_element.build_id == equipment_set.build[0].id).filter(
                Selected_element.position == (base + i)).one()
        element = selected_element.element.name
        stats_dict.update({element : stat_value})
    
    return stats_dict


def get_equipment_stat_totals(equipment, equipment_set):
    """Return a dict with the total stats of an equipment"""
    """ex. (ap : 3), (ap_neg : 1) return (ap : 2)"""

    total_stats = {}
    non_stats = ['id', 'equip_type_id', 'level', 'rarity',
                 'num_random_masteries', 'num_random_resistances',
                 'state', 'farmer', 'lumberjack', 'herbalist',
                 'miner', 'trapper', 'fisherman']
    

    for stat in equipment.show():
        if stat not in non_stats:

            if stat == 'random_masteries':
                random_masteries = get_random_stats_from_equipment(
                    stat, equipment, equipment_set)
                total_stats = get_stat_dict_sum(total_stats, random_masteries)
            elif stat == 'random_resistances':
                random_resistances = get_random_stats_from_equipment(
                    stat, equipment, equipment_set)
                total_stats = get_stat_dict_sum(total_stats, random_resistances)
            else:
                combined_stat = get_stat_combined_with_neg_from_equipment(
                equipment, stat)
                total_stats = get_stat_dict_sum(total_stats, combined_stat)
                # total_stats[stat] = total_stats.get(stat, combined_stat)
                # total_stats[stat] = combined_stat

    return total_stats


def get_stat_dict_sum(dict1, dict2):
    """Add the values of shared keys in dicts"""

    if dict1 and dict2:
        for key,value in dict2.items():
            dict1[key] = dict1.get(key, 0)
            dict1[key] += value
        return dict1
    elif dict1:
        return dict1
    elif dict2:
        return dict2


def get_equipment_set_stat_totals(equipment_set):
    """Return dict of stat totals from all equipment in a set"""

    stat_totals = {}

    for key,value in equipment_set.show().items():
        if not key == 'id':
            item = get_equipment_by_id(value)
            item_totals = get_equipment_stat_totals(item, equipment_set)
            stat_totals = get_stat_dict_sum(stat_totals, item_totals)
    
    return stat_totals


def get_characteristic_stat_totals(characteristic):
    """Return dict of stat totals from characteristics"""
    # If I put {dict : dict} for the majors with 2 values,
    # I can use sample characteristic with all 1 values to dynamically
    # show how much they increment by on the html templates

    stat_totals = {}
    non_stats = ['intelligence', 'strength', 'agility',
                 'fortune', 'major']

    stat_multiplier_4 = ['hp_percentage', 'armor_hp', 'crit_mastery', 'rear_res', 'crit_res']
    stat_multiplier_5 = ['elemental_mastery']
    stat_multiplier_6 = ['healing_received', 'lock', 'dodge', 'rear_mastery', 'healing_mastery']
    stat_multiplier_8 = ['melee_mastery', 'distance_mastery', 'berserk_mastery']
    stat_multiplier_10 = ['elemental_res', 'dmg_inflicted']


    for key,value in characteristic.show().items():
        # Skip non-stat attributes
        if key not in non_stats:
            if key == 'lock_dodge':
                stat_totals['lock'] = stat_totals.get('lock', 0)
                stat_totals['lock'] += value * 4
                stat_totals['dodge'] = stat_totals.get('dodge', 0)
                stat_totals['dodge'] += value * 4
            elif key == 'mp':
                stat_totals['mp'] = stat_totals.get('mp', 0)
                stat_totals['mp'] += value
                stat_totals['elemental_mastery'] = stat_totals.get(
                    'elemental_mastery', 0)
                stat_totals['elemental_mastery'] += value * 20
            elif key == 'spell_range':
                stat_totals['spell_range'] = stat_totals.get('spell_range', 0)
                stat_totals['spell_range'] += value
                stat_totals['elemental_mastery'] = stat_totals.get(
                    'elemental_mastery', 0)
                stat_totals['elemental_mastery'] += value * 40
            elif key == 'wp':
                stat_totals['wp'] = stat_totals.get('wp', 0)
                stat_totals['wp'] += value * 2
            elif key == 'control':
                stat_totals['control'] = stat_totals.get('control', 0)
                stat_totals['control'] += value * 2
                stat_totals['elemental_mastery'] = stat_totals.get('elemental_mastery', 0)
                stat_totals['elemental_mastery'] += value * 40
            elif key == 'hp':
                stat_totals['hp'] = stat_totals.get('hp', 0)
                stat_totals['hp'] += value * 20
            elif key == 'resistance':
                stat_totals['elemental_res'] = stat_totals.get('elemental_res', 0)
                stat_totals['elemental_res'] += value * 50
            elif key in stat_multiplier_4:
                stat_totals[key] = stat_totals.get(key, 0)
                stat_totals[key] += value * 4
            elif key in stat_multiplier_5:
                stat_totals[key] = stat_totals.get(key, 0)
                stat_totals[key] += value * 5
            elif key in stat_multiplier_6:
                stat_totals[key] = stat_totals.get(key, 0)
                stat_totals[key] += value * 6
            elif key in stat_multiplier_8:
                stat_totals[key] = stat_totals.get(key, 0)
                stat_totals[key] += value * 8
            elif key in stat_multiplier_10:
                stat_totals[key] = stat_totals.get(key, 0)
                stat_totals[key] += value * 10
            else:
                stat_totals[key] = stat_totals.get(key, 0)
                stat_totals[key] += value

    return stat_totals


def get_base_stat_by_level(level):
    """Return a dict of the base stat by level"""
    
    base_stat = db.session.query(Base_stat).filter(Base_stat.level == level).one()

    return base_stat


def update_equipment_set(dict):
    """Update and return equipment set"""

    if 'id' not in dict:
        return

    equipment_set = Equipment_set(**dict)
    
    return equipment_set


def get_build_ids_with_search_params(build_stats, search_params_dict):
    """Return a list of build ids that meet search params"""

    result_build_ids_list = []
    non_min_max_params = ['build_name', 'character_class',
                          'main_role', 'content_type']

    # search_params_dict for testing {'ap': {'max': 9, 'min': 1}, 'character_class': 6, 'level': {'max': 50, 'min': 20}, 'mp': {'min': 1}}

    for build in build_stats:
        meet_params = False
        
        for param in search_params_dict:
            # Get search paramater value or dict if a min/max parameter
            search = search_params_dict[param]
            if param not in non_min_max_params:
                if param in build:
                    if not search.get('min') and build[param] <= search.get('max'):
                        meet_params = True
                        continue
                    elif not search.get('max') and build[param] >= search.get('min'):
                        meet_params = True
                        continue
                    elif (build[param] >= search.get('min') 
                        and build[param] <= search.get('max')):
                        meet_params = True
                    else:
                        meet_params = False
                        break
                else:
                    meet_params = False
                    break
            else:
                if param in build:
                    if build[param] == search:
                        meet_params = True
                        continue
                    else:
                        meet_params = False
                        break
        if meet_params == True:
            result_build_ids_list.append(build['id'])
                    
    return result_build_ids_list


# def get_builds_by_search_params(search_params_dict):
#     """Return a list of builds filtered by the search params"""

#     query = db.session.query(Build)
#     #######################
#     # Doesn't seem to work unless I store the build_stats into db
#     #######################

def get_query_case_for_equipment_column_with_neg(param):
    """Return query case for difference of columns with '_neg'
    in the Equipment table"""
    
    stat = getattr(Equipment, param)
    stat_neg = getattr(Equipment, (param + '_neg'))

    param_case = case(
        (stat.isnot(None) & stat_neg.isnot(None), stat - stat_neg),
        (stat.isnot(None) & stat_neg.is_(None), stat),
        (stat.is_(None) & stat_neg.isnot(None), -stat_neg),
        else_=0)
    return param_case

def get_query_case_for_equipment_mastery(param, elemental_list=[]):
    """Return query case for total equipment mastery"""
    
    num_of_elements = len(elemental_list)
    stat = get_query_case_for_equipment_column_with_neg(param)
    random_mastery = func.coalesce(Equipment.random_masteries, 0)
    num_random = func.coalesce(Equipment.num_random_masteries, 0)
    mastery_dict = {'fire_mastery' : 
                            get_query_case_for_equipment_column_with_neg(
                                'fire_mastery'),
                        'water_mastery' : 
                            get_query_case_for_equipment_column_with_neg(
                                'water_mastery'),
                        'earth_mastery' : 
                            get_query_case_for_equipment_column_with_neg(
                                'earth_mastery'),
                        'air_mastery' : 
                            get_query_case_for_equipment_column_with_neg(
                                'air_mastery')}
    mastery1 = mastery_dict['fire_mastery']
    mastery2 = mastery_dict['water_mastery']
    mastery3 = mastery_dict['earth_mastery']
    mastery4 = mastery_dict['air_mastery']

    cases = []

    if num_of_elements == 0:
        cases.append((num_of_elements == 0, func.greatest(mastery1, 
                        mastery2, mastery3, mastery4) + stat + 
                        random_mastery))
        
    if num_of_elements == 1:
        cases.append((and_((num_of_elements == 1), (num_random >= num_of_elements)),
                         mastery_dict[elemental_list[0]] + stat + 
                         random_mastery))
        
    if num_of_elements == 2:
        cases.extend([(num_of_elements == 2 & num_random >= num_of_elements
                          & mastery_dict[elemental_list[0]] == 
                          mastery_dict[elemental_list[1]],
                          mastery_dict[elemental_list[0]] + stat +
                          random_mastery),

                        (num_of_elements == 2 & num_random < num_of_elements
                          & mastery_dict[elemental_list[0]] == 
                          mastery_dict[elemental_list[1]],
                          mastery_dict[elemental_list[0]] + stat)])
        
    if num_of_elements == 3:
        cases.extend([(num_of_elements == 3 & num_random >= num_of_elements
                          & mastery_dict[elemental_list[0]] == 
                          mastery_dict[elemental_list[1]] & 
                          mastery_dict[elemental_list[0]] == 
                          mastery_dict[elemental_list[2]],
                          mastery_dict[elemental_list[0]] + stat +
                          random_mastery),

                        (num_of_elements == 3 & num_random < num_of_elements
                          & mastery_dict[elemental_list[0]] == 
                          mastery_dict[elemental_list[1]] & 
                          mastery_dict[elemental_list[0]] == 
                          mastery_dict[elemental_list[2]],
                          mastery_dict[elemental_list[0]] + stat)])
        
    if num_of_elements == 4:
        cases.append((and_(num_of_elements == 4, num_random == 0), 
                                                  stat))

    
    # param_case = case((num_of_elements == 0, func.greatest(mastery1, 
    #                     mastery2, mastery3, mastery4) + stat + 
    #                     random_mastery),

    #                     (and_((num_of_elements == 1), (num_random >= num_of_elements)),
    #                      mastery_dict[elemental_list[0]] + stat + 
    #                      random_mastery),

    #                     (num_of_elements == 2 & num_random >= num_of_elements
    #                       & mastery_dict[elemental_list[0]] == 
    #                       mastery_dict[elemental_list[1]],
    #                       mastery_dict[elemental_list[0]] + stat +
    #                       random_mastery),

    #                     (num_of_elements == 2 & num_random < num_of_elements
    #                       & mastery_dict[elemental_list[0]] == 
    #                       mastery_dict[elemental_list[1]],
    #                       mastery_dict[elemental_list[0]] + stat),

    #                     (num_of_elements == 3 & num_random >= num_of_elements
    #                       & mastery_dict[elemental_list[0]] == 
    #                       mastery_dict[elemental_list[1]] & 
    #                       mastery_dict[elemental_list[0]] == 
    #                       mastery_dict[elemental_list[2]],
    #                       mastery_dict[elemental_list[0]] + stat +
    #                       random_mastery),

    #                     (num_of_elements == 3 & num_random < num_of_elements
    #                       & mastery_dict[elemental_list[0]] == 
    #                       mastery_dict[elemental_list[1]] & 
    #                       mastery_dict[elemental_list[0]] == 
    #                       mastery_dict[elemental_list[2]],
    #                       mastery_dict[elemental_list[0]] + stat),

    #                     (num_of_elements == 4, stat))
    return case(*cases)


def get_query_case_for_equipment_res(param, elemental_list=[]):
    """Return query case for total equipment res"""
    
    num_of_elements = len(elemental_list)
    stat = get_query_case_for_equipment_column_with_neg(param)
    random_res = func.coalesce(Equipment.random_resistances, 0)
    num_random = func.coalesce(Equipment.num_random_resistances, 0)
    res_dict = {'fire_res' : 
                            get_query_case_for_equipment_column_with_neg(
                                'fire_res'),
                        'water_res' : 
                            get_query_case_for_equipment_column_with_neg(
                                'water_res'),
                        'earth_res' : 
                            get_query_case_for_equipment_column_with_neg(
                                'earth_res'),
                        'air_res' : 
                            get_query_case_for_equipment_column_with_neg(
                                'air_res')}
    res1 = res_dict['fire_res']
    res2 = res_dict['water_res']
    res3 = res_dict['earth_res']
    res4 = res_dict['air_res']

    cases = []

    if num_of_elements == 0:
        cases.append((num_of_elements == 0, res1 + 
                        res2 + res3 + res4 + (stat * 4) + 
                        (random_res * num_random)))
        
    if num_of_elements == 1:
        cases.append((and_((num_of_elements == 1), (num_random >= num_of_elements)),
                         res_dict[elemental_list[0]] + stat + 
                         random_res))
        
    if num_of_elements == 2:
        cases.extend([(num_of_elements == 2 & num_random >= num_of_elements
                          & res_dict[elemental_list[0]] == 
                          res_dict[elemental_list[1]],
                          res_dict[elemental_list[0]] + (stat * 2) +
                          random_res),

                        (num_of_elements == 2 & num_random < num_of_elements
                          & res_dict[elemental_list[0]] == 
                          res_dict[elemental_list[1]],
                          res_dict[elemental_list[0]] + (stat * 2))])
        
    if num_of_elements == 3:
        cases.extend([(num_of_elements == 3 & num_random >= num_of_elements
                          & res_dict[elemental_list[0]] == 
                          res_dict[elemental_list[1]] & 
                          res_dict[elemental_list[0]] == 
                          res_dict[elemental_list[2]],
                          res_dict[elemental_list[0]] + (stat * 3) +
                          random_res),

                        (num_of_elements == 3 & num_random < num_of_elements
                          & res_dict[elemental_list[0]] == 
                          res_dict[elemental_list[1]] & 
                          res_dict[elemental_list[0]] == 
                          res_dict[elemental_list[2]],
                          res_dict[elemental_list[0]] + (stat * 3))])
        
    if num_of_elements == 4:
        cases.append((and_(num_of_elements == 4, num_random == 0), 
                                                  stat * 4))

    return case(*cases)


# def get_query_case_for_equipment_res(param):
#     """Return query case for total res"""

#     stat = get_query_case_for_equipment_column_with_neg(param)
#     random_res = func.coalesce(Equipment.random_resistances, 0)
#     num_random = func.coalesce(Equipment.num_random_resistances, 0)
#     res1 = get_query_case_for_equipment_column_with_neg('fire_res')
#     res2 = get_query_case_for_equipment_column_with_neg('water_res')
#     res3 = get_query_case_for_equipment_column_with_neg('earth_res')
#     res4 = get_query_case_for_equipment_column_with_neg('air_res')

#     return (res1 + res2 + res3 + res4 + stat + (random_res * num_random))

    """
    Return a flask sqlalchemy query case

    if '_mastery' in param
        single_ele_mastery_list
        num_of_ele = len(single_ele_mastery_list)  
        mastery1 = get_case(fire)
        mastery2 = get_case(water)
        mastery3 = get_case(earth)
        mastery4 = get_case(earth) 
        
        param_case = case(if num_of_ele == 0, 
                        max(mastery1-4) + get_case(ele_mastery) + item.random_mastery),
                    (if num_of_ele == 1 and num_mastery >= 1,
                        get_case(single_ele_mastery_list[0]) + get_case(param) + item.random_mastery)
                    (if num_of_ele == 2 and get_case(single_ele_mastery_list[0]) == get_case(single_ele_mastery_list[1]) and num_mastery >= num_of_ele,
                        get_case(single_ele_mastery_list[0]) + get_case(param) + item.random_mastery),
                    (if num_of_ele == 3 and get_case(single_ele_mastery_list[0]) == get_case(single_ele_mastery_list[1]) and get_case(single_ele_mastery_list[0]) == get_case(single_ele_mastery_list[2]) and num_mastery >= num_of_ele,
                        get_case(single_ele_mastery_list[0]) + get_case(param) + item.random_mastery)
                    (if num_of_ele == 4,
                        get_case(param))
        return param_case



    if '_res' in param
        res1 = get_case(fire)
        res2 = get_case(water)
        res3 = get_case(earth)
        res4 = get_case(earth)
        param_case = (sum(res1-4) + get_case(param) + (item.random_res * item.num_res))

        return param_case

    """


def get_equipments_by_search_params_and_language(search_params_dict, language):
    """Return list of equipments which meet search params"""
    
    search_query = db.session.query(Equipment, Name_translation).join(
        Name_translation, Name_translation.name_id == Equipment.id)
    list_type_params = ['equip_type_id', 'rarity',
                        'mastery_element', 'res_element']
    boolean_params = ['state', 'farmer','lumberjack',
                      'herbalist', 'miner', 'trapper',
                      'fisherman']
    

    for param in search_params_dict:
        searched_values = search_params_dict[param]
        column = getattr(Equipment, param)

        if 'elemental_mastery' == param:
            # Handle mastery searches
            if 'mastery_element' in search_params_dict['elemental_mastery']:
                element_list = search_params_dict['elemental_mastery']['mastery_element']
                column_cases = get_query_case_for_equipment_mastery(
                    param, element_list)
                if 'min' in searched_values:
                    search_query = search_query.filter(
                        column_cases >= searched_values['min'])
                if 'max' in searched_values:
                    search_query = search_query.filter(
                        column_cases <= searched_values['max'])
            else:
                column_cases = get_query_case_for_equipment_mastery(
                    param)
                if 'min' in searched_values:
                    search_query = search_query.filter(
                    column_cases >= searched_values['min'])
                if 'max' in searched_values:
                    search_query = search_query.filter(
                        column_cases <= searched_values['max'])
        elif "elemental_res" ==  param:
            # Handle resistance searches
            if 'res_element' in search_params_dict['elemental_res']:
                element_list = search_params_dict['elemental_res']['res_element']
                column_cases = get_query_case_for_equipment_res(
                    param, element_list)
                if 'min' in searched_values:
                    search_query = search_query.filter(
                        column_cases >= searched_values['min'])
                if 'max' in searched_values:
                    search_query = search_query.filter(
                        column_cases <= searched_values['max'])
            else:
                column_cases = get_query_case_for_equipment_res(
                    param)
                if 'min' in searched_values:
                    search_query = search_query.filter(
                    column_cases >= searched_values['min'])
                if 'max' in searched_values:
                    search_query = search_query.filter(
                        column_cases <= searched_values['max'])
        elif param == 'equipment_name':
            # Search for name of equip by user language
            name_column = getattr(Name_translation, language)
            search_query = search_query.filter(
                name_column.ilike(f'%{searched_values}%'))
        elif param in list_type_params:
            # Search params that have a list of types
            if param not in ['mastery_element', 'res_element']:
                for value in searched_values:     
                    search_query = search_query.filter(column == value)
        elif param in boolean_params:
            # User wants to search for equipment where param exists
            search_query = search_query.filter(column != None)
        elif param == 'level':
            # Find equips with level range, which doesn't have _neg
            if 'min' in searched_values:
                search_query = search_query.filter(
                    column >= searched_values['min'])
            if 'max' in searched_values:
                search_query = search_query.filter(
                    column <= searched_values['max'])
        else:
            # Find the params with min and max ranges
            column_cases = get_query_case_for_equipment_column_with_neg(param)
            if 'min' in searched_values:
                search_query = search_query.filter(
                    column_cases >= searched_values['min'])
            if 'max' in searched_values:
                search_query = search_query.filter(
                    column_cases <= searched_values['max'])
        
    return search_query.all()           


def set_build_with_total_stats_by_build_and_base_stats(build_and_base_stats):
    """Sets a build with added attributes for the total
    of each stat"""
    
    # Xelor (id=5) gets +6 wp
    # Hupper QB = 50 base + 75/wp. 999 max, 50 min
    build_params_not_totaled = ['character_class_id', 'main_role',
                                'content_type', 'build_name',
                                'level']
    base_stat_list = ['hp', 'ap', 'mp', 'wp', 'control', 'crit_hit']
    characteristic_stat_list = ['barrier', 'heals_received',
                                'armor', 'melee_mastery',
                                'distance_mastery', 'hp',
                                'lock', 'dodge', 'initiative',
                                'force_of_will', 'crit_hit',
                                'block', 'crit_mastery',
                                'rear_mastery', 'berserk_mastery',
                                'rear_res', 'crit_res', 'ap',
                                'mp', 'spell_range',
                                'wp', 'control', 'dmg_inflicted']
    elemental_res_list = ['fire_res', 'water_res',
                          'earth_res', 'air_res']
    elemental_mastery_list = ['fire_mastery', 'water_mastery',
                              'earth_mastery', 'air_mastery']



    # stat_tables = db.session.query(Build, Base_stat).join(
    #     Base_stat, Base_stat.level == build.level).join(Equipment_set).join(
    #         Characteristic).filter(Build.id == build.id).one()
    build = build_and_base_stats[0]
    base_stats = build_and_base_stats[1]

    for param in BUILD_SEARCH_PARAMS_DICT:
        if param not in build_params_not_totaled:
            total_name = 'total_' + param
            total_value = 0

            if param in base_stat_list:
                total_value += getattr(base_stats, param)

                # total_value += getattr(stat_tables.Base_stat, param)

                # total_value += db.session.query(
                #     getattr(Base_stat, param)).filter(
                #         Base_stat.level == build.level).scalar()
            if param in characteristic_stat_list:
                multiplier = CHARACTERISTIC_MULTIPLIERS_DICT[param]
                base_value = getattr(build.characteristic, param)
                if isinstance(multiplier, dict):
                    for stat in multiplier:
                        stat_name = 'total_' + stat
                        # If it's resistance major point
                        if stat == 'resistance':
                            res_name = 'total_elemental_res'
                            if res_name in build.__dict__:
                                current_value = getattr(build, res_name)
                                setattr(build, 
                                        res_name, 
                                        (current_value +
                                            (base_value * 
                                            multiplier[stat])))
                            else:
                                setattr(build, 
                                        res_name, 
                                        (base_value *
                                         multiplier[stat]))
                        # If the total stat is already an attribute in build
                        elif stat_name in build.__dict__:
                            current_value = getattr(build, stat_name)
                            setattr(build, stat_name, (current_value
                                                       + (base_value * 
                                                          multiplier[stat])))
                        # Else, add the total_stat
                        else:
                            setattr(build, stat_name, (base_value * 
                                                       multiplier[stat]))
                else:
                    total_value += base_value * multiplier

                # total_value += ((getattr(stat_tables.characteristic, param)) 
                #                 * CHARACTERISTIC_MULTIPLIERS_DICT[param])
                # total_value += db.session.query(
                #     getattr(build.characteristic, param)).scalar()
            for equip_slot in build.equipment_set.show():
            # for equip_slot in stat_tables.equipment_set.show():
            # for equip_slot, equip_id in build.equipment_set.show().items():
                if equip_slot.endswith('_id') and param != 'barrier':
                    equip = getattr(build.equipment_set, equip_slot[:-3])
                    # equip = getattr(stat_tables.equipment, equip_slot[:-3])
                    equip_pos = getattr(equip, param)
                    equip_neg = getattr(equip, param + '_neg')
                    if equip_pos and equip_neg:
                        total_value += equip_pos - equip_neg
                    elif equip_pos and not equip_neg:
                        total_value += equip_pos
                    elif not equip_pos and equip_neg:
                        total_value += -equip_neg

                    # Handle random masteries
                    if equip.random_masteries:
                        num_elements = equip.num_random_masteries
                        # Mastery postions are 0-3
                        for element in build.selected_elements:
                            # If the postion is within number of selected elements
                            if element.position < num_elements:
                                element_name = element.element.name
                                if element_name in build.__dict__:
                                    current_value = getattr(build, 
                                                            element_name)
                                    setattr(build, element_name, (
                                        current_value + 
                                        equip.random_masteries))
                                else:
                                    setattr(build, element_name,
                                            equip.random_masteries)

                    if equip.random_resistances:
                        num_elements = equip.num_random_resistances
                        for element in build.selected_elements:
                            position = element.position
                            if position < (num_elements + 4) and position > 3:
                                element_name = element.element.name
                                if element_name in build.__dict__:
                                    current_value = getattr(build, 
                                                            element_name)
                                    setattr(build, element_name, (
                                        current_value + 
                                        equip.random_resistances))
                                else:
                                    setattr(build, element_name,
                                            equip.random_resistances)
                
            # for equip_slot, equip_id in build.equipment_set.show().items():
            #     if equip_slot != 'id':
            #         equip = db.session.query(Equipment).filter(
            #             Equipment.id == equip_id).one()
            #         stat_case = get_query_case_for_equipment_column_with_neg(
            #             param, equip)
            #         total_value += db.session.query(stat_case).scalar()
            # equips = db.session.query(Equipment).filter(Equipment.id.in_(
            #     build.equipment_set.show().values())).all()
            # for equip in equips:

            # Add hp multipliers
            if param == 'hp':
                total_value += int(total_value * ((CHARACTERISTIC_MULTIPLIERS_DICT['hp_percentage']
                                              * build.characteristic.hp_percentage) / 100 ))
            if param == 'wp':
                # For xelor's 6 extra wp
                if build.character_class_id == 5:
                    total_value += 6

            # Handle elemental mastery
            if param in elemental_mastery_list:
                if 'total_elemental_mastery' in build.__dict__:
                    total_value += build.total_elemental_mastery

            # Handle elemental resistance
            if param in elemental_res_list:
                if 'total_elemental_res' in build.__dict__:
                    total_value += build.total_elemental_res
            

            # If the total name is already an attribute in build
            if total_name in build.__dict__:
                current_value = getattr(build, total_name)
                setattr(build, total_name, (current_value
                                            + total_value))
            # Else, add the total value
            else:
                setattr(build, total_name, total_value)


def get_public_builds_with_base_stats():
    """Return a list of tuples with build.model and the base stats 
    for the build's level"""

    return db.session.query(Build, Base_stat).join(
        Base_stat, Base_stat.level == Build.level).filter(
            Build.public == True).all()
    

def is_build_result(build_with_stats, search_params_dict):
    """Return True if build meets search parameters"""

    non_min_max_params = ['build_name', 'character_class_id',
                          'main_role', 'content_type']
    
    for param_name, param_value in search_params_dict.items():

        total_stat_name = 'total_' + param_name

        if param_name in non_min_max_params:
            build_stat = getattr(build_with_stats, param_name)
            if param_name == 'build_name':
                if param_value.lower() not in build_stat.lower():
                    return False
            elif isinstance(param_value, list):

                if build_stat not in param_value:
                    return False
            else:
                if param_value != build_stat:
                    return False
        elif isinstance(param_value, dict):
            # Level is only min/max param without a total
            if param_name == 'level':
                total_stat_name = 'level'
            build_stat_total = getattr(build_with_stats, total_stat_name)
            min_param = param_value.get('min')
            max_param = param_value.get('max')

            if  min_param and max_param:
                if not (build_stat_total >= min_param and
                        build_stat_total <= max_param):
                    return False
            if min_param and not max_param:
                if not (build_stat_total >= min_param):
                    return False
            if not min_param and max_param:
                if not (build_stat_total <= max_param):
                    return False
    return True


# def set_build_stats_by_build(build):
#     """Set total stat attributes by build"""

#     base_stats = get_base_stat_by_level(build.level)
#     combo = (build, base_stats)
#     set_build_with_total_stats_by_build_and_base_stats(combo)


def get_build_characteristic_cap_base_stat_by_build_id(build_id):
    """Return a tuple of a build and it's characteristic caps and base stats."""

    return db.session.query(Build, Characteristic_cap, Base_stat).join(
        Characteristic_cap, Characteristic_cap.level == Build.level).join(
            Base_stat, Base_stat.level == Build.level).filter(
                Build.id == build_id).one()


def get_name_translations():
    return db.session.query(Name_translation).all()


def update_equipment_set_by_build_equipment(build, equipment):
    """Update equipment set of build to include equipment input"""

    slot = EQUIPMENT_SLOTS[equipment.equip_type_id]
    equip_set = build.equipment_set

    if slot == 'ring':
        # If no ring in ring1 slot, add
        if not equip_set.ring1:
            equip_set.ring1 = equipment
        # If no ring in ring2 slot
        elif equip_set.ring1 and not equip_set.ring2:
            # If ring not already equipped, add in slot2
            if equipment != equip_set.ring1:
                equip_set.ring2 = equipment
            # If ring already equipped, move over to slot2
            else:
                equip_set.ring2 = equipment
                equip_set.ring1 = None
        # If both ring slots full
        else:
            # If ring already equipped, swap ring slots
            if equipment == equip_set.ring1:
                equip_set.ring1 = equip_set.ring2
                equip_set.ring2 = equipment
            elif equipment == equip_set.ring2:
                equip_set.ring2 = equip_set.ring1
                equip_set.ring1 = equipment
            # If ring not equipped, place in ring1 slot
            else:
                equip_set.ring1 = equipment
    elif slot == 'two_hand':
        equip_set.main_hand = None
        equip_set.off_hand = None
        setattr(equip_set, slot, equipment)
    elif slot in ['main_hand', 'off_hand']:
        equip_set.two_hand = None
        setattr(equip_set, slot, equipment)
    else:
        setattr(equip_set, slot, equipment)
        

def update_characteristics_by_characteristic_and_points(
        characteristic, section, char_name, points, char_cap):
    """Update build characteristics with input points"""

    verify_and_update_characteristic_section(characteristic, char_cap)
    
    current_points = getattr(characteristic, char_name)
    section_points = getattr(characteristic, section)
    points_cap = getattr(char_cap, char_name)
    section_cap = getattr(char_cap, section)
    available_points = points_cap - current_points
    available_section_points = section_cap - section_points
    point_difference = points - current_points
    
    # When there is no point cap, set available points as section points
    if points_cap == -1:
        points_cap = None
        available_points = available_section_points
    # If current points is less than 0, make it zero
    if current_points < 0:
        current_points = 0
    if section_points < 0:
        section_points = 0

    # No negative characteristic points allowed
    if points < 0:
        setattr(characteristic, char_name, 0)
        setattr(characteristic, section, section_points - current_points)
    # If trying to use more points than available in the section
    elif points > available_section_points:
        points = available_section_points
        if points < current_points and section_points + point_difference >= 0:
            setattr(characteristic, char_name,
                    points)
            setattr(characteristic, section,
                    section_points + point_difference)
        else:
            if points > available_points:
                setattr(characteristic, char_name,
                        available_points + current_points)
                setattr(characteristic, section,
                        section_points + available_points)
            else:
                setattr(characteristic, char_name,
                        points + current_points)
                setattr(characteristic, section,
                    section_cap)
    else:
        # If reducing the number of characteristic points
        if points < current_points and section_points + point_difference >= 0:
            setattr(characteristic, char_name,
                    points)
            setattr(characteristic, section,
                    section_points + point_difference)
        # If trying to use more points than available in characteristic
        elif points > available_points:
            setattr(characteristic, char_name,
                    available_points + current_points)
            setattr(characteristic, section,
                    section_points + available_points)
        else:
            setattr(characteristic, char_name,
                    points)
            setattr(characteristic, section,
                    section_points + point_difference)

def verify_and_update_characteristic_section(characteristic, char_cap):
    """Verify characteristic section totals and update"""

    all_characteristic_sections = [INTELLIGENCE_ORDER,
                                   STRENGTH_ORDER,
                                   AGILITY_ORDER,
                                   FORTUNE_ORDER,
                                   MAJOR_ORDER]
    for section_list in all_characteristic_sections:
        section = ""
        count = 0
        section_cap = 0
        for i in range(len(section_list)):
            if i == 0:
                section = section_list[i]
                count = 0
                section_cap = getattr(char_cap, section)
            else:
                stat_name = section_list[i]
                stat_value = getattr(characteristic, stat_name)
                section_count = getattr(characteristic, section)
                section_available = section_cap - section_count
                cap = getattr(char_cap, stat_name)
                if cap == -1:
                    cap = section_available
                available = cap - count
                
                
                if stat_value > available:
                    stat_value = available
                    setattr(characteristic, stat_name, available)
                elif stat_value > section_available:
                    stat_value = section_available
                    setattr(characteristic, stat_name, section_available)
                    
                if stat_value > cap:
                    count += cap
                    setattr(characteristic, stat_name, cap)
                elif stat_value >= 0:
                    count += stat_value
                else:
                    setattr(characteristic, stat_name, 0)
        if count < 0 :
            setattr(characteristic, section, 0)
        elif count > section_cap:
            setattr(characteristic, section, section_cap)
        else:
            setattr(characteristic, section, count)
        


def get_characteristic_and_characteristic_cap_by_build_id(build_id):
    """Return characteristic and characteric cap by the build id"""

    build, char_cap = db.session.query(Build, Characteristic_cap).filter(
        Build.id == build_id, Characteristic_cap.level == Build.level).one()

    return build.characteristic, char_cap


def update_level_by_build_id(build_id, level):
    """Update the level of a build by the build id"""

    build = get_build_by_id(build_id)
    build.level = level



if __name__ == '__main__':
    from server import app
    connect_to_db(app)



