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

MAX_LEVEL = 245


def create_user(email, password):
    """Create and return a new user"""

    user = User(email = email, password = password)

    return user


def create_build(user, equipment_set, characteristic, character_class, level):
    """Create and return a build"""

    build = Build(user=user, equipment_set=equipment_set, 
                  characteristic=characteristic, 
                  character_class=character_class, level=level)
    
    return build

def create_characteristic(intelligence, hp_percentage, elem_res,
                          barrier, heals_received, armor_hp,
                          strength, elem_mastery, melee,
                          distance, hp, agility, 
                          lock, dodge, initiative,
                          lock_dodge, force_of_will, fortune,
                          crit_hit, block, crit_mastery,
                          rear_mastery, berserk_mastery, healing_mastery,
                          rear_res, crit_res, major,
                          action_points, movement_points, spell_range,
                          wakfu_points, control, dmg_inflicted,
                          resistance):
    """Create and return characteristic"""

    characteristic = Characteristic(intelligence=intelligence, 
                                    hp_percentage=hp_percentage, 
                                    elem_res=elem_res, 
                                    barrier=barrier, 
                                    heals_received=heals_received, 
                                    armor_hp=armor_hp,
                                    strength=strength, 
                                    elem_mastery=elem_mastery, 
                                    melee=melee,
                                    distance=distance, 
                                    hp=hp, 
                                    agility=agility, 
                                    lock=lock, 
                                    dodge=dodge, 
                                    initiative=initiative,
                                    lock_dodge=lock_dodge, 
                                    force_of_will=force_of_will, 
                                    fortune=fortune, 
                                    crit_hit=crit_hit, 
                                    block=block, 
                                    crit_mastery=crit_mastery,
                                    rear_mastery=rear_mastery, 
                                    berserk_mastery=berserk_mastery, 
                                    healing_mastery=healing_mastery,
                                    rear_res=rear_res, 
                                    crit_res=crit_res, 
                                    major=major,
                                    action_points=action_points, 
                                    movement_points=movement_points, 
                                    spell_range=spell_range,
                                    wakfu_points=wakfu_points, 
                                    control=control, 
                                    dmg_inflicted=dmg_inflicted,
                                    resistance=resistance)
    
    return characteristic


def create_characteristic_cap(intelligence, hp_percentage, elem_res,
                          barrier, heals_received, armor_hp,
                          strength, elem_mastery, melee,
                          distance, hp, agility, 
                          lock, dodge, initiative,
                          lock_dodge, force_of_will, fortune,
                          crit_hit, block, crit_mastery,
                          rear_mastery, berserk_mastery, healing_mastery,
                          rear_res, crit_res, major,
                          action_points, movement_points, spell_range,
                          wakfu_points, control, dmg_inflicted,
                          resistance):
    """Create and return characteristic max values"""

    characteristic_cap = Characteristic_cap(intelligence=intelligence, hp_percentage=hp_percentage, elem_res=elem_res,
                          barrier=barrier, heals_received=heals_received, armor_hp=armor_hp,
                          strength=strength, elem_mastery=elem_mastery, melee=melee,
                          distance=distance, hp=hp, agility=agility, 
                          lock=lock, dodge=dodge, initiative=initiative,
                          lock_dodge=lock_dodge, force_of_will=force_of_will, fortune=fortune,
                          crit_hit=crit_hit, block=block, crit_mastery=crit_mastery,
                          rear_mastery=rear_mastery, berserk_mastery=berserk_mastery, healing_mastery=healing_mastery,
                          rear_res=rear_res, crit_res=crit_res, major=major,
                          action_points=action_points, movement_points=movement_points, spell_range=spell_range,
                          wakfu_points=wakfu_points, control=control, dmg_inflicted=dmg_inflicted,
                          resistance=resistance)
    
    return characteristic_cap


def create_equipment_set(helmet, amulet, breastplate,
                         boots, ring1, ring2,
                         cape, epaulettes, belt,
                         pet, off_hand, main_hand,
                         two_hander, emblem, mount):
    """Create and return equipment set"""

    equipment_set = Equipment_set(helmet=helmet, amulet=amulet, 
                                  breastplate=breastplate, boots=boots, 
                                  ring1=ring1, ring2=ring2,
                                  cape=cape, epaulettes=epaulettes, 
                                  belt=belt, pet=pet, 
                                  off_hand=off_hand, main_hand=main_hand,
                                  two_hander=two_hander, emblem=emblem, 
                                  mount=mount)
    
    return equipment_set


