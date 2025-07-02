"""Helper functions for server app."""

from model import connect_to_db, db
import crud


def get_build_base_stats_char_caps_by_build_id(build_id):
    combo = crud.get_build_characteristic_cap_base_stat_by_build_id(build_id)
    build = combo[0]
    base_stats = combo[2]
    characteristic_caps = combo[1]
    
    crud.set_build_with_total_stats_by_build_and_base_stats(
        tuple([build, base_stats]))
    
    return (build, base_stats, characteristic_caps)


def get_total_build_stats_by_build_id(build_id):
    combo = crud.get_build_characteristic_cap_base_stat_by_build_id(build_id)
    build = combo[0]
    base_stats = combo[2]
    
    crud.set_build_with_total_stats_by_build_and_base_stats(
        tuple([build, base_stats]))
    
    return build



if __name__ == '__main__':
    from server import app
    connect_to_db(app)