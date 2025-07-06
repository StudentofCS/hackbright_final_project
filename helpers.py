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

    for attr, value in build.__dict__.items():
        if 'total_' in attr:
            # Remove 'total_'
            stat = attr[6:]
            total_stats_dict.update({stat : value })
    return total_stats_dict


if __name__ == '__main__':
    from server import app
    connect_to_db(app)