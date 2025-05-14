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