def create_equipment(id, equip_type_id, level,
                     hp, hp_neg,
                     armor, armor_neg,
                     ap, ap_neg, 
                     mp, mp_neg, 
                     wp, wp_neg, 
                     water_mastery, water_mastery_neg, 
                     air_mastery, air_mastery_neg, 
                     earth_mastery, earth_mastery_neg, 
                     fire_mastery, fire_mastery_neg, 
                     water_res, water_res_neg, 
                     air_res, air_res_neg, 
                     earth_res, earth_res_neg, 
                     fire_res, fire_res_neg, 
                     dmg_inflicted, dmg_inflicted_neg, 
                     crit_hit, crit_hit_neg, 
                     initiative, initiative_neg, 
                     dodge, dodge_neg, 
                     wisdom, wisdom_neg,
                     control, control_neg, 
                     heals_performed, heals_performed_neg, 
                     block, block_neg, 
                     spell_range, range__neg, 
                     lock, lock_neg, 
                     prospecting, prospecting_neg, 
                     force_of_will, force_of_will_neg, 
                     crit_mastery, crit_mastery_neg, 
                     rear_mastery, rear_mastery_neg, 
                     melee_mastery, melee_mastery_neg, 
                     distance_mastery, distance_mastery_neg, 
                     healing_mastery, healing_mastery_neg, 
                     berserk_mastery, berserk_mastery_neg, 
                     crit_res, crit_res_neg, 
                     rear_res, rear_res_neg, 
                     armor_given, armor_given_neg, 
                     armor_received, armor_received_neg, 
                     indirect_dmg, indirect_dmg_neg, 
                     random_masteries, random_resistances):
    """Create and return equipment"""
    
    equipment = Equipment(id=id, equip_type_id=equip_type_id, level=level,
                     hp=hp, hp_neg=hp_neg,
                     armor=armor, armor_neg=armor_neg,
                     ap=ap, ap_neg=ap_neg, 
                     mp=mp, mp_neg=mp_neg, 
                     wp=wp, wp_neg=wp_neg, 
                     water_mastery=water_mastery, water_mastery_neg=water_mastery_neg, 
                     air_mastery=air_mastery, air_mastery_neg=air_mastery_neg, 
                     earth_mastery=earth_mastery, earth_mastery_neg=earth_mastery_neg, 
                     fire_mastery=fire_mastery, fire_mastery_neg=fire_mastery_neg, 
                     water_res=water_res, water_res_neg=water_res_neg, 
                     air_res=air_res, air_res_neg=air_res_neg, 
                     earth_res=earth_res, earth_res_neg=earth_res_neg, 
                     fire_res=fire_res, fire_res_neg=fire_res_neg, 
                     dmg_inflicted=dmg_inflicted, dmg_inflicted_neg=dmg_inflicted_neg, 
                     crit_hit=crit_hit, crit_hit_neg=crit_hit_neg, 
                     initiative=initiative, initiative_neg=initiative_neg, 
                     dodge=dodge, dodge_neg=dodge_neg, 
                     wisdom=wisdom, wisdom_neg=wisdom_neg,
                     control=control, control_neg=control_neg, 
                     heals_performed=heals_performed, heals_performed_neg=heals_performed_neg, 
                     block=block, block_neg=block_neg, 
                     spell_range=spell_range, range__neg=range__neg, 
                     lock=lock, lock_neg=lock_neg, 
                     prospecting=prospecting, prospecting_neg=prospecting_neg, 
                     force_of_will=force_of_will, force_of_will_neg=force_of_will_neg, 
                     crit_mastery=crit_mastery, crit_mastery_neg=crit_mastery_neg, 
                     rear_mastery=rear_mastery, rear_mastery_neg=rear_mastery_neg, 
                     melee_mastery=melee_mastery, melee_mastery_neg=melee_mastery_neg, 
                     distance_mastery=distance_mastery, distance_mastery_neg=distance_mastery_neg, 
                     healing_mastery=healing_mastery, healing_mastery_neg=healing_mastery_neg, 
                     berserk_mastery=berserk_mastery, berserk_mastery_neg=berserk_mastery_neg, 
                     crit_res=crit_res, crit_res_neg=crit_res_neg, 
                     rear_res=rear_res, rear_res_neg=rear_res_neg, 
                     armor_given=armor_given, armor_given_neg=armor_given_neg, 
                     armor_received=armor_received, armor_received_neg=armor_received_neg, 
                     indirect_dmg=indirect_dmg, indirect_dmg_neg=indirect_dmg_neg, 
                     random_masteries=random_masteries, random_resistances=random_resistances)
    
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






if __name__ == '__main__':
    from server import app
    connect_to_db(app)