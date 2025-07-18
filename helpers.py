"""Helper functions for server app."""

from model import connect_to_db, db
import crud


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


def get_build_base_stats_char_caps_by_build_id(build_id):
    """Return build, base_stats, and characteristic stats by a build's id"""
    combo = crud.get_build_characteristic_cap_base_stat_by_build_id(build_id)
    build = combo[0]
    base_stats = combo[2]
    characteristic_caps = combo[1]
    
    crud.set_build_with_total_stats_by_build_and_base_stats(
        tuple([build, base_stats]))
    
    return (build, base_stats, characteristic_caps)


def get_total_build_stats_by_build_id(build_id):
    """Return a build with total stat attributes by the build id"""
    combo = crud.get_build_characteristic_cap_base_stat_by_build_id(build_id)
    build = combo[0]
    base_stats = combo[2]
    
    crud.set_build_with_total_stats_by_build_and_base_stats(
        tuple([build, base_stats]))
    
    return build


def get_total_stats_dict_by_build(build):
    """Return a dict of a build's total stats by the build 
    with total stat attributes"""

    total_stats_dict = {}

    non_total_stat_keys = ['id', 'user_id',
                           'equipment_set', 'characteristics',
                           'character_class_id', 'level',
                           'updated_at', 'build_name',
                           'public', 'main_role',
                           'content_type']

    for attr, value in build.__dict__.items():
        if 'total_' in attr:
            # Remove 'total_'
            stat = attr[6:]
            total_stats_dict.update({stat : value })
        elif attr in non_total_stat_keys:
            if attr == 'updated_at':
                # Remove time from the date
                total_stats_dict.update({attr, value[:10]})
            else:
                total_stats_dict.update({attr, value})
    return total_stats_dict


def get_name_translations_dict(name_translations, language):
    """Return a dict of name translation in input language 
    by with type, id, translations"""
    """Ex. {'equipment': { 9723: 'Gelano'}}}"""
    
    names_dict = {}
    for nt in name_translations:
        names_dict.update(
            {nt.name_type : {'en' : {nt.name_id : getattr(nt, language)}}})
        
    return names_dict



if __name__ == '__main__':
    from server import app
    connect_to_db(app)